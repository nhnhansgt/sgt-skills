# Events & Listeners

> Event-driven architecture with events, listeners, observers

## Overview

Laravel events provide a simple observer pattern implementation, allowing you to subscribe and listen for events in your application.

## When to Use Events

| Use Case | Example |
|----------|---------|
| **Decoupling** | User registered → Send email, create profile |
| **Side effects** | Order placed → Update inventory, notify admin |
| **Async processing** | File uploaded → Process in background |
| **Auditing** | Model changed → Log changes |
| **Notifications** | Post created → Notify followers |

## Creating Events

### Artisan Command

```bash
php artisan make:event UserRegistered
```

### Event Class

```php
<?php

namespace App\Events;

use App\Models\User;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class UserRegistered
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(
        public User $user
    ) {}
}
```

## Creating Listeners

### Artisan Command

```bash
php artisan make:listener SendWelcomeEmail --event=UserRegistered
```

### Listener Class

```php
<?php

namespace App\Listeners;

use App\Events\UserRegistered;
use App\Mail\WelcomeEmail;
use Illuminate\Support\Facades\Mail;

class SendWelcomeEmail
{
    public function handle(UserRegistered $event): void
    {
        Mail::to($event->user->email)->send(new WelcomeEmail($event->user));
    }
}
```

### Queued Listeners

```php
// ✅ Good - Queue listener for async processing
class SendWelcomeEmail implements ShouldQueue
{
    use InteractsWithQueue;

    public function handle(UserRegistered $event): void
    {
        Mail::to($event->user->email)->send(new WelcomeEmail($event->user));
    }

    public function failed(UserRegistered $event, Throwable $exception): void
    {
        Log::error('Failed to send welcome email', [
            'user_id' => $event->user->id,
            'error' => $exception->getMessage(),
        ]);
    }
}
```

## Registering Events

### EventServiceProvider

```php
<?php

namespace App\Providers;

use App\Events\UserRegistered;
use App\Events\PostCreated;
use App\Listeners\SendWelcomeEmail;
use App\Listeners\CreateUserProfile;
use App\Listeners\NotifyFollowers;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    protected $listen = [
        UserRegistered::class => [
            SendWelcomeEmail::class,
            CreateUserProfile::class,
        ],
        PostCreated::class => [
            NotifyFollowers::class,
        ],
    ];

    public function boot(): void
    {
        parent::boot();

        // ✅ Good - Register events programmatically
        Event::listen(OrderCreated::class, [UpdateInventory::class, 'handle']);
    }
}
```

## Dispatching Events

### In Controllers/Services

```php
use App\Events\UserRegistered;
use Illuminate\Support\Facades\Event;

// ✅ Good - Dispatch event
public function register(RegisterRequest $request): JsonResponse
{
    $user = User::create($request->validated());

    UserRegistered::dispatch($user);

    // Or
    event(new UserRegistered($user));

    return response()->json($user, 201);
}
```

### Event Payload

```php
// ✅ Good - Multiple parameters
class OrderPlaced
{
    public function __construct(
        public Order $order,
        public array $items,
        public string $paymentMethod
    ) {}
}

// ✅ Good - Complex data
class ReportGenerated
{
    public function __construct(
        public Report $report,
        public Collection $data,
        public string $format
    ) {}
}
```

## Model Observers

### Creating Observer

```bash
php artisan make:observer UserObserver --model=User
```

### Observer Class

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Support\Facades\Log;

class UserObserver
{
    /**
     * Handle the User "created" event.
     */
    public function created(User $user): void
    {
        Log::info("User created: {$user->id}");

        // Create user profile
        $user->profile()->create([
            'bio' => 'New user',
        ]);
    }

    /**
     * Handle the User "updated" event.
     */
    public function updated(User $user): void
    {
        Log::info("User updated: {$user->id}");
    }

    /**
     * Handle the User "deleted" event.
     */
    public function deleted(User $user): void
    {
        Log::info("User deleted: {$user->id}");
    }

    /**
     * Handle the User "restored" event.
     */
    public function restored(User $user): void
    {
        Log::info("User restored: {$user->id}");
    }

    /**
     * Handle the User "forceDeleted" event.
     */
    public function forceDeleted(User $user): void
    {
        Log::info("User force deleted: {$user->id}");
    }
}
```

### Registering Observer

```php
// AppServiceProvider.php
use App\Models\User;
use App\Observers\UserObserver;

public function boot(): void
{
    User::observe(UserObserver::class);
}
```

## Event Listeners vs Observers

| Feature | Event Listeners | Observers |
|---------|----------------|-----------|
| **Scope** | Application-wide | Model-specific |
| **Coupling** | Decoupled | Tight to model |
| **Use case** | Business events | Model lifecycle |

```php
// ✅ Good - Use events for business logic
UserRegistered::dispatch($user);

// ✅ Good - Use observers for model lifecycle
class UserObserver
{
    public function creating(User $user): void
    {
        $user->slug = Str::slug($user->name);
    }
}
```

## Advanced Patterns

### Event Subscribers

```php
<?php

