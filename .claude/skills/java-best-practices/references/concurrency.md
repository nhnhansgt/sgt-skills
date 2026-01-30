# Concurrency & Parallel Programming

## Thread Safety Basics

```java
// Bad: Not thread-safe
public class Counter {
    private int count = 0;
    public void increment() { count++; }  // Race condition
}

// Good: Using AtomicInteger
public class Counter {
    private final AtomicInteger count = new AtomicInteger(0);
    public void increment() { count.incrementAndGet(); }
}
```

## Synchronization

```java
// Synchronized method
public synchronized void update() { }

// Synchronized block (preferred - smaller scope)
public void update() {
    synchronized (lock) {
        // Critical section
    }
}

// Use private final lock object
private final Object lock = new Object();
```

## Thread-Safe Collections

```java
// ConcurrentHashMap - multiple readers, single writer per segment
ConcurrentMap<String, User> map = new ConcurrentHashMap<>();

// CopyOnWriteArrayList - read-heavy, write-rarely
List<Listener> listeners = new CopyOnWriteArrayList<>();

// BlockingQueue - producer-consumer
BlockingQueue<Task> queue = new LinkedBlockingQueue<>(100);

// Thread-safe Set
Set<String> set = Collections.newSetFromMap(new ConcurrentHashMap<>());
```

## ExecutorService (Preferred over raw threads)

```java
// Fixed thread pool
ExecutorService executor = Executors.newFixedThreadPool(10);

// Cached thread pool (creates on demand)
ExecutorService executor = Executors.newCachedThreadPool();

// Submit task
Future<String> future = executor.submit(() -> "result");

// Shutdown properly
executor.shutdown();
executor.awaitTermination(60, TimeUnit.SECONDS);
```

## CompletableFuture (Java 8+)

```java
// Async computation
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return longRunningOperation();
});

// Chaining
future.thenApply(result -> result.toUpperCase())
      .thenAccept(result -> System.out.println(result))
      .exceptionally(throwable -> { 
          log.error("Failed", throwable);
          return "default";
      });

// Multiple futures
CompletableFuture.allOf(future1, future2, future3).join();

// Timeout
future.orTimeout(5, TimeUnit.SECONDS);
```

## Parallel Streams (Use Carefully)

```java
// Good: CPU-intensive, large datasets, stateless operations
List<Result> results = items.parallelStream()
    .map(this::expensiveComputation)
    .toList();

// Bad: I/O-bound, small datasets, shared state
list.parallelStream().forEach(item -> {
    sharedList.add(process(item));  // Race condition!
});
```

## Virtual Threads (Java 21+)

```java
// Lightweight threads for I/O-bound operations
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10_000; i++) {
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));  // Blocking is OK
            return fetchDataFromDatabase();
        });
    }
}

// Replace thread-per-request models
void handleRequest(Request req) {
    // Works well with blocking I/O
    String data = fetchFromDb(req.getId());
    String result = callExternalApi(data);
    respond(result);
}
```

## ThreadLocal

```java
// Thread-local variables (use sparingly)
private static final ThreadLocal<SimpleDateFormat> formatter = 
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

// Must clean up
try {
    formatter.get().format(date);
} finally {
    formatter.remove();  // Prevent memory leak
}
```

## Avoid Common Issues

```java
// Deadlock - always acquire locks in same order
synchronized (lockA) {
    synchronized (lockB) { }  // Good
}

// Not this (can deadlock)
synchronized (lockA) {
    // Another thread holds lockB, waiting for lockA
}
synchronized (lockB) {
    // This thread holds lockA, waiting for lockB
}

// Starvation - use fair locks
ReentrantLock lock = new ReentrantLock(true);  // Fair mode

// Livelock - avoid excessive retry without backoff
int attempts = 0;
while (!tryOperation() && attempts++ < MAX_RETRIES) {
    Thread.sleep(100 * attempts);  // Exponential backoff
}
```

## References

- `references/modern-java.md` - Virtual threads, structured concurrency
- `references/performance.md` - Performance optimization
