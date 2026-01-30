# Middleware

## Purpose

Filter HTTP requests entering your application. Authentication, logging, CORS, rate limiting.

## Structure

```
app/Http/Middleware/
├── EnsureTokenIsValid.php
└── LogRequests.php
```

## Generate Middleware

```bash
php artisan make:middleware EnsureTokenIsValid
```

## Basic Middleware

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureTokenIsValid
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->input('token') !== 'my-secret-token') {
            return redirect('home');
        }

        return $next($request);
    }
}
```

## Before / After Middleware

```php
// Before middleware
public function handle(Request $request, Closure $next): Response
{
    // Your logic here
    return $next($request);
}

// After middleware
public function handle(Request $request, Closure $next): Response
{
    $response = $next($request);

    // Your logic here
    return $response;
}
```

## Register Middleware

### Global Middleware (app/Http/Kernel.php)

```php
protected $middleware = [
    // \App\Http\Middleware\TrustHosts::class,
    \App\Http\Middleware\TrimStrings::class,
    \Illuminate\Http\Middleware\ValidatePostSize::class,
];
```

### Route Middleware

```php
protected $middlewareAliases = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
    'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
    'role' => \App\Http\Middleware\CheckRole::class,
];
```

## Assign to Routes

```php
// Single route
Route::get('/admin', [AdminController::class, 'index'])
    ->middleware('auth');

// Multiple middleware
Route::get('/admin', [AdminController::class, 'index'])
    ->middleware(['auth', 'verified']);

// Group of routes
Route::middleware(['auth'])->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit']);
    Route::put('/profile', [ProfileController::class, 'update']);
});

// Controller constructor
class UserController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth');
        $this->middleware('log')->only('index');
        $this->middleware('subscribed')->except('store');
    }
}
```

## Middleware with Parameters

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class CheckRole
{
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if (!$request->user()->hasRole($role)) {
            abort(403, 'Unauthorized action.');
        }

        return $next($request);
    }
}

// Route definition
Route::put('/post/{post}', [PostController::class, 'update'])
    ->middleware('role:editor');
```

## Termination Middleware

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class LogAfterRequest
{
    public function handle(Request $request, Closure $next): Response
    {
        return $next($request);
    }

    public function terminate(Request $request, Response $response): void
    {
        // Log after response sent to browser
        \Log::info('Request processed', [
            'url' => $request->url(),
            'status' => $response->getStatusCode(),
        ]);
    }
}
```

## Common Patterns

### Authentication Middleware

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class RedirectIfAuthenticated
{
    public function handle(Request $request, Closure $next, string ...$guards): Response
    {
        $guards = empty($guards) ? [null] : $guards;

        foreach ($guards as $guard) {
            if (Auth::guard($guard)->check()) {
                return redirect('/dashboard');
            }
        }

        return $next($request);
    }
}
```

### API Rate Limiting

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Cache\RateLimiter;
use Illuminate\Http\Request;

class ThrottleRequests
{
    public function __construct(
        protected RateLimiter $limiter
    ) {}

    public function handle(Request $request, Closure $next, int $maxAttempts = 60, int $decayMinutes = 1): Response
    {
        $key = $this->resolveRequestSignature($request);

        if ($this->limiter->tooManyAttempts($key, $maxAttempts)) {
            return response()->json([
                'message' => 'Too many attempts.',
                'retry_after' => $this->limiter->availableIn($key),
            ], 429);
        }

        $this->limiter->hit($key, $decayMinutes * 60);

        return $next($request);
    }
}
```

### Logging Middleware

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class LogRequests
{
    public function handle(Request $request, Closure $next): Response
    {
        $startTime = microtime(true);

        $response = $next($request);

        $duration = round((microtime(true) - $startTime) * 1000);

        Log::info('Request Log', [
            'method' => $request->method(),
            'url' => $request->fullUrl(),
            'ip' => $request->ip(),
            'status' => $response->getStatusCode(),
            'duration_ms' => $duration,
        ]);

        return $response;
    }
}
```

### CORS Middleware

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class HandleCors
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        $response->headers->set('Access-Control-Allow-Origin', '*');
        $response->headers->set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        $response->headers->set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

        return $response;
    }
}
```

### Locale Detection

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\App;

class SetLocale
{
    public function handle(Request $request, Closure $next): Response
    {
        $locale = $request->session()->get('locale')
            ?? $request->header('Accept-Language')
            ?? config('app.fallback_locale');

        App::setLocale($locale);

        return $next($request);
    }
}
```

## Rules

1. **Keep it focused** - One responsibility per middleware
2. **Type hint properly** - Use `Request` and `Response` types
3. **Return responses** - Always return response or `$next($request)`
4. **Use parameters** - For configurable behavior
5. **Handle errors gracefully** - Don't let exceptions bubble up unexpectedly

## Best Practices

1. **Thin middleware** - Delegate business logic to services
2. **Use termination middleware** - For logging, analytics after response
3. **Order matters** - Register middleware in correct order
4. **Test thoroughly** - Middleware affects all requests it applies to
5. **Use aliases** - For complex middleware with parameters

---

**See also:** `controller-best-practices.md`, `service-layer.md`
