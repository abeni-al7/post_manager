import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getPost, getPostImages } from '../services/api';
import ImageGallery from '../components/ImageGallery';

export default function PostDetailPage() {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPost = async () => {
      setLoading(true);
      setError(null);
      try {
        const [postRes, imagesRes] = await Promise.all([
          getPost(id),
          getPostImages(id),
        ]);
        setPost(postRes.data);
        setImages(imagesRes.data || []);
      } catch (err) {
        setError('Failed to load article. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchPost();
  }, [id]);

  if (loading) {
    return (
      <div className="fortune-card p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-7 bg-gray-200 rounded w-3/4" />
          <div className="h-4 bg-gray-200 rounded w-1/2" />
          <div className="space-y-2">
            <div className="h-3 bg-gray-200 rounded" />
            <div className="h-3 bg-gray-200 rounded" />
            <div className="h-3 bg-gray-200 rounded w-5/6" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="fortune-card p-8 text-center">
        <p className="text-red-600 font-headline">{error || 'Article not found.'}</p>
        <Link to="/" className="fortune-btn inline-block mt-4">
          Back to Home
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="fortune-card p-6">
        <div className="border-b border-fortune-border pb-3 mb-4">
          <h1 className="text-2xl font-headline font-bold text-fortune-maroon leading-tight">
            {post.title}
          </h1>
          {post.subtitle && (
            <p className="text-gray-600 font-headline mt-2 italic text-base">
              {post.subtitle}
            </p>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-3 text-xs font-headline text-gray-500 mb-6">
          {post.author && (
            <span className="text-fortune-dark-maroon font-semibold">
              By {post.author}
            </span>
          )}
          {post.category && (
            <span className="bg-fortune-light-blue text-fortune-dark-maroon px-2 py-1 rounded font-bold uppercase">
              {post.category}
            </span>
          )}
          {post.published_date && (
            <span>{post.published_date}</span>
          )}
          {post.volume && post.issue_number && (
            <span>Vol. {post.volume} No. {post.issue_number}</span>
          )}
          {post.word_count && (
            <span>{post.word_count.toLocaleString()} words</span>
          )}
        </div>

        {post.source_file && (
          <div className="text-[10px] text-gray-400 font-headline mb-4">
            Source: {post.source_file}
          </div>
        )}

        <div className="prose prose-sm max-w-none">
          {post.content ? (
            <div
              className="text-gray-800 font-headline text-sm leading-relaxed whitespace-pre-line"
              dangerouslySetInnerHTML={{ __html: post.content }}
            />
          ) : (
            <p className="text-gray-500 italic font-headline text-sm">
              No content available for this article.
            </p>
          )}
        </div>
      </div>

      <ImageGallery images={images} />
    </div>
  );
}