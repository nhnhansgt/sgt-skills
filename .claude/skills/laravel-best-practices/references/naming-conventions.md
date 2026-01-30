# Naming Conventions

> PSR Standards & Laravel Conventions

## Overview

Laravel naming conventions follow PSR standards and Laravel community best practices. Consistent naming makes code easier to read and maintain.

## Class Naming Conventions

### Controllers

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `singular + Controller` | `UserController` | `UsersController` | singular |
| `Resource + Controller` | `UserController` | `UserController` | RESTful |
| `Admin + Resource + Controller` | `AdminUserController` | `AdminUsersController` | for admin area |

```php
// ✅ Good
namespace App\Http\Controllers;

class UserController extends Controller
{
    // ...
}

class AdminUserController extends Controller
{
    // ...
}

// ❌ Bad
class UsersController extends Controller  // plural
{
}

class UserManagementController extends Controller  // too verbose
{
}
```

### Models

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `singular` | `User` | `Users` | singular |
| `PascalCase` | `UserProfile` | `user_profile` | PascalCase |

```php
// ✅ Good
namespace App\Models;

class User extends Model
{
    protected $table = 'users';  // plural snake_case
}

class UserProfile extends Model
{
    protected $table = 'user_profiles';
}

// ❌ Bad
class Users extends Model  // plural
{
}
```

### Services

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `singular + Service` | `UserService` | `UserManagementService` | concise |
| `Domain + Service` | `PaymentService` | `PaymentsService` | singular |

```php
// ✅ Good
namespace App\Services;

class UserService
{
    // ...
}

class PaymentService
{
    // ...
}

// ❌ Bad
class UserManagementService  // too verbose
{
}
```

### Form Requests

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `Action + Entity + Request` | `StoreUserRequest` | `UserFormRequest` | action first |
| `Update + Entity + Request` | `UpdateUserRequest` | `EditUserRequest` | update action |

```php
// ✅ Good
namespace App\Http\Requests;

class StoreUserRequest extends FormRequest
{
    // ...
}

class UpdateUserRequest extends FormRequest
{
    // ...
}

// ❌ Bad
class UserFormRequest  // missing action
{
}

class CreateUserRequest  // use Store instead of Create
{
}
```

### API Resources

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `singular + Resource` | `UserResource` | `UsersResource` | singular |
| `singular + Collection` | `UserCollection` | `UsersCollection` | for collections |

```php
// ✅ Good
namespace App\Http\Resources;

class UserResource extends JsonResource
{
    // ...
}

class UserCollection extends ResourceCollection
{
    // ...
}

// ❌ Bad
class UsersResource  // plural
{
}
```

### Contracts/Interfaces

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `Name + Interface` | `UserServiceInterface` | `IUserService` | suffix Interface |
| `Contract + Name` | `UserServiceContract` | `IUserService` | less common |

```php
// ✅ Good
namespace App\Services\Contracts;

interface UserServiceInterface
{
    public function createUser(array $data): User;
}

// ❌ Bad (Hungarian notation)
interface IUserService
{
}
```

## Database Naming Conventions

### Tables

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `plural snake_case` | `users` | `User` | lowercase plural |
| `descriptive snake_case` | `user_profiles` | `usersProfiles` | snake_case |
| `pivot table` | `role_user` | `user_role` | alphabetical order |

```php
// ✅ Good
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email')->unique();
    $table->timestamps();
});

Schema::create('user_profiles', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained();
    $table->string('phone');
    $table->timestamps();
});

// Pivot table (alphabetical)
Schema::create('role_user', function (Blueprint $table) {
    $table->foreignId('role_id')->constrained();
    $table->foreignId('user_id')->constrained();
    $table->timestamps();
});
```

### Columns

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `snake_case` | `first_name` | `firstName` | snake_case |
| `foreign key` | `user_id` | `idUser` | singular_id |
| `boolean` | `is_active` | `active` | is_ prefix |
| `timestamp` | `created_at` | `createdAt` | _at suffix |

```php
// ✅ Good
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('first_name');
    $table->string('last_name');
    $table->string('email');
    $table->timestamp('email_verified_at')->nullable();
    $table->boolean('is_active')->default(true);
    $table->timestamps();
});

// ❌ Bad
Schema::create('users', function (Blueprint $table) {
    $table->string('firstName');      // camelCase
    $table->string('lastName');       // camelCase
    $table->integer('idUser');        // Hungarian notation
    $table->boolean('active');        // missing is_ prefix
});
```

### Primary Keys

| Pattern | Correct | Notes |
|---------|---------|-------|
| `id` | `$table->id()` | Default primary key |
| `entity_id` | Custom foreign references |

