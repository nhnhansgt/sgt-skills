# Laravel Best Practices

A structured repository for creating and maintaining Laravel Best Practices optimized for AI agents and LLMs. Based on MVC + Service Pattern architecture for maintainable, scalable Laravel applications.

## Structure

- `rules/` - Individual rule files (one per rule)
  - `_sections.md` - Section metadata (titles, impacts, descriptions)
  - `_template.md` - Template for creating new rules
  - `area-description.md` - Individual rule files
- `references/` - Original detailed documentation (legacy)
- `scripts/` - Build scripts and utilities
- `metadata.json` - Document metadata (version, organization, abstract)
- `SKILL.md` - Skill definition for Claude/LLM

## Getting Started

## Creating a New Rule

1. Copy `rules/_template.md` to `rules/area-description.md`
2. Choose the appropriate area prefix:
   - `perf-` for Performance (Section 1)
   - `security-` for Security (Section 2)
   - `arch-` for Architecture (Section 3)
   - `std-` for Coding Standards (Section 4)
   - `data-` for Data Layer (Section 5)
   - `request-` for Request Handling (Section 6)
   - `views-` for Views (Section 7)
   - `events-` for Events & Testing (Section 8)
3. Fill in the frontmatter and content
4. Ensure you have clear examples with explanations

## Rule File Structure

Each rule file should follow this structure:

```markdown
---
title: Rule Title Here
impact: MEDIUM
impactDescription: Optional description
tags: tag1, tag2
---

## Rule Title Here

**Impact: MEDIUM (optional impact description)**

Brief explanation of the rule and why it matters.

**Incorrect (description of what's wrong):**

```php
// Bad code example
```

**Correct (description of what's right):**

```php
// Good code example
```

Reference: [Link](https://example.com)
```

## File Naming Convention

- Files starting with `_` are special (excluded from builds)
- Rule files: `area-description.md` (e.g., `perf-eager-loading.md`)
- Section is automatically inferred from filename prefix
- IDs are auto-generated during build

## Impact Levels

- `CRITICAL` - Highest priority (security, performance killers)
- `HIGH` - Significant improvements (architecture, standards)
- `MEDIUM-HIGH` - Moderate-high gains (request handling)
- `MEDIUM` - Moderate improvements (views, events)
- `LOW-MEDIUM` - Low-medium gains
- `LOW` - Incremental improvements

## Rule Categories by Priority

| Priority | Category | Prefix | Impact |
|----------|----------|--------|--------|
| 1 | Performance | `perf-` | CRITICAL |
| 2 | Security | `security-` | CRITICAL |
| 3 | Architecture | `arch-` | HIGH |
| 4 | Coding Standards | `std-` | HIGH |
| 5 | Data Layer | `data-` | HIGH |
| 6 | Request Handling | `request-` | MEDIUM-HIGH |
| 7 | Views | `views-` | MEDIUM |
| 8 | Events & Testing | `events-` | MEDIUM |

## Quick Reference

### 1. Performance (CRITICAL)

- `perf-eager-loading` - Prevent N+1 queries with eager loading
- `perf-caching` - Cache strategies for performance

### 2. Security (CRITICAL)

- `security-authentication` - Sanctum, guards, password hashing
- `security-authorization` - Policies, gates, permissions

### 3. Architecture (HIGH)

- `arch-thin-controllers` - Thin controllers with service layer
- `arch-service-layer` - Service pattern for business logic

### 4. Coding Standards (HIGH)

- `std-psr-compliance` - PSR-12 coding standards
- `std-naming-conventions` - Laravel naming conventions

### 5. Data Layer (HIGH)

- `data-eloquent-fat-models` - Fat models with scopes, relationships
- `data-api-resources` - API resources for JSON responses
- `data-pagination` - Pagination for Blade and API

### 6. Request Handling (MEDIUM-HIGH)

- `request-form-requests` - Form Request validation
- `request-middleware` - Middleware for request filtering
- `request-routing` - Route groups, resource routes

### 7. Views (MEDIUM)

- `views-blade-components` - Blade components over includes
- `views-layouts` - Layout inheritance

### 8. Events & Testing (MEDIUM)

- `events-events-observers` - Event listeners and observers
- `events-testing` - PHPUnit and Pest testing

## Contributing

When adding or modifying rules:

1. Use the correct filename prefix for your section
2. Follow the `_template.md` structure
3. Include clear bad/good examples with explanations
4. Add appropriate tags
5. Update this README if adding new categories

## Acknowledgments

- Laravel Documentation: https://laravel.com/docs
- Spatie Guidelines: https://spatie.be/guidelines/laravel-php
- Laravel Best Practices by Alexey Mezenin: https://github.com/alexeymezenin/laravel-best-practices
