---
name: ultrathink
description: Coordinator Agent orchestrating multiple specialist sub-agents for complex problem-solving. Use when tasks require architectural design, research, implementation, and codebase analysis combined. Triggered by complex multi-step tasks, architectural decisions, or when user explicitly runs /ultrathink.
---

# Ultrathink

## Overview

Orchestrate multiple specialist sub-agents to solve complex problems through coordinated effort. Combine architectural thinking, research capabilities, codebase analysis, and implementation work into a cohesive workflow.

## When to Use

Use this skill when:
- Tasks require multiple distinct areas of expertise
- Complex architectural decisions need to be made
- Research must be combined with implementation
- User explicitly invokes `/ultrathink <TASK_DESCRIPTION>`

## Process

### 1. Sequential Thinking (Brainstorming)

Use `/sequential-thinking` to:
- Break down the problem systematically
- Identify assumptions and unknowns
- Generate initial hypotheses
- Map out decision points

### 2. Docs Seeker (Research)

Use `/docs-seeker` to:
- Gather external documentation for relevant libraries
- Research precedents and best practices
- Find API specifications and examples
- Understand framework capabilities

### 3. Analyze Codebase (Context)

Use `/analyze-codebase` to:
- Understand existing architecture patterns
- Identify relevant files and dependencies
- Map relationships between components
- Discover existing implementations

### 4. Feature Cook (Implementation)

Use `/feature-cook` to:
- Implement the solution based on research
- Write or edit code following project patterns
- Integrate with existing codebase
- Ensure consistency with project conventions

## Output Format

After coordinating all sub-agents, present:

### Reasoning Transcript
Show major decision points and how each specialist contributed insights.

### Final Answer
Actionable steps, code edits, or commands in Markdown format.

### Next Actions
Bullet list of follow-up items (if any remain).

## Example Usage

```bash
/ultrathink Implement rate limiting for the API using Redis
```

This would:
1. Use sequential-thinking to design the approach
2. Use docs-seeker to find Redis rate-limiting patterns
3. Use analyze-codebase to understand current API structure
4. Use feature-cook to implement the solution
