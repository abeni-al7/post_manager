import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 max-w-7xl mx-auto w-full px-4 py-6">
        <div className="flex flex-col md:flex-row gap-6">
          <Sidebar />
          <main className="flex-1 min-w-0">
            <Outlet />
          </main>
        </div>
      </div>
      <footer className="bg-fortune-dark-maroon text-white py-4 mt-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-xs font-headline">
          <p>Addis Fortune &copy; 2024. Content Matters.</p>
          <p className="text-red-300 mt-1">
            Post Manager System &mdash; Full-Stack Technical Exam
          </p>
        </div>
      </footer>
    </div>
  );
}