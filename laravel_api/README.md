# Post Manager API

A Laravel REST API that serves scraped news articles and their associated images. This API is the backend data layer for the Post Manager system, consuming data populated by the Python scraper component.

## Tech Stack

- **Framework**: Laravel 11+
- **Database**: MySQL 8.0
- **Language**: PHP 8.2+
- **Package Manager**: Composer

## Architecture Overview

The system consists of two main components:

1. **Python Scraper** (`python_scraper/`) — Extracts articles, images, and metadata from news archives and stores them in the MySQL database.
2. **Laravel API** (`laravel_api/`) — Provides a RESTful interface to query the scraped posts and images.

```
┌─────────────────┐     writes to     ┌──────────┐     served by     ┌─────────────────┐
│  Python Scraper  │ ──────────────▶  │  MySQL   │ ◀─────────────────  │  Laravel API    │
│                  │                  │          │                     │                 │
│  (populates      │                  │  post_   │                     │  (REST         │
│   database)      │                  │  manager │                     │   endpoints)    │
└─────────────────┘                  └──────────┘                     └─────────────────┘
```

## Prerequisites

- PHP 8.2 or higher
- Composer
- MySQL 8.0 (can be run via Docker or locally)
- Node.js 18+ and npm (for frontend)

## Quick Start (Local Development)

### 1. Clone the repository

```bash
git clone <repository-url>
cd post_manager
```

### 2. Start MySQL database

If you have Docker installed, you can start MySQL using the provided docker-compose file:

```bash
docker compose up -d mysql
```

This starts MySQL 8.0 on port `3306` with the following default credentials:
- Database: `post_manager`
- User: `post_manager_user`
- Password: `post_manager_pass`

Alternatively, you can use a local MySQL installation. Ensure you have a database named `post_manager` created.

### 3. Install dependencies

Navigate to the Laravel API directory and install PHP dependencies:

```bash
cd laravel_api
composer install
```

### 4. Configure environment

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` to match your database configuration:

```
APP_NAME=PostManager
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=post_manager
DB_USERNAME=post_manager_user
DB_PASSWORD=post_manager_pass
```

**Note:** If you're using Docker for MySQL (from step 2), use the credentials:
- `DB_HOST=127.0.0.1` (or `mysql` if running Laravel in Docker)
- `DB_DATABASE=post_manager`
- `DB_USERNAME=post_manager_user`
- `DB_PASSWORD=post_manager_pass`

### 5. Generate the application key

```bash
php artisan key:generate
```

This creates a unique encryption key for your Laravel application and updates the `.env` file.

### 6. Run database migrations

```bash
php artisan migrate
```

This creates the necessary database tables:
- `posts` — Stores scraped news articles
- `post_images` — Stores images associated with posts

### 7. Start the development server

```bash
php artisan serve --host=0.0.0.0 --port=8000
```

The API will be available at `http://localhost:8000`.

### 8. Verify the API

In a new terminal, test the API:

```bash
curl http://localhost:8000/api/posts
```

If the database has been populated by the scraper, you should receive a JSON response with paginated posts.

## Populating the Database

The database schema is defined at the project root in `schema.sql`. The Python scraper (`python_scraper/`) is responsible for extracting articles from news archive HTML files and inserting them into the database.

See the [Python Scraper README](../python_scraper/README.md) for detailed instructions on running the scraper.

**Important:** Run the Laravel migrations (step 6) before running the Python scraper. The migrations create the database schema that the scraper depends on.

### Database Tables

**`posts`** — Stores scraped news articles:

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGINT (PK) | Auto-increment primary key |
| `title` | VARCHAR(500) | Article title |
| `subtitle` | TEXT | Article subtitle |
| `author` | VARCHAR(255) | Article author |
| `content` | LONGTEXT | Full article body |
| `category` | VARCHAR(100) | Article category |
| `source_file` | VARCHAR(500) | Original source filename |
| `volume` | VARCHAR(50) | Newspaper volume |
| `issue_number` | VARCHAR(50) | Newspaper issue number |
| `published_date` | DATE | Article publication date |
| `word_count` | INTEGER | Word count of the article |
| `content_hash` | VARCHAR(64) | SHA-256 hash for deduplication |
| `created_at` | TIMESTAMP | Laravel standard created timestamp |
| `updated_at` | TIMESTAMP | Laravel standard updated timestamp |

**`post_images`** — Stores images associated with posts:

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGINT (PK) | Auto-increment primary key |
| `post_id` | BIGINT (FK) | Foreign key to `posts.id` |
| `image_path` | VARCHAR(500) | Path or URL to the image |
| `alt_text` | TEXT | Image alt/description text |
| `sort_order` | INTEGER | Display ordering within the post |
| `created_at` | TIMESTAMP | Laravel standard created timestamp |
| `updated_at` | TIMESTAMP | Laravel standard updated timestamp |

## Running Tests

```bash
# Run all tests
php artisan test

# Run with coverage
php artisan test --coverage
```

The test suite covers:
- Listing posts with pagination
- Filtering by category
- Searching by title, content, or author
- Sorting by various fields
- Retrieving a single post with full content
- Fetching images for a post
- Listing distinct categories
- Error handling for non-existent resources

## API Endpoints

The API exposes the following endpoints. Detailed documentation with request/response examples is available in [API-DOC.md](./API-DOC.md).

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts` | Paginated, filterable post listing |
| GET | `/api/posts/{id}` | Single post with full content |
| GET | `/api/posts/{id}/images` | Images for a specific post |
| GET | `/api/categories` | List of distinct categories |

## CORS Configuration

CORS is configured to allow requests from any origin during development. For production, update the `allowed_origins` setting in `config/cors.php`.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `PostManager` | Application name |
| `APP_ENV` | `local` | Application environment |
| `APP_DEBUG` | `true` | Enable/disable debug mode |
| `APP_URL` | `http://localhost:8000` | Application URL |
| `APP_KEY` | *(required)* | Laravel application encryption key |
| `DB_CONNECTION` | `mysql` | Database driver |
| `DB_HOST` | `127.0.0.1` | Database host |
| `DB_PORT` | `3306` | Database port |
| `DB_DATABASE` | `post_manager` | Database name |
| `DB_USERNAME` | `post_manager_user` | Database user |
| `DB_PASSWORD` | `post_manager_pass` | Database password |

## Troubleshooting

### Database Connection Issues

If you can't connect to the database:

1. Verify MySQL is running: `docker compose ps` (if using Docker)
2. Check your `.env` database credentials match your MySQL setup
3. Ensure the database `post_manager` exists
4. Verify the user `post_manager_user` has proper permissions

### Migration Errors

If migrations fail:

1. Make sure the database exists before running migrations
2. Check that your database user has CREATE and ALTER permissions
3. Review the error message for specific table/column issues

### Artisan Commands Not Working

If artisan commands fail:

1. Ensure dependencies are installed: `composer install`
2. Clear the cache: `php artisan config:clear`
3. Regenerate the autoloader: `composer dump-autoload`

## License

This project is open-sourced under the MIT license.