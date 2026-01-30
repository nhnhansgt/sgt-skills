# Form Request Validation

## Purpose

Separate validation logic from controllers. Reusable validation rules.

## Structure

```
app/Http/Requests/
└── StoreUserRequest.php
```

## Generate Request

```bash
php artisan make:request StoreUserRequest
```

## Basic Form Request

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // Or implement auth logic
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'unique:users,email'],
            'password' => ['required', 'string', 'min:8', 'confirmed'],
        ];
    }

    public function messages(): array
    {
        return [
            'email.required' => 'Email is required',
            'email.unique' => 'Email already exists',
        ];
    }
}
```

## Controller Usage

```php
public function store(StoreUserRequest $request)
{
    // Validation already done, access validated data
    $user = $this->userService->createUser($request->validated());
    return response()->json($user, 201);
}
```

## Update Request

```php
class UpdateUserRequest extends FormRequest
{
    public function rules(): array
    {
        $userId = $this->route('user')->id;

        return [
            'email' => ['required', 'email', "unique:users,email,{$userId}"],
            // Ignore current user's email
        ];
    }
}
```

## Custom Validation

```php
public function withValidator($validator)
{
    $validator->after(function ($validator) {
        if ($this->get('password') === 'password') {
            $validator->errors()->add('password', 'Password too common');
        }
    });
}
```

## Prepare for Validation

```php
protected function prepareForValidation()
{
    $this->merge([
        'slug' => Str::slug($this->title),
    ]);
}
```

## Rules

1. **Return arrays** - Use `['rule1', 'rule2']` syntax
2. **Use specific error messages** - Override `messages()` method
3. **Authorize properly** - Implement auth logic in `authorize()`
4. **Keep rules focused** - One request per action (Store/Update)

---

**See also:** `service-layer.md`, `controller-best-practices.md`
