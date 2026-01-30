# Pagination

> Paginate results for Blade and API endpoints

## Overview

Laravel pagination helps split large datasets into manageable chunks.

## Basic Pagination

### paginate() Method

```php
// ✅ Good - Simple pagination
$users = User::paginate(15);

// Returns: LengthAwarePaginator
// Properties: $users->items(), $users->total(), $users->currentPage()
```

### Passing to Blade

```blade
{{-- resources/views/users/index.blade.php --}}
@foreach ($users as $user)
    <p>{{ $user->name }}</p>
@endforeach

{{ $users->links() }}
{{ $users->appends(['sort' => 'name'])->links() }}
```

## Pagination Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `paginate($perPage)` | Full pagination with total count | `LengthAwarePaginator` |
| `simplePaginate($perPage)` | Pagination without total count | `Paginator` |
| `cursorPaginate($perPage)` | Cursor-based pagination | `CursorPaginator` |

### Full Pagination (LengthAwarePaginator)

```php
// ✅ Good - When you need to show total items
$users = User::orderBy('created_at', 'desc')->paginate(15);

// In blade: "Showing 1-15 of 150 users"
{{ $users->total() }} total
{{ $users->perPage() }} per page
{{ $users->currentPage() }}
{{ $users->lastPage() }}
```

### Simple Pagination

```php
// ✅ Good - Better performance for large datasets
$users = User::orderBy('created_at', 'desc')->simplePaginate(15);

// No total() method
// Faster: Doesn't count all records
```

### Cursor Pagination

```php
// ✅ Good - Infinite scroll, very large datasets
$users = User::orderBy('id')->cursorPaginate(15);

// More efficient for large datasets
// Works well with infinite scroll
```

## Customizing Pagination

### Per Page

```php
// Dynamic per page
$perPage = request()->input('per_page', 15);
$users = User::paginate($perPage);

// Query string: ?per_page=50
```

### Columns

```php
// ✅ Good - Select specific columns
$users = User::paginate(15, ['id', 'name', 'email']);
```

### Path

```php
// ✅ Good - Custom URL path
$users = User::paginate(15);
$users->withPath('/admin/users');
```

### Appending Query Parameters

```php
// ✅ Good - Preserve query parameters
$users = User::paginate(15);
$users->appends(['sort' => 'name', 'order' => 'asc']);

// Or preserve all except page
$users->appends(request()->except('page'));
```

### Fragment

```blade
{{-- ✅ Good - Add fragment to pagination links --}}
{{ $users->fragment('comments')->links() }}

<!-- Generates: /users?page=2#comments -->
```

## Eloquent Relationships

### Paginate Relationships

```php
// ✅ Good - Paginate related models
$user = User::find(1);
$posts = $user->posts()->paginate(15);

// In blade
@foreach ($posts as $post)
    <p>{{ $post->title }}</p>
@endforeach

{{ $posts->links() }}
```

### Eager Loading with Pagination

```php
// ✅ Good - Eager load paginated relationships
$users = User::with(['posts' => function ($query) {
    $query->paginate(15);
}])->paginate(15);
```

## Service Layer Pattern

```php
// ✅ Good - Encapsulate pagination logic
class UserService
{
    public function getPaginatedUsers(int $perPage = 15, array $filters = []): LengthAwarePaginator
    {
        $query = User::query();

        // Apply filters
        if (isset($filters['search'])) {
            $query->where('name', 'like', "%{$filters['search']}%");
        }

        if (isset($filters['status'])) {
            $query->where('status', $filters['status']);
        }

        return $query->orderBy('created_at', 'desc')
            ->paginate($perPage)
            ->appends($filters);
    }
}
```

## API Pagination

### JSON Response

```php
// ✅ Good - Return paginator as JSON
public function index(Request $request): JsonResponse
{
    $users = User::paginate($request->input('per_page', 15));

    return response()->json($users);
}

// Response structure:
// {
//   "current_page": 1,
//   "data": [...],
//   "first_page_url": "...",
//   "from": 1,
//   "last_page": 10,
//   "last_page_url": "...",
//   "links": [...],
//   "next_page_url": "...",
//   "path": "...",
//   "per_page": 15,
//   "prev_page_url": null,
//   "to": 15,
//   "total": 150
// }
```

### API Resource with Pagination

```php
// ✅ Good - Use API Resources
public function index(Request $request): UserCollection
{
    $users = User::paginate($request->input('per_page', 15));

    return new UserCollection($users);
}

// UserCollection.php
class UserCollection extends ResourceCollection
{
    public function toArray($request)
    {
        return [
            'data' => $this->collection,
            'pagination' => [
                'total' => $this->total(),
                'count' => $this->count(),
                'per_page' => $this->perPage(),
                'current_page' => $this->currentPage(),
                'total_pages' => $this->lastPage(),
            ],
            'links' => [
                'next' => $this->nextPageUrl(),
                'prev' => $this->previousPageUrl(),
            ],
        ];
    }
}
```

