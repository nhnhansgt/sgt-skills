# GitHub API Reference

## Pull Requests API

### Get PR Details

```
GET /repos/{owner}/{repo}/pulls/{pull_number}
```

Response includes:
- `number`: PR number
- `title`: PR title
- `body`: PR description
- `head`: Source branch info
- `base`: Target branch info
- `state`: open/closed/merged
- `diff_url`: URL to diff
- `patch_url`: URL to patch

### Get PR Comments

```
GET /repos/{owner}/{repo}/pulls/{pull_number}/comments
```

Query params:
- `page`: Page number (default: 1)
- `per_page`: Results per page (max: 100)

Response items:
- `id`: Comment ID
- `path`: File path
- `line`: Line in new version
- `original_line`: Line in old version
- `body`: Comment text
- `commit_id`: Commit SHA
- `user`: Author info

### Get PR Diff

```
GET /repos/{owner}/{repo}/pulls/{pull_number}
Accept: application/vnd.github.v3.diff
```

Returns unified diff format.

## Authentication

Use Bearer token in header:
```
Authorization: Bearer {token}
```

Or via `gh` CLI:
```bash
gh auth token
```

## Rate Limits

- Authenticated: 5000 req/hour
- Unauthenticated: 60 req/hour

Check rate limit:
```
GET /rate_limit
```

## Using gh CLI

```bash
# Get PR diff
gh pr view {number} --repo {owner}/{repo} --json title,body

# Get PR comments
gh pr view {number} --repo {owner}/{repo} --json comments -q '.comments[]'

# Download diff
gh pr diff {number} --repo {owner}/{repo} > diff.patch
```
