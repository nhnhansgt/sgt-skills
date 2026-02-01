# Git Analysis Patterns

## Repository Status

```bash
# Current working tree status
git status --porcelain

# Show current branch
git branch --show-current
```

## Commit History

```bash
# Recent commits (last 10)
git log --oneline -10

# Detailed recent changes (1 week)
git log --since="1 week ago" --pretty=format:"%h - %an, %ar : %s" --stat

# Commits affecting specific paths
git log --oneline -10 -- "**/routes/**" "**/api/**"
```

## File Changes

```bash
# Changed files in last N commits
git diff --name-status HEAD~10

# Files added in last N commits
git diff --name-status HEAD~10 | grep "^A"

# Files deleted in last N commits
git diff --name-status HEAD~10 | grep "^D"

# Files modified in last N commits
git diff --name-status HEAD~10 | grep "^M"

# List changed files (names only)
git diff HEAD~5 --name-only | head -20
```

## Configuration Changes

```bash
# Package management changes
git diff HEAD~10 -- package.json package-lock.json yarn.lock pnpm-lock.yaml

# Build tool configurations
git diff HEAD~10 -- tsconfig.json webpack.config.js vite.config.js rollup.config.js

# Next.js specific
git diff HEAD~10 -- next.config.js

# Environment files
git diff HEAD~10 -- .env* .env.example

# Docker configurations
git diff HEAD~10 -- Dockerfile docker-compose* Dockerfile*

# Linting/formatting
git diff HEAD~10 -- .eslintrc* .prettierrc*
```

## API/Route Changes

```bash
# Route files
git diff HEAD~10 -- "**/routes/**" "**/api/**" "**/controllers/**" "**/handlers/**"

# Find all route files
find . -name "*route*" -o -name "*api*" -not -path "./node_modules/*" -not -path "./.git/*"
```

## Database/Model Changes

```bash
# Model/schema changes
git diff HEAD~10 -- "**/models/**" "**/schemas/**" "**/entities/**" "**/migrations/**"

# Find all model files
find . -name "*model*" -o -name "*schema*" -not -path "./node_modules/*" -not -path "./.git/*"
```

## Source Code Changes

```bash
# JavaScript/TypeScript changes
git diff HEAD~5 -- "*.js" "*.ts" "*.jsx" "*.tsx" | head -200

# Python changes
git diff HEAD~5 -- "*.py" | head -200

# Combined code file changes
git diff HEAD~5 -- "*.js" "*.ts" "*.jsx" "*.tsx" "*.py" "*.md" "*.json" | head -200
```

## Project Structure

```bash
# Find all markdown files
find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" -not -path "./dist/*" | head -20

# Find main entry points
find . -name "index.*" -o -name "main.*" -o -name "app.*" -not -path "./node_modules/*"

# Directory structure
find . -type d -not -path "./node_modules/*" -not -path "./.git/*" -not -path "./dist/*" -not -path "./build/*"
```

## Analysis Tips

- Use `head -N` to limit output for large diffs
- Use `grep "^PATTERN"` to filter specific change types (A=added, D=deleted, M=modified)
- Combine multiple git commands to get comprehensive view
- Focus on changes that affect developer workflow and documentation
- Look for patterns in commit messages to identify features
