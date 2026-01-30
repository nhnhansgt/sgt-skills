---
title: Fat Models with Scopes and Relationships
impact: HIGH
impactDescription: Better code organization and reusability
tags: data, eloquent, models, scopes, relationships, fat-models
---

## Fat Models with Scopes and Relationships

Models should handle data logic, scopes, accessors, mutators, and relationships. Keep database logic out of controllers.

**Incorrect (Query logic in controller):**

```php
// Controller
public function getActiveUsers()
{
    return User::where('is_active', true)
        ->where('email_verified_at', '!=', null)
        ->orderBy('created_at', 'desc')
        ->get();
}
```

**Correct (Scopes in model):**

```php
// Model
class User extends Model
{
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopeVerified($query)
    {
        return $query->whereNotNull('email_verified_at');
    }
}

// Controller
public function getActiveUsers()
{
    return User::active()->verified()->latest()->get();
}
```

## Model Scopes

**Incorrect (Repeated query logic):**

```php
User::where('is_active', true)->get();
User::where('is_active', true)->with('posts')->get();
User::where('is_active', true)->paginate(15);
```

**Correct (Reusable scope):**

```php
// Model
public function scopeActive($query)
{
    return $query->where('is_active', true);
}

// Usage
User::active()->get();
User::active()->with('posts')->get();
User::active()->paginate(15);
```

## Dynamic Scopes

**Correct (Parameters in scopes):**

```php
// Model
public function scopeByEmail($query, string $email)
{
    return $query->where('email', $email);
}

public function scopeOfType($query, string $type)
{
    return $query->where('type', $type);
}

// Usage
$user = User::active()->byEmail('user@example.com')->first();
$admins = User::ofType('admin')->get();
```

## Accessors and Mutators

**Incorrect (Logic in controller/view):**

```php
// In controller or view
$fullName = $user->first_name . ' ' . $user->last_name;
$user->password = bcrypt($newPassword);
```

**Correct (Accessors/Mutators in model):**

```php
// Model
class User extends Model
{
    // Accessor
    public function getFullNameAttribute(): string
    {
        return "{$this->first_name} {$this->last_name}";
    }

    // Mutator
    public function setPasswordAttribute(string $value): void
    {
        $this->attributes['password'] = bcrypt($value);
    }

    protected $casts = [
        'is_admin' => 'boolean',
        'email_verified_at' => 'datetime',
    ];
}

// Usage
$user->full_name;  // Accessor
$user->password = 'secret';  // Auto-hashed by mutator
```

## Relationships

**Correct (Define relationships in model):**

```php
class User extends Model
{
    // One-to-many
    public function posts()
    {
        return $this->hasMany(Post::class);
    }

    // Many-to-many
    public function roles()
    {
        return $this->belongsToMany(Role::class)->withTimestamps();
    }

    // Has one
    public function profile()
    {
        return $this->hasOne(Profile::class);
    }

    // Inverse relationship
    public function country()
    {
        return $this->belongsTo(Country::class);
    }
}
```

## Model Events

**Correct (Use model events):**

```php
protected static function booted()
{
    static::creating(function ($user) {
        $user->slug = Str::slug($user->name);
    });

    static::created(function ($user) {
        Mail::to($user)->send(new WelcomeMail($user));
    });
}
```

## Mass Assignment Protection

**Correct (Use fillable or guarded):**

```php
class User extends Model
{
    // Allow specific fields
    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    // OR block specific fields
    protected $guarded = [
        'id',
        'is_admin',
    ];
}
```

Reference: [Laravel Eloquent Documentation](https://laravel.com/docs/eloquent)
