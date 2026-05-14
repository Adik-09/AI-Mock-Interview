import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Camera, Mic, Square, Play, Upload, CheckCircle } from 'lucide-react';
import { questionsData } from '../data/questions';

export default function InterviewPage() {
  const { domain } = useParams();
  const navigate = useNavigate();
  
  const [question, setQuestion] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [timeLeft, setTimeLeft] = useState(60); // 60 seconds per answer
  const [hasPermissions, setHasPermissions] = useState(false);

  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    // Select a random question for the domain
    const domainQuestions = questionsData[domain];
    if (domainQuestions && domainQuestions.length > 0) {
      const randomQ = domainQuestions[Math.floor(Math.random() * domainQuestions.length)];
      setQuestion(randomQ);
    } else {
      setQuestion("Tell me about yourself."); // Fallback
    }
    
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [domain]);

  const requestPermissions = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setHasPermissions(true);
      
      // Initialize MediaRecorder
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };
      
      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'video/webm' });
        submitInterview(blob);
      };
      
    } catch (err) {
      console.error("Error accessing media devices.", err);
      alert("Please allow camera and microphone access to proceed.");
    }
  };

  const readQuestion = () => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(question);
      window.speechSynthesis.speak(utterance);
    }
  };

  const startRecording = () => {
    if (!mediaRecorderRef.current) return;
    chunksRef.current = [];
    mediaRecorderRef.current.start();
    setIsRecording(true);
    readQuestion();
    
    // Start Timer
    setTimeLeft(60);
    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          stopRecording();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsProcessing(true);
      clearInterval(timerRef.current);
      
      // Stop all tracks to turn off camera
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const submitInterview = async (blob) => {
    const formData = new FormData();
    formData.append('video', blob, 'interview.webm');
    formData.append('domain', domain);
    formData.append('question', question);

    try {
      // Use 127.0.0.1 to match Uvicorn's default exactly
      const response = await fetch('http://127.0.0.1:8001/api/evaluate', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const results = await response.json();
        setIsProcessing(false);
        setIsCompleted(true);
        navigate('/report', { state: { results } });
      } else {
        throw new Error('Upload failed');
      }
    } catch (err) {
      console.error(err);
      alert("Failed to submit interview. (Check if backend is running)");
      setIsProcessing(false);
      navigate('/'); // Go back to home on error
    }
  };

  if (isCompleted) {
    return (
      <div className="max-w-2xl mx-auto mt-12 bg-white p-8 rounded-2xl shadow-sm border border-slate-200 text-center">
        <h2 className="text-3xl font-bold text-slate-900 mb-2">Processing Complete</h2>
        <p className="text-slate-600 mb-8">Redirecting to your report...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div className="flex justify-between items-start mb-4">
          <div>
            <span className="inline-block px-3 py-1 bg-slate-100 text-slate-600 rounded-full text-sm font-semibold mb-3 uppercase tracking-wider">
              {domain} Interview
            </span>
            <h2 className="text-2xl font-bold text-slate-900">{question}</h2>
          </div>
          {isRecording && (
            <div className="flex flex-col items-end">
              <div className="flex items-center text-red-500 font-bold animate-pulse">
                <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                Recording
              </div>
              <div className="text-slate-500 font-mono text-xl mt-1">00:{timeLeft.toString().padStart(2, '0')}</div>
            </div>
          )}
        </div>
      </div>

      <div className="relative bg-black rounded-2xl overflow-hidden aspect-video shadow-lg">
        <video 
          ref={videoRef} 
          autoPlay 
          muted 
          playsInline
          className="w-full h-full object-cover"
        />
        
        {!hasPermissions && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/80 text-white">
            <Camera className="w-12 h-12 mb-4 text-slate-400" />
            <h3 className="text-xl font-medium mb-4">Camera & Mic Required</h3>
            <button 
              onClick={requestPermissions}
              className="px-6 py-3 bg-blue-600 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Allow Access
            </button>
          </div>
        )}

        {hasPermissions && !isRecording && !isProcessing && (
          <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-4">
            <button 
              onClick={readQuestion}
              className="w-12 h-12 bg-white/20 backdrop-blur-md text-white rounded-full flex items-center justify-center hover:bg-white/30 transition-all"
              title="Hear Question"
            >
              <Mic className="w-5 h-5" />
            </button>
            <button 
              onClick={startRecording}
              className="px-8 py-3 bg-blue-600 text-white rounded-full font-medium hover:bg-blue-700 shadow-lg flex items-center gap-2"
            >
              <Play className="w-5 h-5 fill-current" />
              Start Answering
            </button>
          </div>
        )}

        {isRecording && (
          <div className="absolute bottom-6 left-1/2 -translate-x-1/2">
            <button 
              onClick={stopRecording}
              className="px-8 py-3 bg-red-600 text-white rounded-full font-medium hover:bg-red-700 shadow-lg flex items-center gap-2"
            >
              <Square className="w-5 h-5 fill-current" />
              Finish Answer
            </button>
          </div>
        )}

        {isProcessing && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/80 text-white">
            <Upload className="w-12 h-12 mb-4 animate-bounce text-blue-400" />
            <h3 className="text-xl font-medium">Uploading & Processing...</h3>
          </div>
        )}
      </div>
    </div>
  );
}
