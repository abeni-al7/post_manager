<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\PostIndexRequest;
use App\Http\Resources\PostImageResource;
use App\Http\Resources\PostResource;
use App\Models\Post;

class PostController extends Controller
{
    /**
     * Display a paginated, filterable, searchable listing of posts.
     */
    public function index(PostIndexRequest $request)
    {
        $perPage = $request->integer('per_page', 15);
        $sortField = $request->input('sort', 'created_at');
        $sortDirection = $request->input('direction', 'desc');

        $query = Post::query()->with('images');

        // Filter by category
        if ($request->filled('category')) {
            $query->byCategory($request->input('category'));
        }

        // Search by title, content, or author
        if ($request->filled('search')) {
            $query->search($request->input('search'));
        }

        // Sorting
        $allowedSortFields = ['title', 'published_date', 'created_at', 'author', 'word_count'];
        if (in_array($sortField, $allowedSortFields)) {
            $query->orderBy($sortField, $sortDirection === 'asc' ? 'asc' : 'desc');
        }

        $posts = $query->paginate($perPage);

        return PostResource::collection($posts);
    }

    /**
     * Display the specified post with its images.
     */
    public function show(string $id)
    {
        $post = Post::with('images')->findOrFail($id);

        return new PostResource($post);
    }

    /**
     * Display the images for a specific post.
     */
    public function images(string $id)
    {
        $post = Post::with('images')->findOrFail($id);

        return PostImageResource::collection($post->images);
    }

    /**
     * Display a list of distinct categories.
     */
    public function categories()
    {
        $categories = Post::select('category')
            ->whereNotNull('category')
            ->distinct()
            ->orderBy('category')
            ->pluck('category');

        return response()->json([
            'data' => $categories,
        ]);
    }
}