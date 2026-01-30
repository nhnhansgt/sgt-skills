# Views & Blade

> Blade templates, components, layouts, directives

## Overview

Blade is Laravel's powerful templating engine. It allows you to write clean templates with elegant syntax.

## Blade Files

### File Location

```
resources/views/
├── layouts/
│   └── app.blade.php
├── components/
│   ├── user-card.blade.php
│   └── alert.blade.php
├── users/
│   ├── index.blade.php
│   ├── show.blade.php
│   └── form.blade.php
└── welcome.blade.php
```

### File Naming

| Pattern | Example | Usage |
|---------|---------|-------|
| `kebab-case.blade.php` | `user-profile.blade.php` | `view('user-profile')` |
| Nested with dots | `users.profile.show` | `users/profile/show.blade.php` |

## Displaying Data

### Escaped Output (Default)

```blade
{{-- ✅ Good - Auto escaped --}}
{{ $user->name }}
{{ $user->email }}

{{-- Output: John Doe --}}
```

### Unescaped Output (Use Carefully!)

```blade
{{-- ⚠️ Only use when you trust the content --}}
{!! $htmlContent !!}

{{-- Example: Render HTML from trusted source --}}
{!! $post->body_html !!}
```

### Displaying Data with Defaults

```blade
{{-- ✅ Good - Null coalescing operator --}}
{{ $user->name ?? 'Guest' }}
{{ $user->profile->bio ?? 'No bio available' }}

{{-- ✅ Good - Or operator for falsy values --}}
{{ $user->settings->theme or 'default' }}
```

### JSON Encoding

```blade
{{-- ✅ Good - Pass data to JavaScript --}}
<script>
    const user = {{ Js::from($user) }};
    // Or
    const user = {{ Illuminate\Support\Js::from($user) }};
</script>
```

## Blade Directives

### @if, @elseif, @else, @endif

```blade
@if ($user->isActive())
    {{ $user->name }} is active
@elseif ($user->isPending())
    {{ $user->name }} is pending
@else
    {{ $user->name }} is inactive
@endif
```

### @unless, @endunless

```blade
@unless ($user->isAdmin())
    <p>You are not an admin</p>
@endunless
```

### @isset, @empty

```blade
@isset($user->profile)
    <p>{{ $user->profile->bio }}</p>
@endisset

@empty($user->posts)
    <p>No posts yet</p>
@endempty
```

### @auth, @guest, @endauth, @endguest

```blade
@auth
    <p>Welcome, {{ Auth::user()->name }}</p>
@endauth

@guest
    <p>Please <a href="{{ route('login') }}">login</a></p>
@endguest

@auth('admin')
    <p>Admin area</p>
@endauth
```

### @switch, @case, @break, @default, @endswitch

```blade
@switch($user->role)
    @case('admin')
        <p>Administrator</p>
        @break
    @case('moderator')
        <p>Moderator</p>
        @break
    @default
        <p>User</p>
@endswitch
```

### @for, @foreach, @break, @continue, $loop

```blade
@foreach ($users as $user)
    @if ($loop->first)
        <p>First user!</p>
    @endif

    @if ($loop->last)
        <p>Last user!</p>
    @endif

    <p>User {{ $loop->iteration }} of {{ $loop->count }}</p>
    <p>{{ $user->name }}</p>

    @continue
    @break
@endforeach

{{-- Nested loops --}}
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        <p>{{ $loop->parent->iteration }}.{{ $loop->iteration }}: {{ $post->title }}</p>
    @endforeach
@endforeach
```

### @while

```blade
@while ($item = array_shift($items))
    <p>{{ $item->name }}</p>
@endwhile
```

### @error

```blade
@error('email')
    <p class="text-red">{{ $message }}</p>
@enderror
```

## Layouts

### Basic Layout

```blade
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <title>@slot('title', 'App Name')</title>
</head>
<body>
    @yield('content')

    @slot('footer')
        <p>Default footer</p>
    @endslot
</body>
</html>
```

### Extending Layout

```blade
{{-- resources/views/users/show.blade.php --}}
@extends('layouts.app')

@section('title', 'User Profile')

@section('content')
    <h1>{{ $user->name }}</h1>
@endsection

@slot('footer')
    <p>Custom footer for user profile</p>
@endslot
```

### Multiple Yields

```blade
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    @yield('styles')
</head>
<body>
    @yield('header')
    @yield('content')
    @yield('footer')
    @yield('scripts')
</body>
</html>
```

## Components

### Anonymous Components

```blade
{{-- resources/views/components/user-card.blade.php --}}
@props(['user', 'size' => 'md'])

<div class="user-card user-card-{{ $size }}">
    <img src="{{ $user->avatar_url }}" alt="{{ $user->name }}">
    <h2>{{ $user->name }}</h2>
    <p>{{ $user->email }}</p>

    @isset($description)
        <p>{{ $description }}</p>
    @endisset
</div>
```