namespace App\Listeners;

class UserEventSubscriber
{
    public function handleUserRegistered($event): void
    {
        // Handle user registration
    }

    public function handleUserLogin($event): void
    {
        // Handle user login
    }

    public function subscribe($events): array
    {
        return [
            UserRegistered::class => 'handleUserRegistered',
            UserLogin::class => 'handleUserLogin',
        ];
    }
}
```

```php
// EventServiceProvider.php
protected $subscribe = [
    UserEventSubscriber::class,
];
```

### Conditional Listeners

```php
// ✅ Good - Stop propagation
class SendWelcomeEmail
{
    public function handle(UserRegistered $event): void
    {
        if ($event->user->skip_welcome_email) {
            return false;  // Stop propagation
        }

        Mail::to($event->user->email)->send(new WelcomeEmail($event->user));
    }
}
```

### Event Horizons

```bash
composer require laravel/horizon
```

```php
// ✅ Good - Monitor events
// EventSubscriber.php
class EventSubscriber
{
    public function subscribe($events): void
    {
        $events->listen('*', function ($eventName, array $data) {
            foreach ($data as $event) {
                if ($event instanceof ShouldBroadcast) {
                    // Track broadcast events
                }
            }
        });
    }
}
```

## Broadcasting Events

### Broadcast Event

```php
<?php

namespace App\Events;

use App\Models\Post;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;

class PostCreated implements ShouldBroadcast
{
    use InteractsWithSockets;

    public function __construct(
        public Post $post
    ) {}

    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('posts'),
        ];
    }

    public function broadcastWith(): array
    {
        return [
            'id' => $this->post->id,
            'title' => $this->post->title,
            'user' => $this->post->user->name,
        ];
    }
}
```

### Channels

```php
// routes/channels.php
use Illuminate\Support\Facades\Broadcast;

Broadcast::channel('posts', function ($user) {
    return $user->can('view-posts');
});
```

## Service Layer Pattern

```php
// ✅ Good - Dispatch events in services
class UserService
{
    public function createUser(array $data): User
    {
        return DB::transaction(function () use ($data) {
            $user = User::create($data);

            // Dispatch event
            UserRegistered::dispatch($user);

            return $user;
        });
    }

    public function deleteUser(int $id): bool
    {
        $user = User::findOrFail($id);
        $result = $user->delete();

        if ($result) {
            UserDeleted::dispatch($user);
        }

        return $result;
    }
}
```

## Testing Events

### Fake Events

```php
use Illuminate\Support\Facades\Event;

// ✅ Good - Fake events in tests
public function test_user_registration_dispatches_event()
{
    Event::fake([UserRegistered::class]);

    $this->post('/register', [
        'name' => 'John',
        'email' => 'john@example.com',
        'password' => 'password',
    ]);

    Event::assertDispatched(UserRegistered::class, function ($event) {
        return $event->user->email === 'john@example.com';
    });

    Event::assertDispatchedTimes(UserRegistered::class, 1);
}

// ✅ Good - Assert listener called
Event::assertListening(UserRegistered::class, SendWelcomeEmail::class);
```

### Without Faking

```php
public function test_event_listener_is_called()
{
    Mail::fake();

    $user = User::factory()->create();
    UserRegistered::dispatch($user);

    Mail::assertSent(WelcomeEmail::class, function ($mail) use ($user) {
        return $mail->hasTo($user->email);
    });
}
```

## Best Practices

### DO ✅

```php
// ✅ Use events for side effects
UserRegistered::dispatch($user);

// ✅ Queue listeners for slow operations
class SendWelcomeEmail implements ShouldQueue
{
    //
}

// ✅ Use observers for model lifecycle
class UserObserver
{
    public function creating(User $user): void
    {
        $user->slug = Str::slug($user->name);
    }
}

// ✅ Use typed properties
class UserRegistered
{
    public function __construct(
        public User $user
    ) {}
}
```

### DON'T ❌

```php
// ❌ Don't dispatch events for simple operations
$user->name = 'John';
$user->save();
UserNameUpdated::dispatch($user);  // Unnecessary

// ❌ Don't put business logic in listeners
class SendWelcomeEmail
{
    public function handle(UserRegistered $event): void
    {
        // Don't do this
        $event->user->profile()->create([...]);
    }
}

// ✅ Put logic in services or observers
class UserObserver
{
    public function created(User $user): void
    {
        $user->profile()->create([...]);
    }
}
```

## Quick Reference

| Method | Description |
|--------|-------------|
| `Event::dispatch()` | Dispatch event |
| `event()` | Dispatch event (helper) |
| `Event::fake()` | Fake events in tests |
| `Event::assertDispatched()` | Assert event was dispatched |
| `Event::assertListening()` | Assert listener exists |
| `ShouldQueue` | Queue listener interface |
| `ShouldBroadcast` | Broadcast event interface |

## See Also

- **service-layer.md** - Service layer with events
- **eloquent-best-practices.md** - Model observers

---

**Reference**: Laravel 11.x Events Documentation
