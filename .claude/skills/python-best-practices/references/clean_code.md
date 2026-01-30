# Clean Code Principles in Python

## Function Design

### Keep Functions Short and Focused
```python
# Bad - does too many things
def process_user(user_id):
    user = db.query(User).get(user_id)
    if not user:
        return None
    user.last_login = datetime.now()
    db.commit()
    email_service.send_welcome(user.email)
    return user

# Good - single responsibility
def get_user(user_id: int) -> User | None:
    return db.query(User).get(user_id)

def update_last_login(user: User) -> None:
    user.last_login = datetime.now()
    db.commit()

def send_welcome_email(user: User) -> None:
    email_service.send_welcome(user.email)
```

### Early Returns Over Nesting
```python
# Bad - deeply nested
def process_payment(order):
    if order:
        if order.user:
            if order.user.is_active:
                if order.amount > 0:
                    return charge(order)
    return None

# Good - early returns
def process_payment(order):
    if not order:
        return None
    if not order.user:
        return None
    if not order.user.is_active:
        return None
    if order.amount <= 0:
        return None
    return charge(order)
```

## Naming Best Practices

### Use Intention-Revealing Names
```python
# Bad
def d(d: int, t: int) -> int:
    return d * t

# Good
def calculate_distance(speed: int, time: int) -> int:
    return speed * time
```

### Avoid Disinformation
```python
# Bad - name suggests list
user_list = {"name": "John", "age": 30}

# Good
user_data = {"name": "John", "age": 30}
```

### Use Pronounceable Names
```python
# Bad
genymdhms = datetime.now()

# Good
current_timestamp = datetime.now()
```

## DRY Principle (Don't Repeat Yourself)

```python
# Bad - duplicated logic
def get_users_by_status(status):
    users = db.query(User).filter(User.status == status).all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
    return result

def get_users_by_role(role):
    users = db.query(User).filter(User.role == role).all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
    return result

# Good - extracted common logic
def serialize_user(user: User) -> dict:
    return {"id": user.id, "name": user.name, "email": user.email}

def get_users(filter_clause):
    users = db.query(User).filter(filter_clause).all()
    return [serialize_user(u) for u in users]
```

## Type Hints for Clarity

```python
# Bad
def process(data, items, flag):
    ...

# Good
def process(
    data: dict[str, Any],
    items: list[str],
    flag: bool | None = None
) -> list[dict[str, Any]]:
    ...
```

## List Comprehensions (When Appropriate)

```python
# Good - simple transformation
numbers = [1, 2, 3, 4, 5]
squared = [x ** 2 for x in numbers]

# Bad - too complex, use function instead
result = [x * 2 for x in items if x > 0 and x % 2 == 0 and str(x)[0] != '0']

# Good - extract to function
def should_transform(item):
    return item > 0 and item % 2 == 0 and str(item)[0] != '0'

result = [x * 2 for x in items if should_transform(x)]
```

## Dataclasses Over Dictionaries

```python
# Bad - dict for structured data
user = {
    "name": "John",
    "email": "john@example.com",
    "age": 30
}

# Good - dataclass
@dataclass
class User:
    name: str
    email: str
    age: int

user = User("John", "john@example.com", 30)
```

## Context Managers for Resources

```python
# Good - automatic cleanup
with open("file.txt", "r") as f:
    content = f.read()
# File automatically closed here

# Good - for database connections
with db.transaction():
    user.update(last_login=datetime.now())
# Transaction automatically committed/rolled back
```

## Constants Over Magic Numbers

```python
# Bad
if retry_count > 3:
    raise Exception("Too many retries")

# Good
MAX_RETRY_COUNT = 3

if retry_count > MAX_RETRY_COUNT:
    raise Exception("Too many retries")
```

## Reference
- [Clean Code in Python: 10 Rules](https://medium.com/the-pythonworld/clean-code-in-python-10-rules-to-follow-in-2025-a256dac3434d)
- [The Best Practices for Writing Clean Code](https://blog.logichook.in/2025/03/27/how-to-write-clean-codes-in-python/)
