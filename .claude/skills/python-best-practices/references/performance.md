# Python Performance Optimization

## Golden Rule: Profile Before Optimizing

Always measure first. Use these tools:
- **cProfile**: `python -m cProfile -s time script.py`
- **timeit**: `python -m timeit "code_here"`
- **line_profiler**: For line-by-line analysis

```python
import cProfile

def profile_function():
    pr = cProfile.Profile()
    pr.enable()
    # your code here
    pr.disable()
    pr.print_stats(sort='cumulative')
```

## Data Structure Selection

### Lookup Performance
```python
# Bad - O(n) lookup
items = ["apple", "banana", "cherry"]
if "banana" in items:
    pass

# Good - O(1) lookup
items = {"apple", "banana", "cherry"}
if "banana" in items:
    pass
```

### Choosing Right Structure

| Operation | list | set | dict |
|-----------|------|-----|------|
| Index access | O(1) | - | O(1) |
| Membership test | O(n) | O(1) | O(1) |
| Add element | O(1)* | O(1) | O(1) |
| Remove element | O(n) | O(1) | O(1) |

*May require O(n) for resizing

## List Comprehensions vs map/filter

```python
# Good - list comprehension (faster, more readable)
squared = [x ** 2 for x in range(1000) if x % 2 == 0]

# Slower - map/filter with lambda
squared = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, range(1000))))
```

## Generators for Large Datasets

```python
# Bad - loads everything in memory
def read_large_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f]

# Good - generator, memory efficient
def read_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()
```

## Built-in Functions (Highly Optimized)

```python
# Bad - manual loop
total = 0
for num in numbers:
    total += num

# Good - built-in sum
total = sum(numbers)

# Bad - manual min/max
minimum = numbers[0]
for num in numbers:
    if num < minimum:
        minimum = num

# Good - built-in min
minimum = min(numbers)
```

## String Concatenation

```python
# Bad - creates new string each iteration
result = ""
for item in items:
    result += str(item)

# Good - join is optimized
result = "".join(str(item) for item in items)
```

## Avoid Global Variables

```python
# Bad - global lookup is slower
counter = 0

def increment():
    global counter
    counter += 1

# Good - local variable lookup
def increment(counter):
    return counter + 1
```

## Use __slots__ for Classes

```python
# Good - saves memory for many instances
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

## Caching with functools.lru_cache

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## String Formatting

```python
# Fastest for Python 3.6+
name = "John"
age = 30
message = f"{name} is {age} years old"

# Alternative - format()
message = "{} is {} years old".format(name, age)
```

## Avoid Unnecessary Function Calls in Loops

```python
# Bad - function called every iteration
for item in items:
    process(get_config(item))

# Good - cache config lookup
config = get_config()
for item in items:
    process(config[item])
```

## Use Local Variables in Hot Loops

```python
# Bad - attribute lookup each time
for i in range(10000):
    obj.method(i)

# Good - bind to local variable
method = obj.method
for i in range(10000):
    method(i)
```

## Multiprocessing for CPU-Bound Tasks

```python
from multiprocessing import Pool

def process_item(item):
    # CPU-intensive work
    return item ** 2

# Good - use multiple cores
with Pool() as pool:
    results = pool.map(process_item, large_list)
```

## Reference
- [Ultimate Python Performance Guide 2025](https://www.fyld.pt/blog/python-performance-guide-writing-code-25/)
- [10 Smart Performance Hacks](https://blog.jetbrains.com/pycharm/2025/11/10-smart-performance-hacks-for-faster-python-code/)
