# Coding Standards

> PSR-2, PSR-12, PHPDoc Rules for Laravel

## Overview

Laravel follows PHP Standards Recommendations (PSR) to ensure consistency and maintainability. This document covers PSR-1, PSR-2, PSR-4, and PSR-12.

## PSR Compliance Summary

| PSR | Description | Laravel Status |
|-----|-------------|----------------|
| **PSR-1** | Basic coding standard | ✅ Fully compliant |
| **PSR-2** | Coding style guide | ✅ Fully compliant |
| **PSR-4** | Autoloading standard | ✅ Fully compliant |
| **PSR-12** | Extended coding style | ✅ Fully compliant |

## File Format

### Encoding

- **UTF-8** without BOM
- Unix line endings (`LF`, not `CRLF`)

### Line Ending

```php
// ✅ Good - Unix line endings (LF)
<?php

namespace App\Services;

class UserService
{
    // ...
}

// ❌ Bad - Windows line endings (CRLF)
<?php\r\n
\r\n
namespace App\Services;\r\n
```

### Trailing Whitespace

```php
// ✅ Good - No trailing whitespace
public function getUser(int $id): User
{
    return User::find($id);
}

// ❌ Bad - Trailing whitespace on lines
public function getUser(int $id): User·
{·
    return User::find($id);·
}·
```

## Indentation

### 4 Spaces (No Tabs)

```php
// ✅ Good - 4 spaces
class UserService
{
    public function getUser(int $id): User
    {
        return User::find($id);
    }
}

// ❌ Bad - Tabs
class UserService
{
	public function getUser(int $id): User
	{
		return User::find($id);
	}
}
```

## Line Length

### Soft Limit: 120 Characters

```php
// ✅ Good - Under 120 characters
public function createUserWithEmailVerification(array $data): User
{
    return User::create($data);
}

// ✅ Good - Break long lines
public function createUserWithProfileAndSubscription(
    array $userData,
    array $profileData,
    array $subscriptionData
): User {
    // ...
}

// ❌ Bad - Too long
public function createUserWithProfileAndSubscriptionAndEmailVerification(array $userData, array $profileData, array $subscriptionData, bool $sendEmail = true): User {
    // ... (line exceeds 120 chars)
}
```

## Namespace and Use Declarations

### Namespace Declaration

```php
// ✅ Good
<?php

namespace App\Services;

use App\Models\User;
use App\Services\Contracts\UserServiceInterface;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Pagination\LengthAwarePaginator;

class UserService implements UserServiceInterface
{
    // ...
}

// ❌ Bad - Missing blank line after <?php
<?php
namespace App\Services;

// ❌ Bad - Wrong order (use before namespace)
<?php
use App\Models\User;

namespace App\Services;
```

### Use Statements - Alphabetical Order

```php
// ✅ Good - Alphabetical, grouped by origin
<?php

namespace App\Services;

use App\Models\User;
use App\Models\UserProfile;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;

// ❌ Bad - Not alphabetical
use Illuminate\Support\Facades\DB;
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
```

### Fully Qualified vs Use

```php
// ✅ Good - Use uncommon classes inline, import common ones
<?php

namespace App\Services;

use App\Models\User;

class UserService
{
    public function getUser(int $id): \App\Models\User
    {
        return User::find($id);
    }

    public function logActivity(\Psr\Log\LoggerInterface $logger): void
    {
        $logger->info('User activity logged');
    }
}

// ❌ Bad - Fully qualified for everything
class UserService
{
    public function getUser(int $id): \App\Models\User
    {
        return \App\Models\User::find($id);
    }
}
```

## Class, Property, and Method Declarations

### Class Declaration

```php
// ✅ Good
class UserService
{
    // ...
}

// ❌ Bad - Braces on new line
class UserService
{
    // ...
}
```

### Property Declaration

```php
// ✅ Good - One declaration per line
class UserService
{
    private User $user;
    private Cache $cache;
    private Logger $logger;
}

// ❌ Bad - Multiple declarations
class UserService
{
    private User $user, Cache $cache;  // Multiple properties
    public $name;                      // No type hint
}
```

