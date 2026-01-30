# Testing

> PHPUnit, Pest testing conventions

## Overview

Laravel supports PHPUnit and Pest for unit testing, feature testing, and browser testing.

## Test Structure

```
tests/
├── Unit/
│   ├── Models/
│   │   └── UserTest.php
│   └── Services/
│       └── UserServiceTest.php
├── Feature/
│   ├── Auth/
│   │   └── AuthenticationTest.php
│   └── Api/
│       └── UserApiTest.php
├── Pest.php  (if using Pest)
└── TestCase.php
```

## PHPUnit Setup

### phpunit.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true"
>
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Feature">
            <directory>tests/Feature</directory>
        </testsuite>
    </testsuites>
    <php>
        <env name="APP_ENV" value="testing"/>
        <env name="BCRYPT_ROUNDS" value="4"/>
        <env name="CACHE_DRIVER" value="array"/>
        <env name="DB_CONNECTION" value="sqlite"/>
        <env name="DB_DATABASE" value=":memory:"/>
        <env name="MAIL_MAILER" value="array"/>
        <env name="QUEUE_CONNECTION" value="sync"/>
        <env name="SESSION_DRIVER" value="array"/>
        <env name="TELESCOPE_ENABLED" value="false"/>
    </php>
</phpunit>
```

## Pest Setup

### Installation

```bash
composer require pestphp/pest --dev --with-all-dependencies
php artisan pest:install
```

### pest.php

```php
use Pest\PHPUnit\Tests\Features;

test('example')->assertTrue(true);
```

## Unit Tests

### Model Test (PHPUnit)

```php
<?php

namespace Tests\Unit\Models;

use App\Models\User;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

class UserTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_has_fillable_attributes(): void
    {
        $user = User::factory()->make([
            'name' => 'John Doe',
            'email' => 'john@example.com',
        ]);

        $this->assertEquals('John Doe', $user->name);
        $this->assertEquals('john@example.com', $user->email);
    }

    public function test_user_hashes_password(): void
    {
        $user = User::factory()->create([
            'password' => 'password123',
        ]);

        $this->assertNotEquals('password123', $user->password);
        $this->assertTrue(\Hash::check('password123', $user->password));
    }

    public function test_user_has_posts_relationship(): void
    {
        $user = User::factory()
            ->has(Post::factory()->count(3))
            ->create();

        $this->assertCount(3, $user->posts);
        $this->assertInstanceOf(Post::class, $user->posts->first());
    }
}
```

### Service Test (Pest)

```php
<?php

use App\Models\User;
use App\Services\UserService;
use function Pest\Laravel\assertDatabaseHas;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->userService = new UserService(new User());
});

it('can create a user', function () {
    $userData = [
        'name' => 'John Doe',
        'email' => 'john@example.com',
        'password' => 'password123',
    ];

    $user = $this->userService->createUser($userData);

    expect($user->name)->toBe('John Doe');
    expect($user->email)->toBe('john@example.com');
    assertDatabaseHas('users', [
        'email' => 'john@example.com',
    ]);
});

it('can get paginated users', function () {
    User::factory()->count(20)->create();

    $users = $this->userService->getPaginatedUsers(15);

    expect($users)->toHaveCount(15);
    expect($users->total())->toBe(20);
});
```

## Feature Tests

### API Test (PHPUnit)

```php
<?php

namespace Tests\Feature\Api;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_can_list_users(): void
    {
        User::factory()->count(3)->create();

        $response = $this->getJson('/api/users');

        $response->assertStatus(200)
            ->assertJsonCount(3, 'data')
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'name', 'email'],
                ],
            ]);
    }

    public function test_can_create_user(): void
    {
        $userData = [
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'password' => 'password123',
        ];

        $response = $this->postJson('/api/users', $userData);

        $response->assertStatus(201)
            ->assertJson([
                'name' => 'John Doe',
                'email' => 'john@example.com',
            ]);

        $this->assertDatabaseHas('users', [
            'email' => 'john@example.com',
        ]);
    }

    public function test_requires_authentication(): void
    {
        $response = $this->getJson('/api/user');

        $response->assertStatus(401);
    }

    public function test_authenticated_user_can_fetch_profile(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user, 'sanctum')
            ->getJson('/api/user');

        $response->assertStatus(200)
            ->assertJson([
                'id' => $user->id,
                'name' => $user->name,
            ]);
    }
}
```

### API Test (Pest)

```php
<?php

