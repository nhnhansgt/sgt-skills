---
name: python-best-practices
description: Python best practices covering PEP 8 style guide, clean code principles, performance optimization, security (OWASP), testing (pytest), type hints (Python 3.12+), and anti-patterns. Use this skill when writing, reviewing, or refactoring Python code, or when tasks involve .py files, PEP standards, testing, or type hints.
---

# Python Best Practices

## Overview

Comprehensive guide for Python development covering style conventions, clean code principles, performance optimization, security best practices, testing strategies, modern Python features, and common anti-patterns to avoid.

## When to Use This Skill

- Writing new Python code
- Reviewing or refactoring existing Python code
- Setting up Python project structure
- Implementing testing strategies
- Adding type hints to codebase
- Optimizing Python performance
- Securing Python applications

## Core Categories

### 1. Code Style & Conventions
See `references/style_conventions.md` for PEP 8 guidelines, naming conventions, indentation rules, import ordering, and formatting standards.

### 2. Clean Code Principles
See `references/clean_code.md` for function design, naming practices, DRY principle, docstrings, and code organization.

### 3. Performance Optimization
See `references/performance.md` for data structure selection, optimization patterns, profiling techniques, and best practices.

### 4. Security Best Practices
See `references/security.md` for OWASP Top 10 coverage, injection prevention, input validation, and secure coding practices.

### 5. Testing Strategies
See `references/testing.md` for pytest vs unittest, test organization, mocking, coverage, and CI/CD integration.

### 6. Type Hints & Modern Python
See `references/type_hints.md` for Python 3.12+ features, typing module usage, type checkers, and modern syntax.

### 7. Anti-Patterns
See `references/anti_patterns.md` for common mistakes to avoid, deprecated patterns, and better alternatives.

## Quick Reference

### Essential PEP 8 Rules
- Naming: `snake_case` (functions/variables), `PascalCase` (classes), `UPPER_CASE` (constants)
- Indentation: 4 spaces, no tabs
- Line length: < 79 chars (code), < 72 (comments/docstrings)
- Imports: stdlib → third-party → local

### Clean Code Basics
- Functions: Short (< 20 lines), single responsibility
- Meaningful, descriptive names
- DRY principle
- Docstrings for public APIs
- Type hints for clarity

### Performance First Steps
- Profile before optimizing (cProfile, timeit)
- Right data structures: set/dict (O(1)) vs list (O(n))
- Built-in functions over manual loops
- Generators for large datasets

### Security Essentials
- Parameterized queries for SQL
- No hardcoded credentials
- Input validation & sanitization
- HTTPS in production

### Testing Guidelines
- Prefer pytest for new projects
- AAA pattern: Arrange, Act, Assert
- Coverage > 80%
- Mock external dependencies

## External References

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Python 3.12 What's New](https://docs.python.org/3/whatsnew/3.12.html)
- [Python 3.13 What's New](https://docs.python.org/3/whatsnew/3.13.html)
- [Pytest Documentation](https://docs.pytest.org/)
