<?php

namespace Tests\Feature;

use App\Models\Post;
use App\Models\PostImage;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class PostApiTest extends TestCase
{
    use RefreshDatabase;

    // -----------------------------------------------------------------------
    //  GET /api/categories
    // -----------------------------------------------------------------------

    public function test_categories_returns_empty_array_when_no_posts_exist(): void
    {
        $response = $this->getJson('/api/categories');

        $response->assertOk();
        $response->assertJson(['data' => []]);
    }

    public function test_categories_returns_distinct_sorted_categories(): void
    {
        Post::create([
            'title' => 'Post A',
            'content' => 'Content A',
            'category' => 'Politics',
            'source_file' => 'a.html',
            'content_hash' => hash('sha256', 'a'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Post B',
            'content' => 'Content B',
            'category' => 'Business',
            'source_file' => 'b.html',
            'content_hash' => hash('sha256', 'b'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Post C',
            'content' => 'Content C',
            'category' => 'Politics',
            'source_file' => 'c.html',
            'content_hash' => hash('sha256', 'c'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Post D',
            'content' => 'Content D',
            'category' => 'Sport',
            'source_file' => 'd.html',
            'content_hash' => hash('sha256', 'd'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/categories');

        $response->assertOk();
        // Sorted: Business, Politics, Sport
        $response->assertJson(['data' => ['Business', 'Politics', 'Sport']]);
    }

    public function test_categories_excludes_null_categories(): void
    {
        Post::create([
            'title' => 'With Category',
            'content' => 'Content',
            'category' => 'News',
            'source_file' => 'with.html',
            'content_hash' => hash('sha256', 'with'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Without Category',
            'content' => 'Content',
            'category' => null,
            'source_file' => 'without.html',
            'content_hash' => hash('sha256', 'without'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/categories');

        $response->assertOk();
        $response->assertJson(['data' => ['News']]);
    }

    // -----------------------------------------------------------------------
    //  GET /api/posts  —  Basic & pagination
    // -----------------------------------------------------------------------

    public function test_posts_index_returns_empty_paginated_response_when_no_posts(): void
    {
        $response = $this->getJson('/api/posts');

        $response->assertOk();
        $response->assertJsonStructure([
            'data',
            'links',
            'meta' => ['current_page', 'from', 'last_page', 'per_page', 'to', 'total'],
        ]);
        $this->assertCount(0, $response->json('data'));
        $this->assertEquals(0, $response->json('meta.total'));
    }

    public function test_posts_index_default_pagination_is_15_per_page(): void
    {
        // Create 20 posts
        for ($i = 1; $i <= 20; $i++) {
            Post::create([
                'title' => "Post {$i}",
                'content' => "Content {$i}",
                'source_file' => "post-{$i}.html",
                'content_hash' => hash('sha256', (string) $i),
                'word_count' => 100,
            ]);
        }

        $response = $this->getJson('/api/posts');

        $response->assertOk();
        $this->assertEquals(15, $response->json('meta.per_page'));
        $this->assertEquals(20, $response->json('meta.total'));
        $this->assertEquals(2, $response->json('meta.last_page'));
        $this->assertCount(15, $response->json('data'));
    }

    public function test_posts_index_custom_per_page(): void
    {
        for ($i = 1; $i <= 10; $i++) {
            Post::create([
                'title' => "Post {$i}",
                'content' => "Content {$i}",
                'source_file' => "post-{$i}.html",
                'content_hash' => hash('sha256', "perpage-{$i}"),
                'word_count' => 100,
            ]);
        }

        $response = $this->getJson('/api/posts?per_page=5');

        $response->assertOk();
        $this->assertEquals(5, $response->json('meta.per_page'));
        $this->assertCount(5, $response->json('data'));
    }

    public function test_posts_index_per_page_100_is_accepted(): void
    {
        for ($i = 1; $i <= 120; $i++) {
            Post::create([
                'title' => "Post {$i}",
                'content' => "Content {$i}",
                'source_file' => "load-{$i}.html",
                'content_hash' => hash('sha256', "load-{$i}"),
                'word_count' => 100,
            ]);
        }

        $response = $this->getJson('/api/posts?per_page=100');

        $response->assertOk();
        $this->assertEquals(100, $response->json('meta.per_page'));
        $this->assertCount(100, $response->json('data'));
    }

    public function test_posts_index_per_page_zero_returns_validation_error(): void
    {
        $response = $this->getJson('/api/posts?per_page=0');

        $response->assertStatus(422);
        $response->assertJsonValidationErrors(['per_page']);
    }

    public function test_posts_index_per_page_exceeding_max_returns_validation_error(): void
    {
        $response = $this->getJson('/api/posts?per_page=101');

        $response->assertStatus(422);
        $response->assertJsonValidationErrors(['per_page']);
    }

    public function test_posts_index_second_page_returns_correct_items(): void
    {
        // Create posts with zero-padded titles for deterministic string sorting
        for ($i = 1; $i <= 25; $i++) {
            Post::create([
                'title' => sprintf("Post %02d", $i),
                'content' => "Content {$i}",
                'source_file' => "paging-{$i}.html",
                'content_hash' => hash('sha256', "paging-{$i}"),
                'word_count' => 100,
            ]);
        }
        // Sort by id asc (insertion order) for predictable page content
        $response = $this->getJson('/api/posts?sort=title&direction=asc&per_page=10&page=2');

        $response->assertOk();
        $this->assertEquals(2, $response->json('meta.current_page'));
        $this->assertEquals(10, $response->json('meta.per_page'));
        $this->assertEquals(25, $response->json('meta.total'));
        $this->assertCount(10, $response->json('data'));
        // With zero-padded title asc: Post 01 .. Post 25
        // Page 1 = Post 01-10, Page 2 = Post 11-20
        $this->assertEquals('Post 11', $response->json('data.0.title'));
        $this->assertEquals('Post 20', $response->json('data.9.title'));
    }

    public function test_posts_index_negative_page_returns_validation_error(): void
    {
        $response = $this->getJson('/api/posts?page=-1');

        $response->assertStatus(422);
        $response->assertJsonValidationErrors(['page']);
    }

    // -----------------------------------------------------------------------
    //  GET /api/posts  —  Sorting
    // -----------------------------------------------------------------------

    public function test_posts_index_default_sort_is_created_at_desc(): void
    {
        // Use raw DB inserts to have precise control over created_at timestamps
        $now = now();
        DB::table('posts')->insert([
            'title' => 'First Created',
            'content' => 'Content',
            'source_file' => 'csort1.html',
            'content_hash' => hash('sha256', 'csort1'),
            'word_count' => 100,
            'created_at' => (clone $now)->subDays(2),
            'updated_at' => (clone $now)->subDays(2),
        ]);
        DB::table('posts')->insert([
            'title' => 'Second Created',
            'content' => 'Content',
            'source_file' => 'csort2.html',
            'content_hash' => hash('sha256', 'csort2'),
            'word_count' => 100,
            'created_at' => (clone $now)->subDay(),
            'updated_at' => (clone $now)->subDay(),
        ]);
        DB::table('posts')->insert([
            'title' => 'Last Created',
            'content' => 'Content',
            'source_file' => 'csort3.html',
            'content_hash' => hash('sha256', 'csort3'),
            'word_count' => 100,
            'created_at' => $now,
            'updated_at' => $now,
        ]);

        $response = $this->getJson('/api/posts');

        $response->assertOk();
        $this->assertEquals('Last Created', $response->json('data.0.title'));
    }

    public function test_posts_index_sort_by_title_asc(): void
    {
        Post::create([
            'title' => 'Bravo',
            'content' => 'Content',
            'source_file' => 'bravo.html',
            'content_hash' => hash('sha256', 'bravo'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Alpha',
            'content' => 'Content',
            'source_file' => 'alpha.html',
            'content_hash' => hash('sha256', 'alpha'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Charlie',
            'content' => 'Content',
            'source_file' => 'charlie.html',
            'content_hash' => hash('sha256', 'charlie'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?sort=title&direction=asc');

        $response->assertOk();
        $titles = collect($response->json('data'))->pluck('title')->toArray();
        $this->assertEquals(['Alpha', 'Bravo', 'Charlie'], $titles);
    }

    public function test_posts_index_sort_by_title_desc(): void
    {
        Post::create([
            'title' => 'Bravo',
            'content' => 'Content',
            'source_file' => 'bravo-d.html',
            'content_hash' => hash('sha256', 'bravo-d'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Alpha',
            'content' => 'Content',
            'source_file' => 'alpha-d.html',
            'content_hash' => hash('sha256', 'alpha-d'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?sort=title&direction=desc');

        $response->assertOk();
        $titles = collect($response->json('data'))->pluck('title')->toArray();
        $this->assertEquals(['Bravo', 'Alpha'], $titles);
    }

    public function test_posts_index_sort_by_published_date_asc(): void
    {
        Post::create([
            'title' => 'Later',
            'content' => 'Content',
            'source_file' => 'later.html',
            'content_hash' => hash('sha256', 'later'),
            'published_date' => '2024-06-15',
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Earlier',
            'content' => 'Content',
            'source_file' => 'earlier.html',
            'content_hash' => hash('sha256', 'earlier'),
            'published_date' => '2024-01-10',
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?sort=published_date&direction=asc');

        $response->assertOk();
        $this->assertEquals('Earlier', $response->json('data.0.title'));
    }

    public function test_posts_index_sort_by_word_count_desc(): void
    {
        Post::create([
            'title' => 'Long',
            'content' => 'Content',
            'source_file' => 'long.html',
            'content_hash' => hash('sha256', 'long'),
            'word_count' => 500,
        ]);
        Post::create([
            'title' => 'Short',
            'content' => 'Content',
            'source_file' => 'short.html',
            'content_hash' => hash('sha256', 'short'),
            'word_count' => 50,
        ]);

        $response = $this->getJson('/api/posts?sort=word_count&direction=desc');

        $response->assertOk();
        $this->assertEquals('Long', $response->json('data.0.title'));
    }

    public function test_posts_index_sort_by_author_asc(): void
    {
        Post::create([
            'title' => 'Post Z',
            'content' => 'Content',
            'source_file' => 'postz.html',
            'content_hash' => hash('sha256', 'postz'),
            'author' => 'Zelalem',
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Post A',
            'content' => 'Content',
            'source_file' => 'posta.html',
            'content_hash' => hash('sha256', 'posta'),
            'author' => 'Abebe',
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?sort=author&direction=asc');

        $response->assertOk();
        $this->assertEquals('Post A', $response->json('data.0.title'));
    }

    public function test_posts_index_invalid_sort_field_returns_validation_error(): void
    {
        $response = $this->getJson('/api/posts?sort=invalid_field');

        $response->assertStatus(422);
        $response->assertJsonValidationErrors(['sort']);
    }

    public function test_posts_index_invalid_direction_returns_validation_error(): void
    {
        $response = $this->getJson('/api/posts?direction=sideways');

        $response->assertStatus(422);
        $response->assertJsonValidationErrors(['direction']);
    }

    // -----------------------------------------------------------------------
    //  GET /api/posts  —  Category filtering
    // -----------------------------------------------------------------------

    public function test_posts_index_filter_by_category(): void
    {
        Post::create([
            'title' => 'News Post',
            'content' => 'Content',
            'category' => 'News',
            'source_file' => 'news.html',
            'content_hash' => hash('sha256', 'news'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Business Post',
            'content' => 'Content',
            'category' => 'Business',
            'source_file' => 'biz.html',
            'content_hash' => hash('sha256', 'biz'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Another News',
            'content' => 'Content',
            'category' => 'News',
            'source_file' => 'news2.html',
            'content_hash' => hash('sha256', 'news2'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?category=News');

        $response->assertOk();
        $this->assertEquals(2, $response->json('meta.total'));
        $titles = collect($response->json('data'))->pluck('title')->toArray();
        $this->assertEquals(['News Post', 'Another News'], $titles);
    }

    public function test_posts_index_filter_by_category_no_matches(): void
    {
        Post::create([
            'title' => 'News Post',
            'content' => 'Content',
            'category' => 'News',
            'source_file' => 'news3.html',
            'content_hash' => hash('sha256', 'news3'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?category=NonExistent');

        $response->assertOk();
        $this->assertEquals(0, $response->json('meta.total'));
        $this->assertCount(0, $response->json('data'));
    }

    // -----------------------------------------------------------------------
    //  GET /api/posts  —  Search
    // -----------------------------------------------------------------------

    public function test_posts_index_search_matches_title(): void
    {
        Post::create([
            'title' => 'Ethiopia Economy',
            'content' => 'Some content',
            'source_file' => 'search-title.html',
            'content_hash' => hash('sha256', 'search-title'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Another Title',
            'content' => 'Nothing',
            'source_file' => 'no-match.html',
            'content_hash' => hash('sha256', 'no-match'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?search=Ethiopia');

        $response->assertOk();
        $this->assertEquals(1, $response->json('meta.total'));
        $this->assertEquals('Ethiopia Economy', $response->json('data.0.title'));
    }

    public function test_posts_index_search_matches_content(): void
    {
        Post::create([
            'title' => 'Hidden Gem',
            'content' => 'This article discusses GDP growth in Ethiopia',
            'source_file' => 'search-content.html',
            'content_hash' => hash('sha256', 'search-content'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Unrelated',
            'content' => 'Sports news around the world',
            'source_file' => 'unrelated.html',
            'content_hash' => hash('sha256', 'unrelated'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?search=GDP');

        $response->assertOk();
        $this->assertEquals(1, $response->json('meta.total'));
        $this->assertEquals('Hidden Gem', $response->json('data.0.title'));
    }

    public function test_posts_index_search_matches_author(): void
    {
        Post::create([
            'title' => 'Interview',
            'content' => 'Content',
            'author' => 'Abebe Kebede',
            'source_file' => 'author-search.html',
            'content_hash' => hash('sha256', 'author-search'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Opinion',
            'content' => 'Content',
            'author' => 'Hanna Lemma',
            'source_file' => 'no-author.html',
            'content_hash' => hash('sha256', 'no-author'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?search=Abebe');

        $response->assertOk();
        $this->assertEquals(1, $response->json('meta.total'));
        $this->assertEquals('Interview', $response->json('data.0.title'));
    }

    public function test_posts_index_search_no_matches(): void
    {
        Post::create([
            'title' => 'Regular Post',
            'content' => 'Regular content',
            'source_file' => 'regular.html',
            'content_hash' => hash('sha256', 'regular'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?search=zzzzznotfound');

        $response->assertOk();
        $this->assertEquals(0, $response->json('meta.total'));
    }

    public function test_posts_index_search_combined_with_category_filter(): void
    {
        Post::create([
            'title' => 'Ethiopia News',
            'content' => 'Economic update',
            'category' => 'News',
            'source_file' => 'combined1.html',
            'content_hash' => hash('sha256', 'combined1'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Ethiopia Sport',
            'content' => 'Athletics update',
            'category' => 'Sport',
            'source_file' => 'combined2.html',
            'content_hash' => hash('sha256', 'combined2'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Other News',
            'content' => 'Something else',
            'category' => 'News',
            'source_file' => 'combined3.html',
            'content_hash' => hash('sha256', 'combined3'),
            'word_count' => 100,
        ]);

        // Search for "Ethiopia" in News category only
        $response = $this->getJson('/api/posts?search=Ethiopia&category=News');

        $response->assertOk();
        $this->assertEquals(1, $response->json('meta.total'));
        $this->assertEquals('Ethiopia News', $response->json('data.0.title'));
    }

    public function test_posts_index_search_combined_with_sort_and_pagination(): void
    {
        Post::create([
            'title' => 'Alpha Economy',
            'content' => 'About GDP Ethiopia',
            'category' => 'News',
            'source_file' => 'combo-alpha.html',
            'content_hash' => hash('sha256', 'combo-alpha'),
            'word_count' => 100,
        ]);
        Post::create([
            'title' => 'Beta Economy',
            'content' => 'About growth Ethiopia',
            'category' => 'News',
            'source_file' => 'combo-beta.html',
            'content_hash' => hash('sha256', 'combo-beta'),
            'word_count' => 200,
        ]);

        $response = $this->getJson('/api/posts?search=Ethiopia&sort=title&direction=desc&per_page=1&page=1');

        $response->assertOk();
        $this->assertEquals(2, $response->json('meta.total'));
        $this->assertCount(1, $response->json('data'));
        // Desc order means "Beta" should come first
        $this->assertEquals('Beta Economy', $response->json('data.0.title'));
    }

    // -----------------------------------------------------------------------
    //  GET /api/posts  —  Response structure
    // -----------------------------------------------------------------------

    public function test_posts_index_response_structure_without_content(): void
    {
        Post::create([
            'title' => 'Sample Post',
            'subtitle' => 'A subtitle',
            'author' => 'Author Name',
            'content' => 'Full content here',
            'category' => 'News',
            'source_file' => 'structure.html',
            'volume' => 'Vol 7',
            'issue_number' => '364',
            'published_date' => '2024-06-15',
            'content_hash' => hash('sha256', 'structure'),
            'word_count' => 250,
        ]);

        $response = $this->getJson('/api/posts');

        $response->assertOk();
        $post = $response->json('data.0');

        // Assert present fields
        $this->assertArrayHasKey('id', $post);
        $this->assertArrayHasKey('title', $post);
        $this->assertArrayHasKey('subtitle', $post);
        $this->assertArrayHasKey('author', $post);
        $this->assertArrayHasKey('category', $post);
        $this->assertArrayHasKey('source_file', $post);
        $this->assertArrayHasKey('volume', $post);
        $this->assertArrayHasKey('issue_number', $post);
        $this->assertArrayHasKey('published_date', $post);
        $this->assertArrayHasKey('word_count', $post);
        $this->assertArrayHasKey('images', $post);
        $this->assertArrayHasKey('created_at', $post);
        $this->assertArrayHasKey('updated_at', $post);

        // Content should NOT be present in list
        $this->assertArrayNotHasKey('content', $post);

        // Type checks
        $this->assertIsInt($post['id']);
        $this->assertIsString($post['title']);
        $this->assertIsString($post['subtitle']);
        $this->assertIsString($post['author']);
        $this->assertIsString($post['category']);
        $this->assertIsString($post['source_file']);
        $this->assertIsString($post['published_date']);
        $this->assertIsInt($post['word_count']);
        $this->assertIsArray($post['images']);
    }

    public function test_posts_index_includes_images_relation(): void
    {
        $post = Post::create([
            'title' => 'Post With Images',
            'content' => 'Content',
            'source_file' => 'with-images.html',
            'content_hash' => hash('sha256', 'with-images'),
            'word_count' => 100,
        ]);
        $post->images()->create([
            'image_path' => '/images/photo.jpg',
            'alt_text' => 'A photo',
            'sort_order' => 1,
        ]);

        $response = $this->getJson('/api/posts');

        $response->assertOk();
        $this->assertCount(1, $response->json('data.0.images'));
        $this->assertEquals('/images/photo.jpg', $response->json('data.0.images.0.image_path'));
    }

    // -----------------------------------------------------------------------
    //  GET /api/posts/{id}  —  Show
    // -----------------------------------------------------------------------

    public function test_posts_show_returns_post_with_content(): void
    {
        $post = Post::create([
            'title' => 'Detailed Post',
            'subtitle' => 'A subtitle',
            'author' => 'John Doe',
            'content' => 'This is the full content of the post.',
            'category' => 'Analysis',
            'source_file' => 'detailed.html',
            'volume' => 'Vol 7',
            'issue_number' => '364',
            'published_date' => '2024-06-15',
            'content_hash' => hash('sha256', 'detailed'),
            'word_count' => 300,
        ]);

        // The PostResource conditionally includes content based on route name.
        // Named routes take the pattern: <prefix>.<name>
        // The show route is inside a 'posts' prefix group so the route name
        // is resolved dynamically by Laravel. We use the actual URL.
        $response = $this->getJson("/api/posts/{$post->id}");

        $response->assertOk();
        $data = $response->json('data');

        $this->assertEquals($post->id, $data['id']);
        $this->assertEquals('Detailed Post', $data['title']);
        $this->assertEquals('A subtitle', $data['subtitle']);
        $this->assertEquals('John Doe', $data['author']);
        $this->assertEquals('Analysis', $data['category']);
        $this->assertEquals('This is the full content of the post.', $data['content']);
        $this->assertEquals('Vol 7', $data['volume']);
        $this->assertEquals('364', $data['issue_number']);
        $this->assertEquals('2024-06-15', $data['published_date']);
        $this->assertEquals(300, $data['word_count']);
        $this->assertIsArray($data['images']);
        $this->assertArrayHasKey('created_at', $data);
        $this->assertArrayHasKey('updated_at', $data);
    }

    public function test_posts_show_returns_404_for_non_existent_id(): void
    {
        $response = $this->getJson('/api/posts/99999');

        $response->assertNotFound();
    }

    public function test_posts_show_returns_404_for_string_id(): void
    {
        $response = $this->getJson('/api/posts/abc');

        $response->assertNotFound();
    }

    public function test_posts_show_includes_images(): void
    {
        $post = Post::create([
            'title' => 'Post With Images',
            'content' => 'Content',
            'source_file' => 'show-images.html',
            'content_hash' => hash('sha256', 'show-images'),
            'word_count' => 100,
        ]);
        $post->images()->createMany([
            ['image_path' => '/img/1.jpg', 'alt_text' => 'First', 'sort_order' => 0],
            ['image_path' => '/img/2.jpg', 'alt_text' => 'Second', 'sort_order' => 1],
        ]);

        $response = $this->getJson("/api/posts/{$post->id}");

        $response->assertOk();
        $this->assertCount(2, $response->json('data.images'));
    }

    public function test_posts_show_published_date_formatted_as_y_m_d(): void
    {
        $post = Post::create([
            'title' => 'Date Post',
            'content' => 'Content',
            'source_file' => 'date-post.html',
            'content_hash' => hash('sha256', 'date-post'),
            'published_date' => '2024-01-15',
            'word_count' => 100,
        ]);

        $response = $this->getJson("/api/posts/{$post->id}");

        $response->assertOk();
        $this->assertEquals('2024-01-15', $response->json('data.published_date'));
    }

    public function test_posts_show_timestamps_in_iso_format(): void
    {
        $post = Post::create([
            'title' => 'Timestamps',
            'content' => 'Content',
            'source_file' => 'timestamps.html',
            'content_hash' => hash('sha256', 'timestamps'),
            'word_count' => 100,
        ]);

        $response = $this->getJson("/api/posts/{$post->id}");

        $response->assertOk();
        // ISO 8601 format with timezone suffix
        $this->assertMatchesRegularExpression(
            '/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$/',
            $response->json('data.created_at')
        );
        $this->assertMatchesRegularExpression(
            '/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$/',
            $response->json('data.updated_at')
        );
    }

    // -----------------------------------------------------------------------
    //  GET /api/posts/{id}/images  —  Post Images
    // -----------------------------------------------------------------------

    public function test_post_images_returns_images_sorted_by_sort_order(): void
    {
        $post = Post::create([
            'title' => 'Image Test',
            'content' => 'Content',
            'source_file' => 'image-test.html',
            'content_hash' => hash('sha256', 'image-test'),
            'word_count' => 100,
        ]);
        $post->images()->createMany([
            ['image_path' => '/img/c.jpg', 'alt_text' => 'Third', 'sort_order' => 2],
            ['image_path' => '/img/a.jpg', 'alt_text' => 'First', 'sort_order' => 0],
            ['image_path' => '/img/b.jpg', 'alt_text' => 'Second', 'sort_order' => 1],
        ]);

        $response = $this->getJson("/api/posts/{$post->id}/images");

        $response->assertOk();
        $this->assertCount(3, $response->json('data'));
        $this->assertEquals('Third', $response->json('data.0.alt_text'));
        $this->assertEquals('First', $response->json('data.1.alt_text'));
        $this->assertEquals('Second', $response->json('data.2.alt_text'));
    }

    public function test_post_images_returns_empty_array_when_no_images(): void
    {
        $post = Post::create([
            'title' => 'No Images',
            'content' => 'Content',
            'source_file' => 'no-images.html',
            'content_hash' => hash('sha256', 'no-images'),
            'word_count' => 100,
        ]);

        $response = $this->getJson("/api/posts/{$post->id}/images");

        $response->assertOk();
        $this->assertCount(0, $response->json('data'));
    }

    public function test_post_images_returns_404_for_non_existent_post(): void
    {
        $response = $this->getJson('/api/posts/99999/images');

        $response->assertNotFound();
    }

    public function test_post_images_response_structure(): void
    {
        $post = Post::create([
            'title' => 'Structure',
            'content' => 'Content',
            'source_file' => 'img-structure.html',
            'content_hash' => hash('sha256', 'img-structure'),
            'word_count' => 100,
        ]);
        $post->images()->create([
            'image_path' => '/images/test.jpg',
            'alt_text' => 'Test image',
            'sort_order' => 0,
        ]);

        $response = $this->getJson("/api/posts/{$post->id}/images");

        $response->assertOk();
        $image = $response->json('data.0');

        $this->assertArrayHasKey('id', $image);
        $this->assertArrayHasKey('image_path', $image);
        $this->assertArrayHasKey('alt_text', $image);
        $this->assertArrayHasKey('sort_order', $image);
        $this->assertEquals('/images/test.jpg', $image['image_path']);
        $this->assertEquals('Test image', $image['alt_text']);
        $this->assertEquals(0, $image['sort_order']);
    }

    public function test_post_images_only_returns_images_for_specified_post(): void
    {
        $postA = Post::create([
            'title' => 'Post A',
            'content' => 'Content',
            'source_file' => 'img-only-a.html',
            'content_hash' => hash('sha256', 'img-only-a'),
            'word_count' => 100,
        ]);
        $postB = Post::create([
            'title' => 'Post B',
            'content' => 'Content',
            'source_file' => 'img-only-b.html',
            'content_hash' => hash('sha256', 'img-only-b'),
            'word_count' => 100,
        ]);
        $postA->images()->create([
            'image_path' => '/img/a.jpg',
            'alt_text' => 'A image',
            'sort_order' => 0,
        ]);
        $postB->images()->createMany([
            ['image_path' => '/img/b1.jpg', 'alt_text' => 'B1', 'sort_order' => 0],
            ['image_path' => '/img/b2.jpg', 'alt_text' => 'B2', 'sort_order' => 1],
        ]);

        $response = $this->getJson("/api/posts/{$postA->id}/images");

        $response->assertOk();
        $this->assertCount(1, $response->json('data'));
        $this->assertEquals('A image', $response->json('data.0.alt_text'));

        $responseB = $this->getJson("/api/posts/{$postB->id}/images");
        $this->assertCount(2, $responseB->json('data'));
    }

    // -----------------------------------------------------------------------
    //  CORS & Route tests
    // -----------------------------------------------------------------------

    public function test_cors_preflight_on_api_posts(): void
    {
        $response = $this->optionsJson('/api/posts', headers: [
            'Origin' => 'http://localhost:5173',
            'Access-Control-Request-Method' => 'GET',
        ]);

        $response->assertStatus(204);
        $response->assertHeader('Access-Control-Allow-Origin', 'http://localhost:5173');
    }

    public function test_undefined_api_route_returns_404(): void
    {
        $response = $this->getJson('/api/unknown');

        $response->assertNotFound();
    }

    // -----------------------------------------------------------------------
    //  Edge Cases
    // -----------------------------------------------------------------------

    public function test_search_with_too_long_string_returns_validation_error(): void
    {
        $longString = str_repeat('a', 256);

        $response = $this->getJson('/api/posts?search=' . $longString);

        $response->assertStatus(422);
        $response->assertJsonValidationErrors(['search']);
    }

    public function test_category_with_special_characters_works(): void
    {
        Post::create([
            'title' => 'Special Cat',
            'content' => 'Content',
            'category' => "Tech & Innovation '24",
            'source_file' => 'special-cat.html',
            'content_hash' => hash('sha256', 'special-cat'),
            'word_count' => 100,
        ]);

        $response = $this->getJson('/api/posts?category=Tech+%26+Innovation+%2724');

        $response->assertOk();
        $this->assertEquals(1, $response->json('meta.total'));
    }

    public function test_sql_injection_attempt_treated_as_literal_search(): void
    {
        Post::create([
            'title' => "Normal Title OR '1'='1",
            'content' => 'Content',
            'source_file' => 'sql-inject.html',
            'content_hash' => hash('sha256', 'sql-inject'),
            'word_count' => 100,
        ]);

        // This should not return all posts, just those matching the literal string
        Post::create([
            'title' => 'Other Post',
            'content' => 'Other content',
            'source_file' => 'other.html',
            'content_hash' => hash('sha256', 'other'),
            'word_count' => 100,
        ]);

        $response = $this->getJson("/api/posts?search=OR%20'1'%3D'1");

        $response->assertOk();
        // Only the post with the literal string in its title should match
        $this->assertEquals(1, $response->json('meta.total'));
    }

    public function test_large_dataset_pagination_consistency(): void
    {
        // Create 57 posts to test pagination math
        for ($i = 1; $i <= 57; $i++) {
            Post::create([
                'title' => "Bulk Post {$i}",
                'content' => "Content {$i}",
                'source_file' => "bulk-{$i}.html",
                'content_hash' => hash('sha256', "bulk-{$i}"),
                'word_count' => 100,
            ]);
        }

        $response = $this->getJson('/api/posts?per_page=10&page=3');

        $response->assertOk();
        $meta = $response->json('meta');

        $this->assertEquals(10, $meta['per_page']);
        $this->assertEquals(3, $meta['current_page']);
        $this->assertEquals(6, $meta['last_page']);  // ceil(57/10) = 6
        $this->assertEquals(57, $meta['total']);
        $this->assertEquals(21, $meta['from']);      // (3-1)*10+1 = 21
        $this->assertEquals(30, $meta['to']);         // 3*10 = 30
        $this->assertCount(10, $response->json('data'));
    }

    public function test_post_with_max_length_title_is_stored_and_returned(): void
    {
        $longTitle = str_repeat('A', 500);

        $post = Post::create([
            'title' => $longTitle,
            'content' => 'Content',
            'source_file' => 'max-title.html',
            'content_hash' => hash('sha256', 'max-title'),
            'word_count' => 100,
        ]);

        $response = $this->getJson("/api/posts/{$post->id}");

        $response->assertOk();
        $this->assertEquals(500, strlen($response->json('data.title')));
    }
}