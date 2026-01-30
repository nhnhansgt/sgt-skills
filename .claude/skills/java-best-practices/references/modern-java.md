# Modern Java Features (Java 8+, 17+, 21+)

## Java 8+ Features

### Lambda Expressions
```java
// Before
button.addActionListener(new ActionListener() {
    public void actionPerformed(ActionEvent e) { System.out.println("Click"); }
});

// After
button.addActionListener(e -> System.out.println("Click"));
```

### Stream API
```java
// Filtering and mapping
List<String> names = users.stream()
    .filter(u -> u.getAge() > 18)
    .map(User::getName)
    .sorted()
    .toList();

// Collectors
Map<String, List<User>> byDepartment = users.stream()
    .collect(Collectors.groupingBy(User::getDepartment));

// Reduction
int sum = numbers.stream().reduce(0, Integer::sum);
```

### Optional
```java
// Always use Optional over null
public Optional<User> findById(Long id) { }

// Chaining
user.ifPresent(u -> sendEmail(u));

// Mapping & Filtering
optUser.map(User::getEmail)
      .filter(email -> email.endsWith("@company.com"))
      .ifPresent(this::sendEmail);
```

### New Date/Time API
```java
// Use java.time over java.util.Date
LocalDate today = LocalDate.now();
LocalDateTime now = LocalDateTime.now();
ZonedDateTime utc = ZonedDateTime.now(ZoneId.of("UTC"));

Period period = Period.between(date1, date2);
Duration duration = Duration.between(time1, time2);
```

## Java 11+ Features

### var (Local Variable Type Inference)
```java
// Use when type is obvious
var users = new ArrayList<User>();
var stream = users.stream();

// Not when type is unclear
var result = calculate();  // Bad - type unclear
```

### Text Blocks (Java 15+)
```java
String json = """
    {
        "name": "%s",
        "age": %d
    }
    """.formatted(name, age);
```

### Records (Java 16+)
```java
// Immutable data carriers
public record User(String name, String email) { }

// With validation
public record Email(String value) {
    public Email {
        if (!value.contains("@")) throw new IllegalArgumentException();
    }
}
```

### Pattern Matching instanceof (Java 16+)
```java
// Before
if (obj instanceof String) {
    String str = (String) obj;
    System.out.println(str.toUpperCase());
}

// After
if (obj instanceof String str) {
    System.out.println(str.toUpperCase());
}
```

## Java 17+ Features

### Sealed Classes
```java
public sealed interface Shape 
    permits Circle, Rectangle, Triangle {
}

public final class Circle implements Shape { }
public final class Rectangle implements Shape { }
```

### Enhanced Pseudo-Random Number Generators
```java
RandomGenerator factory = RandomGenerator.getDefault();
RandomGenerator random = factory.create(RandomGeneratorFactory.RandomAlgorithm.Xoshiro256PlusPlus);
```

## Java 21+ Features

### Record Patterns
```java
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + ", y=" + y);
}
```

### Pattern Matching for switch
```java
String formatted = switch (obj) {
    case Integer i -> String.format("int %d", i);
    case Long l -> String.format("long %d", l);
    case Double d -> String.format("double %f", d);
    case String s -> String.format("String %s", s);
    default -> obj.toString();
};
```

### Virtual Threads (Project Loom)
```java
// Lightweight concurrency
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i -> {
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return i;
        });
    });
}
```

### Scoped Values (Incubator)
```java
public static final ScopedValue<String> CONTEXT = ScopedValue.newInstance();
ScopedValue.where(CONTEXT, "value").run(() -> { });
```

### Structured Concurrency (Preview)
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Supplier<String> user = scope.fork(() -> fetchUser());
    Supplier<Integer> order = scope.fork(() -> fetchOrder());
    scope.join().throwIfFailed();
    return new Response(user.get(), order.get());
}
```

## Migration Tips

- **Java 8 → 11**: Replace `String.isEmpty()` with `String.isBlank()` for whitespace checking
- **Java 11 → 17**: Use `Record` for immutable data classes
- **Java 17 → 21**: Adopt virtual threads for I/O-bound operations

## References

- `references/java-conventions.md` - Style guide
- `references/streams-and-collections.md` - Collections & Streams
