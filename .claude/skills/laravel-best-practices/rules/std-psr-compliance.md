---
title: PSR-12 Coding Standards Compliance
impact: HIGH
impactDescription: Consistent code style across team
tags: coding-standards, psr-12, psr-4, phpdoc, type-hints
---

## PSR-12 Coding Standards Compliance

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

## Type Hints Required

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

## Constructor Property Promotion

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

## Return Type Declarations

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

## Nullable Types

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

## PHPDoc Guidelines

**Incorrect (Unnecessary docblock):**

```php
/**
 * Get user by ID
 *
 * @param int $id
 * @return User
 */
public function getUserById(int $id): User
{
    return User::find($id);
}
```

**Correct (No docblock when types are self-documenting):**

```php
public function getUserById(int $id): User
{
    return User::find($id);
}
```

**Correct (Docblock for complex logic):**

```php
/**
 * Create user with profile and subscription in a transaction.
 *
 * @param array $userData User data (name, email, password)
 * @param array $profileData Profile data (phone, address)
 * @return User Created user with relationships
 * @throws \Exception If transaction fails
 */
public function createUserWithProfile(
    array $userData,
    array $profileData
): User {
    return DB::transaction(function () use ($userData, $profileData) {
        $user = User::create($userData);
        $user->profile()->create($profileData);
        return $user;
    });
}
```

## Use Statement Ordering

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
