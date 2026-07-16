import { useParams } from 'react-router-dom';
import { useState } from 'react';
import PostCard from '../components/PostCard';
import Pagination from '../components/Pagination';
import { getPosts } from '../services/api';

export default function CategoryPage() {
  const { slug } = useParams();

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-xl font-headline font-bold text-fortune-maroon border-b border-fortune-border pb-2">
          Category: {decodeURIComponent(slug)}
        </h2>
        <p className="text-xs text-gray-500 font-headline mt-1">
          Browse all articles in this category
        </p>
      </div>
      <CategoryPosts category={decodeURIComponent(slug)} />
    </div>
  );
}

function CategoryPosts({ category }) {
  const [posts, setPosts] = useState([]);
  const [paginationMeta, setPaginationMeta] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchPosts = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getPosts({ page, per_page: 15, category });
        setPosts(data.data || []);
        setPaginationMeta(data.meta || null);
      } catch (err) {
        setError('Failed to load posts. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, [category, page]);

  const handlePageChange = (newPage) => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    setPage(newPage);
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="fortune-card p-4 animate-pulse">
            <div className="h-5 bg-gray-200 rounded w-3/4 mb-2" />
            <div className="h-3 bg-gray-200 rounded w-1/2" />
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="fortune-card p-8 text-center">
        <p className="text-red-600 font-headline">{error}</p>
      </div>
    );
  }

  if (posts.length === 0) {
    return (
      <div className="fortune-card p-8 text-center">
        <p className="text-gray-500 font-headline">No articles found in this category.</p>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-4">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
      <Pagination meta={paginationMeta} onPageChange={handlePageChange} />
    </>
  );
}