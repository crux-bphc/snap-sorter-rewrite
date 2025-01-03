import React, { useState } from "react";
import { useAuth } from "./auth-context";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { token } = useAuth();

  return (
    <header className="top-0 z-10 bg-background text-foreground lg:sticky">
      <div className="container mx-auto flex items-center justify-between px-4 py-4">
        <Link to="/" className="text-2xl uppercase md:text-3xl">
          Snapsorter
        </Link>

        <nav className="hidden space-x-8 md:flex">
          <Link to="/upload" className="uppercase hover:text-gray-400">
            Search
          </Link>
          <Link to="/results" className="uppercase hover:text-gray-400">
            Dashboard
          </Link>
          <Link
            to={token ? "/results" : "/login"}
            className="uppercase hover:text-gray-400"
          >
            {token ? "My profile" : "login"}
          </Link>
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
          <Link to="/upload" className="py-2 uppercase hover:text-gray-400">
            Search
          </Link>
          <Link to="/results" className="py-2 uppercase hover:text-gray-400">
            Dashboard
          </Link>
          <Link
            to={token ? "/results" : "/login"}
            className="py-2 uppercase hover:text-gray-400"
          >
            {token ? "My profile" : "login"}
          </Link>
        </div>
      )}
    </header>
  );
};

export default Navbar;
