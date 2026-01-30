# Collections & Streams API

## Choosing the Right Collection

```java
// List - ordered, allows duplicates
List<String> list = new ArrayList<>();  // Fast access, slow insert/delete
List<String> list = new LinkedList<>(); // Slow access, fast insert/delete

// Set - unique elements
Set<String> set = new HashSet<>();      // Fast, unordered
Set<String> set = new TreeSet<>();      // Sorted, slower
Set<String> set = new LinkedHashSet<>();// Insertion order

// Map - key-value pairs
Map<String, User> map = new HashMap<>();       // Fast, unordered
Map<String, User> map = new TreeMap<>();       // Sorted by key
Map<String, User> map = new LinkedHashMap<>(); // Insertion order
```

## Initialization

```java
// Java 9+ factory methods
List<String> list = List.of("a", "b", "c");
Set<Integer> set = Set.of(1, 2, 3);
Map<String, Integer> map = Map.of("a", 1, "b", 2);

// For mutable collections
List<String> list = new ArrayList<>(List.of("a", "b"));
```

## Common Stream Operations

```java
// Filtering
users.stream()
     .filter(u -> u.getAge() >= 18)
     .collect(Collectors.toList());

// Mapping
List<String> names = users.stream()
    .map(User::getName)
    .toList();

// FlatMap
List<Order> orders = customers.stream()
    .flatMap(c -> c.getOrders().stream())
    .toList();

// Distinct
List<String> unique = items.stream()
    .distinct()
    .toList();

// Sorting
users.stream()
    .sorted(Comparator.comparing(User::getName).reversed())
    .toList();

// Limiting & Skipping
users.stream()
    .skip(10)
    .limit(20)
    .toList();
```

## Collectors

```java
// To list/set
List<User> list = stream.collect(Collectors.toList());

// Grouping
Map<Department, List<User>> byDept = users.stream()
    .collect(Collectors.groupingBy(User::getDepartment));

// Partitioning
Map<Boolean, List<User>> activeInactive = users.stream()
    .collect(Collectors.partitioningBy(User::isActive));

// Joining strings
String names = users.stream()
    .map(User::getName)
    .collect(Collectors.joining(", "));

// Summarizing statistics
IntSummaryStatistics stats = users.stream()
    .collect(Collectors.summarizingInt(User::getAge));
System.out.println("Average age: " + stats.getAverage());

// To Map
Map<Long, User> userMap = users.stream()
    .collect(Collectors.toMap(User::getId, Function.identity()));

// Custom collector
Map<String, User> firstByName = users.stream()
    .collect(Collectors.toMap(
        User::getName,
        Function.identity(),
        (existing, replacement) -> existing  // keep first on duplicate
    ));
```

## Primitive Streams

```java
// Use specialized streams for primitives
IntStream.of(1, 2, 3).sum();
LongStream.range(1, 100).filter(n -> n % 2 == 0);
DoubleStream.generate(Math::random).limit(10);

// Convert to object stream
IntStream.range(0, 10).boxed().collect(Collectors.toList());
```

## Optional in Streams

```java
// Filter out empty optionals
List<String> emails = users.stream()
    .map(User::getEmail)
    .flatMap(Optional::stream)
    .toList();
```

## Performance Tips

- **Prefer `ArrayList`** for most list use cases
- **Use `HashSet`** for O(1) lookups
- **Avoid stream for single operations**: `list.get(0)` is faster than `list.stream().findFirst()`
- **Use `parallelStream()`** sparingly - only for large datasets with CPU-bound operations
- **Reuse comparators**: `Comparator.comparing(User::getName)`

## Common Pitfalls

```java
// Bad: Modifying collection while iterating
list.forEach(item -> {
    if (item.isBad()) list.remove(item);  // ConcurrentModificationException
});

// Good: Use removeIf
list.removeIf(item -> item.isBad());

// Bad: Boxing overhead
List<Integer> list = new ArrayList<>();
for (int i = 0; i < 1000; i++) list.add(i);

// Good: Use primitive arrays or specialized collections
int[] array = new int[1000];

// Bad: Multiple passes
stream.filter(a).map(b).collect(c);  // One pass
stream.filter(d).collect(e);         // Another pass - combine above

// Good: Single pass
stream.filter(a).map(b).filter(d).collect(e);
```

## References

- `references/modern-java.md` - Modern Java features
- `references/performance.md` - Performance optimization