## Custom Presenters

### Bootstrap 5

```php
// AppServiceProvider.php
use Illuminate\Pagination\Paginator;

public function boot()
{
    Paginator::useBootstrapFive();
}
```

### Tailwind CSS

```php
// AppServiceProvider.php
Paginator::useTailwind();
```

### Custom View

```blade
{{-- resources/views/pagination/custom.blade.php --}}
@if ($paginator->hasPages())
    <nav>
        <ul class="pagination">
            @if ($paginator->onFirstPage())
                <li class="disabled"><span>Previous</span></li>
            @else
                <li><a href="{{ $paginator->previousPageUrl() }}">Previous</a></li>
            @endif

            @foreach ($elements as $element)
                @if (is_string($element))
                    <li class="disabled"><span>{{ $element }}</span></li>
                @endif

                @if (is_array($element))
                    @foreach ($element as $page => $url)
                        @if ($page == $paginator->currentPage())
                            <li class="active"><span>{{ $page }}</span></li>
                        @else
                            <li><a href="{{ $url }}">{{ $page }}</a></li>
                        @endif
                    @endforeach
                @endif
            @endforeach

            @if ($paginator->hasMorePages())
                <li><a href="{{ $paginator->nextPageUrl() }}">Next</a></li>
            @else
                <li class="disabled"><span>Next</span></li>
            @endif
        </ul>
    </nav>
@endif
```

```php
// Usage
$users->links('pagination.custom');
```

## Infinite Scroll

### Cursor Pagination for Infinite Scroll

```php
// Service
public function getPostsCursor(?string $cursor = null, int $limit = 15): CursorPaginator
{
    return Post::orderBy('created_at', 'desc')
        ->cursorPaginate($limit, ['*'], 'cursor', $cursor);
}

// Controller
public function index(Request $request): JsonResponse
{
    $posts = $this->postService->getPostsCursor(
        $request->input('cursor'),
        $request->input('limit', 15)
    );

    return response()->json($posts);
}

// Response:
// {
//   "data": [...],
//   "next_cursor": "...",
//   "prev_cursor": null,
//   "per_page": 15
// }
```

### JavaScript Example

```javascript
// Fetch next page
async function loadMore() {
    const response = await fetch(`/api/posts?cursor=${nextCursor}`);
    const data = await response.json();

    posts.push(...data.data);
    nextCursor = data.next_cursor;
}
```

## Conditional Pagination

### Disable Pagination

```php
// ✅ Good - Allow disabling pagination
$perPage = request()->input('paginate', true);
$perPage = $perPage === true ? 15 : null;

if ($perPage) {
    $users = User::paginate($perPage);
} else {
    $users = User::all();
}
```

### Search with Pagination

```php
// ✅ Good - Preserve search parameters
$users = User::where('name', 'like', '%' . request()->input('search') . '%')
    ->paginate(15);

$users->appends(['search' => request()->input('search')]);
```

## Performance Tips

### Avoid count(*) on large tables

```php
// ❌ Bad - Slow on large tables
$users = User::paginate(15);  // Runs COUNT(*)

// ✅ Good - Use simplePaginate
$users = User::simplePaginate(15);  // No COUNT(*)

// ✅ Good - Use cursorPaginate for very large datasets
$users = User::cursorPaginate(15);
```

### Cache pagination counts

```php
// ✅ Good - Cache total count
$cacheKey = 'users_count';
$total = Cache::remember($cacheKey, 3600, function () {
    return User::count();
});

$users = User::paginate(15);
$users->total = $total;
```

## Quick Reference

| Method | Description |
|--------|-------------|
| `$users->total()` | Total items (LengthAware only) |
| `$users->count()` | Items on current page |
| `$users->perPage()` | Items per page |
| `$users->currentPage()` | Current page number |
| `$users->lastPage()` | Last page number |
| `$users->hasPages()` | Has multiple pages |
| `$users->hasMorePages()` | Has pages after current |
| `$users->nextPageUrl()` | URL for next page |
| `$users->previousPageUrl()` | URL for previous page |
| `$users->getUrlRange($start, $end)` | URLs for page range |
| `$users->links()` | Pagination HTML |
| `$users->appends($key, $value)` | Append query params |

## See Also

- **eloquent-best-practices.md** - Query building
- **api-resources.md** - Transform paginated results
- **EAGER-LOADING.md** - Eager loading with pagination

---

**Reference**: Laravel 11.x Pagination Documentation
