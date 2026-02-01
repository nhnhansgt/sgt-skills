---
name: feature-cook
description: Orchestrate feature implementation by combining Explore agent for codebase discovery, Cook agent for implementation, and claudemd-updater for documentation updates. Use when implementing new features that require understanding existing codebase patterns before implementation. Workflow:Explore (serena mcp) → Cook (implement) → claudemd-updater (update CLAUDE.md).
author: sgt-skills
---

# Feature Cook

Orchestrate feature implementation by combining Explore and Cook agents with Serena MCP integration.

## Overview

This skill provides a workflow for implementing features that first requires understanding the existing codebase structure, patterns, and conventions before writing implementation code.

**When to use this skill:**
- Implementing new features in existing codebases
- Adding functionality that requires understanding existing patterns
- Working with unfamiliar codebases where context discovery is needed

## Workflow

### Step 1: Explore with Serena MCP

Use the **Explore subagent** with Serena MCP tools to scout the codebase:

```yaml
subagent_type: Explore
```

**Exploration goals:**
1. Understand project structure and architecture
2. Identify existing patterns and conventions
3. Locate relevant files and symbols
4. Understand data flows and dependencies
5. Find similar implementations for reference

**Key Serena tools to use:**
- `list_dir` - Discover directory structure
- `find_symbol` - Find classes, methods, functions
- `find_referencing_symbols` - Understand relationships
- `search_for_pattern` - Search code patterns
- `get_symbols_overview` - Get file overview

**Thoroughness levels:**
- `quick` - Fast, basic exploration
- `medium` - Moderate exploration (default)
- `very thorough` - Comprehensive analysis

### Step 2: Implement with Cook Agent

Use the **Cook subagent** to implement the feature based on exploration findings:

```yaml
subagent_type: cook
```

**Provide context from exploration:**
- Summarize discovered patterns
- Reference similar implementations found
- Note naming conventions
- Identify files to modify/create

**Cook agent handles:**
1. Documentation research via docs-seeker
2. Knowledge structuring via sequential-thinking
3. Implementation with best-practices skills:
   - **Next.js**: next-best-practices, next-cache-components, react-best-practices, frontend-design, ui-styling
   - **Laravel**: laravel-best-practices
   - **Java**: java-best-practices
   - **Python**: python-best-practices
   - **Shopify**: shopify-development
   - **UI/UX**: frontend-design, ui-styling, web-design-guidelines
4. Code review verification via code-review

### Step 3: Update CLAUDE.md

Use the **claudemd-updater agent** to automatically update `CLAUDE.md` with recent changes:

```yaml
subagent_type: claudemd-updater
```

The agent will:
- Analyze git history for recent changes
- Identify new features, API changes, configuration updates
- Update relevant CLAUDE.md sections
- Add timestamped summary to Recent Updates section

## Example Usage

```
User: Add user profile feature with avatar upload

Agent workflow:
1. [Explore subagent: medium] 
   - Find existing user models/controllers
   - Identify upload handling patterns
   - Discover storage configurations

2. [Cook subagent]
   - Implement profile routes/controller
   - Add avatar upload handling
   - Follow discovered patterns

3. [claudemd-updater agent]
   - Update CLAUDE.md with recent changes
```

## Key Principles

1. **Explore first** - Always understand context before implementing
2. **Specify subagent** - Always explicitly name the subagent (Explore, cook, claudemd-updater)
3. **Preserve patterns** - Follow existing codebase conventions
4. **Document changes** - Use claudemd-updater agent to keep CLAUDE.md updated

## See Also

- `references/workflow.md` - Detailed workflow guide