# API Resources

## Purpose

Transform models into JSON responses. Consistent API output format.

## Structure

```
app/Http/Resources/
├── UserResource.php
└── UserCollection.php
```

## Generate Resource

```bash
php artisan make:resource UserResource
php artisan make:resource UserCollection
```

## Basic Resource

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at?->format('Y-m-d H:i:s'),
        ];
    }
}
```

## Controller Usage

```php
use App\Http\Resources\UserResource;
use App\Models\User;

public function show(User $user): UserResource
{
    return UserResource::make($user);
}

public function index(): AnonymousResourceCollection
{
    $users = User::paginate(15);
    return UserResource::collection($users);
}
```

## Collection Resource

For custom collection formatting:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data' => UserResource::collection($this->collection),
            'meta' => [
                'total' => $this->total(),
                'per_page' => $this->perPage(),
                'current_page' => $this->currentPage(),
                'last_page' => $this->lastPage(),
            ],
        ];
    }
}

// Usage
return new UserCollection(User::paginate(15));
```

## Nested Resources

```php
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        'author' => UserResource::make($this->whenLoaded('user')),
        'comments' => CommentResource::collection($this->whenLoaded('comments')),
    ];
}
```

## Conditional Attributes

```php
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->when($request->user()?->isAdmin(), $this->email),
        'secret' => $this->whenLoaded('secret'),
        'admin_notes' => $this->when(
            $request->user()->can('view_admin_notes'),
            fn() => $this->admin_notes
        ),
    ];
}
```

## Conditional Relationships

```php
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'posts' => PostResource::collection(
            $this->whenLoaded('posts')
        ),
    ];
}

// In controller
$user->load('posts'); // Only loads if needed
```

## Wrapping Response

```php
// In app/Providers/AppServiceProvider.php

public function boot(): void
{
    JsonResource::withoutWrapping();
}
```

## Including Metadata

```php
public function toArray(Request $request): array
{
    return [
        'data' => [
            'id' => $this->id,
            'name' => $this->name,
        ],
        'links' => [
            'self' => route('users.show', $this->id),
        ],
    ];
}
```

## Preserving Keys

```php
// For object collections, preserve keys
public function toArray(Request $request): array
{
    return $this->collection->mapWithKeys(function ($item) {
        return [$item->id => $item->name];
    });
}
```

## Rules

1. **No business logic** - Only transform data
2. **Use `whenLoaded()`** - Prevent N+1 queries
3. **Use `when()`** - Conditional attributes
4. **Use collections** - For list endpoints with pagination
5. **Type hints** - Always type hint `Request $request`

## Common Patterns

### With Relations

```php
// Controller
$user->load(['posts', 'profile']);

// Resource
return [
    'user' => UserResource::make($user),
    'posts' => PostResource::collection($user->posts),
    'profile' => ProfileResource::make($user->profile),
];
```

### Empty State

```php
return [
    'data' => $this->collection->isEmpty()
        ? []
        : UserResource::collection($this->collection),
];
```

---

**See also:** `controller-best-practices.md`, `service-layer.md`