use App\Models\User;
use function Pest\Laravel\{actingAs, getJson, postJson, putJson, deleteJson};
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

it('can list users', function () {
    User::factory()->count(3)->create();

    getJson('/api/users')
        ->assertStatus(200)
        ->assertJsonCount(3, 'data');
});

it('can create user', function () {
    $userData = [
        'name' => 'John Doe',
        'email' => 'john@example.com',
        'password' => 'password123',
    ];

    postJson('/api/users', $userData)
        ->assertStatus(201)
        ->assertJson([
            'name' => 'John Doe',
            'email' => 'john@example.com',
        ]);
});

it('requires email to create user', function () {
    postJson('/api/users', [
        'name' => 'John Doe',
        'password' => 'password123',
    ])
        ->assertStatus(422)
        ->assertJsonValidationErrors(['email']);
});
```

## Authentication Tests

### Login Test (Pest)

```php
<?php

use App\Models\User;
use function Pest\Laravel\{postJson};
use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Sanctum\Sanctum;

uses(RefreshDatabase::class);

it('can login with valid credentials', function () {
    $user = User::factory()->create([
        'password' => bcrypt('password123'),
    ]);

    postJson('/api/login', [
        'email' => $user->email,
        'password' => 'password123',
    ])
        ->assertStatus(200)
        ->assertJsonStructure([
            'token',
            'user' => ['id', 'name', 'email'],
        ]);
});

it('cannot login with invalid credentials', function () {
    $user = User::factory()->create([
        'password' => bcrypt('password123'),
    ]);

    postJson('/api/login', [
        'email' => $user->email,
        'password' => 'wrong-password',
    ])
        ->assertStatus(401);
});
```

## Authorization Tests

### Policy Test (Pest)

```php
<?php

use App\Models\User;
use App\Models\Post;
use App\Policies\PostPolicy;
use function Pest\Laravel\{actingAs};

it('allows user to update own post', function () {
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    expect($user->can('update', $post))->toBeTrue();
});

it('denies user to update others post', function () {
    $user = User::factory()->create();
    $otherUser = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $otherUser->id]);

    expect($user->can('update', $post))->toBeFalse();
});
```

## Data Providers

### PHPUnit Data Providers

```php
<?php

class UserServiceTest extends TestCase
{
    /**
     * @dataProvider emailProvider
     */
    public function test_validates_email_format($email, $isValid): void
    {
        $validator = Validator::make([
            'email' => $email,
        ], [
            'email' => 'required|email',
        ]);

        expect($validator->passes())->toBe($isValid);
    }

    public static function emailProvider(): array
    {
        return [
            'valid email' => ['john@example.com', true],
            'invalid email' => ['not-an-email', false],
            'missing email' => ['', false],
        ];
    }
}
```

### Pest Datasets

```php
<?php

use App\Services\UserService;

beforeEach(function () {
    $this->userService = new UserService(new User());
});

dataset('user_roles', [
    'admin' => ['admin', true],
    'user' => ['user', false],
    'guest' => ['guest', false],
]);

it('can check user role', function ($role, $expected) {
    $user = User::factory()->create(['role' => $role]);

    expect($user->isAdmin())->toBe($expected);
})->with('user_roles');
```

## Factories

### Model Factory

```php
// database/factories/UserFactory.php
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
    protected $model = User::class;

    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'password' => bcrypt('password'),
            'is_active' => true,
        ];
    }

    public function inactive(): static
    {
        return $this->state(fn (array $attributes) => [
            'is_active' => false,
        ]);
    }

    public function admin(): static
    {
        return $this->state(fn (array $attributes) => [
            'role' => 'admin',
        ]);
    }
}
```

### Using Factories

```php
// ✅ Good
$user = User::factory()->create();
$users = User::factory()->count(10)->create();
$inactiveUser = User::factory()->inactive()->create();
$admin = User::factory()->admin()->create();

