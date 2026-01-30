# Authentication

> Guards, providers, Sanctum, password reset

## Overview

Laravel authentication provides flexible guards, providers, and password reset functionality.

## Authentication Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    User     │────▶│    Guard    │────▶│   Provider  │
│  (Session)  │     │  (Session/  │     │  (Eloquent/  │
│             │     │   Token)    │     │   Database)  │
└─────────────┘     └─────────────┘     └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   Session   │
                     │  Storage    │
                     └─────────────┘
```

## Configuration

### config/auth.php

```php
return [
    'defaults' => [
        'guard' => 'web',
        'passwords' => 'users',
    ],

    'guards' => [
        'web' => [
            'driver' => 'session',
            'provider' => 'users',
        ],
        'api' => [
            'driver' => 'token',  // or 'sanctum'
            'provider' => 'users',
            'hash' => false,
        ],
    ],

    'providers' => [
        'users' => [
            'driver' => 'eloquent',
            'model' => App\Models\User::class,
        ],
    ],
];
```

## Session Authentication (Web)

### Login Controller

```php
<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class LoginController extends Controller
{
    public function showLoginForm()
    {
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $credentials = $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        if (Auth::attempt($credentials, $request->boolean('remember'))) {
            $request->session()->regenerate();

            return redirect()->intended('/dashboard');
        }

        return back()->withErrors([
            'email' => 'The provided credentials do not match our records.',
        ]);
    }

    public function logout(Request $request)
    {
        Auth::logout();

        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect('/');
    }
}
```

### Protecting Routes

```php
// routes/web.php
Route::middleware(['auth'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
    Route::get('/profile', [ProfileController::class, 'show']);
});
```

### Blade Directives

```blade
@auth
    <p>Welcome, {{ Auth::user()->name }}</p>
@endauth

@guest
    <p>Please <a href="{{ route('login') }}">login</a></p>
@endguest

@auth('admin')
    <p>Admin user</p>
@endauth
```

## Laravel Sanctum (API)

### Installation

```bash
php artisan install:api
```

### Configuration

```php
// config/sanctum.php
return [
    'stateful' => explode(',', env('SANCTUM_STATEFUL_DOMAINS', sprintf(
        '%s%s',
        'localhost,localhost:3000,127.0.0.1,127.0.0.1:8000,::1',
        env('APP_URL') ? ','.parse_url(env('APP_URL'), PHP_URL_HOST) : ''
    ))),
];
```

### API Authentication

```php
// routes/api.php
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', function (Request $request) {
        return response()->json($request->user());
    });

    Route::apiResource('posts', PostController::class);
});
```

### Token Creation

```php
// ✅ Good - Create token for user
$user = User::find(1);
$token = $user->createToken('api-token')->plainTextToken;

// Response
return response()->json([
    'token' => $token,
]);
```

### Token Abilities

```php
// ✅ Good - Token with specific abilities
$user->createToken('read-only', ['posts:read'])->plainTextToken;

// Check abilities
if ($user->tokenCan('posts:read')) {
    // User can read posts
}
```

### SPA Authentication

```php
// config/sanctum.php
'stateful' => explode(',', env('SANCTUM_STATEFUL_DOMAINS', sprintf(
    '%s%s',
    'localhost,localhost:3000',
    env('APP_URL') ? ','.parse_url(env('APP_URL'), PHP_URL_HOST) : ''
))),

// config/cors.php
'paths' => ['api/*', 'sanctum/csrf-cookie'],

routes/api.php
Route::middleware(['auth:sanctum'])->group(function () {
    Route::get('/user', [UserController::class, 'show']);
});
```

## Password Reset

### Database Setup

```bash
php artisan make:migration create_password_resets_table
```

```php
Schema::create('password_resets', function (Blueprint $table) {
    $table->string('email')->index();
    $table->string('token');
    $table->timestamp('created_at')->nullable();
});
```

### Forgot Password Controller

```php
<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Str;

class ForgotPasswordController extends Controller
{
    public function showLinkRequestForm()
    {
        return view('auth.forgot-password');
    }

