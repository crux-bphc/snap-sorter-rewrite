import React, { useState } from "react";

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-background text-foreground">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <h1 className="text-2xl md:text-3xl">SNAPSORTER</h1>

        <nav className="hidden md:flex space-x-8">
          <a href="#search" className="hover:text-gray-400">
            SEARCH
          </a>
          <a href="#dashboard" className="hover:text-gray-400">
            DASHBOARD
          </a>
          <a href="#profile" className="hover:text-gray-400">
            MY PROFILE
          </a>
        </nav>

        <button
          className="md:hidden text-foreground focus:outline-none"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16m-7 6h7"
            />
          </svg>
        </button>
      </div>

      {isMenuOpen && (
        <div className="absolute top-14 right-4 bg-background text-foreground px-4 py-4 shadow-lg z-50 text-right">
          <a href="#search" className="block py-2 hover:text-gray-400">
            SEARCH
          </a>
          <a href="#dashboard" className="block py-2 hover:text-gray-400">
            DASHBOARD
          </a>
          <a href="#profile" className="block py-2 hover:text-gray-400">
            MY PROFILE
          </a>
        </div>
      )}
    </header>
  );
};

export default Navbar;
