# Routing

> Route definitions, groups, model binding, API routes

## Overview

Laravel routing files are located in the `routes/` directory. Each file serves a different purpose.

## Route Files

| File | Purpose | Middleware |
|------|---------|------------|
| `web.php` | Web routes, sessions, cookies | `web` |
| `api.php` | API endpoints, stateless | `api` (throttle) |
| `console.php` | Artisan console routes | None |
| `channels.php` | Broadcast channels | None |

## Basic Routing

### GET Route

```php
// routes/web.php
Route::get('/users', [UserController::class, 'index']);
Route::get('/users/{user}', [UserController::class, 'show']);
```

### POST Route

```php
Route::post('/users', [UserController::class, 'store']);
```

### PUT/PATCH Route

```php
Route::put('/users/{user}', [UserController::class, 'update']);
Route::patch('/users/{user}', [UserController::class, 'update']);
```

### DELETE Route

```php
Route::delete('/users/{user}', [UserController::class, 'destroy']);
```

### Match Multiple Methods

```php
Route::match(['get', 'post'], '/users', [UserController::class, 'form']);
```

### Any Method

```php
Route::any('/users', [UserController::class, 'any']);
```

## Route Groups

### Prefix Grouping

```php
// ✅ Good - Admin routes with prefix
Route::prefix('admin')->group(function () {
    Route::get('/users', [AdminUserController::class, 'index']);
    Route::get('/posts', [AdminPostController::class, 'index']);
});

// /admin/users, /admin/posts
```

### Middleware Grouping

```php
// ✅ Good - Protected routes
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('/profile', [ProfileController::class, 'show']);
    Route::post('/profile', [ProfileController::class, 'update']);
});

Route::middleware(['auth:admin', 'role:admin'])->prefix('admin')->group(function () {
    Route::resource('users', AdminUserController::class);
});
```

### Namespace Grouping (Deprecated in Laravel 11+)

```php
// Laravel 10 and below
Route::namespace('Admin')->prefix('admin')->group(function () {
    // Uses App\Http\Controllers\Admin\...
});

// Laravel 11+ - Use full class path
Route::prefix('admin')->group(function () {
    Route::get('/users', [Admin\UserController::class, 'index']);
});
```

### Subdomain Routing

```php
Route::domain('{account}.myapp.com')->group(function () {
    Route::get('/users', [UserController::class, 'index']);
});

// account-name.myapp.com/users
```

### Combined Grouping

```php
Route::middleware(['auth', 'admin'])
    ->prefix('admin/v1')
    ->name('admin.')
    ->group(function () {
        Route::apiResource('users', AdminUserController::class);
        Route::apiResource('posts', AdminPostController::class);
    });

// admin.users.index, admin.users.show, etc.
```

## Resource Routes

### Basic Resource

```php
// ✅ Good - Full resource controller
Route::resource('users', UserController::class);

// Methods: index, create, store, show, edit, update, destroy
// URLs: /users, /users/create, /users/{user}, /users/{user}/edit
// Names: users.index, users.create, users.store, etc.
```

### API Resource (No create/edit views)

```php
// ✅ Good - API routes (no create/edit views)
Route::apiResource('users', UserController::class);

// Methods: index, store, show, update, destroy
// URLs: /users, /users/{user}
```

### Partial Resource

```php
// ✅ Good - Only specific methods
Route::resource('users', UserController::class)
    ->only(['index', 'show', 'update']);

Route::resource('users', UserController::class)
    ->except(['create', 'edit', 'destroy']);
```

### Nested Resources

```php
// ✅ Good
Route::resource('users.posts', UserPostController::class);

// /users/{user}/posts
// /users/{user}/posts/{post}
```

### Shallow Nesting

```php
// ✅ Good - Avoid deep nesting
Route::resource('users.posts', UserPostController::class)
    ->shallow();

// /users/{user}/posts
// /posts/{post} (not /users/{user}/posts/{post})
```

### Resource Naming

```php
Route::resource('users', UserController::class)
    ->name('members');

// members.index, members.show, etc.

Route::resource('users.posts', UserPostController::class)
    ->shallow()
    ->names([
        'index' => 'users.posts.all',
        'show' => 'users.posts.view',
    ]);
```

### Resource Parameters

```php
Route::resource('users', UserController::class)
    ->parameters(['users' => 'user_id']);

// /users/{user_id} instead of /users/{user}

// Nested
Route::resource('users.posts', UserPostController::class)
    ->parameters([
        'users' => 'admin_user',
        'posts' => 'admin_post',
    ]);

// /users/{admin_user}/posts/{admin_post}
```

## Route Model Binding

### Implicit Binding

```php
// ✅ Good - Laravel tự động resolve model by key
Route::get('/users/{user}', [UserController::class, 'show']);

// Controller
public function show(User $user)
{
    return $user;  // Auto-resolved by {user}
}
```

### Custom Key

```php
// Model
public function getRouteKeyName(): string
{
    return 'slug';  // Use slug instead of id
}

// Route stays the same
Route::get('/users/{user}', [UserController::class, 'show']);

// URL: /users/john-doe instead of /users/1
```

### Explicit Binding

```php
// RouteServiceProvider
public function boot()
{
    // Custom resolution logic
    Route::bind('user', function ($value) {
        return User::where('slug', $value)->firstOrFail();
    });

    // Or use custom method
    Route::bind('user', [UserResolver::class, 'resolve']);
}
```

