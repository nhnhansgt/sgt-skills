#!/usr/bin/env python3
"""
Direct feedback parser - Parses chat-based feedback text.
Supports formats like:
  @path/to/file
  @path/to/file:45
  @path/to/file:function_name
  @path/to/file:ClassName.method

Usage: python3 direct_feedback_parser.py "@path/to/file" "feedback text"
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileReference:
    """Parsed file reference from @ notation."""
    file_path: str
    line_number: int | None = None
    symbol_name: str | None = None
    symbol_type: str | None = None  # "function", "class", "method"


@dataclass
class FeedbackItem:
    """A feedback item from text."""
    file_ref: FileReference
    description: str
    line_number: int | None = None
    category: str = "other"
    action: str = "fix"


def parse_file_reference(ref: str) -> FileReference:
    """Parse file reference from @ notation."""
    # Remove @ prefix if present
    ref = ref.lstrip("@")

    # Extract line number: path/file.py:45
    line_match = re.match(r"^(.+?):(\d+)$", ref)
    if line_match:
        return FileReference(
            file_path=line_match.group(1),
            line_number=int(line_match.group(2))
        )

    # Extract symbol: path/file.py:function_name or path/file.py:ClassName.method
    symbol_match = re.match(r"^(.+?):(.+)$", ref)
    if symbol_match:
        symbol = symbol_match.group(2)
        if "." in symbol:
            # Class.method
            parts = symbol.split(".")
            return FileReference(
                file_path=symbol_match.group(1),
                symbol_name=symbol,
                symbol_type="method"
            )
        else:
            # function
            return FileReference(
                file_path=symbol_match.group(1),
                symbol_name=symbol,
                symbol_type="function"
            )

    # Just file path
    return FileReference(file_path=ref)


def parse_feedback_text(text: str, default_ref: FileReference) -> list[FeedbackItem]:
    """Parse feedback text into structured items."""
    items = []

    # Pattern 1: "Line N: description"
    line_pattern = re.compile(r"^\s*(\d+)\.\s*Line\s+(\d+)\s*:\s*(.+)$", re.MULTILINE)
    for match in line_pattern.finditer(text):
        items.append(FeedbackItem(
            file_ref=default_ref,
            description=match.group(3).strip(),
            line_number=int(match.group(2))
        ))

    # Pattern 2: "Line N - description" or "Line N description"
    line_pattern2 = re.compile(r"Line\s+(\d+)\s*[:-]\s*(.+?)(?=Line\s+\d|$", re.MULTILINE | re.DOTALL)
    for match in line_pattern2.finditer(text):
        desc = match.group(2).strip().split("\n")[0]  # First line only
        if len(desc) > 5:  # Minimum meaningful length
            items.append(FeedbackItem(
                file_ref=default_ref,
                description=desc,
                line_number=int(match.group(1))
            ))

    # Pattern 3: "Function 'name' description"
    func_pattern = re.compile(r"Function\s+['\"]([^'\"]+)['\"]\s+(.+?)(?=Function\s+['\"]|$", re.MULTILINE | re.DOTALL)
    for match in func_pattern.finditer(text):
        desc = match.group(2).strip().split("\n")[0]
        if len(desc) > 5:
            items.append(FeedbackItem(
                file_ref=FileReference(
                    file_path=default_ref.file_path,
                    symbol_name=match.group(1),
                    symbol_type="function"
                ),
                description=desc
            ))

    # Pattern 4: Numbered list "1. description"
    numbered_pattern = re.compile(r"^\s*\d+\.\s*(.+)$", re.MULTILINE)
    numbered_matches = list(numbered_pattern.finditer(text))
    if len(numbered_matches) > 1 and not items:
        for match in numbered_matches:
            desc = match.group(1).strip()
            if len(desc) > 5:
                items.append(FeedbackItem(
                    file_ref=default_ref,
                    description=desc
                ))

    # Pattern 5: Entire text as single feedback item
    if not items and len(text.strip()) > 10:
        # Check if there's a line number embedded in the text
        embedded_line = re.search(r"(?:line|at|row)\s+(\d+)", text, re.IGNORECASE)
        line = int(embedded_line.group(1)) if embedded_line else None

        items.append(FeedbackItem(
            file_ref=default_ref,
            description=text.strip(),
            line_number=line
        ))

    return items


def categorize_feedback(text: str) -> str:
    """Categorize feedback based on keywords."""
    text_lower = text.lower()

    categories = {
        "type": ["type", "annotation", "hint", "typing"],
        "import": ["import", "include", "module"],
        "logic": ["bug", "wrong", "incorrect", "logic", "fix"],
        "style": ["format", "style", "lint", "naming"],
        "security": ["security", "vulnerability", "injection"],
        "performance": ["slow", "optimize", "efficient"],
        "docs": ["doc", "comment", "document"],
    }

    for category, keywords in categories.items():
        if any(kw in text_lower for kw in keywords):
            return category

    return "other"


def main():
    parser = argparse.ArgumentParser(description="Parse direct feedback text")
    parser.add_argument("file_ref", help="File reference (e.g., @src/file.py:45)")
    parser.add_argument("feedback_text", help="Feedback text content")
    parser.add_argument("--output", "-o", help="Output JSON file")
    args = parser.parse_args()

    try:
        # Parse file reference
        file_ref = parse_file_reference(args.file_ref)

        # Parse feedback text
        items = parse_feedback_text(args.feedback_text, file_ref)

        # Categorize items
        for item in items:
            item.category = categorize_feedback(item.description)

        # Build result
        result = {
            "file_reference": {
                "path": file_ref.file_path,
                "line_number": file_ref.line_number,
                "symbol_name": file_ref.symbol_name,
                "symbol_type": file_ref.symbol_type
            },
            "total_items": len(items),
            "items": [
                {
                    "file_path": item.file_ref.file_path,
                    "line_number": item.line_number or item.file_ref.line_number,
                    "symbol_name": item.file_ref.symbol_name,
                    "symbol_type": item.file_ref.symbol_type,
                    "description": item.description,
                    "category": item.category,
                    "action": item.action
                }
                for item in items
            ]
        }

        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2))
            print(f"Saved {len(items)} feedback items to {args.output}", file=sys.stderr)
        else:
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