### Method Declaration

```php
// ✅ Good
public function getUserById(int $id): ?User
{
    return User::find($id);
}

// ❌ Bad - No return type
public function getUserById($id)  // No type hints
{
    return User::find($id);
}
```

### Constructor Property Promotion (PHP 8.0+)

```php
// ✅ Good - Constructor property promotion
class UserService
{
    public function __construct(
        private User $user,
        private Cache $cache,
    ) {}
}

// ✅ Also Good - Traditional (when more complex)
class UserService
{
    private User $user;
    private Cache $cache;

    public function __construct(User $user, Cache $cache)
    {
        $this->user = $user;
        $this->cache = $cache;
    }
}

// ❌ Bad - Mixed approach
class UserService
{
    private User $user;

    public function __construct(
        private User $user,
        Cache $cache  // Not promoted
    ) {
        $this->cache = $cache;
    }
}
```

## Control Structures

### If Statement

```php
// ✅ Good
if ($user->isActive()) {
    return $user;
}

if ($user->isActive()) {
    return $user;
} else {
    return null;
}

if ($user->isAdmin()) {
    // ...
} elseif ($user->isModerator()) {
    // ...
} else {
    // ...
}

// ❌ Bad - Braces on new line
if ($user->isActive())
{
    return $user;
}

// ❌ Bad - No braces for single line (discouraged)
if ($user->isActive())
    return $user;
```

### Switch Statement

```php
// ✅ Good
switch ($user->status) {
    case 'active':
        $this->sendWelcomeEmail($user);
        break;
    case 'inactive':
        $this->sendReactivationEmail($user);
        break;
    default:
        $this->sendDefaultEmail($user);
        break;
}

// ❌ Bad - Indented cases
switch ($user->status) {
    case 'active':
        $this->sendWelcomeEmail($user);
        break;
    default:
        $this->sendDefaultEmail($user);
        break;
}
```

### For, Foreach, While

```php
// ✅ Good
foreach ($users as $user) {
    $user->markAsActive();
}

for ($i = 0; $i < 10; $i++) {
    // ...
}

while ($condition) {
    // ...
}

// ✅ Good - Alternative syntax for views
@foreach ($users as $user)
    <div>{{ $user->name }}</div>
@endforeach
```

### Try-Catch-Finally

```php
// ✅ Good
try {
    $user = User::create($data);
} catch (QueryException $e) {
    Log::error('Failed to create user', ['error' => $e->getMessage()]);
    throw $e;
} finally {
    // Cleanup
}

// ❌ Bad - Wrong brace placement
try
{
    $user = User::create($data);
}
catch (QueryException $e)
{
    Log::error('Failed to create user');
}
```

## Closures

```php
// ✅ Good - Proper spacing
$users = User::active()->get()->map(function (User $user) {
    return $user->name;
});

// ✅ Good - Arrow functions (PHP 7.4+)
$users = User::active()->get()->map(fn (User $user) => $user->name);

// ❌ Bad - No space after function keyword
$users = User::active()->get()->map(function(User $user) {
    return $user->name;
});
```

## Type Hints

### Return Types (Required)

```php
// ✅ Good - Always declare return types
public function getUser(int $id): ?User
{
    return User::find($id);
}

public function getAllUsers(): Collection
{
    return User::all();
}

public function createUser(array $data): User
{
    return User::create($data);
}

// ❌ Bad - Missing return types
public function getUser($id)  // No return type
{
    return User::find($id);
}
```

### Parameter Types (Required)

```php
// ✅ Good
public function updateUser(int $id, array $data): User
{
    $user = User::findOrFail($id);
    $user->update($data);
    return $user;
}

// ❌ Bad - No parameter types
public function updateUser($id, $data)  // No type hints
{
    $user = User::findOrFail($id);
    $user->update($data);
    return $user;
}
```

### Nullable Types

