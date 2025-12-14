import React from 'react';
import { motion } from 'framer-motion';

export default function Team() {
    const Member = ({ image, name, description, github, linkedin }) => (
        <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="bg-white border border-gray-200 rounded-2xl p-8 transition-all duration-300 ease-in-out shadow-sm hover:transform hover:-translate-y-2 hover:shadow-lg w-full max-w-sm mx-auto"
        >
            <div className="flex justify-center mb-6">
                <img 
                    src={image} 
                    alt={name} 
                    className="w-24 h-24 rounded-full object-cover border-2 border-gray-200 transition-transform duration-300 hover:scale-105"
                />
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center text-ink">{name}</h3>
            <p className="text-sm text-center mb-6 text-muted">{description}</p>
            <div className="flex justify-center gap-6">
                {github && (
                    <a href={github} target="_blank" rel="noreferrer" className="text-muted hover:text-ink transition-colors duration-200">
                        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
                        </svg>
                    </a>
                )}
                {linkedin && (
                    <a href={linkedin} target="_blank" rel="noreferrer" className="text-muted hover:text-ink transition-colors duration-200">
                        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                        </svg>
                    </a>
                )}
            </div>
        </motion.div>
    );

    return (
        <main className="min-h-screen bg-white text-ink pt-20">
            <section className="py-20 px-4 sm:px-6 lg:px-8">
                <div className="max-w-7xl mx-auto">
                    <div className="text-center mb-16">
                        <motion.h1 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6 }}
                            className="text-4xl md:text-5xl font-bold mb-6 text-ink"
                        >
                            Our Team
                        </motion.h1>
                        <motion.p 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className="text-muted text-lg"
                        >
                            Meet the developers behind AdvocaDabra Legal AI
                        </motion.p>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 lg:gap-12 justify-items-center max-w-6xl mx-auto">
                        <Member
                            image="/assets/boi.jpeg"
                            name="P JYE PRAHAAS"
                            description="245523748087"
                            github="https://github.com/Jye-Prahaas"
                            linkedin="https://www.linkedin.com/in/jye-prahaas-pentlavelli-a01085339/"
                        />
                        <Member
                            image="/assets/boi.jpeg"
                            name="K.P. Srinandana Sarma"
                            description="245523748096"
                            github="https://github.com/Swio9152"
                            linkedin="https://www.linkedin.com/in/srinandana-sarma-923104263"
                        />
                        <Member
                            image="/assets/boi.jpeg"
                            name="P SAI KRUTHIN"
                            description="245523748111"
                            github="https://github.com/PSRIKRUTHIN"
                            linkedin="https://www.linkedin.com/in/palatla-sri-kruthin-b326b5286/"
                        />
                        <Member
                            image="/assets/boi.jpeg"
                            name="ABHINAV SHINDE"
                            description="245523748119"
                            github="https://github.com/SAbhinav1608"
                            linkedin="https://www.linkedin.com/in/abhinav-shinde-805765393/"
                        />
                        <Member
                            image="/assets/boi.jpeg"
                            name="UDIT KANDI"
                            description="2455237480122"
                            github="https://github.com/Pluto01"
                            linkedin="https://www.linkedin.com/in/udit-kandi-1005b337b/"
                        />
                    </div>
                </div>
            </section>
        </main>
    );
}
