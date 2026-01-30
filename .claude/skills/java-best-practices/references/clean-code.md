# Clean Code Principles for Java

## Naming Conventions

- Use **intention-revealing names**: `int d;` → `int daysInWeek;`
- Classes: **PascalCase** - `CustomerService`, `OrderProcessor`
- Methods/variables: **camelCase** - `calculateTotal()`, `userName`
- Constants: **UPPER_SNAKE_CASE** - `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`
- Packages: **lowercase** - `com.example.service`

```java
// Bad
public class calc {
    public int c(int a, int b) { return a + b; }
}

// Good
public class Calculator {
    public int calculateSum(int addend1, int addend2) { return addend1 + addend2; }
}
```

## Functions

- **Small**: Functions should do one thing
- **Descriptive names**: `getCustomer()` not `getData()`
- **Arguments**: 0-2 ideal, 3 acceptable, avoid more
- **No side effects**: Functions should either change state OR return value, not both

```java
// Bad
public void process(boolean sendEmail) { /* does multiple things */ }

// Good
public void processOrder() { }
public void sendConfirmationEmail() { }
```

## Comments

- **Code should be self-documenting**
- Comments explain **why**, not **what**
- Delete commented code - use git history
- Javadoc for public APIs only

```java
// Bad
// Check if user is valid
if (user.isValid()) { }

// Good
if (user.hasActiveSubscription()) { }
```

## Code Structure

- **DRY** (Don't Repeat Yourself)
- **Single Responsibility Principle**: Each class/method has one reason to change
- **Vertical density**: Related concepts should be vertically close
- **Indentation**: 4 spaces, no tabs

## References

- See `references/solid-principles.md` for SOLID principles
- See `references/design-patterns.md` for design patterns
