import { Link } from 'react-router-dom';

export default function PostCard({ post }) {
  const imageCount = post.images ? post.images.length : 0;

  return (
    <article className="fortune-card p-4 hover:shadow-md transition-shadow">
      <div className="border-b border-fortune-border pb-2 mb-2">
        <Link
          to={`/post/${post.id}`}
          className="text-fortune-maroon font-headline font-bold text-base hover:text-red-800 transition-colors leading-tight"
        >
          {post.title}
        </Link>
        {post.subtitle && (
          <p className="text-gray-600 text-xs font-headline mt-1 italic">
            {post.subtitle}
          </p>
        )}
      </div>
      <div className="flex items-center justify-between text-xs font-headline text-gray-500">
        <div className="flex items-center gap-3">
          {post.author && (
            <span className="text-fortune-dark-maroon font-semibold">
              By {post.author}
            </span>
          )}
          {post.category && (
            <span className="bg-fortune-light-blue text-fortune-dark-maroon px-2 py-0.5 rounded text-[10px] font-bold uppercase">
              {post.category}
            </span>
          )}
        </div>
        <div className="flex items-center gap-3">
          {post.published_date && (
            <span>{post.published_date}</span>
          )}
          {imageCount > 0 && (
            <span className="text-fortune-maroon">
              {imageCount} {imageCount === 1 ? 'image' : 'images'}
            </span>
          )}
          {post.word_count && (
            <span>{post.word_count.toLocaleString()} words</span>
          )}
        </div>
      </div>
    </article>
  );
}