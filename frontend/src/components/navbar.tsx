import React, { useState } from "react";
import { useAuth } from "./auth-context";

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { token } = useAuth();

  return (
    <header className="top-0 z-10 bg-background text-foreground lg:sticky">
      <div className="container mx-auto flex items-center justify-between px-4 py-4">
        <h1 className="text-2xl md:text-3xl">SNAPSORTER</h1>

        <nav className="hidden space-x-8 md:flex">
          <a href="/upload" className="hover:text-gray-400">
            SEARCH
          </a>
          <a href="/results" className="hover:text-gray-400">
            DASHBOARD
          </a>
          {token ? (
            <a href="/results" className="hover:text-gray-400">
              MY PROFILE
            </a>
          ) : (
            <a href="/login" className="hover:text-gray-400">
              LOGIN
            </a>
          )}
        </nav>

        <button
          className="text-foreground focus:outline-none md:hidden"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            className="h-6 w-6"
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
        <div className="absolute right-4 top-14 z-50 bg-background px-4 py-4 text-right text-foreground shadow-lg">
          <a href="/upload" className="block py-2 hover:text-gray-400">
            SEARCH
          </a>
          <a href="/results" className="block py-2 hover:text-gray-400">
            DASHBOARD
          </a>
          {token ? (
            <a href="/results" className="block py-2 hover:text-gray-400">
              MY PROFILE
            </a>
          ) : (
            <a href="/login" className="block py-2 hover:text-gray-400">
              LOGIN
            </a>
          )}
        </div>
      )}
    </header>
  );
};

export default Navbar;
