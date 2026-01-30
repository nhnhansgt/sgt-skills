# Java Conventions & Style Guide

## Code Style (Follow Google Java Style Guide)

### Indentation & Spacing
- **4 spaces** for indentation (no tabs)
- **1 blank line** between methods
- **No trailing whitespace**

### Line Length
- **Max 100 characters** per line
- Break at logical points (operators, commas)

### Braces
```java
// K&R style (opening brace on same line)
public void method() {
    if (condition) {
        doSomething();
    }
}
```

### Imports
- **No wildcards**: `import java.util.List;` not `import java.util.*;`
- **Static imports last**
- **Sorted alphabetically** (IDE default)

## Package Structure

```
com.company.project
├── model/          # Domain entities
├── repository/     # Data access
├── service/        # Business logic
├── controller/     # REST/WEB layer
├── dto/            # Data transfer objects
├── exception/      # Custom exceptions
└── util/           # Utilities (use sparingly)
```

## Class Organization

```java
// 1. Static fields (constants first)
// 2. Instance fields
// 3. Constructors
// 4. Static methods
// 5. Instance methods (public, then protected, then private)
// 6. Inner classes
```

## Access Modifiers

- **Prefer private**: Hide implementation
- **protected only**: For inheritance
- **public**: API surface only
- **package-private**: Default, use intentionally

## Method Design

```java
// Good: Clear purpose, single responsibility
public Optional<User> findById(Long id) { }
public List<User> findActiveUsers() { }

// Bad: Unclear, does too much
public Object getData(Object input) { }
```

## Constants

```java
// Good
public static final int MAX_RETRY_COUNT = 3;
public static final String DEFAULT_ENCODING = "UTF-8";

// Bad
public static final int n = 3;
```

## Logging (SLF4J)

```java
// Use parameterized logging
log.debug("User {} logged in at {}", user.getName(), LocalDateTime.now());
log.error("Failed to process order {}", orderId, exception);

// Not string concatenation
log.debug("User " + user + " logged in");  // Bad
```

## Equals & HashCode

```java
// Always override together
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    User user = (User) o;
    return Objects.equals(id, user.id);
}

@Override
public int hashCode() { return Objects.hash(id); }
```

## References

- `references/clean-code.md` - Clean code principles
- `references/modern-java.md` - Modern Java features
