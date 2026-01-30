# Common Feedback Patterns

## Type Annotations

### Missing Type Hints

**Feedback:** "Add type hint for return value"
**Fix:** Add `-> Type` annotation

```python
# Before
def calculate(x, y):
    return x + y

# After
def calculate(x: int, y: int) -> int:
    return x + y
```

### Generic Types

**Feedback:** "Use List[str] instead of list"
**Fix:** Import from typing module

```python
# Before
def get_items() -> list:
    return ["a", "b"]

# After
from typing import List

def get_items() -> List[str]:
    return ["a", "b"]
```

## Import Issues

### Missing Import

**Feedback:** "Missing import for requests"
**Fix:** Add import at top of file

```python
# Add at module level
import requests
```

### Unused Import

**Feedback:** "Remove unused import"
**Fix:** Delete import statement

## Logic Errors

### Off-by-One

**Feedback:** "Off-by-one error in range"
**Fix:** Adjust range boundaries

```python
# Before
for i in range(len(items)):
    process(items[i])

# After
for i in range(len(items) - 1):
    process(items[i])
```

### Inverted Condition

**Feedback:** "Condition is backwards"
**Fix:** Negate or swap condition

```python
# Before
if not user.is_admin:
    allow_access()

# After
if user.is_admin:
    allow_access()
```

## Style Violations

### Naming Convention

**Feedback:** "Use snake_case for function names"
**Fix:** Rename identifiers

```python
# Before
def processData():
    pass

# After
def process_data():
    pass
```

### Line Length

**Feedback:** "Line too long (>88 chars)"
**Fix:** Break line or use parens

```python
# Before
result = some_function(with_many, arguments, that_make, line_very_long)

# After
result = some_function(
    with_many, arguments,
    that_make, line_very_long
)
```

## Security Issues

### SQL Injection

**Feedback:** "Vulnerable to SQL injection"
**Fix:** Use parameterized queries

```python
# Before
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# After
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### Path Traversal

**Feedback:** "Unsafe path handling"
**Fix:** Validate and sanitize paths

## Performance

### Inefficient Loop

**Feedback:** "O(n²) complexity - use set for lookup"
**Fix:** Use appropriate data structure

```python
# Before
for item in items:
    if item.id in [other.id for other in others]:
        process(item)

# After
other_ids = {other.id for other in others}
for item in items:
    if item.id in other_ids:
        process(item)
```

## Testing

### Missing Test

**Feedback:** "Add test for edge case"
**Fix:** Add test function

```python
def test_edge_case():
    result = function(None)
    assert result == expected_value
```

## Documentation

### Missing Docstring

**Feedback:** "Add docstring for this function"
**Fix:** Add docstring

```python
def process_data(data: dict) -> list:
    """
    Transform input data into processed list.

    Args:
        data: Input dictionary with raw data

    Returns:
        List of processed items
    """
    return list(data.values())
```
