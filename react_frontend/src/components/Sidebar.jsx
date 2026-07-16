import { Link, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { getCategories } from '../services/api';

export default function Sidebar() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await getCategories();
        setCategories(response.data || []);
      } catch (err) {
        console.error('Failed to fetch categories:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchCategories();
  }, []);

  const currentCategory = new URLSearchParams(location.search).get('category');

  return (
    <aside className="w-full md:w-56 flex-shrink-0">
      <div className="bg-white border border-fortune-border rounded-sm overflow-hidden">
        <div className="bg-fortune-green text-white px-4 py-2 font-headline font-bold text-sm uppercase tracking-wide">
          Categories
        </div>
        <nav className="py-1">
          <Link
            to="/"
            className={`block px-4 py-2 text-sm font-headline border-l-2 transition-colors ${
              !currentCategory && location.pathname === '/'
                ? 'border-fortune-green bg-green-50 text-fortune-green font-bold'
                : 'border-transparent text-gray-700 hover:bg-gray-50 hover:border-fortune-border'
            }`}
          >
            All Posts
          </Link>
          {loading ? (
            <div className="px-4 py-2 text-sm text-gray-400">Loading...</div>
          ) : (
            categories.map((cat) => (
              <Link
                key={cat}
                to={`/?category=${encodeURIComponent(cat)}`}
                className={`block px-4 py-2 text-sm font-headline border-l-2 transition-colors ${
                  currentCategory === cat
                    ? 'border-fortune-green bg-green-50 text-fortune-green font-bold'
                    : 'border-transparent text-gray-700 hover:bg-gray-50 hover:border-fortune-border'
                }`}
              >
                {cat}
              </Link>
            ))
          )}
        </nav>
      </div>
    </aside>
  );
}