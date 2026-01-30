---
title: Laravel Naming Conventions
impact: HIGH
impactDescription: Consistent naming across codebase
tags: coding-standards, naming, conventions, psr, laravel
---

## Laravel Naming Conventions

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

## Class Naming

| Type | Pattern | Correct | Incorrect |
|------|---------|---------|-----------|
| Controller | `singular + Controller` | `UserController` | `UsersController` |
| Model | `singular` | `User` | `Users` |
| Service | `singular + Service` | `UserService` | `UserManagementService` |
| Request | `Action + Entity + Request` | `StoreUserRequest` | `UserFormRequest` |
| Resource | `singular + Resource` | `UserResource` | `UsersResource` |

**Correct examples:**

```php
class UserController extends Controller {}
class UserService {}
class StoreUserRequest extends FormRequest {}
class UserResource extends JsonResource {}
```

## Database Naming

| Type | Pattern | Correct | Incorrect |
|------|---------|---------|-----------|
| Table | `plural snake_case` | `user_profiles` | `userProfiles` |
| Column | `snake_case` | `first_name` | `firstName` |
| Foreign key | `singular_table_id` | `user_id` | `idUser` |
| Pivot table | `singular_alphabetical` | `role_user` | `user_role` |
| Primary key | `id` | `$table->id()` | Custom unless needed |

**Correct examples:**

```php
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('first_name');
    $table->string('last_name');
    $table->foreignId('country_id')->constrained();
    $table->timestamps();
});

// Pivot table (alphabetical)
Schema::create('role_user', function (Blueprint $table) {
    $table->foreignId('role_id')->constrained();
    $table->foreignId('user_id')->constrained();
    $table->timestamps();
});
```

## Route Naming

| Type | Pattern | Correct | Incorrect |
|------|---------|---------|-----------|
| URL path | `plural kebab-case` | `/users/{user}` | `/user/{id}` |
| Route name | `dot notation` | `users.show` | `userShow` |
| Parameter | `singular` | `{user}` | `{id}` |

**Correct examples:**

```php
Route::apiResource('users', UserController::class);
// Generates: /users, /users/{user}, users.index, users.show

Route::get('/users/{user}/posts', [UserPostController::class, 'index'])
    ->name('users.posts.index');
```

## Variable Naming

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

**Incorrect (snake_case or inconsistent):**

```php
$user_id = 1;  // Use camelCase
$user_data = ['name' => 'John'];  // Use camelCase
$active = true;  // Use $isActive for clarity
```

## Method Naming

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

## Constant Naming

**Correct (UPPER_SNAKE_CASE):**

```php
class User extends Model
{
    const STATUS_ACTIVE = 'active';
    const STATUS_INACTIVE = 'inactive';
    const MAX_LOGIN_ATTEMPTS = 5;
}
```

## File Naming

| Type | Pattern | Example |
|------|---------|---------|
| View file | `kebab-case.blade.php` | `user-profile.blade.php` |
| Config file | `snake_case.php` | `google_calendar.php` |
| Migration | `verb_table_table` | `create_users_table` |
| Class file | `PascalCase.php` | `UserService.php` |

Reference: [Laravel Contribution Guide](https://laravel.com/docs/contributions#coding-style)