### Using Components

```blade
{{-- Basic usage --}}
<x-user-card :user="$user" />

{{-- With props --}}
<x-user-card :user="$user" size="lg" />

{{-- With slot --}}
<x-user-card :user="$user">
    <x-slot:description>
        <p>{{ $user->bio }}</p>
    </x-slot:description>
</x-user-card>

{{-- With attributes --}}
<x-user-card :user="$user" class="border rounded" />
```

### Class-Based Components

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use App\Models\User;

class UserCard extends Component
{
    public $user;
    public $size;

    public function __construct(User $user, string $size = 'md')
    {
        $this->user = $user;
        $this->size = $size;
    }

    public function render()
    {
        return view('components.user-card');
    }
}
```

```blade
{{-- resources/views/components/user-card.blade.php --}}
<div class="user-card user-card-{{ $size }}">
    <h2>{{ $user->name }}</h2>
</div>
```

### Inline Component Views

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    public function __construct(public string $type = 'info')
    {
    }

    public function render()
    {
        return <<<'BLADE'
            <div class="alert alert-{{ $type }}">
                {{ $slot }}
            </div>
            BLADE;
    }
}
```

## Including Subviews

### @include

```blade
{{-- resources/views/users/profile.blade.php --}}
<div class="profile">
    @include('users._header', ['title' => 'User Profile'])

    <p>{{ $user->bio }}</p>

    @include('users._footer')
</div>

{{-- resources/views/users/_header.blade.php --}}
<header>
    <h1>{{ $title }}</h1>
</header>
```

### @includeIf

```blade
@includeIf('partials.custom-header', ['title' => 'Welcome'])
```

### @includeWhen

```blade
@includeWhen($user->isAdmin(), 'partials.admin-nav')
```

### @includeFirst

```blade
@includeFirst(['partials.custom-nav', 'partials.default-nav'])
```

## Forms

### CSRF Field

```blade
<form method="POST" action="{{ route('login') }}">
    @csrf

    <input type="email" name="email" value="{{ old('email') }}">
    <input type="password" name="password">

    @error('email')
        <p class="error">{{ $message }}</p>
    @enderror

    <button type="submit">Login</button>
</form>
```

### Method Spoofing

```blade
<form action="{{ route('users.update', $user) }}" method="POST">
    @method('PUT')
    @csrf

    <input type="text" name="name" value="{{ $user->name }}">
    <button type="submit">Update</button>
</form>
```

## Directives Cheat Sheet

| Directive | Description |
|-----------|-------------|
| `@if` | Conditional |
| `@unless` | Negative conditional |
| `@isset` | Check if variable is set |
| `@empty` | Check if variable is empty |
| `@auth` | Check if user is authenticated |
| `@guest` | Check if user is guest |
| `@switch` | Switch statement |
| `@for` | For loop |
| `@foreach` | Foreach loop |
| `@while` | While loop |
| `@error` | Display validation errors |
| `@csrf` | CSRF token field |
| `@method` | HTTP method spoofing |
| `@yield` | Define section |
| `@section` | Fill section |
| `@extends` | Extend layout |
| `@include` | Include subview |
| `@verbatim` | Escape Blade directives |
| `@php` | Execute PHP code |

## Best Practices

### DO ✅

```blade
{{-- ✅ Use components over includes --}}
<x-user-card :user="$user" />

{{-- ✅ Use layouts --}}
@extends('layouts.app')

{{-- ✅ Use directives for logic --}}
@if ($user->isAdmin())
    <p>Admin</p>
@endif

{{-- ✅ Escape output (default) --}}
{{ $user->name }}

{{-- ✅ Use $loop variable --}}
@foreach ($users as $user)
    @if ($loop->first)
        <p>First!</p>
    @endif
@endforeach
```

### DON'T ❌

```blade
{{-- ❌ Don't put business logic in views --}}
@foreach ($users as $user)
    @if ($user->posts->count() > 5 && $user->isPremium())
        <p>Premium user with many posts</p>
    @endif
@endforeach

{{-- Instead, compute in controller/service --}}
{{-- $usersWithStats = $userService->getUsersWithPostCounts(); --}}
@foreach ($usersWithStats as $user)
    @if ($user->hasManyPosts())
        <p>{{ $user->name }} has many posts!</p>
    @endif
@endforeach

{{-- ❌ Don't use {!! !!} unless trusted --}}
{!! $userInput !!}

{{-- ❌ Don't write complex PHP in views --}}
@php
    $users = User::active()->get();
    $count = $users->count();
@endphp
```

## See Also

- **controller-best-practices.md** - Passing data to views
- **eloquent-best-practices.md** - Preparing data for views

---

**Reference**: Laravel 11.x Blade Documentation
