# Authorization

> Policies, Gates, permissions for access control

## Overview

Laravel authorization provides 2 main ways to manage access control: **Gates** and **Policies**.

## Gates vs Policies

| Feature | Gates | Policies |
|---------|-------|----------|
| **Use case** | Simple, non-model authorization | Model-specific authorization |
| **Location** | `AuthServiceProvider` | Separate policy classes |
| **Example** | `is-admin`, `access-dashboard` | `update-post`, `delete-user` |
| **Granularity** | Coarse-grained | Fine-grained |

## Gates

### Defining Gates

```php
// App\Providers\AuthServiceProvider.php
use Illuminate\Support\Facades\Gate;

public function boot()
{
    // ✅ Good - Simple gate
    Gate::define('admin', function ($user) {
        return $user->role === 'admin';
    });

    // ✅ Good - Gate with parameters
    Gate::define('update-post', function ($user, $post) {
        return $user->id === $post->user_id;
    });

    // ✅ Good - Gate for super admin
    Gate::before(function ($user, $ability) {
        if ($user->isSuperAdmin()) {
            return true;
        }
    });

    // ✅ Good - Gate after check (deny)
    Gate::after(function ($user, $ability, $result) {
        if (!$result && $user->hasBannedRole()) {
            return false;  // Always deny banned users
        }
    });
}
```

### Checking Gates

```php
// ✅ Good - In controllers
public function update(Request $request, Post $post)
{
    if (!Gate::allows('update-post', $post)) {
        abort(403);
    }

    // Or use authorize method
    Gate::authorize('update-post', $post);

    // Update post
}

// ✅ Good - In blade
@can('update-post', $post)
    <button>Edit Post</button>
@elsecan('update-post', $post)
    <p>Not authorized</p>
@endcan

@cannot('delete-post', $post)
    <p>Cannot delete</p>
@endcannot

// ✅ Good - In models (or anywhere)
if (Gate::forUser($user)->allows('update-post', $post)) {
    // User can update post
}
```

### Gate Responses

```php
// ✅ Good - Custom response messages
Gate::define('update-post', function ($user, $post) {
    if ($user->id !== $post->user_id) {
        Gate::deny('You are not the author of this post');
    }

    return true;
});
```

## Policies

### Creating Policy

```bash
# Artisan command
php artisan make:policy PostPolicy --model=Post
```

### Registering Policy

```php
// App\Providers\AuthServiceProvider.php
protected $policies = [
    Post::class => PostPolicy::class,
    User::class => UserPolicy::class,
];
```

### Policy Structure

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the user can view any models.
     */
    public function viewAny(User $user): bool
    {
        return true;  // Can view list of posts
    }

    /**
     * Determine if the user can view the model.
     */
    public function view(User $user, Post $post): bool
    {
        // Can view if published or is owner
        return $post->isPublished()
            || $user->id === $post->user_id;
    }

    /**
     * Determine if the user can create models.
     */
    public function create(User $user): bool
    {
        return $user->can('create_posts');
    }

    /**
     * Determine if the user can update the model.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }

    /**
     * Determine if the user can delete the model.
     */
    public function delete(User $user, Post $post): bool
    {
        return $user->id === $post->user_id
            || $user->isAdmin();
    }

    /**
     * Determine if the user can restore the model.
     */
    public function restore(User $user, Post $post): bool
    {
        return $user->isAdmin();
    }

    /**
     * Determine if the user can permanently delete the model.
     */
    public function forceDelete(User $user, Post $post): bool
    {
        return $user->isSuperAdmin();
    }
}
```

### Policy Responses

```php
// ✅ Good - Custom messages
public function update(User $user, Post $post): bool|Response
{
    if ($post->isLocked()) {
        return response()->deny('This post is locked and cannot be edited.');
    }

    return $user->id === $post->user_id;
}
```

### Using Policies in Controllers

```php
// ✅ Good - Controller helper method
class PostController extends Controller
{
    public function update(UpdatePostRequest $request, Post $post)
    {
        $this->authorize('update', $post);

        // Or use model
        $this->authorize($post);

        // Update post
    }

    public function destroy(Post $post)
    {
        $this->authorize('delete', $post);

        $post->delete();
        return response()->json(null, 204);
    }
}
```

### Policy Auto-Discovery

```php
// No need to register in AuthServiceProvider
// Laravel automatically finds:
// App\Policies\PostPolicy → Post model
// App\Policies\UserPolicy → User model
```

## Using Policies

### In Blade

```blade
@can('update', $post)
    <button>Edit Post</button>