```php
// ✅ Good - default primary key
$table->id();  // creates 'id' column

// ✅ Good - custom primary key
$table->unsignedBigInteger('uuid')->primary();
```

### Foreign Keys

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `singular_table_name_id` | `user_id` | `idUser` | snake_case |
| Constrained | `$table->foreignId('user_id')->constrained()` | Manual constraint | Use helper |

```php
// ✅ Good
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->foreignId('user_id')->constrained()->cascadeOnDelete();
    $table->timestamps();
});

// ❌ Bad
Schema::create('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('idUser');  // Hungarian notation
    $table->foreign('idUser')->references('id')->on('users');
});
```

### Indexes

| Pattern | Correct | Notes |
|---------|---------|-------|
| `table_column_index` | `posts_user_id_index` | Laravel auto naming |

```php
// ✅ Good - let Laravel name it
$table->foreignId('user_id')->index();

// ✅ Good - custom index
$table->index(['user_id', 'is_active'], 'posts_user_active_index');
```

## Routes Naming Conventions

### URL Paths

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `plural kebab-case` | `/users` | `/user` | plural |
| `nested resource` | `/users/{user}/posts` | `/user/{id}/posts` | use singular key |

```php
// ✅ Good
Route::apiResource('users', UserController::class);
// /users, /users/{user}, /users/{user}/posts

Route::get('/users/{user}/posts', [UserPostController::class, 'index']);
// /users/1/posts

// ❌ Bad
Route::apiResource('user', UserController::class);
// /user, /user/{user}

Route::get('/user/{id}/posts', [UserPostController::class, 'index']);
// /user/1/posts
```

### Route Names

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `dot notation` | `users.index` | `user-index` or `userIndex` | dot notation |
| `resource.action` | `users.show` | `showUser` | resource first |

```php
// ✅ Good
Route::apiResource('users', UserController::class);
// users.index, users.show, users.store, users.update, users.destroy

Route::get('/users/{user}/posts', [UserPostController::class, 'index'])
    ->name('users.posts.index');

// ❌ Bad
Route::get('/users', [UserController::class, 'index'])
    ->name('userIndex');  // camelCase
```

## Method Naming Conventions

### Controllers

| Pattern | Correct | Notes |
|---------|---------|-------|
| RESTful | `index()`, `show()`, `store()`, `update()`, `destroy()` | ResourceController |
| Custom action | `getActive()`, `toggleStatus()` | descriptive verbs |

```php
// ✅ Good
class UserController extends Controller
{
    public function index()  // GET /users
    {
    }

    public function show(User $user)  // GET /users/{user}
    {
    }

    public function store(StoreUserRequest $request)  // POST /users
    {
    }

    public function update(UpdateUserRequest $request, User $user)  // PUT/PATCH /users/{user}
    {
    }

    public function destroy(User $user)  // DELETE /users/{user}
    {
    }
}
```

### Models (Scopes)

| Pattern | Correct | Notes |
|---------|---------|-------|
| `scope + CamelCase` | `scopeActive()` | creates `active()` query |

```php
// ✅ Good
class User extends Model
{
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopeByEmail($query, string $email)
    {
        return $query->where('email', $email);
    }
}

// Usage
User::active()->byEmail('user@example.com')->first();
```

### Models (Accessors/Mutators)

| Pattern | Correct | Notes |
|---------|---------|-------|
| Accessor: `get + Attribute + Attribute` | `getFirstNameAttribute()` | `$user->first_name` |
| Mutator: `set + Attribute + Attribute` | `setFirstNameAttribute()` | `$user->first_name = 'John'` |

```php
// ✅ Good
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
}

// Usage
$user->full_name;  // accessor
$user->password = 'secret';  // mutator
```

### Services

| Pattern | Correct | Notes |
|---------|---------|-------|
| `action + Entity` | `createUser()`, `updateUser()` | descriptive |
| `get + Entity + By + Field` | `getUserById()`, `getUserByEmail()` | retrieval methods |

```php
// ✅ Good
class UserService
{
    public function getAllUsers(): Collection
    {
    }

    public function getUserById(int $id): User
    {
    }

    public function getUserByEmail(string $email): User
    {
    }

    public function createUser(array $data): User
    {
    }

    public function updateUser(int $id, array $data): User
    {
    }

    public function deleteUser(int $id): bool
    {
    }
}
```

## Variable Naming Conventions

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `camelCase` | `$userData` | `$user_data` | camelCase |
| Descriptive | `$userCollection` | `$users` | be specific |
| Boolean | `$isActive`, `$hasAccess` | `$active`, `$access` | is/has prefix |

