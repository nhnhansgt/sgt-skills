# Python Testing Strategies

## Framework Choice

### Prefer pytest for New Projects

```python
# pytest - simpler, more powerful
def test_calculate_discount():
    result = calculate_discount(100, 20)
    assert result == 80

# Parameterized testing
@pytest.mark.parametrize("price,discount,expected", [
    (100, 20, 80),
    (50, 10, 45),
    (200, 50, 100),
])
def test_calculate_discount(price, discount, expected):
    assert calculate_discount(price, discount) == expected
```

### unittest for Legacy Code

```python
# unittest - built-in, more verbose
import unittest

class TestDiscount(unittest.TestCase):
    def test_calculate_discount(self):
        result = calculate_discount(100, 20)
        self.assertEqual(result, 80)
```

## Test Organization

### Directory Structure
```
project/
├── src/
│   └── app.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # pytest fixtures
│   ├── test_app.py         # tests for app.py
│   └── unit/               # unit tests
│   └── integration/        # integration tests
```

### Naming Conventions
- Files: `test_*.py` or `*_test.py`
- Test functions: `test_*`
- Test classes: `Test*`
- Test methods: `test_*`

## AAA Pattern (Arrange, Act, Assert)

```python
def test_user_update():
    # Arrange - Set up test data
    user = User(name="John", email="john@example.com")
    db.add(user)
    db.commit()

    # Act - Execute the function being tested
    updated_user = update_user(user.id, name="Jane")

    # Assert - Verify expected outcome
    assert updated_user.name == "Jane"
    assert updated_user.email == "john@example.com"  # Unchanged
```

## Fixtures (pytest)

```python
# conftest.py
import pytest

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(name="Test User", email="test@example.com")

@pytest.fixture
def db_session():
    """Create a test database session."""
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

# Using fixtures
def test_user_update(sample_user, db_session):
    result = update_user(sample_user.id, name="Updated")
    assert result.name == "Updated"
```

## Mocking External Dependencies

```python
from unittest.mock import Mock, patch

def test_api_call():
    # Mock the external API
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": 1}

        result = fetch_user(1)

        assert result == {"id": 1}
        mock_get.assert_called_once_with("https://api.example.com/users/1")

# Using pytest-mock
def test_api_call_with_pytest(mocker):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200

    result = fetch_user(1)

    assert result.status_code == 200
```

## Test Coverage

### Measuring Coverage
```bash
# pytest with coverage
pytest --cov=src tests/

# Generate HTML report
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html
```

### Coverage Goals
- **Unit tests**: > 80% coverage
- **Critical paths**: 100% coverage
- **Configuration**: Don't chase 100% if it adds noise

## Integration Testing

```python
def test_user_registration_integration(client, db_session):
    """Test full registration flow."""
    response = client.post("/register", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "securepass123"
    })

    assert response.status_code == 201
    assert "id" in response.json()

    # Verify user was created in database
    user = db_session.query(User).filter_by(email="john@example.com").first()
    assert user is not None
    assert user.name == "John Doe"
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3
```

## Testing Best Practices

1. **One assertion per test** - Makes failures easier to diagnose
2. **Independent tests** - No shared state between tests
3. **Descriptive names** - `test_user_login_with_invalid_credentials` not `test_login_2`
4. **Test edge cases** - Empty inputs, None values, boundary conditions
5. **Use factories** - Use `factory_boy` for complex test data
6. **Avoid testing implementation details** - Test behavior, not internals

## Common Testing Pitfalls

| Pitfall | Solution |
|---------|----------|
| Fragile tests (break on refactoring) | Test behavior, not implementation |
| Slow tests | Mock external dependencies, use fixtures |
| Flaky tests | Isolate tests, avoid shared state |
| Testing private methods | Test public interface only |
| No tests for error cases | Add tests for exceptions, edge cases |

## Reference
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://dev.to/nkpydev/python-testing-unit-tests-pytest-and-best-practices-45gl)
- [Pytest vs Unittest Comparison](https://blog.jetbrains.com/pycharm/2024/03/pytest-vs-unittest/)
