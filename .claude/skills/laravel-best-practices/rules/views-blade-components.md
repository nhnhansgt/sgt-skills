---
title: Blade Components over Includes
impact: MEDIUM
impactDescription: Better component reusability and data isolation
tags: views, blade, components, templates, layouts
---

## Blade Components over Includes

Use Blade components instead of includes for better reusability, data isolation, and cleaner syntax.

**Incorrect (Using @include):**

```blade
{{-- resources/views/users/_card.blade.php --}}
<div class="user-card">
    <h2>{{ $name }}</h2>
    <p>{{ $email }}</p>
</div>

{{-- Usage --}}
@include('users._card', ['name' => $user->name, 'email' => $user->email])
```

**Correct (Using component):**

```blade
{{-- resources/views/components/user-card.blade.php --}}
@props(['user', 'size' => 'md'])

<div class="user-card user-card-{{ $size }}">
    <h2>{{ $user->name }}</h2>
    <p>{{ $user->email }}</p>
</div>

{{-- Usage --}}
<x-user-card :user="$user" size="lg" />
```

## Component Attributes

**Correct (Attribute merging):**

```blade
{{-- Component --}}
@props(['user'])

<div {{ $attributes }}>
    <h2>{{ $user->name }}</h2>
</div>

{{-- Usage --}}
<x-user-card :user="$user" class="border rounded" id="user-1" />
{{-- Renders: <div class="user-card border rounded" id="user-1"> --}}
```

## Component Slots

**Correct (Named slots for flexibility):**

```blade
{{-- resources/views/components/modal.blade.php --}}
@props(['title' => 'Default Title'])

<div class="modal">
    <div class="modal-header">
        <h2>{{ $title }}</h2>
    </div>

    <div class="modal-body">
        {{ $slot }}
    </div>

    @if(isset($footer))
        <div class="modal-footer">
            {{ $footer }}
        </div>
    @endif
</div>

{{-- Usage --}}
<x-modal title="Delete User">
    <p>Are you sure you want to delete this user?</p>

    <x-slot:footer>
        <button>Cancel</button>
        <button class="danger">Delete</button>
    </x-slot:footer>
</x-modal>
```

## Inline Components

**Correct (Simple components without view file):**

```php
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

## Layouts

**Incorrect (Repeated HTML):**

```blade
{{-- Every file repeats header/footer --}}
<!DOCTYPE html>
<html>
<head><title>Page 1</title></head>
<body>@yield('content')</body>
</html>
```

**Correct (Use layouts):**

```blade
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <title>@slot('title', 'App')</title>
    @stack('styles')
</head>
<body>
    @yield('content')
    @stack('scripts')
</body>
</html>

{{-- resources/views/users/show.blade.php --}}
@extends('layouts.app')

@section('title', 'User Profile')

@push('styles')
    <link rel="stylesheet" href="/css/user.css">
@endpush

@section('content')
    <h1>{{ $user->name }}</h1>
@endsection
```

## Directives Best Practices

**Correct (Use Blade directives):**

```blade
@auth
    <p>Welcome, {{ Auth::user()->name }}</p>
@endauth

@isset($user->profile)
    <p>{{ $user->profile->bio }}</p>
@endisset

@error('email')
    <p class="error">{{ $message }}</p>
@enderror

@foreach ($users as $user)
    @if ($loop->first)
        <p>First user!</p>
    @endif
    <p>{{ $loop->iteration }}: {{ $user->name }}</p>
@endforeach
```

## Security: XSS Prevention

**Incorrect (Unescaped output):**

```blade
{!! $userInput !!}  <!-- XSS vulnerability! -->
```

**Correct (Auto-escaped output):**

```blade
{{ $userInput }}  <!-- Safe -->

{{-- Only use {!! !!} for trusted HTML --}}
{!! $post->body_html !!}
```

Reference: [Laravel Blade Documentation](https://laravel.com/docs/blade)
