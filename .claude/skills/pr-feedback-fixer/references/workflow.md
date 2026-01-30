# Detailed Workflow

## Workflow Selection

```
User Input
    │
    ├── Is GitHub PR URL? ──Yes──→ GitHub PR Mode
    │                              (Fetch → Parse → Apply)
    │
    └── No ──→ Chat-Based Mode
                 (Parse text → Locate → Apply)
```

## GitHub PR Mode

### 1. User Input

User provides GitHub PR URL: `https://github.com/owner/repo/pull/123`

### 2. Fetch Context

```bash
# Run fetch script
python3 scripts/github_fetch.py https://github.com/owner/repo/pull/123 -o /tmp/pr-context

# Outputs:
# - pr_data.json   (PR metadata)
# - comments.json  (Review comments)
# - diff.patch     (Unified diff)
```

### 3. Parse Diff

```bash
# Map comment lines to actual file locations
python3 scripts/diff_parser.py /tmp/pr-context/diff.patch /tmp/pr-context/comments.json -o /tmp/pr-context/mappings.json
```

### 4. Analyze Feedback

```bash
# Extract actionable items
python3 scripts/comment_analyzer.py /tmp/pr-context/comments.json -m /tmp/pr-context/mappings.json -o /tmp/pr-context/feedback.json
```

### 5. Interactive Fix Loop

For each feedback item:

```
┌─────────────────────────────────────────────────────────────┐
│ Feedback #3: src/utils.py:45                                │
│ Category: type                                              │
│                                                              │
│ Comment: "Add type hint for return value"                   │
│                                                              │
│ Proposed fix:                                               │
│   def calculate(x, y) -> int:                               │
│       return x + y                                          │
│                                                              │
│ Apply this fix? [y/n/skip/q] >                              │
└─────────────────────────────────────────────────────────────┘
```

**User responses:**
- `y` - Apply fix
- `n` - Skip this item
- `s` - Show more context
- `q` - Quit

### 6. Apply Fix

Using Serena tools:
- `replace_content` for simple edits
- `replace_symbol_body` for function/class changes
- `insert_after_symbol` for additions

### 7. Verify

Optional verification:
- Run tests: `pytest tests/`
- Run linter: `ruff check src/`
- Show diff: `git diff`

### 8. Summary

```
──────────────────────────────────────────────────────────────
Summary of Changes
──────────────────────────────────────────────────────────────

Files modified: 3
  - src/utils.py      (2 changes)
  - src/main.py       (1 change)
  - tests/test_utils.py (1 change)

Total feedback items: 8
  Applied: 4
  Skipped: 2
  Failed: 0
  Requires manual: 2

Next steps:
  - Review changes: git diff
  - Run tests: pytest
  - Commit: git commit -am "Fix PR feedback"
──────────────────────────────────────────────────────────────
```

## Chat-Based Mode

### When to Use

- No GitHub PR available
- Feedback from code review tools (SonarQube, CodeClimate)
- Manual code review notes
- Local development feedback

### 1. User Input

```
/fix-pr-feedback @src/utils.py
[Feedback text]
```

### 2. Parse File Reference

```python
# Extract from @ notation
@src/utils.py:45          # Line number
@src/utils.py:calculate   # Function name
@src/api.py:User.get_name # Class method
@src/utils.py             # Entire file
```

### 3. Parse Feedback Text

```bash
python3 scripts/direct_feedback_parser.py "@src/utils.py" "feedback text"
```

Supported formats:
```
# Format 1: Line-specific
Line 23: Add type hint for return value
Line 45: Missing import for 'requests'

# Format 2: Numbered list
1. Function 'calculate' has wrong logic
2. Add docstring for 'process_data'
3. Variable 'result' should be 'items'

# Format 3: Free text
The condition on line 67 is backwards, should be != instead of ==
```

### 4. Locate Code

Use Serena tools based on reference type:

| Reference | Tool |
|-----------|------|
| Line number | `read_file` with offset/limit |
| Function | `find_symbol` with name path |
| Class method | `find_symbol` with `Class/method` |
| Entire file | `get_symbols_overview` then search |

### 5. Apply Fixes

Same interactive loop as GitHub mode.

