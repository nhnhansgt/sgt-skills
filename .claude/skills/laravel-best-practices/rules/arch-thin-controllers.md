---
title: Thin Controllers with Service Layer
impact: HIGH
impactDescription: Better maintainability and testability
tags: architecture, controllers, service-layer, mvc, separation-of-concerns
---

## Thin Controllers with Service Layer

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

## Service Class Structure

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

## Controller Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Validation | Form Request | Inline validation |
| Business Logic | In Service | In Controller |
| Data Access | Via Service | Direct Model calls |
| Response Type | Return JSON | Return views |
| Dependencies | Constructor Injection | New keyword |

## Complete Controller Example

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
