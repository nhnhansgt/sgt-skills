---
title: Secure Authentication with Sanctum
impact: CRITICAL
impactDescription: Critical for application security
tags: security, authentication, sanctum, guards, authorization
---

## Secure Authentication with Sanctum

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

## Sanctum API Authentication

**Incorrect (Simple tokens without expiration):**

```php
$token = Str::random(60);  // Never expires, insecure
```

**Correct (Sanctum tokens with abilities):**

```php
$token = $user->createToken('api-token', ['posts:read'])->plainTextToken;
```

## Token Abilities

**Correct (Granular permissions):**

```php
// Create token with specific abilities
$user->createToken('read-only', ['posts:read', 'comments:read'])->plainTextToken;

// Check abilities in code
if ($user->tokenCan('posts:read')) {
    // User can read posts
}
```

## Session Authentication

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

## Route Protection

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

## Logout Security

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
