import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 backdrop-blur-xl bg-white/80 border-b border-gray-200 relative">      <div className="max-w-6xl mx-auto px-4 md:px-6 h-14 flex items-center justify-between">
        {/* Logo - absolute to extreme left */}
        <Link to="/" className="absolute left-0 pl-4 flex items-center hover:opacity-80 transition-opacity">
          <img 
            src="/assets/advoca-dabra.jpeg" 
            alt="AdvocaDabra" 
            className="h-12 md:h-16 lg:h-20 w-auto"
          />
        </Link>
        {/* Desktop menu - absolute to extreme right */}
        <nav className="hidden md:flex items-center gap-8 text-[14px] text-gray-600 absolute right-0 pr-4">
          <Link to="/login" className="hover:text-gray-900">Login</Link>
          <Link to="/signup" className="hover:text-gray-900">Signup</Link>
        </nav>

      </div>
    </header>
  );
}