    public function sendResetLinkEmail(Request $request)
    {
        $request->validate(['email' => 'required|email']);

        $status = Password::sendResetLink(
            $request->only('email')
        );

        return $status === Password::RESET_LINK_SENT
            ? back()->with(['status' => __($status)])
            : back()->withErrors(['email' => __($status)]);
    }
}
```

### Reset Password Controller

```php
<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Auth\Events\PasswordReset;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Str;

class ResetPasswordController extends Controller
{
    public function showResetForm(Request $request, $token = null)
    {
        return view('auth.reset-password', [
            'token' => $token,
            'email' => $request->email,
        ]);
    }

    public function reset(Request $request)
    {
        $request->validate([
            'token' => 'required',
            'email' => 'required|email',
            'password' => 'required|string|min:8|confirmed',
        ]);

        $status = Password::reset(
            $request->only('email', 'password', 'password_confirmation', 'token'),
            function ($user, $password) {
                $user->forceFill([
                    'password' => Hash::make($password)
                ])->setRememberToken(Str::random(60));

                $user->save();

                event(new PasswordReset($user));
            }
        );

        return $status === Password::PASSWORD_RESET
            ? redirect()->route('login')->with('status', __($status))
            : back()->withErrors(['email' => [__($status)]]);
    }
}
```

## User Model

### Must Implement Contracts

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'password' => 'hashed',
    ];
}
```

## Guards and Providers

### Custom Guard

```php
// App\Services\CustomGuard
use Illuminate\Auth\GuardHelpers;
use Illuminate\Contracts\Auth\Guard;
use Illuminate\Http\Request;

class CustomGuard implements Guard
{
    use GuardHelpers;

    protected $request;

    public function __construct(Request $request)
    {
        $this->request = $request;
    }

    public function user()
    {
        // Custom logic to retrieve user
        if (!is_null($this->user)) {
            return $this->user;
        }

        $user = null;
        // Implement custom authentication logic

        return $this->user = $user;
    }

    public function validate(array $credentials = [])
    {
        // Implement validation logic
    }
}
```

### Register Custom Guard

```php
// AppServiceProvider.php
use Illuminate\Support\Facades\Auth;

public function boot()
{
    Auth::extend('custom', function ($app, $name, array $config) {
        return new CustomGuard($app['request']);
    });
}
```

## Best Practices

### DO ✅

```php
// ✅ Use Auth facade for authentication
Auth::check();  // Check if user is authenticated
Auth::user();   // Get authenticated user
Auth::id();     // Get authenticated user ID

// ✅ Use middleware for route protection
Route::middleware(['auth'])->group(function () {
    // Protected routes
});

// ✅ Use Sanctum for API authentication
Route::middleware('auth:sanctum')->group(function () {
    // API routes
});

// ✅ Use token abilities for granular permissions
$user->createToken('app-token', ['posts:read', 'posts:create']);
```

### DON'T ❌

```php
// ❌ Don't store passwords as plain text
User::create([
    'password' => $request->password,  // Bad!
]);

// ✅ Use Hash facade
User::create([
    'password' => Hash::make($request->password),
]);

// ❌ Don't use simple tokens without expiration
$token = Str::random(60);  // Never expires

// ✅ Use Sanctum tokens with expiration
$user->createToken('api-token')->accessToken;

// ❌ Don't trust client-side authentication
if ($request->input('authenticated')) {  // Bad!
}
```

## Quick Reference

| Method | Description |
|--------|-------------|
| `Auth::check()` | Check if user is authenticated |
| `Auth::user()` | Get authenticated user |
| `Auth::id()` | Get authenticated user ID |
| `Auth::attempt($credentials)` | Attempt authentication |
| `Auth::login($user)` | Login user |
| `Auth::logout()` | Logout user |
| `Auth::guard($name)` | Get specific guard |
| `$user->createToken($name)` | Create API token |

## See Also

- **AUTHORIZATION.md** - Policies, Gates, permissions
- **middleware.md** - Authentication middleware
- **request-validation.md** - Login form validation

---

**Reference**: Laravel 11.x Authentication Documentation