## Example Sessions

### GitHub PR Example

```
User: /fix-pr-feedback https://github.com/me/project/pull/42

Claude: Fetching PR me/project#42...
        Found 5 review comments
        Analyzing feedback...

        Feedback #1: src/api.py:23 (type)
        "Add return type annotation"

        Current code:
          def get_user(id):
              return db.query(id)

        Proposed fix:
          def get_user(id: int) -> User | None:
              return db.query(id)

        Apply this fix? [y/n/skip/q] > y

        ✓ Applied fix to src/api.py:23

        Feedback #2: tests/test_api.py:15 (testing)
        "Add test for None case"

        Proposed fix:
          def test_get_user_not_found():
              result = get_user(999)
              assert result is None

        Apply this fix? [y/n/skip/q] > y

        ✓ Applied fix to tests/test_api.py:15

        ...

        Summary: 4/5 fixes applied, 1 skipped
```

### Chat-Based Example (SonarQube Output)

```
User: /fix-pr-feedback @src/services/user.py
Here is the SonarQube feedback:
Line 15: Add type hint for parameter 'user_id'
Line 23: Function 'get_user' is missing docstring
Line 45: Remove unused import 'logging'

Claude: Parsing feedback for src/services/user.py...
        Found 3 feedback items

        Feedback #1: src/services/user.py:15 (type)
        "Add type hint for parameter 'user_id'"

        Current code:
          def get_user(user_id):

        Proposed fix:
          def get_user(user_id: int):

        Apply this fix? [y/n/skip/q] > y

        ✓ Applied fix

        Feedback #2: src/services/user.py:23 (docs)
        "Function 'get_user' is missing docstring"

        Proposed fix:
          def get_user(user_id: int) -> User | None:
              """
              Retrieve user by ID from database.

              Args:
                  user_id: Unique identifier for user

              Returns:
                  User object or None if not found
              """
              return db.query(user_id)

        Apply this fix? [y/n/skip/q] > y

        ✓ Applied fix

        Summary: 3/3 fixes applied
```

### Chat-Based Example (Manual Review)

```
User: /fix-pr-feedback @src/utils.py
Line 67: The condition is backwards - should use != instead of ==
Line 89: This variable is never used, can be removed

Claude: Parsing feedback for src/utils.py...
        Found 2 feedback items

        Feedback #1: src/utils.py:67 (logic)
        "The condition is backwards"

        Current code:
          if user.status == "inactive":

        Proposed fix:
          if user.status != "inactive":

        Apply this fix? [y/n/skip/q] > y

        ✓ Applied fix

        Feedback #2: src/utils.py:89 (style)
        "Unused variable"

        Proposed fix:
          # Remove line: temp_result = ...

        Apply this fix? [y/n/skip/q] > y

        ✓ Applied fix

        Summary: 2/2 fixes applied
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| **GitHub PR Mode** |
| Auth error | Missing/invalid GITHUB_TOKEN | Set env var or run `gh auth login` |
| PR not found | Invalid URL or no access | Verify URL and token permissions |
| No comments | PR has no review comments | Exit gracefully |
| Location mismatch | Diff outdated | Refetch latest PR state |
| Apply failed | Code structure changed | Flag for manual review |
| **Chat-Based Mode** |
| File not found | Invalid path | Check path relative to project root |
| Line not found | Code changed | Use symbol reference instead |
| Symbol not found | Typo in name | Use `get_symbols_overview` to find correct name |
| Ambiguous location | Multiple matches | Provide more context |

## Advanced Features

### Batch Mode

```bash
# Auto-apply safe fixes only
/fix-pr-feedback <URL> --auto-safe

# Patterns considered safe:
# - Type annotations
# - Import statements
# - Simple formatting
```

### Filter by Category

```bash
# Only fix type hints
/fix-pr-feedback <URL> --category type

# Exclude style fixes
/fix-pr-feedback <URL> --exclude style
```

### Dry Run

```bash
# Show what would be changed without applying
/fix-pr-feedback <URL> --dry-run
```

### Multiple Files (Chat Mode)

```
/fix-pr-feedback
@src/api.py
Line 15: Add type hint

@src/utils.py
Line 23: Fix logic error
```
