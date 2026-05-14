import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Code, Database, Brain, Users } from 'lucide-react';

const domains = [
  { id: 'python', name: 'Python', icon: Code, description: 'Core Python concepts, data structures, and algorithms.' },
  { id: 'dbms', name: 'DBMS', icon: Database, description: 'Database design, SQL queries, and normalization.' },
  { id: 'ml', name: 'Machine Learning', icon: Brain, description: 'Algorithms, model evaluation, and concepts.' },
  { id: 'hr', name: 'HR / Behavioral', icon: Users, description: 'Soft skills, teamwork, and behavioral questions.' },
];

export default function LandingPage() {
  const navigate = useNavigate();

  const handleStart = (domainId) => {
    navigate(`/interview/${domainId}`);
  };

  return (
    <div className="flex flex-col items-center justify-center py-12 space-y-12">
      <div className="text-center space-y-4 max-w-2xl">
        <h2 className="text-4xl font-extrabold text-slate-900 tracking-tight sm:text-5xl">
          Ace Your Next Interview
        </h2>
        <p className="text-lg text-slate-600">
          Practice with our AI-assisted mock interview system. Answer questions, record your responses, and get instant feedback on technical accuracy and communication skills.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
        {domains.map((domain) => {
          const Icon = domain.icon;
          return (
            <div 
              key={domain.id}
              className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:shadow-md hover:border-blue-300 transition-all cursor-pointer group"
              onClick={() => handleStart(domain.id)}
            >
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-blue-50 text-blue-600 rounded-lg group-hover:bg-blue-600 group-hover:text-white transition-colors">
                  <Icon size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 mb-1">{domain.name}</h3>
                  <p className="text-slate-500 mb-4">{domain.description}</p>
                  <span className="text-blue-600 font-medium inline-flex items-center text-sm group-hover:text-blue-700">
                    Start Interview &rarr;
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
