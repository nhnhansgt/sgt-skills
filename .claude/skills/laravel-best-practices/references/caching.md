# Caching

> Cache strategies, drivers, tags, locking

## Overview

Laravel caching provides unified API for various cache drivers like File, Database, Redis, Memcached.

## Configuration

### config/cache.php

```php
return [
    'default' => env('CACHE_DRIVER', 'redis'),

    'stores' => [
        'redis' => [
            'driver' => 'redis',
            'connection' => 'cache',
        ],
        'memcached' => [
            'driver' => 'memcached',
            'persistent_id' => env('MEMCACHED_PERSISTENT_ID'),
            'sasl' => [
                env('MEMCACHED_USERNAME'),
                env('MEMCACHED_PASSWORD'),
            ],
            'options' => [
                // Memcached::OPT_CONNECT_TIMEOUT => 2000,
            ],
        ],
    ],
];
```

## Basic Usage

### Cache Facade

```php
use Illuminate\Support\Facades\Cache;

// ✅ Good - Retrieve with default
$value = Cache::get('key', 'default');

// ✅ Good - Store for duration
Cache::put('key', 'value', $seconds = 60);
Cache::put('key', 'value', now()->addHours(1));

// ✅ Good - Store if not exists
Cache::add('key', 'value', $seconds);

// ✅ Good - Remember forever
Cache::rememberForever('key', function () {
    return DB::table('users')->get();
});

// ✅ Good - Check existence
if (Cache::has('key')) {
    //
}

// ✅ Good - Remove
Cache::forget('key');

// ✅ Good - Clear all
Cache::flush();
```

### Remember Pattern

```php
// ✅ Good - Cache remember
$users = Cache::remember('users.all', 3600, function () {
    return User::all();
});

// ✅ Good - Cache remember forever
$settings = Cache::rememberForever('app.settings', function () {
    return Setting::all()->pluck('value', 'key');
});
```

## Cache Drivers

| Driver | Description | Use Case |
|--------|-------------|----------|
| `file` | File system | Development, simple apps |
| `database` | Database table | Need cache queries |
| `redis` | Redis | Production, high performance |
| `memcached` | Memcached | Production, high performance |
| `array` | In-memory array | Testing only |

### Redis Configuration

```php
// config/database.php
'redis' => [
    'client' => env('REDIS_CLIENT', 'phpredis'),
    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],
    'default' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_CACHE_DB', '1'),
    ],
    'cache' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_CACHE_DB', '1'),
    ],
],
```

## Cache Tags

### Tagging Items

```php
// ✅ Good - Cache with tags
Cache::tags(['users', 'active'])->remember('users.active', 3600, function () {
    return User::active()->get();
});

Cache::tags(['posts'])->remember('posts.featured', 3600, function () {
    return Post::featured()->get();
});
```

### Flushing Tags

```php
// ✅ Good - Clear specific tag
Cache::tags(['users'])->flush();

// ✅ Good - Clear multiple tags
Cache::tags(['users', 'active'])->flush();
```

## Cache Locks

### Atomic Locks

```php
use Illuminate\Support\Facades\Cache;

// ✅ Good - Acquire lock
$lock = Cache::lock('export-users', 10);

if ($lock->get()) {
    // Perform expensive operation
    exportUsers();
    $lock->release();
}

// ✅ Good - Auto release
Cache::lock('export-users', 10)->get(function () {
    exportUsers();
});

// ✅ Good - Block until available
$lock = Cache::lock('export-users', 10);
$lock->block(5);  // Wait max 5 seconds

try {
    exportUsers();
} finally {
    $lock->release();
}
```

### Cross-Process Locks

```php
// ✅ Good - Prevent race conditions
$lock = Cache::lock('process-payment', 10);

if ($lock->block(5)) {
    try {
        // Only one process can execute this at a time
        $payment = processPayment($orderId);
    } finally {
        $lock->release();
    }
}
```

## Service Layer Pattern

```php
<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Support\Facades\Cache;

class UserService
{
    private const CACHE_TTL = 3600;  // 1 hour

    public function getAllUsers(): Collection
    {
        return Cache::remember('users.all', self::CACHE_TTL, function () {
            return User::with(['profile', 'roles'])->get();
        });
    }

    public function getActiveUsers(): Collection
    {
        return Cache::tags(['users', 'active'])->remember('users.active', self::CACHE_TTL, function () {
            return User::active()->get();
        });
    }

    public function getUserById(int $id): User
    {
        return Cache::remember("users.{$id}", self::CACHE_TTL, function () use ($id) {
            return User::with(['profile', 'roles'])->findOrFail($id);
        });
    }

    public function createUser(array $data): User
    {
        $user = User::create($data);

        // Clear caches
        Cache::forget('users.all');
        Cache::tags(['users'])->flush();

        return $user;
    }

    public function updateUser(int $id, array $data): User
    {
        $user = $this->getUserById($id);
        $user->update($data);

        // Clear specific cache
        Cache::forget("users.{$id}");
        Cache::tags(['users'])->flush();

        return $user;
    }

    public function deleteUser(int $id): bool
    {
        $user = User::findOrFail($id);
        $result = $user->delete();

        // Clear all user caches
        Cache::forget("users.{$id}");
        Cache::tags(['users'])->flush();

        return $result;
    }
}
```

