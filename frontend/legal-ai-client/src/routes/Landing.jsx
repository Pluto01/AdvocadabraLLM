import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <main className="min-h-screen bg-white text-ink">

      {/* HERO */}
      <section className="pt-20 pb-24">
        <div className="max-w-6xl mx-auto px-4 md:px-6 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          {/* LEFT */}
          <div>
            <h1 className="text-4xl md:text-6xl font-semibold leading-tight">
              Advoca-Dabra  
              <span className="block text-muted text-xl md:text-2xl mt-3">
                AI-powered legal judgment analysis & prediction.
              </span>
            </h1>

            <p className="mt-6 text-muted max-w-xl text-base md:text-lg">
              A clean, modern interface designed to help lawyers, students, and 
              researchers understand case outcomes faster and more reliably.
            </p>

            <div className="mt-8 flex gap-3">
              <Link
                className="px-6 py-3 rounded-full bg-ink text-white text-sm font-medium"
                to="/signup"
              >
                Get Started
              </Link>

              <Link
                className="px-6 py-3 rounded-full border border-gray-300 text-sm"
                to="/login"
              >
                Login
              </Link>
            </div>
          </div>

          {/* RIGHT — Hero Image */}
          <div className="rounded-3xl shadow-subtle overflow-hidden">
            <img
              src="/assets/product-demo.jpg"
              className="w-full h-full object-cover"
              alt="Advoca-Dabra preview"
            />
          </div>
        </div>
      </section>


      {/* FEATURES SECTION */}
      <section className="max-w-6xl mx-auto px-4 md:px-6 pb-20">
        <h2 className="text-3xl font-semibold mb-6">Built for clarity</h2>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              title: "Judgment Prediction",
              desc: "AI-generated verdict tendency and reasoning based on case patterns."
            },
            {
              title: "Explainability",
              desc: "Clear bullet-point explanations that break down model decisions."
            },
            {
              title: "Document Management",
              desc: "Upload case files and analyze them through a clean, simple workflow."
            },
          ].map((item) => (
            <div
              key={item.title}
              className="bg-white border border-gray-200 rounded-2xl p-6 shadow-subtle"
            >
              <h3 className="text-lg font-medium">{item.title}</h3>
              <p className="text-muted text-sm mt-2">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>


      {/* PREVIEW SECTION */}
      <section className="max-w-6xl mx-auto px-4 md:px-6 pb-24">
        <div className="rounded-3xl border border-gray-200 bg-gray-50 p-6 shadow-soft">
          <h2 className="text-2xl font-semibold">Dashboard Preview</h2>
          <p className="text-muted text-sm mt-1 mb-4">
            A modern workspace for analyzing legal documents.
          </p>

          <div className="rounded-2xl overflow-hidden border border-gray-200">
            <img
              src="/assets/dashboard-preview.jpg"
              alt="Dashboard"
              className="w-full"
            />
          </div>
        </div>
      </section>


      {/* CALL TO ACTION */}
      <section className="max-w-6xl mx-auto px-4 md:px-6 pb-20">
        <div className="rounded-3xl border border-gray-300 bg-white p-8 text-center shadow-subtle">
          <h2 className="text-2xl font-semibold">Start analyzing smarter.</h2>
          <p className="text-muted mt-2 text-sm">
            Create an account and try Advoca-Dabra today.
          </p>

          <div className="mt-6 flex justify-center gap-3">
            <Link to="/signup" className="px-6 py-3 rounded-full bg-ink text-white text-sm">
              Create Account
            </Link>
            <Link to="/login" className="px-6 py-3 rounded-full border border-gray-300 text-sm">
              Login
            </Link>
          </div>
        </div>
      </section>

    </main>
  );
}