@elsecan('update', $post)
    <p>You cannot edit this post</p>
@endcan

@cannot('delete', $post)
    <p>You cannot delete this post</p>
@endcannot

// ✅ Good - @canany
@canany(['update', 'delete'], $post)
    <button>Manage Post</button>
@elsecanany(['update', 'delete'], $post)
    <p>No permissions</p>
@endcanany
```

### In Models/Services

```php
// ✅ Good - Check policy anywhere
if ($user->can('update', $post)) {
    // User can update post
}

if ($user->cannot('delete', $post)) {
    // User cannot delete post
}
```

### In Middleware

```php
// ✅ Good - Route middleware
Route::put('/posts/{post}', [PostController::class, 'update'])
    ->middleware('can:update,post');

Route::delete('/posts/{post}', [PostController::class, 'delete'])
    ->middleware('can:delete,post');
```

## Resource Controllers

### Policy Methods Mapping

| Controller Method | Policy Method | Description |
|-------------------|---------------|-------------|
| `index()` | `viewAny()` | List all resources |
| `show()` | `view()` | View single resource |
| `create()` | `create()` | Show create form |
| `store()` | `create()` | Store new resource |
| `edit()` | `update()` | Show edit form |
| `update()` | `update()` | Update resource |
| `destroy()` | `delete()` | Delete resource |

### Full Resource Policy

```php
<?php

namespace App\Policies;

use App\Models\User;
use App\Models\Post;

class PostPolicy
{
    public function viewAny(User $user): bool
    {
        return true;
    }

    public function view(User $user, Post $post): bool
    {
        return $post->isPublished() || $user->id === $post->user_id;
    }

    public function create(User $user): bool
    {
        return true;  // Authenticated users can create
    }

    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }

    public function delete(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```

## Roles and Permissions

### Simple Role-Based

```php
// User model
class User extends Model
{
    public function hasRole(string $role): bool
    {
        return $this->role === $role;
    }

    public function isAdmin(): bool
    {
        return $this->role === 'admin';
    }
}

// Gate
Gate::define('admin', function ($user) {
    return $user->isAdmin();
});
```

### Advanced Permissions with Spatie

```bash
composer require spatie/laravel-permission
php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"
php artisan migrate
```

```php
// User model
use Spatie\Permission\Traits\HasRoles;

class User extends Model
{
    use HasRoles;
}

// Usage
$user->assignRole('admin');
$user->givePermissionTo('edit posts');

// Check
$user->hasRole('admin');
$user->hasPermissionTo('edit posts');

// Blade
@role('admin')
    <p>Admin content</p>
@endrole

@can('edit posts')
    <p>Can edit posts</p>
@endcan
```

## Best Practices

### DO ✅

```php
// ✅ Use policies for model authorization
class PostPolicy
{
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}

// ✅ Use gates for non-model authorization
Gate::define('access-dashboard', function ($user) {
    return $user->isAdmin();
});

// ✅ Use authorize() method in controllers
public function update(Post $post)
{
    $this->authorize('update', $post);
    // Update post
}

// ✅ Return bool from policy methods
public function delete(User $user, Post $post): bool
{
    return $user->id === $post->user_id;
}
```

### DON'T ❌

```php
// ❌ Don't put authorization logic in controllers
public function update(Post $post)
{
    if ($user->id !== $post->user_id) {
        abort(403);
    }
}

// ✅ Use policies instead
public function update(Post $post)
{
    $this->authorize('update', $post);
}

// ❌ Don't check roles directly in controllers
public function destroy(Post $post)
{
    if (!$user->isAdmin()) {
        abort(403);
    }
}

// ✅ Use gates
Gate::define('admin', fn ($user) => $user->isAdmin());
```

## Quick Reference

| Method | Description |
|--------|-------------|
| `Gate::allows()` | Check if current user can |
| `Gate::denies()` | Check if current user cannot |
| `Gate::authorize()` | Authorize or throw 403 |
| `$user->can()` | Check if user can |
| `$user->cannot()` | Check if user cannot |
| `$this->authorize()` | Controller authorization |
| `@can()` | Blade directive |
| `@cannot()` | Blade directive |
| `@canany()` | Multiple permissions |

## See Also

- **AUTHENTICATION.md** - Guards, providers, Sanctum
- **middleware.md** - Route middleware

---

**Reference**: Laravel 11.x Authorization Documentation