```php
// ✅ Good
public function store(StoreUserRequest $request): JsonResponse
{
    $validatedData = $request->validated();
    $user = $this->userService->createUser($validatedData);
    $isActive = true;
    $hasAccess = $user->hasPermission('access');

    return response()->json($user, 201);
}

// ❌ Bad
public function store(StoreUserRequest $request): JsonResponse
{
    $validated_data = $request->validated();  // snake_case
    $u = $this->userService->createUser($validated_data);  // too short
    $active = true;  // missing is_ prefix

    return response()->json($u, 201);
}
```

## Constant Naming Conventions

| Pattern | Correct | Incorrect | Notes |
|---------|---------|-----------|-------|
| `UPPER_SNAKE_CASE` | `MAX_LOGIN_ATTEMPTS` | `maxLoginAttempts` | all caps |

```php
// ✅ Good
class User extends Model
{
    const STATUS_ACTIVE = 'active';
    const STATUS_INACTIVE = 'inactive';
    const MAX_LOGIN_ATTEMPTS = 5;

    protected $fillable = [
        'name',
        'email',
        'status',
    ];
}

// Usage
$user->status = User::STATUS_ACTIVE;
```

## Enum Naming Conventions

| Pattern | Correct | Notes |
|---------|---------|-------|
| `singular` | `UserStatus` | Not `UserStatuses` |

```php
// ✅ Good
enum UserStatus: string
{
    case ACTIVE = 'active';
    case INACTIVE = 'inactive';
    case SUSPENDED = 'suspended';
}

// Usage
$user->status = UserStatus::ACTIVE;
```

## Config File Naming

| Pattern | Correct | Notes |
|---------|---------|-------|
| `snake_case.php` | `google_calendar.php` | lowercase |

```php
// config/google_calendar.php
return [
    'client_id' => env('GOOGLE_CALENDAR_CLIENT_ID'),
    'client_secret' => env('GOOGLE_CALENDAR_CLIENT_SECRET'),
];
```

## View File Naming

| Pattern | Correct | Notes |
|---------|---------|-------|
| `kebab-case.blade.php` | `user-profile.blade.php` | lowercase with dashes |
| Nested with dots | `users.profile.show` | `users/profile/show.blade.php` |

```blade
{{-- resources/views/user-profile.blade.php --}}
<div>{{ $user->name }}</div>

{{-- resources/views/users/profile/show.blade.php --}}
<h1>{{ $user->name }}</h1>

{{-- Usage in controller --}}
return view('user-profile', ['user' => $user]);
return view('users.profile.show', ['user' => $user]);
```

## Migration Naming

| Pattern | Correct | Notes |
|---------|---------|-------|
| `verb_table_table` | `create_users_table` | describe action |
| `add_column_to_table` | `add_status_to_users_table` | for additions |
| `drop_column_from_table` | `drop_status_from_users_table` | for removals |

```bash
# ✅ Good
php artisan make:migration create_users_table
php artisan make:migration add_status_to_users_table
php artisan make:migration drop_status_from_users_table

# ❌ Bad
php artisan make:migration users_table
php artisan make:migration add_status_to_users
php artisan make:migration create_table_for_users
```

## Quick Reference Table

| Type | Pattern | Example |
|------|---------|---------|
| **Controller** | singular + Controller | `UserController` |
| **Model** | singular | `User` |
| **Service** | singular + Service | `UserService` |
| **Request** | Action + singular + Request | `StoreUserRequest` |
| **Resource** | singular + Resource | `UserResource` |
| **Collection** | singular + Collection | `UserCollection` |
| **Contract** | singular + Interface | `UserServiceInterface` |
| **Route** | plural | `users/1` |
| **Route name** | dot notation | `users.index` |
| **Table** | plural snake_case | `user_profiles` |
| **Column** | snake_case | `first_name` |
| **Foreign key** | singular_id | `user_id` |
| **Pivot table** | singular alphabetical | `role_user` |
| **Method** | camelCase | `getFullName()` |
| **Variable** | camelCase | `$userData` |
| **Constant** | UPPER_SNAKE | `MAX_ATTEMPTS` |
| **Enum** | singular | `UserStatus` |
| **Config file** | snake_case | `google_calendar.php` |
| **View file** | kebab-case | `user-profile.blade.php` |
| **Migration** | verb_table | `create_users_table` |

## See Also

- **CODING-STANDARDS.md** - PSR-2, PSR-12 compliance
- **controller-best-practices.md** - Controller naming patterns
- **eloquent-best-practices.md** - Model naming and organization

---

**Reference**: Laravel 11.x Documentation, PSR-1, PSR-2, PSR-4
