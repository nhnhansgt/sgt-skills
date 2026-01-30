# Python Code Style & Conventions (PEP 8)

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions/Variables | `snake_case` | `get_user_data`, `is_active` |
| Classes | `PascalCase` | `UserDataManager`, `APIHandler` |
| Constants | `UPPER_CASE` | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| Private | `_leading_underscore` | `_internal_method`, `_cache` |
| Dunder | `__double_underscore__` | `__init__`, `__str__` |

### Name Guidelines
- Use descriptive names: `user_count` not `uc` or `count`
- Avoid single-letter variables except loop counters (`i`, `j`, `k`)
- Boolean names: `is_valid`, `has_permission`, `can_edit`
- Avoid built-in shadowing: don't use `list`, `dict`, `type` as variable names

## Indentation & Spacing

- **4 spaces** per indentation level (no tabs)
- Space after commas: `func(a, b, c)`
- Space around operators: `x + y`, `a == b`
- No space inside brackets: `data[x]`, `func(arg)`
- Blank lines: 2 between top-level definitions, 1 between methods

## Line Length

- **79 characters** max for code
- **72 characters** max for comments/docstrings
- Use backslash or parentheses for line continuation:
  ```python
  # Good
  long_string = (
      "first part "
      "second part"
  )

  # Also acceptable
  long_string = "first part " \
                 "second part"
  ```

## Import Ordering

```python
# 1. Standard library
import os
import sys
from pathlib import Path

# 2. Third-party
import requests
from fastapi import APIRouter

# 3. Local/Application
from .models import User
from .utils import format_date
```

### Import Guidelines
- One import per line: `import os, sys` → two separate lines
- Use absolute imports: `from pkg.mod import func`
- Avoid wildcards: `from module import *` (except `__init__.py`)
- Group imports by type with blank line between groups

## Whitespace in Expressions

```python
# Good
if x == 4:
    print(x, y)

# Bad
if x == 4 :
    print ( x, y )

# Good - spaces around operators
x = x + 1
hypot2 = x*x + y*y

# Good - no spaces for keyword arguments
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
```

## String Quotes

- Use **double quotes** for strings: `"hello"`
- Use single quotes only when string contains double quotes: `'He said "hello"'`
- Triple double quotes for docstrings: `"""Docstring here"""`

## Comments

```python
# Inline comment - separate by 2 spaces
x = x + 1  # Increment x

# Block comments - # + space
# This function calculates the total cost
# including tax and shipping fees
def calculate_total():
    pass
```

### Comment Guidelines
- Write comments that explain **why**, not **what**
- Keep comments up-to-date when code changes
- Avoid obvious comments: `i = i + 1  # increment i`

## Docstrings

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate discounted price.

    Args:
        price: Original price
        discount_percent: Discount percentage (0-100)

    Returns:
        Final price after discount

    Raises:
        ValueError: If discount_percent is negative or > 100

    Example:
        >>> calculate_discount(100.0, 20)
        80.0
    """
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

## Reference
[PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
