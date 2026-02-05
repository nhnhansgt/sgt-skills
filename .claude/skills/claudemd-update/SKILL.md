---
name: claudemd-update
description: Automatically update CLAUDE.md file based on recent code changes. Use this skill when CLAUDE.md needs to be refreshed with new features, API changes, configuration updates, or structural changes discovered through git analysis.
---

# Update CLAUDE.md

Automatically update the CLAUDE.md file to reflect recent code changes discovered through git analysis.

## When to Use

- After implementing significant features
- When API endpoints change
- After refactoring code structure
- When new dependencies are added
- Before developer onboarding
- After configuration changes

## Analysis Workflow

### 1. Gather Current State

Read the existing CLAUDE.md:
```
@CLAUDE.md
```

### 2. Git Analysis

Use git commands to discover changes. See `references/git-analysis.md` for detailed command patterns:

- Repository status: `git status --porcelain`
- Recent commits: `git log --oneline -10`
- File changes: `git diff --name-status HEAD~10`
- Configuration diffs: `git diff HEAD~10 -- package.json tsconfig.json`

### 3. Analyze Changes

Categorize discovered changes:

- **New Features**: Added functionality from commit messages
- **API Changes**: Modified routes/controllers/endpoints
- **Configuration Updates**: Build tools, dependencies, environment variables
- **File Structure**: New directories, moved files, deleted components
- **Database**: New models, schema updates, migrations

### 4. Update CLAUDE.md

Update sections based on discovered changes. See `references/claudemd-structure.md` for section guidelines.

### 5. Generate Output

Produce complete updated CLAUDE.md content organized as:

```markdown
# Project Name

## Overview
[Updated project description]

## Architecture
[Updated architecture information]

## Setup & Installation
[Updated setup instructions]

## Development Workflow
[Updated development processes]

## API Documentation
[Updated API information]

## File Structure
[Updated directory explanations]

## Recent Updates (Updated: YYYY-MM-DD)
[Summary of recent changes]

## Important Notes
[Key information for developers]
```

## Content Principles

- **Preserve existing content**: Keep core project description, architecture, setup instructions
- **Intelligent integration**: Add new changes without duplicating existing information
- **Conciseness**: Summarize rather than listing every small change
- **Maintain structure**: Follow existing CLAUDE.md organization
- **Timestamp updates**: Note when major updates were made

## References

- `references/git-analysis.md` - Git command patterns for analyzing changes
- `references/claudemd-structure.md` - CLAUDE.md section guidelines and best practices
