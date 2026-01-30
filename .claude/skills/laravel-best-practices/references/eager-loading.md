# Eager Loading

> Prevent N+1 query problems with eager loading

## Overview

Eager loading solves the **N+1 query problem** - a common performance issue when working with relationships.

## What is N+1 Problem?

### Example of N+1 Problem

```php
// ❌ BAD - N+1 queries
$posts = Post::all();  // 1 query to get all posts

foreach ($posts as $post) {
    echo $post->user->name;  // N queries (one per post)
}

// Total: 1 + N queries (N = number of posts)
```

### Solution with Eager Loading

```php
// ✅ GOOD - Eager loading
$posts = Post::with('user')->get();  // 2 queries total

foreach ($posts as $post) {
    echo $post->user->name;  // No additional queries
}

// Query 1: SELECT * FROM posts
// Query 2: SELECT * FROM users WHERE id IN (1, 2, 3, ...)
```

## Basic Eager Loading

### Loading Single Relationship

```php
// ✅ Good
$posts = Post::with('user')->get();

foreach ($posts as $post) {
    echo $post->user->name;
}
```

### Loading Multiple Relationships

```php
// ✅ Good - Load multiple relationships
$posts = Post::with(['user', 'comments'])->get();

foreach ($posts as $post) {
    echo $post->user->name;
    echo $post->comments->count();
}
```

### Nested Eager Loading

```php
// ✅ Good - Load nested relationships
$posts = Post::with('comments.user')->get();

// Or array syntax
$posts = Post::with(['comments.user'])->get();

// This loads:
// 1. All posts
// 2. All comments for those posts
// 3. All users for those comments
```

## Selective Column Loading

### Select Specific Columns

```php
// ✅ Good - Only load needed columns
$posts = Post::with(['user:id,name,email'])->get();

// Or with constraints
$posts = Post::with(['user' => function ($query) {
    $query->select('id', 'name', 'email');
}])->get();
```

### Important Note

```php
// ⚠️ Remember to include foreign key!
$posts = Post::with(['user:id,name'])->get();

// Must include 'id' and the foreign key (e.g., 'user_id')
// Otherwise Laravel can't match relationships
```

## Constrained Eager Loading

### Query Constraints

```php
// ✅ Good - Load active users only
$posts = Post::with(['user' => function ($query) {
    $query->where('is_active', true);
}])->get();

// ✅ Good - Load published comments only
$posts = Post::with(['comments' => function ($query) {
    $query->where('published', true)
          ->orderBy('created_at', 'desc');
}])->get();
```

### Lazy Eager Loading

```php
// ✅ Good - Load after initial query
$posts = Post::all();

// Later decide to load users
$posts->load('user');

// Or with constraints
$posts->load(['user' => function ($query) {
    $query->where('is_active', true);
}]);
```

## Counting Related Models

### withCount

```php
// ✅ Good - Add {relation}_count attribute
$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;  // Available as attribute
}
```

### Multiple Counts

```php
// ✅ Good
$posts = Post::withCount(['comments', 'likes'])->get();

foreach ($posts as $post) {
    echo $post->comments_count;
    echo $post->likes_count;
}
```

### Conditional Counting

```php
// ✅ Good - Count with constraints
$posts = Post::withCount(['comments' => function ($query) {
    $query->where('published', true);
}])->get();

foreach ($posts as $post) {
    echo $post->comments_count;  // Only published comments
}
```

### Alias Counts

```php
// ✅ Good - Custom count attribute names
$posts = Post::withCount([
    'comments as published_comments_count' => function ($query) {
        $query->where('published', true);
    },
    'comments as draft_comments_count' => function ($query) {
        $query->where('published', false);
    },
])->get();

foreach ($posts as $post) {
    echo $post->published_comments_count;
    echo $post->draft_comments_count;
}
```

## Existence Checking

### whereHas

```php
// ✅ Good - Filter by relationship existence
$posts = Post::whereHas('comments', function ($query) {
    $query->where('published', true);
})->get();

// Only posts with published comments
```

### doesntHave

