import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <header className="bg-fortune-maroon text-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-3">
            <div className="bg-white text-fortune-maroon font-bold text-xl px-2 py-1 rounded">
              AF
            </div>
            <div>
              <h1 className="font-headline font-bold text-lg leading-tight">
                Addis Fortune
              </h1>
              <p className="text-xs text-red-200 font-headline">
                Content Matters
              </p>
            </div>
          </Link>
          <nav className="hidden md:flex items-center space-x-6">
            <Link
              to="/"
              className="text-sm font-headline hover:text-red-200 transition-colors"
            >
              Home
            </Link>
          </nav>
        </div>
      </div>
      <div className="bg-fortune-dark-maroon h-1" />
    </header>
  );
}