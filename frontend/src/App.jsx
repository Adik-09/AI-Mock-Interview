import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import InterviewPage from './components/InterviewPage';
import ReportPage from './components/ReportPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
        <header className="bg-white shadow-sm sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                AI
              </div>
              <h1 className="text-xl font-semibold tracking-tight text-slate-800">Mock Interview System</h1>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/interview/:domain" element={<InterviewPage />} />
            <Route path="/report" element={<ReportPage />} />
          </Routes>
        </main>
        
        <footer className="mt-auto py-6 border-t border-slate-200 text-center text-sm text-slate-500">
          Lightweight AI-Assisted Mock Interview System
        </footer>
      </div>
    </Router>
  );
}

export default App;
