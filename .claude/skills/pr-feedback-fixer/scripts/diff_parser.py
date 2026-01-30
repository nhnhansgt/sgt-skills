#!/usr/bin/env python3
"""
Diff parser - Parses unified diff and maps comment lines to code locations.
Usage: python3 diff_parser.py diff.patch comments.json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Hunk:
    """A diff hunk representing a contiguous change."""
    file_path: str
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: list[str]


@dataclass
class LineMapping:
    """Maps a comment line to actual file location."""
    comment_path: str
    comment_line: int
    actual_file: str
    actual_line: int
    confidence: str  # "high", "medium", "low"


def parse_unified_diff(diff_text: str) -> list[Hunk]:
    """Parse unified diff into hunks."""
    hunks = []
    current_file = None
    current_hunk = None

    for line in diff_text.split("\n"):
        # File header
        if line.startswith("+++ b/"):
            current_file = line[6:]
        elif line.startswith("--- a/"):
            current_file = line[6:]

        # Hunk header
        hunk_match = re.match(r"^@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@", line)
        if hunk_match and current_file:
            if current_hunk:
                hunks.append(current_hunk)

            old_start = int(hunk_match.group(1))
            old_count = int(hunk_match.group(2)) if hunk_match.group(2) else 1
            new_start = int(hunk_match.group(3))
            new_count = int(hunk_match.group(4)) if hunk_match.group(4) else 1

            current_hunk = Hunk(
                file_path=current_file,
                old_start=old_start,
                old_lines=old_count,
                new_start=new_start,
                new_lines=new_count,
                lines=[]
            )
        elif current_hunk is not None:
            current_hunk.lines.append(line)

    if current_hunk:
        hunks.append(current_hunk)

    return hunks


def find_hunk_for_line(hunks: list[Hunk], file_path: str, line: int) -> Hunk | None:
    """Find hunk containing the given line."""
    for hunk in hunks:
        if hunk.file_path != file_path:
            continue
        if hunk.new_start <= line < hunk.new_start + hunk.new_lines:
            return hunk
    return None


def map_comment_to_line(comment: dict, hunks: list[Hunk]) -> LineMapping:
    """Map a PR comment to actual file location."""
    path = comment.get("path", "")
    line = comment.get("line", 0) or comment.get("original_line", 0)

    hunk = find_hunk_for_line(hunks, path, line)

    if not hunk:
        # No hunk found - might be on unchanged line
        return LineMapping(
            comment_path=path,
            comment_line=line,
            actual_file=path,
            actual_line=line,
            confidence="medium"
        )

    # Calculate actual line position
    # Count context lines in hunk before the comment line
    context_count = 0
    in_hunk_line = hunk.new_start

    for hunk_line in hunk.lines:
        if in_hunk_line >= line:
            break

        if hunk_line.startswith(" ") or hunk_line.startswith("+"):
            context_count += 1
        in_hunk_line += 1

    actual_line = hunk.old_start + context_count

    return LineMapping(
        comment_path=path,
        comment_line=line,
        actual_file=path,
        actual_line=actual_line,
        confidence="high"
    )


def main():
    parser = argparse.ArgumentParser(description="Parse diff and map comment lines")
    parser.add_argument("diff_file", help="Diff file (.patch)")
    parser.add_argument("comments_file", help="Comments JSON file")
    parser.add_argument("--output", "-o", help="Output JSON file")
    args = parser.parse_args()

    # Read inputs
    diff_text = Path(args.diff_file).read_text()
    comments = json.loads(Path(args.comments_file).read_text())

    # Parse diff
    hunks = parse_unified_diff(diff_text)
    print(f"Parsed {len(hunks)} hunks from diff", file=sys.stderr)

    # Map comments
    mappings = []
    for comment in comments:
        if comment.get("path"):
            mapping = map_comment_to_line(comment, hunks)
            mappings.append({
                "comment_id": comment.get("id"),
                "comment_path": mapping.comment_path,
                "comment_line": mapping.comment_line,
                "actual_file": mapping.actual_file,
                "actual_line": mapping.actual_line,
                "confidence": mapping.confidence,
                "body": comment.get("body", "")[:100]
            })

    # Output
    result = {
        "mappings": mappings,
        "total_comments": len(comments),
        "mapped_comments": len(mappings)
    }

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))
        print(f"Saved mappings to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