// ✅ Good - With relationships
$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();

// ✅ Good - Raw data
User::factory()->create([
    'name' => 'John Doe',
    'email' => 'john@example.com',
]);
```

## Mocking

### Mocking Facades

```php
use Illuminate\Support\Facades\Cache;

test('caches user data', function () {
    Cache::shouldReceive('remember')
        ->once()
        ->with('users.all', 3600, \Closure::class)
        ->andReturn($users = User::all());

    $result = $this->userService->getAllUsers();

    expect($result)->toBe($users);
});
```

### Mocking Events

```php
use Illuminate\Support\Facades\Event;

test('dispatches user registered event', function () {
    Event::fake([UserRegistered::class]);

    $user = User::factory()->create();

    UserRegistered::dispatch($user);

    Event::assertDispatched(UserRegistered::class);
});
```

### Mocking Mail

```php
use Illuminate\Support\Facades\Mail;

test('sends welcome email', function () {
    Mail::fake();

    $user = User::factory()->create();

    Mail::to($user->email)->send(new WelcomeEmail($user));

    Mail::assertSent(WelcomeEmail::class, function ($mail) use ($user) {
        return $mail->hasTo($user->email);
    });
});
```

## HTTP Tests

### Acting As

```php
// ✅ Good - Sanctum authentication
 Sanctum::actingAs(
    User::factory()->create(),
    ['create-posts']
);

$response = $this->post('/api/posts', [
    'title' => 'Test Post',
]);

$response->assertStatus(201);
```

### JSON Responses

```php
// ✅ Good - Test JSON structure
$response = $this->getJson('/api/users');

$response->assertStatus(200)
    ->assertJsonStructure([
        'data' => [
            '*' => ['id', 'name', 'email'],
        ],
    ])
    ->assertJsonPath('data.0.name', 'John Doe');
```

## Best Practices

### DO ✅

```php
// ✅ Test behavior, not implementation
test('user can create post', function () {
    // Test what should happen
    $user = User::factory()->create();

    actingAs($user)
        ->post('/posts', ['title' => 'Test'])
        ->assertStatus(201);
});

// ✅ Use descriptive test names
test('user receives error when creating post without title');
test('admin can delete any post');
test('guest cannot access protected routes');

// ✅ Use factories for test data
$user = User::factory()->create();

// ✅ Clean up between tests
uses(RefreshDatabase::class);
```

### DON'T ❌

```php
// ❌ Don't test implementation details
test('userService calls User::create', function () {
    // Testing internal implementation
});

// ✅ Test behavior instead
test('user can be created', function () {
    // Test expected outcome
});

// ❌ Don't share state between tests
class UserTest extends TestCase
{
    private $user;  // Bad: shared state

    public function test_something()
    {
        // Tests can affect each other
    }
}

// ✅ Use setUp or factory for each test
class UserTest extends TestCase
{
    protected function setUp(): void
    {
        parent::setUp();
        // Fresh state for each test
    }
}
```

## Running Tests

### Commands

```bash
# Run all tests
php artisan test

# Run PHPUnit
./vendor/bin/phpunit

# Run Pest
./vendor/bin/pest

# Run specific test
php artisan test --filter test_user_can_login

# Run with coverage
php artisan test --coverage

# Run in parallel
php artisan test --parallel
```

## Quick Reference

| Method | Description |
|--------|-------------|
| `actingAs()` | Authenticate as user |
| `assertStatus()` | Assert HTTP status |
| `assertJson()` | Assert JSON response |
| `assertDatabaseHas()` | Assert database has record |
| `assertDatabaseMissing()` | Assert database missing record |
| `Event::fake()` | Fake events |
| `Mail::fake()` | Fake mail |
| `Cache::shouldReceive()` | Mock cache |

## See Also

- **service-layer.md** - Testing services
- **eloquent-best-practices.md** - Testing models

---

**Reference**: Laravel 11.x Testing Documentation