```php
// ✅ Good
public function getUserByEmail(string $email): ?User
{
    return User::where('email', $email)->first();
}

// ❌ Bad - Old-style nullable (PHP < 7.1)
/**
 * @return User|null
 */
public function getUserByEmail(string $email)
{
    return User::where('email', $email)->first();
}
```

### Union Types (PHP 8.0+)

```php
// ✅ Good
public function processInput(int|string $input): string
{
    return (string) $input;
}
```

## PHPDoc Rules

### When Docblocks Are NOT Needed

```php
// ✅ Good - No docblock needed (types are self-documenting)
public function createUser(array $data): User
{
    return User::create($data);
}

public function getUserById(int $id): ?User
{
    return User::find($id);
}

// ✅ Good - Constructor property promotion (no docblock)
public function __construct(
    private User $user,
    private Cache $cache,
) {}
```

### When Docblocks ARE Needed

```php
// ✅ Good - For generic types
/**
 * @return Collection<int, User>
 */
public function getActiveUsers(): Collection
{
    return User::active()->get();
}

// ✅ Good - For complex logic
/**
 * Create user with profile and subscription in a transaction.
 *
 * @param array $userData User data (name, email, password)
 * @param array $profileData Profile data (phone, address)
 * @param array $subscriptionData Subscription data (plan, expires_at)
 * @return User Created user with relationships
 * @throws \Exception If transaction fails
 */
public function createUserWithSubscription(
    array $userData,
    array $profileData,
    array $subscriptionData
): User {
    return DB::transaction(function () use ($userData, $profileData, $subscriptionData) {
        $user = User::create($userData);
        $user->profile()->create($profileData);
        $user->subscription()->create($subscriptionData);
        return $user;
    });
}

// ✅ Good - For array shapes
/**
 * @param array{email: string, password: string} $credentials
 */
public function login(array $credentials): bool
{
    return Auth::attempt($credentials);
}
```

### Docblock Format

```php
// ✅ Good
/**
 * Get active users with their posts.
 *
 * @param int $perPage Number of items per page
 * @param bool $withPosts Include posts in results
 * @return LengthAwarePaginator Paginated user collection
 */
public function getActiveUsersPaginated(int $perPage = 15, bool $withPosts = false): LengthAwarePaginator
{
    $query = User::active();

    if ($withPosts) {
        $query->with('posts');
    }

    return $query->paginate($perPage);
}

// ❌ Bad - Missing description, wrong tag order
/**
 * @param int $perPage
 * @return LengthAwarePaginator
 * @param bool $withPosts
 */
public function getActiveUsersPaginated(int $perPage = 15, bool $withPosts = false): LengthAwarePaginator
{
    // ...
}
```

## Magic Methods

```php
// ✅ Good - Document magic methods
class UserService
{
    /**
     * Handle dynamic method calls.
     *
     * @param string $method
     * @param array $parameters
     * @return mixed
     */
    public function __call(string $method, array $parameters)
    {
        // ...
    }
}
```

## Constants

```php
// ✅ Good - UPPER_CASE
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

// ❌ Bad - Lowercase or camelCase
class User extends Model
{
    const status_active = 'active';
    const maxLoginAttempts = 5;
}
```

## String Concatenation

```php
// ✅ Good - Spaces around concatenation operator
$message = 'Hello, ' . $name . '!';

// ✅ Good - Use sprintf for complex strings
$message = sprintf('Hello, %s! Your ID is %d.', $name, $id);

// ✅ Good - Use interpolation for simple cases
$message = "Hello, {$name}!";

// ❌ Bad - No spaces
$message = 'Hello, '.$name.'!';
```

## Array Declarations

```php
// ✅ Good - Short syntax
$users = [
    'john' => ['email' => 'john@example.com'],
    'jane' => ['email' => 'jane@example.com'],
];

// ✅ Good - Multi-line for complex arrays
$userData = [
    'name' => $request->input('name'),
    'email' => $request->input('email'),
    'password' => Hash::make($request->input('password')),
    'status' => 'active',
];

// ❌ Bad - Old array() syntax
$users = array(
    'john' => array('email' => 'john@example.com'),
);
```

