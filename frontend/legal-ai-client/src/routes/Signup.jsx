import React, { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.jsx";

export default function Signup() {
  const { user, signup } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!name.trim()) {
      setError("Please enter your full name");
      return;
    }

    if (!email.trim()) {
      setError("Please enter your email address");
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError("Please enter a valid email address");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setIsLoading(true);

    try {
      const result = await signup(email, password, name);
      if (result.success) {
        navigate("/dashboard");
      } else {
        setError(result.error || "Signup failed");
      }
    } catch (error) {
      setError("An unexpected error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Apple-style Logo Area */}
        <div className="text-center mb-12">
          <div className="w-16 h-16 mx-auto mb-8 bg-black rounded-3xl flex items-center justify-center">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14,2 14,8 20,8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10,9 9,9 8,9"/>
            </svg>
          </div>
          <h1 className="text-4xl font-semibold text-gray-900 mb-3">
            Legal AI
          </h1>
          <p className="text-xl text-gray-600 font-medium">
            Create your account
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-2xl mb-8 text-center">
            {error}
          </div>
        )}

        {/* Sign Up Form */}
        <div className="bg-white rounded-3xl shadow-xl border border-gray-100 p-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-6 py-4 border border-gray-200 rounded-2xl bg-gray-50 text-gray-900 text-lg focus:bg-white focus:border-gray-400 focus:outline-none transition-all placeholder:text-gray-500"
                placeholder="Full Name"
                required
                disabled={isLoading}
              />
            </div>

            <div>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-6 py-4 border border-gray-200 rounded-2xl bg-gray-50 text-gray-900 text-lg focus:bg-white focus:border-gray-400 focus:outline-none transition-all placeholder:text-gray-500"
                placeholder="Email"
                required
                disabled={isLoading}
              />
            </div>

            <div>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-6 py-4 border border-gray-200 rounded-2xl bg-gray-50 text-gray-900 text-lg focus:bg-white focus:border-gray-400 focus:outline-none transition-all placeholder:text-gray-500"
                placeholder="Password (min 6 characters)"
                required
                disabled={isLoading}
              />
            </div>

            <div>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-6 py-4 border border-gray-200 rounded-2xl bg-gray-50 text-gray-900 text-lg focus:bg-white focus:border-gray-400 focus:outline-none transition-all placeholder:text-gray-500"
                placeholder="Confirm Password"
                required
                disabled={isLoading}
              />
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={isLoading || !name || !email || !password || !confirmPassword}
                className="w-full bg-black text-white py-4 px-6 rounded-2xl font-semibold text-lg hover:bg-gray-800 focus:bg-gray-800 focus:outline-none transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Creating Account...
                  </span>
                ) : (
                  'Create Account'
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Sign In Link */}
        <div className="text-center mt-8">
          <p className="text-gray-600">
            Already have an account?{' '}
            <Link 
              to="/login" 
              className="text-black font-semibold hover:underline transition-all"
            >
              Sign in
            </Link>
          </p>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-sm text-gray-500">
          <p>Join thousands of legal professionals using AI-powered document analysis</p>
        </div>
      </div>
    </div>
  );
}
