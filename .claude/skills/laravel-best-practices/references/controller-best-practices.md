# Controller Best Practices

## Core Principle

**Thin Controllers** - Controllers should only:
- Validate input (via Form Requests)
- Call service/business logic
- Return HTTP responses

## Structure

```
app/Http/Controllers/
└── UserController.php
```

## Good Controller Example

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreUserRequest;
use App\Http\Requests\UpdateUserRequest;
use App\Models\User;
use App\Services\UserService;
use Illuminate\Http\JsonResponse;

class UserController extends Controller
{
    public function __construct(
        private UserService $userService
    ) {}

    public function index(): JsonResponse
    {
        $users = User::all();
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

    public function update(UpdateUserRequest $request, User $user): JsonResponse
    {
        $user = $this->userService->updateUser($user, $request->validated());
        return response()->json($user);
    }

    public function destroy(User $user): JsonResponse
    {
        $this->userService->deleteUser($user);
        return response()->json(null, 204);
    }
}
```

## Bad Controller Example

```php
// ❌ DON'T DO THIS - Too much logic
public function store(Request $request)
{
    $validated = $request->validate([
        'email' => 'required|email|unique:users',
        // ... 10 more validation rules
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

## Rules

1. **Inject dependencies** - Use constructor property promotion
2. **Use route model binding** - `User $user` instead of `User::find($id)`
3. **Single action controllers** - For complex single actions, use `__invoke()`
4. **RESTful conventions** - Use resource routes
5. **Return JSON responses** - For APIs, use `response()->json()`

## Single Action Controller

```php
class ExportUsersController extends Controller
{
    public function __invoke(ExportService $exportService)
    {
        return $exportService->exportUsers();
    }
}

// Route: Route::get('/export/users', ExportUsersController::class);
```

---

**See also:** `service-layer.md`, `request-validation.md`
