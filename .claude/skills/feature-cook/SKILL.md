---
name: feature-cook
description: Orchestrate feature implementation by combining Explore agent for codebase discovery and Cook agent for implementation. Use when implementing new features that require understanding existing codebase patterns before implementation. Workflow: Explore (serena mcp) → Cook (implement).
author: sgt-skills
---

# Feature Cook

Orchestrate feature implementation by combining Explore and Cook agents with Serena MCP integration.

## Overview

This skill provides a two-phase workflow for implementing features:

1. **Explore (Scout)** - Serena MCP agent scouts the codebase and prepares comprehensive implementation context
2. **Cook (Execute)** - Implements the feature using the prepared context without redundant exploration

**When to use this skill:**
- Implementing new features that require understanding existing codebase patterns
- Adding functionality where you need to discover conventions before implementing
- Working with unfamiliar codebases where context discovery enables clean implementation

## Workflow

### Step 1: Explore with Serena MCP (Scout & Prepare Context)

Use the **Explore subagent** with Serena MCP tools to scout the codebase and prepare comprehensive context for the Cook subagent:

```yaml
subagent_type: Explore
```

**Purpose**: Gather and structure all necessary context so Cook can execute implementation efficiently without needing to explore the codebase itself.

**Exploration goals (Context Preparation):**
1. **Project structure** - Map out directories, entry points, and architecture
2. **Patterns & conventions** - Identify coding style, naming conventions, architectural patterns
3. **Relevant files & symbols** - Pinpoint exact files, classes, functions to modify/create
4. **Data flows & dependencies** - Understand how data moves through the system
5. **Reference implementations** - Find similar features to use as templates
6. **Tech stack & tools** - Note frameworks, libraries, build tools in use

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

### Step 2: Implement with Cook Agent (Execute with Context)

Use the **Cook subagent** to implement the feature using the context prepared by Explore:

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
   - **Next.js**: next-best-practices, next-cache-components, react-best-practices, vercel-composition-patterns, frontend-design, ui-styling
   - **Laravel**: laravel-best-practices
   - **Java**: java-best-practices
   - **Python**: python-best-practices
   - **Supabase/Postgres**: supabase-postgres-best-practices
   - **Shopify**: shopify-development
   - **UI/UX**: frontend-design, ui-styling, web-design-guidelines
4. Code review verification via code-review

## Example Usage

```
User: Add user profile feature with avatar upload

Agent workflow:

1. **[Explore subagent: medium]** - Scout codebase & prepare context
   - Locate: User model at `src/models/User.ts`, existing auth controllers
   - Identify: Upload pattern uses `multer` middleware in `src/middleware/upload.ts`
   - Discover: Storage configured in `src/config/storage.ts` (S3 bucket)
   - Context prepared for Cook: File paths, patterns, storage config

2. **[Cook subagent]** - Execute with provided context
   - Create profile controller using discovered patterns
   - Implement avatar upload with multer middleware
   - Follow existing code style and architecture
```

## Key Principles

1. **Explore to prepare** - Scout codebase to gather context, not to implement
2. **Cook to execute** - Implement using prepared context, avoid redundant exploration
3. **Pass context explicitly** - Cook should receive all necessary context from Explore
4. **Preserve patterns** - Follow existing codebase conventions discovered by Explore

## See Also

- `references/workflow.md` - Detailed workflow guide