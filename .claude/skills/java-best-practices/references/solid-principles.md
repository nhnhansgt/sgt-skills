# SOLID Principles for Java

## Single Responsibility Principle (SRP)

A class should have one reason to change.

```java
// Bad: One class handles everything
class UserManager {
    void createUser(User u) { }
    void sendEmail(User u) { }
    void logAudit(User u) { }
}

// Good: Separated concerns
class UserService { void createUser(User u) { } }
class EmailService { void sendEmail(User u) { } }
class AuditService { void logAudit(User u) { } }
```

## Open/Closed Principle (OCP)

Open for extension, closed for modification.

```java
// Bad: Modify for each new payment type
class PaymentProcessor {
    void process(String type) {
        if (type.equals("credit")) { }
        else if (type.equals("paypal")) { }
    }
}

// Good: Extensible via interface
interface Payment { void pay(); }
class CreditPayment implements Payment { public void pay() { } }
class PaypalPayment implements Payment { public void pay() { } }
```

## Liskov Substitution Principle (LSP)

Subtypes must be substitutable for base types.

```java
// Bad: Square breaks Rectangle behavior
class Rectangle {
    void setWidth(int w) { }
    void setHeight(int h) { }
}
class Square extends Rectangle {
    void setWidth(int w) { super.setWidth(w); super.setHeight(w); }
}

// Good: Separate shapes with common interface
interface Shape { int getArea(); }
```

## Interface Segregation Principle (ISP)

Clients shouldn't depend on unused methods.

```java
// Bad: Fat interface
interface Worker {
    void work();
    void eat();
}

// Good: Segregated interfaces
interface Workable { void work(); }
interface Eatable { void eat(); }
```

## Dependency Inversion Principle (DIP)

Depend on abstractions, not concretions.

```java
// Bad: Depends on concrete class
class OrderProcessor {
    private MySQLDatabase db = new MySQLDatabase();
}

// Good: Depends on abstraction
class OrderProcessor {
    private Database db;
    OrderProcessor(Database db) { this.db = db; }
}
```

## References

- `references/clean-code.md` - Clean code principles
- `references/design-patterns.md` - Design patterns
