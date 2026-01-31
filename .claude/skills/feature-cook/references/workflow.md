# Feature Cook Workflow Guide

Detailed workflow for orchestrating feature implementation with Explore and Cook agents.

## Phase 1: Codebase Exploration (Explore Subagent)

### Launch Explore Agent

```yaml
subagent_type: Explore
model: sonnet  # or haiku for faster exploration
prompt: |
  Explore the codebase to understand:
  1. Project structure and architecture
  2. Existing patterns for [feature domain]
  3. Relevant files and symbols
  4. Naming conventions
  5. Dependencies and integrations

  Set thoroughness to: medium
```

### Exploration Checklist

- [ ] **Project Structure**
  - Main directories and their purposes
  - Framework/stack identification
  - Entry points (main, index, routes)

- [ ] **Code Patterns**
  - Similar existing implementations
  - Naming conventions (files, variables, functions)
  - Error handling patterns
  - State management approach

- [ ] **Key Symbols**
  - Relevant classes/modules
  - API endpoints/routes
  - Database models/schemas
  - Utility functions

- [ ] **Data Flow**
  - Request/response patterns
  - Database queries
  - External API calls
  - File operations

### Serena MCP Tools Reference

| Tool | Purpose | Usage |
|------|---------|-------|
| `list_dir` | Directory structure | `list_dir({relative_path, recursive})` |
| `find_symbol` | Find classes/functions | `find_symbol({name_path_pattern, relative_path})` |
| `get_symbols_overview` | File overview | `get_symbols_overview({relative_path})` |
| `search_for_pattern` | Search code patterns | `search_for_pattern({substring_pattern})` |
| `find_referencing_symbols` | Find relationships | `find_referencing_symbols({name_path})` |

### Output from Exploration

Document findings for Cook agent:

```markdown
## Exploration Summary

### Project Context
- Framework: [e.g., Laravel, Next.js, Django]
- Architecture: [e.g., MVC, components, services]
- Language: [e.g., PHP, TypeScript, Python]

### Relevant Patterns Found
1. **Pattern Name**: Description
   - File location: `path/to/example`
   - Key implementation notes

### Files to Modify
- `path/to/file1` - Purpose
- `path/to/file2` - Purpose

### Files to Create
- `path/to/new_file` - Purpose

### Naming Conventions
- Classes: PascalCase
- Functions: camelCase/snake_case
- Files: kebab-case
```

## Phase 2: Implementation (Cook Subagent)

### Launch Cook Agent

```yaml
subagent_type: cook
prompt: |
  Implement [feature] based on exploration findings:

  ## Context from Exploration
  [Paste exploration summary here]

  ## Requirements
  [Detailed feature requirements]

  Follow the cook workflow: docs → structure → implement → review
```

### Cook Workflow (Built-in)

The Cook agent follows this 4-phase workflow:

1. **Documentation Research** - Uses docs-seeker skill
2. **Knowledge Structuring** - Uses sequential-thinking skill
3. **Implementation** - Uses best-practices skills
4. **Code Review** - Uses code-review skill

### Providing Context to Cook

Essential context from exploration:

```markdown
## Codebase Context

### Existing Similar Implementation
Reference: `path/to/similar/file.ts:line_number`
Key pattern: [description]

### Project Conventions
- File organization: [description]
- Naming style: [description]
- Testing approach: [description]

### Dependencies
- [Package]: [version] - [purpose]
- [Package]: [version] - [purpose]
```

## Phase 3: Update CLAUDE.md

### What to Document

```markdown
## Recent Changes

### [Feature Name] - YYYY-MM-DD

**Description**
[1-2 sentence feature description]

**Implementation**
- Created: `path/to/new_files`
- Modified: `path/to/modified_files`

**Patterns Discovered**
- [Pattern 1]: Description
- [Pattern 2]: Description

**Dependencies Added**
- [package]: [version]

**Notes**
[Any additional context for future work]
```

### CLAUDE.md Best Practices

- **Keep it chronological** - Newest changes at top
- **Be concise** - 1-2 sentences per item
- **Link to code** - Use `file:line` format
- **Document patterns** - Not just changes, but conventions

## Common Workflows

### Adding a New API Endpoint

```
1. Explore: Find existing routes, controllers, validation patterns
2. Cook: Implement endpoint following discovered patterns
3. CLAUDE.md: Document new route and patterns used
```

### Adding a New UI Component

```
1. Explore: Find component structure, styling patterns, state management
2. Cook: Build component with frontend-design/ui-styling skills
3. CLAUDE.md: Document component and design patterns
```

### Adding Database Migration

```
1. Explore: Find existing migrations, model conventions
2. Cook: Create migration following framework patterns
3. CLAUDE.md: Document schema change and model updates
```

## Troubleshooting

### Exploration Returns Too Much

- Reduce thoroughness to `quick`
- Narrow `relative_path` to specific directories
- Use more specific search patterns

### Cook Agent Doesn't Follow Patterns

- Provide explicit context from exploration
- Reference specific file:line examples
- List naming conventions explicitly

### CLAUDE.md Getting Too Long

- Summarize older changes into `CHANGELOG.md`
- Keep only recent 3-6 months of detailed changes
- Focus on patterns, not just file lists
