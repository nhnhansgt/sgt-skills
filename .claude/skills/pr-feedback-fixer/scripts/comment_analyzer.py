#!/usr/bin/env python3
"""
Comment analyzer - Analyzes PR feedback comments and extracts actionable items.
Usage: python3 comment_analyzer.py comments.json [--mappings MAPPINGS.json]
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class FeedbackCategory(Enum):
    """Categories of feedback."""
    TYPE_ANNOTATION = "type"
    IMPORT = "import"
    LOGIC = "logic"
    STYLE = "style"
    SECURITY = "security"
    PERFORMANCE = "performance"
    TESTING = "testing"
    DOCUMENTATION = "docs"
    OTHER = "other"


@dataclass
class FeedbackItem:
    """An actionable feedback item."""
    id: str
    file_path: str
    line_number: int
    category: FeedbackCategory
    action: str  # "add", "remove", "replace", "move"
    description: str
    suggestion: str
    confidence: str


# Pattern matching for common feedback types
PATTERNS = {
    FeedbackCategory.TYPE_ANNOTATION: [
        r"add type",
        r"type hint",
        r"type annotation",
        r": (int|str|bool|list|dict)",
        r"typing\.",
    ],
    FeedbackCategory.IMPORT: [
        r"import ",
        r"from .* import",
        r"missing import",
        r"unused import",
    ],
    FeedbackCategory.LOGIC: [
        r"\bbug\b",
        r"\bfix\b",
        r"\bwrong\b",
        r"\bincorrect\b",
        r"\boff-by-one\b",
        r"condition",
    ],
    FeedbackCategory.STYLE: [
        r"\bformat\b",
        r"\blint\b",
        r"\bnaming\b",
        r"\bconvention\b",
        r"black|flake8|pylint|ruff",
    ],
    FeedbackCategory.SECURITY: [
        r"\bsecurity\b",
        r"\bvulnerability\b",
        r"\bsql injection\b",
        r"\bxss\b",
        r"\bsanitize\b",
    ],
    FeedbackCategory.PERFORMANCE: [
        r"\bslow\b",
        r"\boptimize\b",
        r"\befficient\b",
        r"\bcache\b",
        r"\bcomplexity\b",
    ],
    FeedbackCategory.TESTING: [
        r"\btest\b",
        r"\bcoverage\b",
        r"\bassert\b",
        r"\bmock\b",
    ],
    FeedbackCategory.DOCUMENTATION: [
        r"\bdocstring\b",
        r"\bcomment\b",
        r"\bdocument\b",
        r"\bexplain\b",
    ],
}


def categorize_feedback(text: str) -> FeedbackCategory:
    """Categorize feedback based on text patterns."""
    text_lower = text.lower()

    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return category

    return FeedbackCategory.OTHER


def extract_action(text: str) -> str:
    """Extract the action type from feedback."""
    text_lower = text.lower()

    action_keywords = {
        "add": ["add", "include", "append", "insert"],
        "remove": ["remove", "delete", "drop", "omit"],
        "replace": ["replace", "change", "fix", "correct", "update"],
        "move": ["move", "reorder", "reorganize"],
    }

    for action, keywords in action_keywords.items():
        if any(kw in text_lower for kw in keywords):
            return action

    return "replace"  # Default


def parse_comment(comment: dict, mapping: dict | None = None) -> FeedbackItem | None:
    """Parse a comment into a feedback item."""
    body = comment.get("body", "").strip()

    # Skip non-actionable comments
    if len(body) < 10:
        return None

    # Skip questions
    if re.match(r"^(why|what|how|when|where|who|can you|could you|please)", body.lower()):
        return None

    # Get location
    path = comment.get("path", "")
    line = comment.get("line", 0) or comment.get("original_line", 0)

    # Use mapping if available
    if mapping:
        path = mapping.get("actual_file", path)
        line = mapping.get("actual_line", line)

    category = categorize_feedback(body)
    action = extract_action(body)

    # Extract suggestion (first sentence or up to 200 chars)
    suggestion_match = re.search(r"^(.{10,200}[.!?])", body)
    if suggestion_match:
        suggestion = suggestion_match.group(1)
    else:
        suggestion = body[:200]

    return FeedbackItem(
        id=str(comment.get("id", "")),
        file_path=path,
        line_number=line,
        category=category,
        action=action,
        description=body,
        suggestion=suggestion,
        confidence="medium"
    )


def main():
    parser = argparse.ArgumentParser(description="Analyze PR comments")
    parser.add_argument("comments_file", help="Comments JSON file")
    parser.add_argument("--mappings", "-m", help="Line mappings JSON file")
    parser.add_argument("--output", "-o", help="Output JSON file")
    args = parser.parse_args()

    # Read inputs
    comments = json.loads(Path(args.comments_file).read_text())

    mappings = None
    if args.mappings:
        mappings_data = json.loads(Path(args.mappings).read_text())
        mappings = {m["comment_id"]: m for m in mappings_data.get("mappings", [])}

    # Analyze comments
    items = []
    for comment in comments:
        mapping = mappings.get(str(comment.get("id"))) if mappings else None
        item = parse_comment(comment, mapping)
        if item:
            items.append({
                "id": item.id,
                "file_path": item.file_path,
                "line_number": item.line_number,
                "category": item.category.value,
                "action": item.action,
                "description": item.description,
                "suggestion": item.suggestion,
                "confidence": item.confidence
            })

    # Group by category
    by_category = {}
    for item in items:
        cat = item["category"]
        by_category.setdefault(cat, [])
        by_category[cat].append(item)

    # Output
    result = {
        "total_items": len(items),
        "by_category": {k: len(v) for k, v in by_category.items()},
        "items": items
    }

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))
        print(f"Saved {len(items)} feedback items to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
