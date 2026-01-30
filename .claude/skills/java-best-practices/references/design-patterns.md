# Design Patterns for Java

## Creational Patterns

### Singleton (use sparingly)
```java
public enum Database {
    INSTANCE;
    public void connect() { }
}
```

### Factory Method
```java
interface Payment { void pay(); }
class PaymentFactory {
    static Payment create(String type) {
        return switch (type) {
            case "credit" -> new CreditPayment();
            case "paypal" -> new PaypalPayment();
            default -> throw new IllegalArgumentException();
        };
    }
}
```

### Builder
```java
class User {
    private String name;
    private String email;
    
    public static class Builder {
        private String name;
        private String email;
        public Builder name(String n) { this.name = n; return this; }
        public Builder email(String e) { this.email = e; return this; }
        public User build() { return new User(this); }
    }
}
```

## Structural Patterns

### Adapter
```java
interface MediaPlayer { void play(String type); }
class MediaAdapter implements MediaPlayer {
    AdvancedPlayer player;
    public void play(String type) { player.playAdvanced(type); }
}
```

### Decorator
```java
interface Coffee { double cost(); }
class SimpleCoffee implements Coffee { public double cost() { return 1; } }
class MilkDecorator implements Coffee {
    Coffee coffee;
    public double cost() { return coffee.cost() + 0.5; }
}
```

### Facade
```java
class ComputerFacade {
    private CPU cpu;
    private Memory memory;
    public void start() { cpu.freeze(); memory.load(); cpu.jump(); }
}
```

## Behavioral Patterns

### Strategy
```java
interface SortStrategy { void sort(int[] arr); }
class BubbleSort implements SortStrategy { public void sort(int[] arr) { } }
class QuickSort implements SortStrategy { public void sort(int[] arr) { } }

class Sorter {
    private SortStrategy strategy;
    public void setStrategy(SortStrategy s) { this.strategy = s; }
    public void sort(int[] arr) { strategy.sort(arr); }
}
```

### Observer
```java
interface Observer { void update(String msg); }
interface Subject {
    void attach(Observer o);
    void notifyObservers(String msg);
}
```

### Command
```java
interface Command { void execute(); }
class LightOnCommand implements Command {
    private Light light;
    public void execute() { light.on(); }
}
```

## When to Use Each

- **Singleton**: Logging, configuration, DB connections (prefer DI containers)
- **Factory**: Creating objects without specifying exact class
- **Builder**: Complex object construction
- **Strategy**: Interchangeable algorithms
- **Observer**: Event-driven systems
- **Command**: Undo/redo, queueing operations

## References

- `references/clean-code.md` - Clean code
- `references/solid-principles.md` - SOLID principles
