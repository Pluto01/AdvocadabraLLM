import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <main className="min-h-screen bg-white text-ink">

      {/* HERO */}
      <section className="pt-20 pb-24">
        <div className="max-w-6xl mx-auto px-4 md:px-6 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">          {/* LEFT */}
          <div>
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-4xl md:text-6xl font-semibold leading-tight"
            >
              AdvocaDabra  
              <span className="block text-muted text-xl md:text-2xl mt-3">
                AI-powered legal judgment analysis & prediction.
              </span>
            </motion.h1><motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="mt-6 text-muted max-w-xl text-base md:text-lg"
            >
              A clean, modern interface designed to help lawyers, students, and 
              researchers understand case outcomes faster and more reliably.
            </motion.p>

            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="mt-8 flex gap-3"
            >              <Link
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
            </motion.div>
          </div>          {/* RIGHT — Logo Display */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex items-center justify-center p-8"
          >
            <img
              src="/assets/advoca-dabra.jpeg"
              className="w-full max-w-lg h-auto object-contain rounded-2xl shadow-lg"
              alt="AdvocaDabra Logo"
            />
          </motion.div>
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
