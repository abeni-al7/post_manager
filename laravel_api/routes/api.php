<?php

use App\Http\Controllers\Api\PostController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where registered API routes are for this application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group.
|
*/

Route::get('/categories', [PostController::class, 'categories']);

Route::prefix('posts')->name('posts.')->group(function () {
    Route::get('/', [PostController::class, 'index'])->name('index');
    Route::get('{id}', [PostController::class, 'show'])->name('show');
    Route::get('{id}/images', [PostController::class, 'images'])->name('images');
});
