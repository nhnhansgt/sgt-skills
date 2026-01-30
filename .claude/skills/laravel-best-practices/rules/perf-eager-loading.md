---
title: Eager Loading to Prevent N+1 Queries
impact: CRITICAL
impactDescription: 10-100× query reduction
tags: performance, eager-loading, n+1, eloquent, relationships
---

## Eager Loading to Prevent N+1 Queries

Prevent N+1 query problems - the most common database performance issue in Laravel applications. Each relationship accessed in a loop triggers a separate query without eager loading.

**Incorrect (N+1 queries - 1 + N round trips):**

```php
$posts = Post::all();  // 1 query

foreach ($posts as $post) {
    echo $post->user->name;  // N additional queries
}
```

**Correct (Eager loading - 2 queries total):**

```php
$posts = Post::with('user')->get();  // 2 queries

foreach ($posts as $post) {
    echo $post->user->name;  // No additional queries
}
```

## Multiple Relationships

**Incorrect (Multiple N+1 problems):**

```php
$posts = Post::all();

foreach ($posts as $post) {
    echo $post->user->name;      // N queries
    echo $post->comments->count();  // N queries
}
```

**Correct (Load multiple relationships):**

```php
$posts = Post::with(['user', 'comments'])->get();

foreach ($posts as $post) {
    echo $post->user->name;      // No query
    echo $post->comments->count();  // No query
}
```

## Nested Relationships

**Incorrect (N+1 on nested relationships):**

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->user->name;  // N+1 on comments!
    }
}
```

**Correct (Eager load nested):**

```php
$posts = Post::with('comments.user')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->user->name;  // No query
    }
}
```

## Constrained Eager Loading

**Correct (Load with constraints):**

```php
$posts = Post::with(['comments' => function ($query) {
    $query->where('published', true)
          ->orderBy('created_at', 'desc');
}])->get();
```

## Counting Related Models

**Incorrect (Query in loop):**

```php
$posts = Post::all();

foreach ($posts as $post) {
    echo $post->comments()->count();  // N queries
}
```

**Correct (Use withCount):**

```php
$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;  // No query
}
```

## Service Layer Pattern

**Correct (Encapsulate eager loading logic):**

```php
class PostService
{
    public function getPostsWithRelationships(int $perPage = 15): LengthAwarePaginator
    {
        return Post::with(['author', 'comments.user'])
            ->withCount(['comments', 'likes'])
            ->latest()
            ->paginate($perPage);
    }
}
```

Reference: [Laravel Eloquent Documentation](https://laravel.com/docs/eloquent-relationships#eager-loading)
