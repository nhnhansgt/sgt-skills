# Python Type Hints & Modern Features (3.12+)

## Basic Type Hints

```python
def calculate_total(price: float, quantity: int) -> float:
    """Calculate total price."""
    return price * quantity

# With optional parameter
def greet(name: str, greeting: str | None = None) -> str:
    if greeting is None:
        greeting = "Hello"
    return f"{greeting}, {name}!"

# With multiple return types
def parse_response(data: dict) -> str | dict | None:
    if "error" in data:
        return None
    if "data" in data:
        return data["data"]
    return "success"
```

## Common Type Hints from typing Module

```python
from typing import List, Dict, Optional, Union, Any, TypedDict

# Before Python 3.9 (use from typing)
def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# Python 3.9+ (use built-in types)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Optional (can be None)
def find_user(user_id: int) -> Optional[User]:
    return User.query.get(user_id)

# Union (one of several types)
def process_data(data: str | bytes) -> str:
    if isinstance(data, bytes):
        return data.decode()
    return data

# TypedDict for structured dictionaries
class UserData(TypedDict):
    name: str
    email: str
    age: int

def create_user(data: UserData) -> User:
    return User(**data)
```

## Python 3.12+ Features

### Type Alias Syntax (PEP 695)
```python
# Python 3.12+
type UserId = int
type Json = dict[str, Any]

def get_user(user_id: UserId) -> Json:
    ...
```

### Type Parameter Syntax (PEP 695)
```python
# Python 3.12+
def max[T](items: list[T]) -> T:
    return max(items)

# Generic class
class Container[T]:
    def __init__(self, value: T):
        self.value = value
```

## Python 3.13+ Improvements

- **Better type error messages** - More informative error reporting
- **Deprecated typing features** - Some old syntax is now deprecated

## Generics with TypeVar

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

# Usage
int_box: Box[int] = Box(42)
str_box: Box[str] = Box("hello")
```

## Protocol for Structural Typing

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing square")

def render(shape: Drawable) -> None:
    shape.draw()

# Both work because they implement draw()
render(Circle())  # OK
render(Square())  # OK
```

## Type Checkers

### mypy
```bash
pip install mypy
mypy src/
```

### pyright (VS Code default)
```bash
npm install -g pyright
pyright src/
```

## Configuration

### pyproject.toml for type checking
```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pyright]
include = ["src"]
pythonVersion = "3.12"
typeCheckingMode = "strict"
```

## Best Practices

1. **Avoid Any** - Use specific types or `Unknown`
2. **Type public APIs** - Minimum for library interfaces
3. **Use TypedDict** - For structured dictionaries
4. **Protocol over ABC** - For duck typing
5. **Gradual typing** - Add types where beneficial first
6. **Run type checker** - In CI/CD pipeline

## Common Patterns

```python
# Callable type hint
from typing import Callable

def apply_func(items: list[int], func: Callable[[int], int]) -> list[int]:
    return [func(x) for x in items]

# Literal types
from typing import Literal

Mode = Literal["read", "write", "append"]

def open_file(path: str, mode: Mode) -> None:
    ...

# Self reference
from typing import Self

class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.next: Self | None = None
```

## Reference
- [Python 3.12 What's New](https://docs.python.org/3/whatsnew/3.12.html)
- [Python 3.13 What's New](https://docs.python.org/3/whatsnew/3.13.html)
- [Python Typing in 2025](https://khaled-jallouli.medium.com/python-typing-in-2025-a-comprehensive-guide-d61b4f562b99)
- [Typing Module Documentation](https://docs.python.org/3/library/typing.html)
