# Performance Optimization

## Profiling First

Always measure before optimizing:
- **VisualVM** - Built into JDK
- **JProfiler** - Commercial
- **Java Mission Control (JMC)** - Flight recorder
- **Async-profiler** - Low overhead

## String Operations

```java
// Bad: String concatenation in loops
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i;  // Creates new String each iteration
}

// Good: Use StringBuilder
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);
}
String result = sb.toString();

// String.format() is slow - use for complex formatting only
String.format("User: %s, Age: %d", name, age);

// Faster: Simple concatenation
"User: " + name + ", Age: " + age;
```

## Collection Performance

```java
// ArrayList vs LinkedList
// ArrayList: O(1) access, O(n) insert at arbitrary position
// LinkedList: O(n) access, O(1) insert if you have the reference

// HashSet: O(1) add, contains, remove
// TreeSet: O(log n) add, contains, remove - use only if sorted needed

// Initialize with capacity when known
List<User> users = new ArrayList<>(10000);  // Avoids resizing
Map<String, User> map = new HashMap<>(expectedSize * 4 / 3);  // Load factor
```

## Stream vs Loop

```java
// For simple operations, traditional loops are often faster
int sum = 0;
for (int n : numbers) sum += n;

// Streams are cleaner but have overhead
int sum = numbers.stream().mapToInt(Integer::intValue).sum();

// Use streams for readability, loops for hot paths
```

## Object Creation

```java
// Avoid object allocation in hot loops
// Bad
for (Item item : items) {
    Date now = new Date();  // Creates millions of objects
    item.setTimestamp(now);
}

// Good
Date now = new Date();
for (Item item : items) {
    item.setTimestamp(now);
}

// Better: Use primitive types instead of wrappers
int total = 0;  // Good
Integer total = 0;  // Boxing overhead
```

## Caching

```java
// Cache expensive computations
private final Map<Input, Result> cache = new ConcurrentHashMap<>();

public Result compute(Input input) {
    return cache.computeIfAbsent(input, this::expensiveCompute);
}

// Or use Caffeine library
Cache<Input, Result> cache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(10, TimeUnit.MINUTES)
    .build();
```

## Lazy Initialization

```java
// Java 8+ lazy holder pattern
public class Singleton {
    private Singleton() { }
    
    private static class Holder {
        static final Singleton INSTANCE = new Singleton();
    }
    
    public static Singleton getInstance() {
        return Holder.INSTANCE;
    }
}
```

## Database Performance

```java
// Use connection pooling (HikariCP recommended)
HikariConfig config = new HikariConfig();
config.setMaximumPoolSize(20);
config.setJdbcUrl(jdbcUrl);
HikariDataSource ds = new HikariDataSource(config);

// Batch operations
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    for (Record r : records) {
        ps.setString(1, r.getValue());
        ps.addBatch();
        if (++count % BATCH_SIZE == 0) ps.executeBatch();
    }
    ps.executeBatch();  // Remaining
}

// Fetch size for large results
statement.setFetchSize(1000);
```

## JVM Tuning

```java
// Heap sizing
-Xms2g -Xmx2g  // Min and max heap equal - no resizing

// GC selection (Java 17+)
-XX:+UseZGC           // Low latency, < 10ms pauses
-XX:+UseG1GC          // Balanced (default)
-XX:+UseParallelGC    // High throughput, longer pauses

// Monitor GC
-XX:+PrintGC -XX:+PrintGCDetails -Xlog:gc*:file=gc.log
```

## NIO for I/O

```java
// FileChannel for large files
try (FileChannel channel = FileChannel.open(path, StandardOpenOption.READ)) {
    ByteBuffer buffer = ByteBuffer.allocate(8192);
    while (channel.read(buffer) != -1) {
        buffer.flip();
        // Process buffer
        buffer.clear();
    }
}

// Memory-mapped files for huge files
MappedByteBuffer mapped = channel.map(
    FileChannel.MapMode.READ_WRITE, 0, channel.size()
);
```

## References

- `references/concurrency.md` - Parallel processing
- `references/streams-and-collections.md` - Collections
