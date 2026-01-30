#!/usr/bin/env python3
"""
GitHub PR fetcher - Retrieves PR context, comments, and diff.
Usage: python3 github_fetch.py <PR_URL> [--output-dir DIR]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests module required. pip install requests", file=sys.stderr)
    sys.exit(1)


def parse_pr_url(url: str) -> tuple[str, str, int]:
    """Parse GitHub PR URL into owner, repo, and PR number."""
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)/pull/(\d+)', url)
    if not match:
        raise ValueError(f"Invalid PR URL: {url}")
    return match.group(1), match.group(2), int(match.group(3))


def get_token() -> str:
    """Get GitHub token from env or gh CLI."""
    # Check env var first
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    # Try gh CLI
    import subprocess
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            "GITHUB_TOKEN not set and gh CLI not available. "
            "Set GITHUB_TOKEN or run: gh auth login"
        )


def fetch_pr(owner: str, repo: str, pr_number: int, token: str) -> dict:
    """Fetch PR details via GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def fetch_review_comments(owner: str, repo: str, pr_number: int, token: str) -> list:
    """Fetch all review comments for PR."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    comments = []
    page = 1
    while True:
        resp = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        comments.extend(data)
        page += 1
    return comments


def fetch_diff(owner: str, repo: str, pr_number: int, token: str) -> str:
    """Fetch PR diff."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.diff"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub PR context")
    parser.add_argument("pr_url", help="GitHub PR URL")
    parser.add_argument("--output-dir", "-o", default=".", help="Output directory")
    args = parser.parse_args()

    try:
        owner, repo, pr_number = parse_pr_url(args.pr_url)
        token = get_token()

        print(f"Fetching PR {owner}/{repo}#{pr_number}...")

        # Fetch data
        pr_data = fetch_pr(owner, repo, pr_number, token)
        comments = fetch_review_comments(owner, repo, pr_number, token)
        diff = fetch_diff(owner, repo, pr_number, token)

        # Prepare output
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Save results
        (out_dir / "pr_data.json").write_text(json.dumps(pr_data, indent=2))
        (out_dir / "comments.json").write_text(json.dumps(comments, indent=2))
        (out_dir / "diff.patch").write_text(diff)

        print(f"✓ Saved pr_data.json")
        print(f"✓ Saved comments.json ({len(comments)} comments)")
        print(f"✓ Saved diff.patch")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
