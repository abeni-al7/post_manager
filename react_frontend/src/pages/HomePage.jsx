import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import PostCard from '../components/PostCard';
import SearchBar from '../components/SearchBar';
import Pagination from '../components/Pagination';
import { getPosts } from '../services/api';

export default function HomePage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [posts, setPosts] = useState([]);
  const [paginationMeta, setPaginationMeta] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const page = parseInt(searchParams.get('page') || '1', 10);
  const category = searchParams.get('category') || '';
  const search = searchParams.get('search') || '';
  const sort = searchParams.get('sort') || 'published_date';
  const direction = searchParams.get('direction') || 'desc';

  const fetchPosts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = { page, per_page: 15 };
      if (category) params.category = category;
      if (search) params.search = search;
      if (sort) params.sort = sort;
      if (direction) params.direction = direction;

      const data = await getPosts(params);
      setPosts(data.data || []);
      setPaginationMeta(data.meta || null);
    } catch (err) {
      setError('Failed to load posts. Please try again later.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [page, category, search, sort, direction]);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  const updateParam = (key, value) => {
    const newParams = new URLSearchParams(searchParams);
    if (value) {
      newParams.set(key, value);
    } else {
      newParams.delete(key);
    }
    if (key !== 'page') {
      newParams.delete('page');
    }
    setSearchParams(newParams);
  };

  const handlePageChange = (newPage) => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    updateParam('page', String(newPage));
  };

  const handleSearchChange = (value) => {
    updateParam('search', value);
  };

  const handleCategoryChange = (cat) => {
    const newParams = new URLSearchParams();
    if (cat) newParams.set('category', cat);
    setSearchParams(newParams);
  };

  return (
    <div>
      <div className="mb-6 space-y-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1">
            <SearchBar value={search} onChange={handleSearchChange} />
          </div>
        </div>
        {category && (
          <div className="flex items-center gap-2">
            <span className="text-xs font-headline text-gray-500 uppercase">
              Filtered by:
            </span>
            <span className="bg-fortune-light-blue text-fortune-dark-maroon px-2 py-1 rounded text-xs font-headline font-bold">
              {category}
            </span>
            <button
              onClick={() => handleCategoryChange('')}
              className="text-xs text-fortune-maroon hover:text-red-800 font-headline underline"
            >
              Clear filter
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4 text-sm font-headline">
          {error}
        </div>
      )}

      {loading ? (
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="fortune-card p-4 animate-pulse">
              <div className="h-5 bg-gray-200 rounded w-3/4 mb-2" />
              <div className="h-3 bg-gray-200 rounded w-1/2" />
            </div>
          ))}
        </div>
      ) : posts.length === 0 ? (
        <div className="fortune-card p-8 text-center">
          <p className="text-gray-500 font-headline">No articles found.</p>
          {search && (
            <p className="text-sm text-gray-400 mt-1 font-headline">
              Try adjusting your search terms.
            </p>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          {posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      )}

      {!loading && posts.length > 0 && (
        <Pagination meta={paginationMeta} onPageChange={handlePageChange} />
      )}
    </div>
  );
}