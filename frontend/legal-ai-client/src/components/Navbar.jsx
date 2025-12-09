import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 backdrop-blur-xl bg-gray-100 border-b border-gray-200 relative">
      {/* Logo - absolute to extreme left */}
      <div className="absolute left-0 top-0 h-16 flex items-center pl-4">
        <Link to="/" className="flex items-center hover:opacity-80 transition-opacity">
          <img
            src="/assets/advoca-dabra.jpeg"
            alt="AdvocaDabra"
            className="h-12 md:h-16 lg:h-20 w-auto"
          />
        </Link>
      </div>

      <div className="max-w-6xl mx-auto px-4 md:px-6 h-16 flex items-center justify-center">
        {/* Desktop menu - absolute to extreme right */}
        <nav className="hidden md:flex items-center gap-8 text-[14px] text-gray-600 absolute right-0 pr-4">
          <Link to="/team" className="hover:text-gray-900">Team</Link>
          <Link to="/login" className="hover:text-gray-900">Login</Link>
          <Link to="/signup" className="hover:text-gray-900">Signup</Link>
        </nav>
      </div>
    </header>
  );
}
