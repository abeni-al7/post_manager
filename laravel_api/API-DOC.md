# Post Manager API — API Reference

Base URL: `http://localhost:8000/api`

All endpoints return JSON responses. Paginated responses follow Laravel's standard pagination structure.

---

## Table of Contents

1. [List Posts](#1-list-posts)
2. [Get Single Post](#2-get-single-post)
3. [Get Post Images](#3-get-post-images)
4. [List Categories](#4-list-categories)
5. [Error Codes](#5-error-codes)
6. [Response Format Reference](#6-response-format-reference)

---

## 1. List Posts

Returns a paginated, filterable, searchable list of posts.

**Endpoint:** `GET /api/posts`

### Query Parameters

| Parameter    | Type    | Default        | Description                                                |
|-------------|---------|----------------|------------------------------------------------------------|
| `page`      | integer | `1`            | Page number (minimum: 1)                                   |
| `per_page`  | integer | `15`           | Items per page (minimum: 1, maximum: 100)                  |
| `category`  | string  | —              | Filter by exact category name                              |
| `search`    | string  | —              | Search across title, content, and author (case-insensitive)|
| `sort`      | string  | `created_at`   | Sort field. One of: `title`, `published_date`, `created_at`, `author`, `word_count` |
| `direction` | string  | `desc`         | Sort direction. One of: `asc`, `desc`                      |

> **Note:** The `content` field is **excluded** from the list response for performance. Full content is available when fetching a single post.

### Example Request

```bash
curl "http://localhost:8000/api/posts?page=1&per_page=10&category=News&sort=published_date&direction=desc"
```

### Example Response — `200 OK`

```json
{
    "data": [
        {
            "id": 1,
            "title": "NBE Power Outage Freezes Gov't Accounts",
            "subtitle": null,
            "author": "Staff Reporter",
            "category": "News",
            "source_file": "NBE Power Outage Freezes Gov\u2019t Accounts.htm",
            "volume": "7",
            "issue_number": "364",
            "published_date": "2012-03-15",
            "word_count": 850,
            "images": [
                {
                    "id": 1,
                    "image_path": "/images/news/power-outage.jpg",
                    "alt_text": "Power outage at NBE headquarters",
                    "sort_order": 1
                }
            ],
            "created_at": "2024-01-15T10:30:00.000000Z",
            "updated_at": "2024-01-15T10:30:00.000000Z"
        },
        {
            "id": 2,
            "title": "MIDROC Sister Co's Close to 260m Br Road Construction Deal",
            "subtitle": null,
            "author": "Staff Reporter",
            "category": "Business",
            "source_file": "MIDROC Sister Co\u2019s Close to 260m Br Road Construction Deal.htm",
            "volume": "7",
            "issue_number": "364",
            "published_date": "2012-03-15",
            "word_count": 620,
            "images": [],
            "created_at": "2024-01-15T10:31:00.000000Z",
            "updated_at": "2024-01-15T10:31:00.000000Z"
        }
    ],
    "links": {
        "first": "http://localhost:8000/api/posts?page=1",
        "last": "http://localhost:8000/api/posts?page=5",
        "prev": null,
        "next": "http://localhost:8000/api/posts?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 5,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "http://localhost:8000/api/posts?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "http://localhost:8000/api/posts?page=2",
                "label": "2",
                "active": false
            }
        ],
        "next_page_url": "http://localhost:8000/api/posts?page=2",
        "path": "http://localhost:8000/api/posts",
        "per_page": 10,
        "prev_page_url": null,
        "to": 10,
        "total": 50
    }
}
```

### Example Request — Filter by Category

```bash
curl "http://localhost:8000/api/posts?category=Business"
```

### Example Request — Search

```bash
curl "http://localhost:8000/api/posts?search=power%20outage"
```

### Example Request — Custom Sort

```bash
curl "http://localhost:8000/api/posts?sort=title&direction=asc&per_page=20"
```

### Error Response — `422 Unprocessable Content`

Returned when query parameters fail validation.

```json
{
    "message": "The per page field must be between 1 and 100. (and 1 more error)",
    "errors": {
        "per_page": [
            "The per page field must be between 1 and 100."
        ],
        "sort": [
            "The selected sort is invalid."
        ]
    }
}
```

---

## 2. Get Single Post

Returns a single post with full content and all associated images.

**Endpoint:** `GET /api/posts/{id}`

### Path Parameters

| Parameter | Type    | Description          |
|-----------|---------|----------------------|
| `id`      | integer | The post's ID        |

> **Note:** The `content` field is **included** only in this endpoint (not in the list response).

### Example Request

```bash
curl "http://localhost:8000/api/posts/1"
```

### Example Response — `200 OK`

```json
{
    "data": {
        "id": 1,
        "title": "NBE Power Outage Freezes Gov't Accounts",
        "subtitle": "Central bank services halted for three days",
        "author": "Staff Reporter",
        "content": "The National Bank of Ethiopia (NBE) experienced a major power outage...\n\nFull article content continues here...",
        "category": "News",
        "source_file": "NBE Power Outage Freezes Gov\u2019t Accounts.htm",
        "volume": "7",
        "issue_number": "364",
        "published_date": "2012-03-15",
        "word_count": 850,
        "images": [
            {
                "id": 1,
                "image_path": "/images/news/power-outage.jpg",
                "alt_text": "Power outage at NBE headquarters",
                "sort_order": 1
            },
            {
                "id": 2,
                "image_path": "/images/news/power-outage-2.jpg",
                "alt_text": "NBE building exterior",
                "sort_order": 2
            }
        ],
        "created_at": "2024-01-15T10:30:00.000000Z",
        "updated_at": "2024-01-15T10:30:00.000000Z"
    }
}
```

### Error Response — `404 Not Found`

```json
{
    "message": "No query results for model [App\\Models\\Post] 9999"
}
```

---

## 3. Get Post Images

Returns all images associated with a specific post.

**Endpoint:** `GET /api/posts/{id}/images`

### Path Parameters

| Parameter | Type    | Description          |
|-----------|---------|----------------------|
| `id`      | integer | The post's ID        |

### Example Request

```bash
curl "http://localhost:8000/api/posts/1/images"
```

### Example Response — `200 OK`

```json
{
    "data": [
        {
            "id": 1,
            "image_path": "/images/news/power-outage.jpg",
            "alt_text": "Power outage at NBE headquarters",
            "sort_order": 1
        },
        {
            "id": 2,
            "image_path": "/images/news/power-outage-2.jpg",
            "alt_text": "NBE building exterior",
            "sort_order": 2
        }
    ]
}
```

### Example Response — Post with No Images

```json
{
    "data": []
}
```

### Error Response — `404 Not Found`

Returned when the post does not exist.

```json
{
    "message": "No query results for model [App\\Models\\Post] 9999"
}
```
(Unchanged from the single post endpoint — standard Laravel `findOrFail` behavior.)

---

## 4. List Categories

Returns a sorted list of all distinct categories present in the posts table.

**Endpoint:** `GET /api/categories`

### Example Request

```bash
curl "http://localhost:8000/api/categories"
```

### Example Response — `200 OK`

```json
{
    "data": [
        "Business",
        "Editorial",
        "Interview",
        "Life & Matters",
        "News",
        "Opinion",
        "Perspective",
        "Sport"
    ]
}
```

The categories are sorted alphabetically. Categories containing null values are excluded.

---

## 5. Error Codes

| HTTP Status | Meaning                  | Typical Cause                                       |
|-------------|--------------------------|-----------------------------------------------------|
| `200`       | OK                       | Request succeeded                                   |
| `404`       | Not Found                | The requested post ID does not exist                |
| `422`       | Unprocessable Content    | Query parameter validation failed                   |
| `500`       | Internal Server Error    | Server-side exception (check Laravel logs)          |

---

## 6. Response Format Reference

### Post Object (list view)

Appears in the `data` array of `GET /api/posts`.

| Field            | Type           | Description                                     |
|------------------|----------------|-------------------------------------------------|
| `id`             | integer        | Post ID                                         |
| `title`          | string         | Article title                                   |
| `subtitle`       | string\|null   | Article subtitle                                |
| `author`         | string\|null   | Article author                                  |
| `category`       | string\|null   | Article category                                |
| `source_file`    | string\|null   | Original source filename                        |
| `volume`         | string\|null   | Newspaper volume                                |
| `issue_number`   | string\|null   | Newspaper issue number                          |
| `published_date` | string\|null   | Publication date (Y-m-d format)                 |
| `word_count`     | integer\|null  | Article word count                              |
| `images`         | array          | Array of [image objects](#image-object)         |
| `created_at`     | string         | ISO 8601 timestamp                              |
| `updated_at`     | string         | ISO 8601 timestamp                              |

### Post Object (detail view)

Same as list view, plus:

| Field     | Type           | Description                                     |
|-----------|----------------|-------------------------------------------------|
| `content` | string\|null   | Full article body (included only in detail view)|

### Image Object

| Field        | Type         | Description                   |
|-------------|--------------|-------------------------------|
| `id`         | integer      | Image ID                      |
| `image_path` | string       | Path or URL to the image      |
| `alt_text`   | string\|null | Image alt/description text    |
| `sort_order` | integer      | Display order within the post |

### Pagination Structure

Standard Laravel pagination wrapper with:

| Field       | Type   | Description                           |
|-------------|--------|---------------------------------------|
| `links`     | object | First, last, prev, next page URLs    |
| `meta`      | object | Pagination metadata (current page, total, per page, etc.)