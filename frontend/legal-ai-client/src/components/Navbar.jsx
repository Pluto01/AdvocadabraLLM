import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 backdrop-blur-xl bg-white/80 border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 md:px-6 h-14 flex items-center justify-between">        {/* Logo */}
        <Link to="/" className="text-[15px] font-medium text-gray-900">
          Legal AI
        </Link>

        {/* Desktop menu */}
        <nav className="hidden md:flex items-center gap-8 text-[14px] text-gray-600">
          <Link to="/" className="hover:text-gray-900">Home</Link>
          <Link to="/login" className="hover:text-gray-900">Login</Link>
          <Link to="/signup" className="hover:text-gray-900">Signup</Link>
          {/* Dashboard removed */}
        </nav>

      </div>
    </header>
  );
}
