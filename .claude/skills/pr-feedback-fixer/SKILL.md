---
name: pr-feedback-fixer
description: |
  Fix pull request feedback by analyzing review comments and applying code changes.
  Use when user mentions "fix PR feedback", "handle review comments", "apply PR suggestions",
  provides a GitHub PR URL, or shares feedback text with file path reference.
  Supports both GitHub PR integration and direct chat-based feedback with interactive confirmation.
---

# PR Feedback Fixer

## Overview

Analyze pull request review comments and automatically apply code fixes with user confirmation.
Two workflows: (1) GitHub PR integration for fetching comments/diff, or (2) direct chat-based feedback
when PR URL is not available.

## When to Use

- User provides GitHub PR URL with review comments
- User mentions "fix PR feedback", "handle review comments", "apply PR suggestions"
- User shares feedback text with file reference: `/fix-pr-feedback @path/to/file`
- User wants to address code review feedback systematically

## Quick Start

### GitHub PR Mode
```bash
/fix-pr-feedback https://github.com/owner/repo/pull/123
```

### Chat-Based Mode
```bash
/fix-pr-feedback @src/utils.py
[Feedback content pasted here]
```

## Workflow Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│                    Input Received                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Is input a GitHub PR URL?                                  │
│     │                                                        │
│     ├── Yes → GitHub PR Mode                                │
│     │         ├── Fetch PR context                          │
│     │         ├── Parse diff + comments                     │
│     │         └── Apply fixes                               │
│     │                                                        │
│     └── No → Chat-Based Mode                                │
│               ├── Parse file path from @path                │
│               ├── Extract feedback from text                │
│               └── Apply fixes                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## GitHub PR Mode

### 1. Fetch PR Context

Use `scripts/github_fetch.py` to retrieve:
- PR review comments
- Pull request diff
- File changes

**Requires:** `GITHUB_TOKEN` environment variable

```bash
python3 scripts/github_fetch.py <PR_URL>
```

### 2. Parse and Categorize Feedback

Use `scripts/comment_analyzer.py` to analyze comments and extract:
- File paths referenced
- Line numbers
- Actionable fix suggestions
- Feedback category (style, logic, type, etc.)

```bash
python3 scripts/comment_analyzer.py comments.json
```

### 3. Map Comments to Code Locations

Use `scripts/diff_parser.py` to:
- Parse unified diff format
- Match comment lines to actual code locations
- Handle diff line shifts

```bash
python3 scripts/diff_parser.py diff.patch comments.json
```

### 4. Apply Fixes Interactively

For each feedback item:
1. Show the comment and proposed fix
2. Display diff preview
3. Ask user for confirmation
4. Apply change using Serena tools (`replace_content`, `replace_symbol_body`)
5. Verify fix (run tests/linters if specified)

### 5. Summary

Display summary of all applied changes with file paths and modification count.

## Chat-Based Mode

### When to Use

- No GitHub PR URL available
- Feedback from code review tools (SonarQube, CodeClimate, etc.)
- Manual code review notes
- Local development feedback

### Input Format

```
/fix-pr-feedback @path/to/file
[Optional: Line numbers like @path/to/file:45]
[Paste feedback content here]

Multiple items supported:
/fix-pr-feedback @src/utils.py
1. Line 23: Add type hint for return value
2. Line 45: Missing import for 'requests'
3. Function 'calculate' has logic error
```

### Workflow

1. **Parse file reference** - Extract path from `@path/to/file` or `@path/to/file:line`
2. **Parse feedback text** - Use `scripts/direct_feedback_parser.py`
3. **Locate code** - Use Serena tools to find symbols/lines
4. **Apply fixes** - Same interactive process as GitHub mode

### Line Reference Formats

| Format | Example | Meaning |
|--------|---------|---------|
| `@file:line` | `@src/utils.py:45` | Specific line |
| `@file:function` | `@src/utils.py:calculate` | Function scope |
| `@file:class.method` | `@src/api.py:User.get_name` | Class method |
| `@file` only | `@src/utils.py` | Entire file |

## Fix Patterns

See `references/fix_patterns.md` for common feedback patterns:
- Type annotations missing
- Import statement issues
- Logic errors
- Style violations

## Safety Features

- **Interactive mode**: Confirm each fix before applying
- **Diff preview**: Show changes before commit
- **Undo support**: Keep original code reference
- **Uncertain handling**: Flag ambiguous cases for manual review

## Requirements

**GitHub PR Mode:**
- `gh` CLI installed and authenticated
- Python 3.10+
- `GITHUB_TOKEN` environment variable

**Chat-Based Mode:**
- Serena tools available
- File access permissions

## Troubleshooting

**GitHub PR Mode:**
- **Auth error**: Set `GITHUB_TOKEN` or run `gh auth login`
- **Location mismatch**: Diff may be outdated - fetch latest PR state
- **Conflicting feedback**: User must resolve manually

**Chat-Based Mode:**
- **File not found**: Check path is relative to project root
- **Line not found**: Code may have changed - use symbol reference instead
- **Ambiguous location**: Provide more context or use function/class name

## Resources

### scripts/

- `github_fetch.py` - GitHub API integration for PR context
- `diff_parser.py` - Diff parsing and line mapping
- `comment_analyzer.py` - Feedback analysis and categorization
- `direct_feedback_parser.py` - Parse chat-based feedback text
- `requirements.txt` - Python dependencies

### references/

- `github_api.md` - GitHub REST API reference for PR operations
- `fix_patterns.md` - Common feedback patterns and fix strategies
- `workflow.md` - Detailed workflow with examples
