# Service Layer Pattern

## Purpose

Encapsulate business logic outside of controllers. Single Responsibility Principle.

## Structure

```
app/Services/
└── UserService.php
```

## Basic Service Class

```php
<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserService
{
    public function createUser(array $data): User
    {
        return User::create([
            'name' => $data['name'],
            'email' => $data['email'],
            'password' => Hash::make($data['password']),
        ]);
    }

    public function updateUser(User $user, array $data): User
    {
        $user->update($data);
        return $user;
    }

    public function deleteUser(User $user): bool
    {
        return $user->delete();
    }
}
```

## Controller Usage

```php
class UserController extends Controller
{
    public function __construct(
        private UserService $userService
    ) {}

    public function store(StoreUserRequest $request)
    {
        $user = $this->userService->createUser($request->validated());
        return response()->json($user, 201);
    }
}
```

## Rules

1. **No HTTP concerns** - Services return data, not responses
2. **No validation** - Use Form Requests for that
3. **Single responsibility** - One service per domain concept
4. **Dependency injection** - Inject dependencies via constructor

## When to Use

- Complex business logic beyond CRUD
- Logic used by multiple controllers
- External API calls
- Complex data transformations

## When NOT to Use

- Simple CRUD (keep in controller)
- Only database queries (use Model scopes)
- Trivial one-off operations

---

**See also:** `controller-best-practices.md`, `request-validation.md`
