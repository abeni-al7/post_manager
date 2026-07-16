<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->string('title', 500);
            $table->text('subtitle')->nullable();
            $table->string('author', 255)->nullable();
            $table->longText('content');
            $table->string('category', 100)->nullable();
            $table->string('source_file', 500)->unique();
            $table->string('volume', 50)->nullable();
            $table->string('issue_number', 50)->nullable();
            $table->date('published_date')->nullable();
            $table->string('content_hash', 64)->unique();
            $table->unsignedInteger('word_count')->default(0);
            $table->timestamps();

            $table->index('category');
            $table->index('author');

            // Fulltext index is only supported on MySQL/MariaDB, not on SQLite
            if (DB::connection()->getDriverName() !== 'sqlite') {
                $table->fullText(['title', 'content'], 'posts_title_content_fulltext');
            }
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};