### Soft Delete Binding

```php
// ✅ Good - Include soft deleted models
Route::bind('user', function ($value) {
    return User::withTrashed()->where('id', $value)->firstOrFail();
});
```

## Route Names

### Naming Routes

```php
// ✅ Good
Route::get('/users/{user}/posts', [UserPostController::class, 'index'])
    ->name('users.posts.index');

// Usage
$url = route('users.posts.index', ['user' => 1]);
// /users/1/posts

// With parameters
$url = route('users.posts.show', ['user' => 1, 'post' => 5]);
// /users/1/posts/5
```

### Route Groups with Names

```php
Route::name('admin.')->prefix('admin')->group(function () {
    Route::get('/users', [AdminUserController::class, 'index'])
        ->name('users.index');  // admin.users.index

    Route::get('/posts', [AdminPostController::class, 'index'])
        ->name('posts.index');  // admin.posts.index
});
```

## Route Parameters

### Required Parameters

```php
Route::get('/users/{user}', [UserController::class, 'show']);
Route::get('/users/{user}/posts/{post}', [UserPostController::class, 'show']);

// Controller
public function show(User $user, Post $post)
{
    return $post;
}
```

### Optional Parameters

```php
Route::get('/users/{user?}', [UserController::class, 'show']);

// Controller
public function show(?User $user)
{
    return $user ?? 'User not found';
}
```

### Regular Expression Constraints

```php
Route::get('/users/{id}', [UserController::class, 'show'])
    ->where('id', '[0-9]+');

Route::get('/users/{name}', [UserController::class, 'show'])
    ->where('name', '[A-Za-z]+');

Route::get('/users/{id}/{slug}', [UserController::class, 'show'])
    ->where(['id' => '[0-9]+', 'slug' => '[A-Za-z-]+']);
```

### Global Constraints (RouteServiceProvider)

```php
public function boot()
{
    // Apply to all routes using {id}
    Route::pattern('id', '[0-9]+');

    // Now all {id} parameters must be numeric
    Route::get('/users/{id}', [UserController::class, 'show']);
    Route::get('/posts/{id}', [PostController::class, 'show']);
}
```

## Fallback Routes

### 404 Handler

```php
// routes/web.php
Route::fallback(function () {
    return response()->view('errors.404', [], 404);
});

// routes/api.php
Route::fallback(function () {
    return response()->json([
        'error' => 'Endpoint not found'
    ], 404);
});
```

## Route Caching

### Cache Routes

```bash
# Cache routes for production
php artisan route:cache

# Clear cache
php artisan route:clear
```

### Notes

- Closure routes cannot be cached
- Only use in production
- Run after deploying

## API Routes

### Version Prefixing

```php
// routes/api.php
Route::prefix('v1')->group(function () {
    Route::apiResource('users', UserController::class);
    Route::apiResource('posts', PostController::class);
});

// /api/v1/users
```

### API Resource Controllers

```php
// ✅ Good
Route::apiResource('users', UserController::class);

// Generates:
// GET    /api/users         → index
// POST   /api/users         → store
// GET    /api/users/{user}  → show
// PUT/PATCH /api/users/{user} → update
// DELETE /api/users/{user}  → destroy
```

### API Authentication

```php
// routes/api.php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('users', UserController::class);
    Route::apiResource('posts', PostController::class);
});

// Public routes
Route::post('/login', [AuthController::class, 'login']);
Route::post('/register', [AuthController::class, 'register']);
```

## Best Practices

### DO ✅

```php
// ✅ Use resource controllers
Route::apiResource('users', UserController::class);

// ✅ Group related routes
Route::middleware(['auth', 'admin'])
    ->prefix('admin')
    ->name('admin.')
    ->group(function () {
        Route::apiResource('users', AdminUserController::class);
    });

// ✅ Name your routes
Route::post('/users/{user}/activate', [UserController::class, 'activate'])
    ->name('users.activate');

// ✅ Use route model binding
Route::get('/users/{user}', [UserController::class, 'show']);

// ✅ Use constraints
Route::get('/users/{id}', [UserController::class, 'show'])
    ->where('id', '[0-9]+');
```

### DON'T ❌

```php
// ❌ Don't use closures in production (can't cache)
Route::get('/users', function () {
    return User::all();
});

// ❌ Don't put business logic in routes
Route::post('/users', function (Request $request) {
    $validated = $request->validate([...]);
    $user = User::create($validated);
    Mail::to($user)->send(new WelcomeMail());
    return response()->json($user, 201);
});

// ❌ Don't use deep nesting
Route::resource('users.posts.comments.replies', ReplyController::class);

// Instead, use shallow nesting
Route::resource('users.posts.comments', CommentController::class)->shallow();
```

## Route Listing

```bash
# List all routes
php artisan route:list

# Filter by URI
php artisan route:list --path=users

# Filter by method
php artisan route:list --method=GET

# Show route middleware
php artisan route:list -v

# Show route names
php artisan route:list --columns=method,uri,name
```

## See Also

- **controller-best-practices.md** - Controller organization
- **middleware.md** - Middleware for route filtering
- **request-validation.md** - Form Request validation

---

**Reference**: Laravel 11.x Routing Documentation