## Model Caching

### Caching Model Queries

```php
// ✅ Good - Cache model queries
class Post extends Model
{
    public static function getCachedPosts(): Collection
    {
        return Cache::remember('posts.all', 3600, function () {
            return self::with(['user', 'tags'])->get();
        });
    }
}
```

### Caching Single Models

```php
// ✅ Good - Cache single model
$post = Cache::remember("posts.{$id}", 3600, function () use ($id) {
    return Post::with(['user', 'comments'])->findOrFail($id);
});
```

### Cache on Model Events

```php
// ✅ Good - Clear cache on model events
class Post extends Model
{
    protected static function booted()
    {
        static::saved(function ($post) {
            Cache::forget("posts.{$post->id}");
            Cache::tags(['posts'])->flush();
        });

        static::deleted(function ($post) {
            Cache::forget("posts.{$post->id}");
            Cache::tags(['posts'])->flush();
        });
    }
}
```

## Pagination with Cache

```php
// ✅ Good - Cache paginated results
public function getPaginatedPosts(int $page = 1, int $perPage = 15): LengthAwarePaginator
{
    $cacheKey = "posts.page.{$page}.per.{$perPage}";

    return Cache::remember($cacheKey, 3600, function () use ($page, $perPage) {
        return Post::with(['user'])->paginate($perPage, ['*'], 'page', $page);
    });
}
```

## Query Caching

### Database Query Cache

```php
use Illuminate\Support\Facades\DB;

// ✅ Good - Cache query results
$users = DB::table('users')
    ->orderBy('created_at', 'desc')
    ->cacheFor(3600)  // Cache for 1 hour
    ->cacheTags(['users'])
    ->get();
```

### Rememberable Trait

```php
// ✅ Good - Use rememberable
use Illuminate\Database\Eloquent\Model as BaseModel;

class Model extends BaseModel
{
    use \Awobaz\Compilable\Eloquent\Compilable;
}

// Usage
$users = User::remember(3600)->get();
```

## Cache Keys

### Naming Convention

```php
// ✅ Good - Descriptive cache keys
'users.all'
'users.active'
'users.by.email.' . md5($email)
'posts.featured'
'posts.user.' . $userId
'settings.app'
'stats.daily.' . now()->format('Y-m-d')
```

### Cache Key Prefixes

```php
// ✅ Good - Use prefixes
Cache::put('users:all', $users, 3600);
Cache::put('posts:featured', $posts, 3600);
```

## Performance Tips

### Warm Cache

```php
// ✅ Good - Warm cache on deployment
class WarmCacheCommand extends Command
{
    protected $signature = 'cache:warm';

    public function handle()
    {
        $this->info('Warming cache...');

        Cache::remember('users.all', 3600, fn () => User::all());
        Cache::remember('posts.featured', 3600, fn () => Post::featured()->get());

        $this->info('Cache warmed!');
    }
}
```

### Cache Events

```php
// ✅ Good - Listen to cache events
Event::listen(CacheMissed::class, function ($event) {
    Log::debug("Cache missed: {$event->key}");
});

Event::listen(CacheHit::class, function ($event) {
    Log::debug("Cache hit: {$event->key}");
});
```

## Best Practices

### DO ✅

```php
// ✅ Use cache for expensive operations
$results = Cache::remember('expensive.query', 3600, function () {
    return DB::table('large_table')->complexJoin()->get();
});

// ✅ Clear cache on updates
$user->update($data);
Cache::forget("users.{$user->id}");

// ✅ Use tags for related items
Cache::tags(['posts', 'user.' . $userId])->remember("posts.user.{$userId}", 3600, function () use ($userId) {
    return Post::where('user_id', $userId)->get();
});

// ✅ Use locks for race conditions
$lock = Cache::lock('process-payment', 10);
```

### DON'T ❌

```php
// ❌ Don't cache everything
Cache::remember('user.' . $user->id, 3600, function () use ($user) {
    return $user;  // User data changes frequently
});

// ❌ Don't forget to clear cache
$user->update($data);
// Cache not cleared!

// ❌ Don't use confusing cache keys
Cache::put('data1', $users, 3600);
Cache::put('data2', $posts, 3600);
```

## Quick Reference

| Method | Description |
|--------|-------------|
| `Cache::get()` | Retrieve from cache |
| `Cache::put()` | Store in cache |
| `Cache::remember()` | Get or store |
| `Cache::forget()` | Remove from cache |
| `Cache::flush()` | Clear all cache |
| `Cache::tags()` | Tag cache items |
| `Cache::lock()` | Acquire lock |
| `Cache::has()` | Check existence |
| `Cache::add()` | Add if not exists |
| `Cache::increment()` | Increment value |
| `Cache::decrement()` | Decrement value |

## See Also

- **eloquent-best-practices.md** - Model caching patterns
- **service-layer.md** - Service layer caching

---

**Reference**: Laravel 11.x Cache Documentation
