# Post Manager System

A full-stack system for extracting, storing, and displaying posts from local HTML newspaper archives. Built with **Python** (scraper), **Laravel** (API), and **React** (frontend).

## Architecture

```
┌─────────────────┐     writes to     ┌──────────┐     served by     ┌─────────────────┐     consumed by     ┌─────────────────┐
│  Python Scraper  │ ──────────────▶  │  MySQL   │ ◀─────────────────  │  Laravel API    │ ◀─────────────────  │  React Frontend  │
│                  │                  │          │                     │  (PHP native)   │                     │  (Vite +        │
│  (parses HTML    │                  │  post_   │                     │                 │                     │   Tailwind)      │
│   archives)      │                  │  manager │                     │                 │                     │                 │
└─────────────────┘                  └──────────┘                     └─────────────────┘                     └─────────────────┘
       │                                                                        ▲                                       ▲
       └────────────────────────────────────────────────────────────────────────┴───────────────────────────────────────┘
                                    MySQL runs in Docker, Backend & Frontend run natively
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Scraper** | Python, BeautifulSoup, MySQL Connector |
| **Backend** | Laravel 11+, PHP 8.2+, MySQL 8.0 |
| **Frontend** | React 18, Vite, Tailwind CSS v3, React Router v6 |
| **Infrastructure** | Docker (MySQL only) |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) (for MySQL only)
- PHP 8.2+ and Composer (for Laravel backend)
- Node.js 18+ and npm (for React frontend)
- Python 3.8+ (for scraper)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/abeni-al7/post_manager
cd post_manager
```

### 2. Start MySQL database

```bash
docker compose up -d mysql
```

This starts MySQL 8.0 on port `3306` with the following default credentials:
- Database: `post_manager`
- User: `post_manager_user`
- Password: `post_manager_pass`

### 3. Setup Laravel backend

Open a new terminal and navigate to the Laravel API directory:

```bash
cd laravel_api
```

Install PHP dependencies:

```bash
composer install
```

Configure environment:

```bash
cp .env.example .env
```

Edit `.env` and configure the database connection (use the same credentials from step 2):

```
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=post_manager
DB_USERNAME=post_manager_user
DB_PASSWORD=post_manager_pass
```

Generate the Laravel application key:

```bash
php artisan key:generate
```

Run database migrations:

```bash
php artisan migrate
```

Start the Laravel development server:

```bash
php artisan serve --host=0.0.0.0 --port=8000
```

The API will be available at `http://localhost:8000`.

### 4. Setup React frontend

Open a new terminal and navigate to the React frontend directory:

```bash
cd react_frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### 5. Populate the database

Run the Python scraper to extract articles from the HTML archives:

```bash
# See python_scraper/README.md for detailed instructions
python3 python_scraper/scraper.py
```

**Note:** The Python scraper will only insert data into the existing tables. It does not create or modify the database schema. Make sure to run the Laravel migrations (step 3) before running the scraper.

### 6. Access the application

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000/api
- **API Docs**: See [laravel_api/API-DOC.md](./laravel_api/API-DOC.md)

## Project Structure

```
post_manager/
├── docker-compose.yml          # Orchestrates MySQL only
├── schema.sql                  # Database schema reference
├── python_scraper/             # Python HTML parser and data ingestion
│   ├── scraper.py
│   ├── parser.py
│   ├── extractors/             # Title, author, content, image extractors
│   ├── classifiers/            # Category classification
│   ├── storage/                # Database writer
│   └── utils/                  # File scanning, deduplication
├── laravel_api/                # Laravel REST API
│   ├── app/
│   │   ├── Http/Controllers/Api/PostController.php
│   │   ├── Models/Post.php
│   │   ├── Models/PostImage.php
│   │   └── Http/Resources/
│   ├── routes/api.php
│   ├── database/migrations/
│   └── API-DOC.md
└── react_frontend/             # React frontend
    ├── src/
    │   ├── components/         # Reusable UI components
    │   ├── pages/              # Route pages
    │   ├── services/api.js     # Axios API client
    │   └── App.jsx
    ├── Dockerfile
    └── nginx.conf
```

## Frontend Features

- **Newspaper-inspired design** matching the Addis Fortune archive aesthetic
- **Post listing** with pagination, search, and category filtering
- **Single post view** with full content and image gallery
- **Category sidebar** navigation
- **Responsive layout** (sidebar collapses on mobile)
- **Debounced search** (300ms delay)
- **Image lightbox** with navigation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts` | Paginated, filterable post listing |
| GET | `/api/posts/{id}` | Single post with full content |
| GET | `/api/posts/{id}/images` | Images for a specific post |
| GET | `/api/categories` | List of distinct categories |

See [laravel_api/API-DOC.md](./laravel_api/API-DOC.md) for full documentation.

## Environment Variables

### Docker (MySQL)

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_ROOT_PASSWORD` | `root_password` | MySQL root password |
| `MYSQL_DATABASE` | `post_manager` | Database name |
| `MYSQL_USER` | `post_manager_user` | Database user |
| `MYSQL_PASSWORD` | `post_manager_pass` | Database password |
| `MYSQL_PORT` | `3306` | Host port for MySQL |

### Laravel Backend

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `local` | Application environment |
| `APP_DEBUG` | `true` | Enable/disable debug mode |
| `APP_KEY` | *(required)* | Laravel encryption key (run `php artisan key:generate`) |
| `DB_CONNECTION` | `mysql` | Database driver |
| `DB_HOST` | `127.0.0.1` | Database host (use `mysql` if running in Docker) |
| `DB_PORT` | `3306` | Database port |
| `DB_DATABASE` | `post_manager` | Database name |
| `DB_USERNAME` | `post_manager_user` | Database user |
| `DB_PASSWORD` | `post_manager_pass` | Database password |

### React Frontend

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000/api` | Laravel API base URL |

## Running Tests

### Laravel API tests

```bash
cd laravel_api
php artisan test
```

## Stopping Services

To stop the MySQL container:

```bash
docker compose down
```

To stop the Laravel development server, press `Ctrl+C` in the terminal where it's running.

To stop the React development server, press `Ctrl+C` in the terminal where it's running.

## License

MIT