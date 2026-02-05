# CLAUDE.md Structure Guidelines

## Section Update Guidelines

### Project Overview

Update when:
- Project scope changes significantly
- New technologies or frameworks added
- Version information changes

Include:
- Project type (web app, API, library, etc.)
- Primary technologies and frameworks
- Architecture pattern (MVC, microservices, etc.)
- Target platforms/environments

### Architecture

Update when:
- New architectural patterns introduced
- Significant structural changes occur
- Component relationships change

Include:
- Overall application architecture
- Key design patterns used
- Component relationships
- Data flow and request lifecycle

### Setup & Installation

Update when:
- New environment variables added
- Installation steps change
- Dependencies change significantly
- New configuration requirements

Include:
- Prerequisites (runtime, package manager)
- Installation commands
- Environment configuration
- Build/development server startup

### Development Workflow

Update when:
- New scripts added to package.json
- Development tools change
- Testing procedures updated
- Build processes change

Include:
- Available npm/yarn/pnpm scripts
- Development server commands
- Testing commands
- Linting/formatting procedures

### API Documentation

Update when:
- New endpoints added
- Existing endpoints modified
- Authentication/authorization changes
- Request/response formats change

Include:
- Base URL and versioning
- Authentication method
- Endpoint list with methods
- Request/response examples
- Error handling patterns

### File Structure

Update when:
- New directories added
- Files moved/reorganized
- Components deleted or renamed

Include:
- Directory explanations with purposes
- Key files and their functions
- How directories connect to each other

### Recent Updates

Add/update with:
- Timestamp of update (YYYY-MM-DD)
- Summary of major changes from git analysis
- New features and their impact
- Important bug fixes
- Breaking changes developers should know about

### Important Notes

Include:
- Key information for developers
- Security considerations
- Performance considerations
- Gotchas and common pitfalls

## Content Management Principles

### Don't Duplicate

- Avoid repeating information already in README
- Don't duplicate code comments
- Reference external docs instead of copying

### Prioritize Relevance

- Focus on changes affecting developer workflow
- Document what's not obvious from code
- Include context for architectural decisions

### Keep Concise

- Summarize changes; don't list every file
- Use bullet points for readability
- Link to detailed docs where available

### Maintain Structure

- Follow existing CLAUDE.md organization
- Keep consistent heading levels
- Use markdown formatting consistently

## Section Prioritization

When updating CLAUDE.md, prioritize these sections based on changes:

1. **High Priority**: API Documentation, Recent Updates, Setup & Installation
2. **Medium Priority**: Architecture, File Structure, Development Workflow
3. **Low Priority**: Overview (unless scope changed), Important Notes