```php
// ✅ Good - Filter by relationship absence
$posts = Post::doesntHave('comments')->get();

// Only posts without comments
```

### withWhereHas

```php
// ✅ Good - Filter AND load relationships
$posts = Post::withWhereHas('comments', function ($query) {
    $query->where('published', true);
})->get();

// Filters AND loads in one query
```

## Advanced Patterns

### Eager Loading with Pagination

```php
// ✅ Good
$posts = Post::with('user')
    ->paginate(15);

// Or on paginator
$posts = Post::paginate(15);
$posts->load('user');
```

### MorphTo Relationships

```php
// ✅ Good - Eager load polymorphic relationships
$comments = Comment::with('commentable')->get();

foreach ($comments as $comment) {
    echo $comment->commentable->title;
}
```

### Default Models

```php
// Model
class Post extends Model
{
    protected $with = ['user'];

    // Or define default model
    public function user()
    {
        return $this->belongsTo(User::class)->withDefault();
    }
}

// ✅ Good - Always loads user relationship
$posts = Post::all();

// No null errors
echo $posts->first()->user->name;  // Returns null if user doesn't exist
```

## Prevention Patterns

### Detect N+1 Queries

```php
// ✅ Good - Use Laravel Debugbar
// https://github.com/barryvdh/laravel-debugbar

// Or use clockwork
// https://github.com/itsgoingd/clockwork

// Enable query logging
DB::enableQueryLog();

$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name;
}

dd(DB::getQueryLog());  // See all queries
```

### Service Layer Pattern

```php
// ✅ Good - Encapsulate eager loading logic
class PostService
{
    public function getPostsWithAuthorsAndComments(int $perPage = 15): LengthAwarePaginator
    {
        return Post::with(['author', 'comments.user'])
            ->withCount(['comments', 'likes'])
            ->latest()
            ->paginate($perPage);
    }

    public function getPostWithRelationships(int $postId): Post
    {
        return Post::with([
            'author',
            'comments' => function ($query) {
                $query->where('approved', true)
                      ->with('user');
            },
            'tags',
        ])->findOrFail($postId);
    }
}
```

## Common Mistakes

### ❌ Bad Examples

```php
// ❌ Don't use all() with relationships
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name;  // N+1!
}

// ❌ Don't forget nested relationships
$posts = Post::with('comments')->get();
foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->user->name;  // N+1 on comments!
    }
}

// ❌ Don't query in loops
$posts = Post::all();
foreach ($posts as $post) {
    $post->load('user');  // Still N+1!
}
```

### ✅ Good Alternatives

```php
// ✅ Use with() instead
$posts = Post::with('user')->get();

// ✅ Eager load nested relationships
$posts = Post::with('comments.user')->get();

// ✅ Load once before loop
$posts = Post::all();
$posts->load('user', 'comments');
```

## Performance Tips

### Over-Eager Loading

```php
// ⚠️ Be careful not to over-eager load
// ❌ Bad - Too many relationships
$posts = Post::with([
    'author',
    'author.profile',
    'author.settings',
    'comments',
    'comments.user',
    'comments.user.profile',
    'tags',
    'category',
    'media',
])->get();

// ✅ Good - Load only what you need
$posts = Post::with(['author', 'comments.user'])->get();
```

### Chunk Processing

```php
// ✅ Good - Process large datasets in chunks
Post::chunk(100, function ($posts) {
    $posts->load('author', 'comments');

    foreach ($posts as $post) {
        // Process post
    }
});
```

## Quick Reference

| Method | Description | Example |
|--------|-------------|---------|
| `with()` | Eager load relationships | `Post::with('user')->get()` |
| `load()` | Lazy eager loading | `$posts->load('user')` |
| `withCount()` | Count relationships | `Post::withCount('comments')->get()` |
| `whereHas()` | Filter by relationship | `Post::whereHas('comments')->get()` |
| `doesntHave()` | No relationships | `Post::doesntHave('comments')->get()` |

## See Also

- **eloquent-best-practices.md** - Model relationships
- **service-layer.md** - Service layer patterns

---

**Reference**: Laravel 11.x Eloquent Documentation