## Ternary Operator

```php
// ✅ Good
$status = $user->isActive() ? 'active' : 'inactive';

// ✅ Good - Elvis operator (PHP 5.3+)
$status = $user->status ?: 'unknown';

// ✅ Good - Null coalescing (PHP 7.0+)
$name = $user->name ?? 'Guest';

// ✅ Good - Null coalescing assignment (PHP 7.4+)
$user->profile ??= new Profile();

// ❌ Bad - Nested ternary (hard to read)
$status = $user->isActive() ? ($user->isAdmin() ? 'admin' : 'user') : 'inactive';
```

## Comparison Operators

```php
// ✅ Good - Strict comparison
if ($user->id === $userId) {
    // ...
}

if ($status !== null) {
    // ...
}

// ❌ Bad - Loose comparison (unless intentional)
if ($user->id == $userId) {  // Can cause type juggling issues
    // ...
}
```

## Method Chaining

```php
// ✅ Good - Indent for each method
$users = User::active()
    ->with(['posts', 'profile'])
    ->orderBy('created_at', 'desc')
    ->paginate(15);

// ✅ Good - Break into lines for readability
$users = User::active()
    ->with(['posts' => function ($query) {
        $query->where('published', true);
    }])
    ->orderBy('created_at', 'desc')
    ->paginate(15);

// ❌ Bad - Everything on one line
$users = User::active()->with(['posts', 'profile'])->orderBy('created_at', 'desc')->paginate(15);
```

## Laravel-Specific Patterns

### Service Container Binding

```php
// ✅ Good - Use type hints
$this->app->bind(UserServiceInterface::class, UserService::class);

// ✅ Good - Singleton for stateless services
$this->app->singleton(UserServiceInterface::class, UserService::class);
```

### Validation

```php
// ✅ Good - Form Request
public function store(StoreUserRequest $request): JsonResponse
{
    $user = $this->userService->createUser($request->validated());
    return response()->json($user, 201);
}

// ❌ Bad - Inline validation
public function store(Request $request): JsonResponse
{
    $validated = $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
    ]);
    // ...
}
```

## Quick Checklist

- [ ] File encoded as UTF-8 without BOM
- [ ] Unix line endings (LF)
- [ ] 4 spaces for indentation (no tabs)
- [ ] Lines under 120 characters
- [ ] Namespace declaration first
- [ ] Use statements alphabetical
- [ ] Opening brace on same line
- [ ] No trailing whitespace
- [ ] Type hints on all parameters
- [ ] Return type declarations
- [ ] Docblocks only when needed
- [ ] Constants in UPPER_SNAKE_CASE
- [ ] Variables in camelCase
- [ ] Strict comparisons (`===`, `!==`)

## Tools

### PHP-CS-Fixer

```bash
# Install
composer require --dev friendsofphp/php-cs-fixer

# Run
./vendor/bin/php-cs-fixer fix

# Config (.php-cs-fixer.php)
<?php

return (new \PhpCsFixer\Config())
    ->setRules([
        '@PSR12' => true,
        'array_syntax' => ['syntax' => 'short'],
        'ordered_imports' => ['sort_algorithm' => 'alpha'],
        'no_unused_imports' => true,
    ])
    ->setLineEnding("\n");
```

### Laravel Pint (Built-in)

```bash
# Run
./vendor/bin/pint

# Specific files
./vendor/bin/pint app/Services
```

## See Also

- **NAMING-CONVENTIONS.md** - Naming rules for Laravel
- **PSR-1**: https://www.php-fig.org/psr/psr-1/
- **PSR-2**: https://www.php-fig.org/psr/psr-2/
- **PSR-4**: https://www.php-fig.org/psr/psr-4/
- **PSR-12**: https://www.php-fig.org/psr/psr-12/

---

**Reference**: PSR Standards, Laravel Documentation
