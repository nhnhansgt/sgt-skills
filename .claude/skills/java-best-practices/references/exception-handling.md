# Exception Handling Best Practices

## Basic Principles

```java
// Bad: Catching generic exceptions
try { } catch (Exception e) { }  // Never do this

// Bad: Silent catch
try { } catch (IOException e) { }  // Error swallowed

// Good: Catch specific exceptions
try { } catch (IOException e) { log.error("Failed", e); throw e; }
```

## Checked vs Unchecked

- **Checked**: `IOException`, `SQLException` - Recoverable, expected
- **Unchecked**: `NullPointerException`, `IllegalArgumentException` - Programming errors

```java
// Prefer unchecked for programming errors
if (email == null) {
    throw new IllegalArgumentException("Email required");
}

// Use checked for external failures
public void readFile(String path) throws IOException { }
```

## Exception Chaining

```java
// Always preserve root cause
try {
    executeQuery();
} catch (SQLException e) {
    throw new DataAccessException("Query failed", e);  // e is the cause
}
```

## Custom Exceptions

```java
// Business exceptions - unchecked
public class InsufficientFundsException extends RuntimeException {
    public InsufficientFundsException(BigDecimal amount, BigDecimal balance) {
        super(String.format("Insufficient funds: attempted %s, available %s", amount, balance));
    }
}

// System exceptions - checked
public class ConfigurationException extends Exception { }
```

## Try-with-Resources

```java
// Always auto-close resources
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql)) {
    // Auto-closes in reverse order
    return ps.executeQuery();
}
```

## Multi-catch (Java 7+)

```java
try {
    process();
} catch (IOException | SQLException | DataAccessException e) {
    log.error("Processing failed", e);
}
```

## Never Catch NullPointerException

```java
// Bad
try { user.getName().toUpperCase(); }
catch (NullPointerException e) { }

// Good
Optional.ofNullable(user)
         .map(User::getName)
         .map(String::toUpperCase)
         .orElse("");
```

## Validation at Boundaries

```java
public void withdraw(BigDecimal amount) {
    // Validate early, fail fast
    if (amount == null) throw new IllegalArgumentException("Amount required");
    if (amount.compareTo(BigDecimal.ZERO) <= 0) {
        throw new IllegalArgumentException("Amount must be positive");
    }
    // Business logic...
}
```

## Logging Exceptions

```java
// Include both message and cause
log.error("Failed to process order {}: {}", orderId, reason, exception);

// Not just the message
log.error("Error: " + exception.getMessage());  // Loses stack trace
```

## Return Results vs Exceptions

```java
// Use Optional for missing values (expected case)
public Optional<User> findById(Long id) { }

// Use exceptions for errors (unexpected case)
public User findByIdRequired(Long id) {
    return findById(id).orElseThrow(() -> 
        new NotFoundException("User not found: " + id));
}
```

## Retry Pattern

```java
@Retryable(maxAttempts = 3, backoff = @Backoff(delay = 1000))
public void callExternalService() throws TemporaryException {
    // Automatically retries on failure
}
```

## References

- `references/clean-code.md` - Clean code
- `references/security.md` - Error handling security
