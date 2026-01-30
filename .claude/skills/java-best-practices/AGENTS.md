# Java Best Practices - Agent Instructions

This document provides additional guidance for agents using the java-best-practices skill.

## Agent Usage Guidelines

### When Activating This Skill

Activate this skill when the user asks for help with:
- Writing or reviewing Java code
- Refactoring Java applications
- Implementing design patterns in Java
- Writing Java tests (JUnit, Mockito)
- Optimizing Java application performance
- Implementing concurrency or multi-threading
- Working with Spring framework
- Applying security practices in Java
- Migrating to modern Java versions

### How to Approach Java Tasks

1. **Understand the context** - Read existing code to understand patterns and conventions
2. **Apply relevant best practices** - Consult the appropriate reference files
3. **Explain trade-offs** - When multiple approaches exist, explain pros and cons
4. **Provide examples** - Show both "bad" and "good" code examples
5. **Follow conventions** - Use Google Java Style Guide as default

### Progressive Disclosure Strategy

Start with SKILL.md overview, then load specific references based on task:

| Task Type | Primary Reference |
|-----------|-------------------|
| General code quality | `clean-code.md`, `java-conventions.md` |
| Architecture design | `solid-principles.md`, `design-patterns.md` |
| Feature implementation | `modern-java.md`, relevant topic reference |
| Performance issues | `performance.md`, `streams-and-collections.md` |
| Concurrent code | `concurrency.md` |
| Security review | `security.md` |
| Writing tests | `testing.md` |
| Spring development | `spring-best-practices.md` |

### Common Decision Points

**Java Version Selection**
- Java 8 LTS: Baseline for most projects (lambdas, streams, Optional)
- Java 17 LTS: Modern standard (records, pattern matching, sealed classes)
- Java 21+: Latest features (virtual threads, pattern matching for switch)
- Default to Java 17 unless otherwise specified

**Collection Selection**
```
ArrayList      - General purpose, fast access
HashSet        - Unique elements, fast lookup
HashMap        - Key-value pairs, fast lookup
LinkedList     - Frequent insert/delete at arbitrary positions
TreeSet/Map    - Sorted data required
ConcurrentHashMap - Thread-safe, multiple readers
```

**Testing Approach**
- Unit tests for business logic (80% of tests)
- Integration tests for database/external APIs (15%)
- E2E tests for critical paths (5%)
- Aim for 80%+ line coverage on critical business logic

### Code Review Checklist

When reviewing Java code, check:
- [ ] Intention-revealing names (PascalCase/camelCase)
- [ ] Single Responsibility Principle
- [ ] No code duplication (DRY)
- [ ] Proper exception handling (no catch Exception)
- [ ] Thread safety for shared state
- [ ] Input validation at boundaries
- [ ] No hardcoded secrets
- [ ] Try-with-resources for AutoCloseable
- [ ] Optional over null for return values
- [ ] Stream API appropriate for operation

### Security Considerations

Always verify:
- Input validation and sanitization
- Parameterized queries (no SQL injection)
- Password hashing (bcrypt/Argon2, never plain text)
- Secrets from environment, never hardcoded
- HTTPS enabled for production
- Sensitive data not logged

### Performance Heuristics

Before optimizing:
1. Profile to identify actual bottlenecks
2. Consider algorithm complexity first
3. String concatenation in loops → StringBuilder
4. HashSet/HashMap for O(1) lookups
5. Streams for readability, loops for hot paths
6. Virtual threads for I/O-bound, parallel streams for CPU-bound

### Spring-Specific Guidance

- Prefer constructor injection
- Use @Service for business logic, @Repository for data access
- @Transactional at service layer, not controller
- RESTful URL design: GET/POST/PUT/PATCH/DELETE
- DTO validation with @Valid
- @RestControllerAdvice for exception handling

### Migration Tips

**Java 8 → 17**
- Replace `Optional.ofNullable()` with pattern matching
- Use records for immutable data classes
- Adopt text blocks for multi-line strings

**Java 17 → 21**
- Migrate to virtual threads for I/O-bound operations
- Use pattern matching for switch expressions
- Consider record patterns for deconstruction

## References

- SKILL.md - Main skill documentation
- references/ - Topic-specific best practices
