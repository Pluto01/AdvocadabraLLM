import React from 'react';

// Since boi.jpg doesn't exist yet, using a placeholder
// Once you add boi.jpg to public/assets/, update this import to:
// import boiImage from '../../public/assets/boi.jpg';
const boiImage = '/assets/placeholder-avatar.jpg';

function Team() {
  const Member = ({ image, name, description, github, linkedin }) => (
    <div className="border rounded-2xl p-8 transition-all duration-300 ease-in-out shadow-sm hover:transform hover:-translate-y-2 hover:shadow-lg w-full max-w-sm mx-auto bg-white"
         style={{ 
             borderColor: '#e5e7eb'
         }}>
      <div className="flex justify-center mb-6">
        <img 
          src={image} 
          alt={`${name}`} 
          className="w-24 h-24 rounded-full object-cover border-2 transition-transform duration-300 hover:scale-105"
          style={{ borderColor: '#e5e7eb' }}
        />
      </div>
      <h3 className="text-xl font-semibold mb-3 text-center text-gray-900">{name}</h3>
      <p className="text-sm text-center mb-6 text-gray-600">{description}</p>
      <div className="flex justify-center gap-6">
        {github && (
          <a href={github} target="_blank" rel="noreferrer">
            <i className="fab fa-github text-2xl transition-all duration-200 hover:scale-110 text-gray-600 hover:text-gray-900"></i>
          </a>
        )}
        {linkedin && (
          <a href={linkedin} target="_blank" rel="noreferrer">
            <i className="fab fa-linkedin text-2xl transition-all duration-200 hover:scale-110 text-gray-600 hover:text-gray-900"></i>
          </a>
        )}
      </div>
    </div>
  );

  const teamMembers = [
    {
      image: boiImage,
      name: "UDIT KANDI",
      description: "2455237480122",
      github: "https://github.com/Pluto01",
      linkedin: "https://www.linkedin.com/in/udit-kandi-1005b337b/"
    },
    {
      image: boiImage,
      name: "P SAI KRUTHIN",
      description: "245523748111",
      github: "https://github.com/PSRIKRUTHIN",
      linkedin: "https://www.linkedin.com/in/palatla-sri-kruthin-b326b5286/"
    },
    {
      image: boiImage,
      name: "P JYE PRAHAAS",
      description: "245523748087",
      github: "https://github.com/Jye-Prahaas",
      linkedin: "https://www.linkedin.com/in/jye-prahaas-pentlavelli-a01085339/"
    },
    {
      image: boiImage,
      name: "K.P. Srinandana Sarma",
      description: "245523748096",
      github: "https://github.com/Swio9152",
      linkedin: "https://www.linkedin.com/in/srinandana-sarma-923104263"
    },
    {
      image: boiImage,
      name: "SHINDE ABHINAV",
      description: "245523748119",
      github: "https://github.com/SAbhinav1608",
      linkedin: "https://www.linkedin.com/in/abhinav-shinde-805765393/"
    }
  ];

  return (
    <div className="min-h-screen bg-white text-gray-900">
      {/* Team Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 pt-32">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">Our Team</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Meet the talented developers behind AdvocaDabra
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 lg:gap-12 justify-items-center max-w-6xl mx-auto">
            {teamMembers.map((member, index) => (
              <Member
                key={index}
                image={member.image}
                name={member.name}
                description={member.description}
                github={member.github}
                linkedin={member.linkedin}
              />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default Team;
