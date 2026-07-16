# React Frontend — Post Manager

A React + Vite frontend for the Post Manager system, built with Tailwind CSS v3 and styled to match the Addis Fortune newspaper archive aesthetic.

## Tech Stack

- **React 18** with Vite
- **Tailwind CSS v3** for styling
- **React Router v6** for client-side routing
- **Axios** for API communication

## Project Structure

```
react_frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx          # Top navigation bar (maroon header)
│   │   ├── Sidebar.jsx         # Category navigation sidebar
│   │   ├── Layout.jsx          # Page layout wrapper
│   │   ├── PostCard.jsx        # Post list item card
│   │   ├── SearchBar.jsx       # Debounced search input
│   │   ├── Pagination.jsx      # Page navigation controls
│   │   └── ImageGallery.jsx    # Image grid + lightbox
│   ├── pages/
│   │   ├── HomePage.jsx        # Paginated post list with search/filter
│   │   ├── PostDetailPage.jsx  # Single post with full content + images
│   │   └── CategoryPage.jsx    # Posts filtered by category
│   ├── services/
│   │   └── api.js              # Axios client for Laravel API
│   ├── App.jsx                 # Router configuration
│   ├── main.jsx                # Entry point
│   └── index.css               # Tailwind directives + custom styles
├── Dockerfile                  # Multi-stage build (Node + Nginx)
├── nginx.conf                  # Nginx config with SPA routing + API proxy
├── tailwind.config.js          # Custom Fortune color palette
└── package.json
```

## Routes

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | `HomePage` | Paginated post list, search, category filter |
| `/post/:id` | `PostDetailPage` | Full article with images |
| `/category/:slug` | `CategoryPage` | Posts filtered by category |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000/api` | Laravel API base URL |

## Local Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev
```

The app will be available at `http://localhost:5173`.

## Building for Production

```bash
npm run build
```

Output goes to `dist/`.

## Docker

The frontend is containerized with a multi-stage Docker build:

1. **Builder stage**: Node 20 Alpine installs dependencies and builds the Vite app
2. **Production stage**: Nginx Alpine serves the built assets

The Nginx configuration includes:
- Gzip compression
- Static asset caching (1 year)
- SPA routing fallback (`try_files` to `index.html`)
- Proxy `/api` requests to the Laravel backend

## Design System

The UI uses a newspaper-inspired color palette derived from the Addis Fortune archive:

| Token | Hex | Usage |
|-------|-----|-------|
| `fortune-maroon` | `#800000` | Headings, navbar, category badges |
| `fortune-dark-maroon` | `#420909` | Body headings, author text |
| `fortune-green` | `#008000` | Sidebar active section |
| `fortune-light-blue` | `#b3c7e3` | Category badges, info panels |
| `fortune-light-gray` | `#e4ebf5` | Card backgrounds |
| `fortune-border` | `#cccccc` | Card borders, separators |

Font family: **Verdana** (headlines and body).