---
name: java-best-practices
description: Java best practices covering clean code, SOLID principles, design patterns, Java conventions (Google style guide), modern Java features (Java 8/17/21+), exception handling, Collections & Streams API, concurrency and parallel programming (including virtual threads), performance optimization, security best practices, testing (JUnit 5, Mockito), and Spring/DI best practices. Use when writing, reviewing, or refactoring Java code; implementing new Java features; applying design patterns; writing tests; optimizing Java performance; or working with Spring framework.
---

# Java Best Practices

Apply industry-standard Java best practices when writing, reviewing, or refactoring Java code.

## When to Use This Skill

Use this skill when:
- Writing new Java code
- Reviewing or refactoring existing Java code
- Implementing design patterns in Java
- Writing tests (JUnit, Mockito)
- Optimizing Java application performance
- Working with concurrency and multi-threading
- Implementing Spring-based applications
- Applying security practices
- Migrating to modern Java versions (8, 17, 21+)

## Core Principles

Start with foundational concepts:
- `references/clean-code.md` - Naming, functions, comments, structure
- `references/solid-principles.md` - SRP, OCP, LSP, ISP, DIP
- `references/design-patterns.md` - Creational, structural, behavioral patterns

## Code Style & Conventions

Follow Google Java Style Guide:
- `references/java-conventions.md` - Formatting, package structure, organization
- `references/modern-java.md` - Java 8+ lambdas, streams, Optional, records, pattern matching, virtual threads

## Essential Practices

- **Exception Handling**: `references/exception-handling.md` - Checked vs unchecked, custom exceptions, try-with-resources
- **Collections & Streams**: `references/streams-and-collections.md` - Choosing collections, stream operations, collectors
- **Concurrency**: `references/concurrency.md` - Thread safety, ExecutorService, CompletableFuture, virtual threads
- **Performance**: `references/performance.md` - Profiling, string operations, caching, JVM tuning
- **Security**: `references/security.md` - Input validation, password hashing, SQL injection prevention, secrets management

## Testing & Spring

- **Testing**: `references/testing.md` - JUnit 5, Mockito, test coverage, integration tests
- **Spring/DI**: `references/spring-best-practices.md` - Constructor injection, configuration, transactions, REST APIs

## Quick Reference

### Clean Code Checklist
- Intention-revealing names (PascalCase for classes, camelCase for methods/vars)
- Functions do one thing, are small, have 0-2 arguments
- Comments explain "why", not "what"
- No code duplication (DRY)

### SOLID Principles
- **S**RP: One reason to change
- **O**CP: Open for extension, closed for modification
- **L**SP: Subtypes must be substitutable
- **I**SP: No fat interfaces
- **D**IP: Depend on abstractions

### Modern Java Features (Java 21+)
- Records for immutable data carriers
- Pattern matching for `switch` and `instanceof`
- Virtual threads for I/O-bound operations
- Text blocks for multi-line strings
- Sealed classes for restricted inheritance
