# Common Python Anti-Patterns to Avoid

## Mutable Default Arguments

### The Problem
```python
# BAD - Default argument evaluated once at definition
def append_item(item, items=[]):
    items.append(item)
    return items

# Calling multiple times accumulates items!
append_item(1)  # [1]
append_item(2)  # [1, 2] - Unexpected!
```

### The Solution
```python
# GOOD - Use None as default
def append_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

## Bare Except Clauses

### The Problem
```python
# BAD - Catches everything, including KeyboardInterrupt
try:
    dangerous_operation()
except:
    pass  # Silent failure
```

### The Solution
```python
# GOOD - Catch specific exceptions
try:
    dangerous_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except SpecificError as e:
    handle_error(e)

# If you must catch all, at least log
except Exception as e:
    logger.exception("Unexpected error occurred")
```

## Comparing with True/False

### The Problem
```python
# BAD - Unnecessary comparison
if is_valid == True:
    pass

if is_active == False:
    pass
```

### The Solution
```python
# GOOD - Direct boolean evaluation
if is_valid:
    pass

if not is_active:
    pass

# GOOD - Use "is" for None/True/False singleton comparison
if value is None:
    pass
```

## Not Using Context Managers

### The Problem
```python
# BAD - File may not close if error occurs
f = open("file.txt", "r")
content = f.read()
f.close()
```

### The Solution
```python
# GOOD - Automatic cleanup
with open("file.txt", "r") as f:
    content = f.read()
# File always closed here, even if exception occurs
```

## Star Imports

### The Problem
```python
# BAD - Pollutes namespace, unclear origin
from module import *
```

### The Solution
```python
# GOOD - Explicit imports
from module import function1, function2
# OR
import module
module.function1()
```

## Premature Optimization

### The Problem
```python
# BAD - Optimizing without profiling
def calculate():
    # Complex "optimizations" that may not matter
    result = sum([x * 2 for x in range(1000)])  # "Faster"?
```

### The Solution
```python
# GOOD - Simple, readable code first
def calculate():
    return sum(x * 2 for x in range(1000))

# Only optimize after profiling shows it's a bottleneck
```

## No Virtual Environments

### The Problem
```bash
# BAD - Global Python installation
pip install package-name
```

### The Solution
```bash
# GOOD - Isolated environments
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

pip install package-name
```

## Hardcoded Paths

### The Problem
```python
# BAD - Not portable
data_path = "/home/user/data/file.txt"
```

### The Solution
```python
# GOOD - Use pathlib
from pathlib import Path

data_path = Path("data") / "file.txt"
# Or relative to script
script_dir = Path(__file__).parent
data_path = script_dir / "data" / "file.txt"
```

## Using print() for Debugging

### The Problem
```python
# BAD - Hard to control output levels
print(f"Debug: {variable}")
print(f"Error occurred: {error}")
```

### The Solution
```python
# GOOD - Use logging module
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Variable value: {variable}")
logger.error(f"Error occurred: {error}")
```

## Ignoring Type Checker Warnings

### The Problem
```python
# BAD - Silencing type errors without justification
value: Any = get_value()  # type: ignore
```

### The Solution
```python
# GOOD - Fix the type or explain the ignore
# Type ignore because external library has incorrect type hints
value: Any = get_value()  # type: ignore[annotation-unchecked]

# Better - Fix the type
value: dict[str, Any] = get_value()
```

## Not Using enumerate() for Index

### The Problem
```python
# BAD - Manual index tracking
index = 0
for item in items:
    process(item, index)
    index += 1
```

### The Solution
```python
# GOOD - Use enumerate
for index, item in enumerate(items):
    process(item, index)
```

## String Concatenation in Loops

### The Problem
```python
# BAD - O(n²) complexity
result = ""
for item in large_list:
    result += str(item)
```

### The Solution
```python
# GOOD - Use join (O(n))
result = "".join(str(item) for item in large_list)
```

## Checking Empty Containers

### The Problem
```python
# BAD - Less Pythonic
if len(items) == 0:
    pass
if len(items) > 0:
    pass
```

### The Solution
```python
# GOOD - Truthiness check
if not items:  # Empty
    pass
if items:  # Not empty
    pass
```

## Reference Table

| Anti-Pattern | Why Bad | Better Alternative |
|--------------|---------|-------------------|
| `def f(x=[])` | Mutable default | `def f(x=None)` |
| `except:` | Catches KeyboardInterrupt | `except Exception:` |
| `if x == True` | Unnecessary comparison | `if x:` |
| `f = open(...)` | Resource leak | `with open(...) as f:` |
| `from x import *` | Namespace pollution | Explicit imports |
| Global pip | Dependency conflicts | Virtual environments |
| `print()` debugging | No control | `logging` module |
| `result += s` in loop | O(n²) | `"".join()` |
| `len(x) == 0` | Not Pythonic | `if not x:` |
| `for i in range(len(x))` | Unnecessary | `for i, item in enumerate(x):` |

## Quick Checklist Before Committing Code

- [ ] No mutable default arguments
- [ ] Specific exception types caught
- [ ] Context managers used for resources
- [ ] No star imports
- [ ] Virtual environment isolated
- [ ] Logging instead of print
- [ ] Type hints added (at least for public APIs)
- [ ] No hardcoded paths
- [ ] Code profiled before "optimizing"
- [ ] PEP 8 compliant (run `pylint` or `flake8`)
