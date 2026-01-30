# Laravel Best Practices

**Version 1.2.0**
Laravel Community & SGT Skills
January 2026

> **Note:**
> This document is mainly for agents and LLMs to follow when maintaining,
> generating, or refactoring Laravel codebases. Humans may also find it useful,
> but guidance here is optimized for automation and consistency by AI-assisted workflows.

---

## Abstract

Comprehensive Laravel best practices guide covering MVC + Service Pattern architecture, security (authentication/authorization), performance (eager loading, caching), coding standards (PSR-12, naming conventions), Eloquent models, Blade components, request handling, and testing. Contains 15+ rules across 8 categories, prioritized by impact from critical (security, performance) to incremental (events, testing). Each rule includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and specific impact metrics.

---

## Table of Contents

1. [Performance](#1-performance) — **CRITICAL**
   - 1.1 [Eager Loading to Prevent N+1 Queries](#11-eager-loading-to-prevent-n1-queries)
2. [Security](#2-security) — **CRITICAL**
   - 2.1 [Secure Authentication with Sanctum](#21-secure-authentication-with-sanctum)
3. [Architecture](#3-architecture) — **HIGH**
   - 3.1 [Thin Controllers with Service Layer](#31-thin-controllers-with-service-layer)
4. [Coding Standards](#4-coding-standards) — **HIGH**
   - 4.1 [PSR-12 Coding Standards Compliance](#41-psr-12-coding-standards-compliance)
   - 4.2 [Laravel Naming Conventions](#42-laravel-naming-conventions)
5. [Data Layer](#5-data-layer) — **HIGH**
   - 5.1 [Fat Models with Scopes and Relationships](#51-fat-models-with-scopes-and-relationships)
6. [Views](#6-views) — **MEDIUM**
   - 6.1 [Blade Components over Includes](#61-blade-components-over-includes)

---

## 1. Performance

**Impact: CRITICAL**

Performance optimizations for database queries and caching. Critical for application scalability and response times.

### 1.1 Eager Loading to Prevent N+1 Queries

**Impact: CRITICAL (10-100× query reduction)**

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

**Multiple Relationships**

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

**Nested Relationships**

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

**Constrained Eager Loading**

**Correct (Load with constraints):**

```php
$posts = Post::with(['comments' => function ($query) {
    $query->where('published', true)
          ->orderBy('created_at', 'desc');
}])->get();
```

**Counting Related Models**

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

**Service Layer Pattern**

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

---

## 2. Security

**Impact: CRITICAL**

Authentication, authorization, and security best practices to protect your application from vulnerabilities.

### 2.1 Secure Authentication with Sanctum

**Impact: CRITICAL (Critical for application security)**

Use Laravel Sanctum for API authentication with token-based auth. Never store passwords as plain text, and always use proper guards.

**Incorrect (Plain text passwords):**

```php
User::create([
    'password' => $request->password,  // Security risk!
]);
```

**Correct (Hashed passwords):**

```php
User::create([
    'password' => Hash::make($request->password),
]);
```

**Sanctum API Authentication**

**Incorrect (Simple tokens without expiration):**

```php
$token = Str::random(60);  // Never expires, insecure
```

**Correct (Sanctum tokens with abilities):**

```php
$token = $user->createToken('api-token', ['posts:read'])->plainTextToken;
```

**Token Abilities**

**Correct (Granular permissions):**

```php
// Create token with specific abilities
$user->createToken('read-only', ['posts:read', 'comments:read'])->plainTextToken;

// Check abilities in code
if ($user->tokenCan('posts:read')) {
    // User can read posts
}
```

**Session Authentication**

**Correct (Proper session handling):**

```php
public function login(Request $request)
{
    $credentials = $request->validate([
        'email' => 'required|email',
        'password' => 'required',
    ]);

    if (Auth::attempt($credentials, $request->boolean('remember'))) {
        $request->session()->regenerate();  // Prevent session fixation
        return redirect()->intended('/dashboard');
    }

    return back()->withErrors([
        'email' => 'The provided credentials do not match our records.',
    ]);
}
```

**Route Protection**

**Incorrect (No authentication):**

```php
Route::get('/dashboard', [DashboardController::class, 'index']);
Route::apiResource('posts', PostController::class);
```

**Correct (Middleware protection):**

```php
Route::middleware(['auth'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
});

Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('posts', PostController::class);
});
```

**Logout Security**

**Correct (Proper session invalidation):**

```php
public function logout(Request $request)
{
    Auth::logout();

    $request->session()->invalidate();
    $request->session()->regenerateToken();  // Prevent CSRF

    return redirect('/');
}
```

Reference: [Laravel Sanctum Documentation](https://laravel.com/docs/sanctum)

---

## 3. Architecture

**Impact: HIGH**

MVC + Service Pattern architecture for maintainable, scalable Laravel applications.

### 3.1 Thin Controllers with Service Layer

**Impact: HIGH (Better maintainability and testability)**

Controllers should only handle HTTP concerns: request validation, response formatting, and delegating to services. Business logic belongs in services.

**Incorrect (Fat controller with business logic):**

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8',
    ]);

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => bcrypt($validated['password']),
    ]);

    // Business logic in controller
    if ($user->role === 'admin') {
        Mail::to($user)->send(new AdminWelcomeMail());
    }

    return response()->json($user, 201);
}
```

**Correct (Thin controller with service):**

```php
public function __construct(
    private UserService $userService
) {}

public function store(StoreUserRequest $request): JsonResponse
{
    $user = $this->userService->createUser($request->validated());
    return response()->json($user, 201);
}
```

**Service Class Structure**

**Correct (Service with business logic):**

```php
class UserService
{
    public function __construct(
        private User $user,
        private Mailer $mailer
    ) {}

    public function createUser(array $data): User
    {
        $user = $this->user->create([
            'name' => $data['name'],
            'email' => $data['email'],
            'password' => Hash::make($data['password']),
        ]);

        // Business logic in service
        if ($user->role === 'admin') {
            $this->mailer->send(new AdminWelcomeMail($user));
        }

        return $user;
    }
}
```

**Controller Rules**

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Validation | Form Request | Inline validation |
| Business Logic | In Service | In Controller |
| Data Access | Via Service | Direct Model calls |
| Response Type | Return JSON | Return views |
| Dependencies | Constructor Injection | New keyword |

**Complete Controller Example**

**Correct:**

```php
class UserController extends Controller
{
    public function __construct(
        private UserService $userService
    ) {}

    public function index(): JsonResponse
    {
        $users = $this->userService->getPaginatedUsers();
        return response()->json($users);
    }

    public function store(StoreUserRequest $request): JsonResponse
    {
        $user = $this->userService->createUser($request->validated());
        return response()->json($user, 201);
    }

    public function show(User $user): JsonResponse
    {
        return response()->json($user);
    }
}
```

Reference: [Laravel Service Layer Pattern](https://spatie.be/guides/laravel-service-pattern)

---

## 4. Coding Standards

**Impact: HIGH**

PSR standards, naming conventions, and coding style for consistent, readable code.

### 4.1 PSR-12 Coding Standards Compliance

**Impact: HIGH (Consistent code style across team)**

Follow PSR-12 (Extended Coding Style) for consistent, readable code. This includes proper indentation, line length, type hints, and return types.

**Incorrect (Missing type hints and formatting):**

```php
class userservice
{
    public function getuser($id)
    {
        return User::find($id);
    }
}
```

**Correct (PSR-12 compliant):**

```php
class UserService
{
    public function getUserById(int $id): ?User
    {
        return User::find($id);
    }
}
```

**Type Hints Required**

**Incorrect (No type hints):**

```php
public function updateUser($id, $data)
{
    $user = User::findOrFail($id);
    $user->update($data);
    return $user;
}
```

**Correct (Full type hints):**

```php
public function updateUser(int $id, array $data): User
{
    $user = User::findOrFail($id);
    $user->update($data);
    return $user;
}
```

**Constructor Property Promotion**

**Incorrect (Traditional constructor):**

```php
class UserService
{
    private $userRepository;
    private $cache;

    public function __construct(UserRepository $userRepository, Cache $cache)
    {
        $this->userRepository = $userRepository;
        $this->cache = $cache;
    }
}
```

**Correct (Property promotion - PHP 8.0+):**

```php
class UserService
{
    public function __construct(
        private UserRepository $userRepository,
        private Cache $cache
    ) {}
}
```

**Return Type Declarations**

**Incorrect (Missing return types):**

```php
public function getAllUsers()
{
    return User::all();
}

public function createUser(array $data)
{
    return User::create($data);
}
```

**Correct (Explicit return types):**

```php
public function getAllUsers(): Collection
{
    return User::all();
}

public function createUser(array $data): User
{
    return User::create($data);
}
```

**Nullable Types**

**Incorrect (Old-style nullable):**

```php
/**
 * @return User|null
 */
public function getUserByEmail(string $email)
{
    return User::where('email', $email)->first();
}
```

**Correct (Modern nullable syntax):**

```php
public function getUserByEmail(string $email): ?User
{
    return User::where('email', $email)->first();
}
```

**Use Statement Ordering**

**Incorrect (Unordered imports):**

```php
use Illuminate\Support\Facades\DB;
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
```

**Correct (Alphabetical, grouped by origin):**

```php
use App\Models\User;
use App\Models\UserProfile;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\DB;
```

Reference: [PSR-12 Specification](https://www.php-fig.org/psr/psr-12/)

### 4.2 Laravel Naming Conventions

**Impact: HIGH (Consistent naming across codebase)**

Follow Laravel and PSR naming conventions for consistency. Use singular for classes, plural for tables/routes, and snake_case for database.

**Incorrect (Inconsistent naming):**

```php
class UsersController extends Controller  // Plural - Wrong
{
    public function index()
    {
        $usersData = User::all();  // camelCase - OK
        return view('user/index');  // Inconsistent
    }
}

// Route
Route::get('/user', 'UsersController@index');  // Inconsistent
```

**Correct (Laravel conventions):**

```php
class UserController extends Controller  // Singular
{
    public function index()  // RESTful method
    {
        $users = User::all();  // Descriptive variable
        return view('users.index');  // Dot notation
    }
}

// Route
Route::apiResource('users', UserController::class);  // Plural resource
```

**Class Naming**

| Type | Pattern | Correct | Incorrect |
|------|---------|---------|-----------|
| Controller | `singular + Controller` | `UserController` | `UsersController` |
| Model | `singular` | `User` | `Users` |
| Service | `singular + Service` | `UserService` | `UserManagementService` |
| Request | `Action + Entity + Request` | `StoreUserRequest` | `UserFormRequest` |
| Resource | `singular + Resource` | `UserResource` | `UsersResource` |

**Database Naming**

| Type | Pattern | Correct | Incorrect |
|------|---------|---------|-----------|
| Table | `plural snake_case` | `user_profiles` | `userProfiles` |
| Column | `snake_case` | `first_name` | `firstName` |
| Foreign key | `singular_table_id` | `user_id` | `idUser` |
| Pivot table | `singular_alphabetical` | `role_user` | `user_role` |

**Route Naming**

| Type | Pattern | Correct | Incorrect |
|------|---------|---------|-----------|
| URL path | `plural kebab-case` | `/users/{user}` | `/user/{id}` |
| Route name | `dot notation` | `users.show` | `userShow` |
| Parameter | `singular` | `{user}` | `{id}` |

**Variable Naming**

**Correct (camelCase):**

```php
$userId = 1;
$userData = ['name' => 'John'];
$isActive = true;
$hasAccess = false;

// Boolean with is/has prefix
$user->is_active;
$user->hasPermission('admin');
```

**Method Naming**

**Correct (Descriptive, camelCase):**

```php
// Controllers - RESTful
public function index() {}
public function show(User $user) {}
public function store(StoreUserRequest $request) {}

// Services - action + entity
public function createUser(array $data): User {}
public function getUserById(int $id): User {}
public function deleteUser(int $id): bool {}

// Models - scopes
public function scopeActive($query) {}
public function scopeByEmail($query, string $email) {}
```

**Constant Naming**

**Correct (UPPER_SNAKE_CASE):**

```php
class User extends Model
{
    const STATUS_ACTIVE = 'active';
    const STATUS_INACTIVE = 'inactive';
    const MAX_LOGIN_ATTEMPTS = 5;
}
```

Reference: [Laravel Contribution Guide](https://laravel.com/docs/contributions#coding-style)

---

## 5. Data Layer

**Impact: HIGH**

Eloquent models, relationships, API resources, and pagination best practices.

### 5.1 Fat Models with Scopes and Relationships

**Impact: HIGH (Better code organization and reusability)**

Models should handle data logic, scopes, accessors, mutators, and relationships. Keep database logic out of controllers.

**Incorrect (Query logic in controller):**

```php
// Controller
public function getActiveUsers()
{
    return User::where('is_active', true)
        ->where('email_verified_at', '!=', null)
        ->orderBy('created_at', 'desc')
        ->get();
}
```

**Correct (Scopes in model):**

```php
// Model
class User extends Model
{
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopeVerified($query)
    {
        return $query->whereNotNull('email_verified_at');
    }
}

// Controller
public function getActiveUsers()
{
    return User::active()->verified()->latest()->get();
}
```

**Model Scopes**

**Incorrect (Repeated query logic):**

```php
User::where('is_active', true)->get();
User::where('is_active', true)->with('posts')->get();
User::where('is_active', true)->paginate(15);
```

**Correct (Reusable scope):**

```php
// Model
public function scopeActive($query)
{
    return $query->where('is_active', true);
}

// Usage
User::active()->get();
User::active()->with('posts')->get();
User::active()->paginate(15);
```

**Dynamic Scopes**

**Correct (Parameters in scopes):**

```php
// Model
public function scopeByEmail($query, string $email)
{
    return $query->where('email', $email);
}

public function scopeOfType($query, string $type)
{
    return $query->where('type', $type);
}

// Usage
$user = User::active()->byEmail('user@example.com')->first();
$admins = User::ofType('admin')->get();
```

**Accessors and Mutators**

**Incorrect (Logic in controller/view):**

```php
// In controller or view
$fullName = $user->first_name . ' ' . $user->last_name;
$user->password = bcrypt($newPassword);
```

**Correct (Accessors/Mutators in model):**

```php
// Model
class User extends Model
{
    // Accessor
    public function getFullNameAttribute(): string
    {
        return "{$this->first_name} {$this->last_name}";
    }

    // Mutator
    public function setPasswordAttribute(string $value): void
    {
        $this->attributes['password'] = bcrypt($value);
    }

    protected $casts = [
        'is_admin' => 'boolean',
        'email_verified_at' => 'datetime',
    ];
}

// Usage
$user->full_name;  // Accessor
$user->password = 'secret';  // Auto-hashed by mutator
```

**Relationships**

**Correct (Define relationships in model):**

```php
class User extends Model
{
    // One-to-many
    public function posts()
    {
        return $this->hasMany(Post::class);
    }

    // Many-to-many
    public function roles()
    {
        return $this->belongsToMany(Role::class)->withTimestamps();
    }

    // Has one
    public function profile()
    {
        return $this->hasOne(Profile::class);
    }

    // Inverse relationship
    public function country()
    {
        return $this->belongsTo(Country::class);
    }
}
```

**Model Events**

**Correct (Use model events):**

```php
protected static function booted()
{
    static::creating(function ($user) {
        $user->slug = Str::slug($user->name);
    });

    static::created(function ($user) {
        Mail::to($user)->send(new WelcomeMail($user));
    });
}
```

**Mass Assignment Protection**

**Correct (Use fillable or guarded):**

```php
class User extends Model
{
    // Allow specific fields
    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    // OR block specific fields
    protected $guarded = [
        'id',
        'is_admin',
    ];
}
```

Reference: [Laravel Eloquent Documentation](https://laravel.com/docs/eloquent)

---

## 6. Views

**Impact: MEDIUM**

Blade templates, components, layouts, and view organization.

### 6.1 Blade Components over Includes

**Impact: MEDIUM (Better component reusability and data isolation)**

Use Blade components instead of includes for better reusability, data isolation, and cleaner syntax.

**Incorrect (Using @include):**

```blade
{{-- resources/views/users/_card.blade.php --}}
<div class="user-card">
    <h2>{{ $name }}</h2>
    <p>{{ $email }}</p>
</div>

{{-- Usage --}}
@include('users._card', ['name' => $user->name, 'email' => $user->email])
```

**Correct (Using component):**

```blade
{{-- resources/views/components/user-card.blade.php --}}
@props(['user', 'size' => 'md'])

<div class="user-card user-card-{{ $size }}">
    <h2>{{ $user->name }}</h2>
    <p>{{ $user->email }}</p>
</div>

{{-- Usage --}}
<x-user-card :user="$user" size="lg" />
```

**Component Attributes**

**Correct (Attribute merging):**

```blade
{{-- Component --}}
@props(['user'])

<div {{ $attributes }}>
    <h2>{{ $user->name }}</h2>
</div>

{{-- Usage --}}
<x-user-card :user="$user" class="border rounded" id="user-1" />
{{-- Renders: <div class="user-card border rounded" id="user-1"> --}}
```

**Component Slots**

**Correct (Named slots for flexibility):**

```blade
{{-- resources/views/components/modal.blade.php --}}
@props(['title' => 'Default Title'])

<div class="modal">
    <div class="modal-header">
        <h2>{{ $title }}</h2>
    </div>

    <div class="modal-body">
        {{ $slot }}
    </div>

    @if(isset($footer))
        <div class="modal-footer">
            {{ $footer }}
        </div>
    @endif
</div>

{{-- Usage --}}
<x-modal title="Delete User">
    <p>Are you sure you want to delete this user?</p>

    <x-slot:footer>
        <button>Cancel</button>
        <button class="danger">Delete</button>
    </x-slot:footer>
</x-modal>
```

**Layouts**

**Incorrect (Repeated HTML):**

```blade
{{-- Every file repeats header/footer --}}
<!DOCTYPE html>
<html>
<head><title>Page 1</title></head>
<body>@yield('content')</body>
</html>
```

**Correct (Use layouts):**

```blade
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <title>@slot('title', 'App')</title>
    @stack('styles')
</head>
<body>
    @yield('content')
    @stack('scripts')
</body>
</html>

{{-- resources/views/users/show.blade.php --}}
@extends('layouts.app')

@section('title', 'User Profile')

@push('styles')
    <link rel="stylesheet" href="/css/user.css">
@endpush

@section('content')
    <h1>{{ $user->name }}</h1>
@endsection
```

**Directives Best Practices**

**Correct (Use Blade directives):**

```blade
@auth
    <p>Welcome, {{ Auth::user()->name }}</p>
@endauth

@isset($user->profile)
    <p>{{ $user->profile->bio }}</p>
@endisset

@error('email')
    <p class="error">{{ $message }}</p>
@enderror

@foreach ($users as $user)
    @if ($loop->first)
        <p>First user!</p>
    @endif
    <p>{{ $loop->iteration }}: {{ $user->name }}</p>
@endforeach
```

**Security: XSS Prevention**

**Incorrect (Unescaped output):**

```blade
{!! $userInput !!}  <!-- XSS vulnerability! -->
```

**Correct (Auto-escaped output):**

```blade
{{ $userInput }}  <!-- Safe -->

{{-- Only use {!! !!} for trusted HTML --}}
{!! $post->body_html !!}
```

Reference: [Laravel Blade Documentation](https://laravel.com/docs/blade)

---

## References

- **Laravel Documentation**: https://laravel.com/docs
- **Laravel Contribution Guide**: https://laravel.com/docs/contributions
- **Spatie Guidelines**: https://spatie.be/guides/laravel-php
- **Laravel Best Practices**: https://github.com/alexeymezenin/laravel-best-practices
- **PSR-12 Specification**: https://www.php-fig.org/psr/psr-12/

---

**Version**: 1.2.0 | **Last Updated**: 2026-01-28
