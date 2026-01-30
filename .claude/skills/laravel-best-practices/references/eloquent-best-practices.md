# Eloquent Best Practices

## Fat Models, Skinny Controllers

Models handle data logic. Controllers handle HTTP logic.

## Model Scopes

Reuse query logic.

```php
// User.php
class User extends Model
{
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopeByEmail($query, string $email)
    {
        return $query->where('email', $email);
    }
}

// Usage
$activeUsers = User::active()->get();
$user = User::active()->byEmail('user@example.com')->first();
```

## Accessors & Mutators

Transform attributes when getting/setting.

```php
class User extends Model
{
    protected $casts = [
        'is_admin' => 'boolean',
    ];

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
}

// Usage
$user->full_name; // Accessor
$user->password = 'secret'; // Hashed automatically
```

## Relationships

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

    // Eager loading
    public function getWithPosts()
    {
        return $this->with('posts')->get();
    }
}
```

## Mass Assignment

```php
protected $fillable = ['name', 'email', 'password'];

// Or use $guarded
protected $guarded = ['id', 'is_admin'];
```

## Query Building

```php
// ❌ Bad
User::where('active', 1)->get();

// ✅ Good
User::active()->get();

// ❌ Bad
Post::with('user.comments')->get();

// ✅ Good
Post::with(['user:id,name', 'comments:id,user_id'])->get();
```

## Casting

```php
protected $casts = [
    'email_verified_at' => 'datetime',
    'is_active' => 'boolean',
    'metadata' => 'array',
    'amount' => 'decimal:2',
];
```

## Events

```php
protected static function booted()
{
    static::creating(function ($user) {
        $user->slug = Str::slug($user->name);
    });

    static::created(function ($user) {
        Mail::to($user)->send(new WelcomeMail());
    });
}
```

## Rules

1. **Use scopes** for reusable queries
2. **Use casting** for type conversion
3. **Use relationships** instead of manual joins
4. **Eager load** to prevent N+1 queries
5. **Keep queries in models** - Move complex queries to scopes

---

**See also:** `service-layer.md`, `controller-best-practices.md`
