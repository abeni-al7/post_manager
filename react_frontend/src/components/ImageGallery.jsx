import { useState } from 'react';

export default function ImageGallery({ images }) {
  const [lightboxIndex, setLightboxIndex] = useState(null);

  if (!images || images.length === 0) return null;

  const openLightbox = (index) => setLightboxIndex(index);
  const closeLightbox = () => setLightboxIndex(null);

  const goNext = (e) => {
    e.stopPropagation();
    setLightboxIndex((prev) => (prev + 1) % images.length);
  };

  const goPrev = (e) => {
    e.stopPropagation();
    setLightboxIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  return (
    <div className="mt-6">
      <h3 className="font-headline font-bold text-fortune-dark-maroon text-sm uppercase mb-3 border-b border-fortune-border pb-1">
        Related Images ({images.length})
      </h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        {images.map((img, index) => (
          <button
            key={img.id}
            onClick={() => openLightbox(index)}
            className="group relative aspect-video bg-gray-100 rounded overflow-hidden border border-fortune-border hover:shadow-md transition-shadow"
          >
            <img
              src={img.image_path}
              alt={img.alt_text || `Image ${index + 1}`}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = `https://placehold.co/400x225/e4ebf5/800000?text=${encodeURIComponent(img.alt_text || 'Image')}`;
              }}
            />
            {img.alt_text && (
              <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/60 to-transparent p-2">
                <p className="text-white text-[10px] font-headline truncate">
                  {img.alt_text}
                </p>
              </div>
            )}
          </button>
        ))}
      </div>

      {/* Lightbox */}
      {lightboxIndex !== null && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
          onClick={closeLightbox}
        >
          <button
            onClick={closeLightbox}
            className="absolute top-4 right-4 text-white hover:text-gray-300 z-10"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          {images.length > 1 && (
            <>
              <button
                onClick={goPrev}
                className="absolute left-4 text-white hover:text-gray-300 z-10"
              >
                <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                onClick={goNext}
                className="absolute right-4 text-white hover:text-gray-300 z-10"
              >
                <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </>
          )}

          <div className="max-w-4xl max-h-[90vh]" onClick={(e) => e.stopPropagation()}>
            <img
              src={images[lightboxIndex].image_path}
              alt={images[lightboxIndex].alt_text || `Image ${lightboxIndex + 1}`}
              className="max-w-full max-h-[85vh] object-contain rounded"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = `https://placehold.co/800x600/e4ebf5/800000?text=${encodeURIComponent(images[lightboxIndex].alt_text || 'Image')}`;
              }}
            />
            {images[lightboxIndex].alt_text && (
              <p className="text-white text-sm text-center mt-2 font-headline">
                {images[lightboxIndex].alt_text}
              </p>
            )}
            <p className="text-gray-400 text-xs text-center mt-1 font-headline">
              {lightboxIndex + 1} / {images.length}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}