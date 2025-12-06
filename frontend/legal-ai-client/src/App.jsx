import React from "react";
import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./hooks/useAuth.jsx";
import Navbar from "./components/Navbar.jsx";
import Landing from "./routes/Landing.jsx";
import Signup from "./routes/Signup.jsx";
import Dashboard from "./routes/Dashboard.jsx";
import Login from "./routes/Login.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-white text-gray-900">
        <Navbar />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* 🔒 Protect Dashboard */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </AuthProvider>
  );
}
