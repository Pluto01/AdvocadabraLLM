import React from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import { AuthProvider } from "./Auth.jsx";
import Navbar from "./components/Navbar.jsx";
import Landing from "./routes/Landing.jsx";
import Signup from "./routes/Signup.jsx";
import Dashboard from "./routes/Dashboard.jsx";
import Login from "./routes/Login.jsx";
import Team from "./routes/Team.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

function AppContent() {
  const location = useLocation();
  // Hide navbar on dashboard (authenticated pages)
  const showNavbar = location.pathname !== '/dashboard';

  return (
    <div className="min-h-screen bg-white text-gray-900">
      {showNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/team" element={<Team />} />
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
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
