import React, { useMemo } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import {
  Download,
  ArrowLeft,
  Award,
  Brain,
  TrendingUp,
  Mic,
  Video,
  CheckCircle2,
  AlertTriangle,
  BarChart3,
  ShieldCheck,
  Eye,
  Activity,
  Users,
  Camera,
  Info,
  MessageSquare,
  Zap,
  Target
} from 'lucide-react';

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  PieChart,
  Pie,
} from 'recharts';

export default function ReportPage() {

  const location = useLocation();
  const navigate = useNavigate();

  const results = location.state?.results;

  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center bg-white p-12 rounded-3xl shadow-xl border border-slate-200">
          <AlertTriangle className="w-16 h-16 text-rose-500 mx-auto mb-6" />
          <h2 className="text-3xl font-bold text-slate-900">No report data found</h2>
          <p className="text-slate-500 mt-2">Please complete an interview first.</p>
          <button
            onClick={() => navigate('/')}
            className="mt-8 px-8 py-4 bg-indigo-600 text-white rounded-2xl font-bold hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-100"
          >
            Return Home
          </button>
        </div>
      </div>
    );
  }

  const {
    domain,
    question,
    transcript,
    technical_analysis,
    audio_analysis,
    video_analysis,
    performance_summary,
    overall_score
  } = results;

  // ---------------------------------------------------
  // RADAR DATA
  // ---------------------------------------------------
  const radarData = [
    { metric: "Technical", value: technical_analysis.score || 0 },
    { metric: "Grammar", value: technical_analysis.metrics?.grammar_score || 0 },
    { metric: "Vocabulary", value: technical_analysis.metrics?.vocabulary_score || 0 },
    { metric: "Confidence", value: technical_analysis.metrics?.confidence_score || 0 },
    { metric: "Fluency", value: audio_analysis.fluency_score || 0 },
    { metric: "Behavior", value: video_analysis.behavior_score || 0 },
    { metric: "Relevance", value: technical_analysis.topic_relevance || 0 }
  ];

  const fillerData = useMemo(() => {
    return Object.entries(audio_analysis.fillers_detected || {}).map(([word, count]) => ({
      word, count
    }));
  }, [audio_analysis]);

  const handleDownload = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8001/api/download_report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(results),
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `AI_Mock_Interview_Report_${domain}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      } else {
        alert("Failed to download report.");
      }
    } catch (err) {
      console.error(err);
      alert("Error downloading report.");
    }
  };

  return (
    <div className="max-w-7xl mx-auto pb-24 space-y-8 animate-in fade-in duration-1000">

      {/* HEADER */}
      <div className="bg-white rounded-[2.5rem] border border-slate-200 shadow-sm p-8 flex flex-col lg:flex-row justify-between items-center gap-6">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <div className="px-4 py-1 bg-indigo-50 text-indigo-600 rounded-full text-xs font-bold uppercase tracking-wider">
              {domain} Domain
            </div>
            <div className="px-4 py-1 bg-emerald-50 text-emerald-600 rounded-full text-xs font-bold uppercase tracking-wider">
              AI Certified
            </div>
          </div>
          <h1 className="text-4xl font-black text-slate-900 leading-tight">
            Interview Intelligence <span className="text-indigo-600">Report</span>
          </h1>
          <p className="text-slate-500 mt-2 font-medium">Question: "{question}"</p>
        </div>

        <div className="flex gap-4">
          <button onClick={() => navigate('/')} className="px-6 py-4 bg-slate-100 text-slate-700 rounded-2xl font-bold hover:bg-slate-200 transition-all flex items-center gap-2">
            <ArrowLeft className="w-5 h-5" /> Retry
          </button>
          <button onClick={handleDownload} className="px-8 py-4 bg-indigo-600 text-white rounded-2xl font-bold hover:bg-indigo-700 transition-all shadow-xl shadow-indigo-100 flex items-center gap-2">
            <Download className="w-5 h-5" /> Export PDF
          </button>
        </div>
      </div>

      {/* OVERALL SCORE HERO */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1 bg-slate-900 rounded-[3rem] p-12 text-white relative overflow-hidden shadow-2xl">
          <div className="absolute -right-10 -top-10 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl"></div>
          <Award className="w-16 h-16 text-indigo-400 mb-8" />
          <h3 className="text-slate-400 font-bold uppercase tracking-widest text-sm mb-2">Overall Interview Index</h3>
          <div className="text-9xl font-black tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white to-slate-400">
            {Math.round(overall_score)}
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-white/10 rounded-2xl border border-white/10 w-fit">
            <Zap className="w-4 h-4 text-yellow-400" />
            <span className="text-sm font-bold">{performance_summary.overall_rating} Performance</span>
          </div>
        </div>

        <div className="lg:col-span-2 bg-white rounded-[3rem] p-10 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-3 mb-6 text-indigo-600">
              <Brain className="w-6 h-6" />
              <h3 className="text-xl font-bold">AI Semantic Insights</h3>
            </div>
            <p className="text-2xl text-slate-700 leading-relaxed font-semibold italic">
              "{technical_analysis.feedback}"
            </p>
          </div>
          
          <div className="grid grid-cols-3 gap-6 pt-10 border-t border-slate-100">
            <QuickStat label="Speaking Pace" value={`${audio_analysis.wpm} WPM`} color="text-blue-600" />
            <QuickStat label="Vocabulary" value={`${technical_analysis.metrics?.vocabulary_score}%`} color="text-indigo-600" />
            <QuickStat label="Grammar" value={`${technical_analysis.metrics?.grammar_score}%`} color="text-emerald-600" />
          </div>
        </div>
      </div>

      {/* KPI GRID */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <KPIBox title="Semantic Similarity" value={`${technical_analysis.semantic_similarity}%`} icon={<Target className="text-indigo-500" />} />
        <KPIBox title="Concept Coverage" value={`${technical_analysis.concept_coverage}%`} icon={<Zap className="text-amber-500" />} />
        <KPIBox title="Eye Contact" value={`${video_analysis.eye_contact_ratio}%`} icon={<Eye className="text-blue-500" />} />
        <KPIBox title="Behavior Score" value={`${video_analysis.behavior_score}%`} icon={<Camera className="text-rose-500" />} />
      </div>

      {/* ANALYSIS DEEP DIVE */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Radar Performance Chart */}
        <div className="bg-white rounded-[3rem] p-10 border border-slate-200 shadow-sm">
          <div className="flex items-center gap-3 mb-10">
            <Activity className="w-6 h-6 text-indigo-600" />
            <h3 className="text-xl font-bold text-slate-900">Multimodal Proficiency</h3>
          </div>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="metric" tick={{ fill: '#64748b', fontSize: 12, fontWeight: 600 }} />
                <Radar name="Score" dataKey="value" stroke="#4f46e5" fill="#4f46e5" fillOpacity={0.2} dot />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Strengths & Weaknesses */}
        <div className="space-y-6">
          <AnalysisSection title="Key Strengths" items={[...(technical_analysis.strengths || []), ...(video_analysis.strengths || [])]} type="strength" />
          <AnalysisSection title="Improvement Areas" items={[...(technical_analysis.weaknesses || []), ...(video_analysis.weaknesses || [])]} type="weakness" />
        </div>
      </div>

      {/* FILLER & VOCAB DASHBOARD */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Filler Word Chart */}
        <div className="bg-white rounded-[3rem] p-10 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-3 text-rose-600">
              <Mic className="w-6 h-6" />
              <h3 className="text-xl font-bold">Verbal Fillers</h3>
            </div>
            <div className="px-4 py-1 bg-rose-50 text-rose-600 rounded-full text-xs font-bold uppercase">
              Count: {audio_analysis.filler_count}
            </div>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={fillerData}>
                <XAxis dataKey="word" axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontWeight: 600 }} />
                <YAxis hide />
                <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }} />
                <Bar dataKey="count" fill="#f43f5e" radius={[10, 10, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Word Distribution */}
        <div className="bg-white rounded-[3rem] p-10 border border-slate-200 shadow-sm">
          <div className="flex items-center gap-3 mb-8 text-indigo-600">
            <MessageSquare className="w-6 h-6" />
            <h3 className="text-xl font-bold">Vocabulary Distribution</h3>
          </div>
          <div className="flex flex-wrap gap-3">
            {audio_analysis.word_distribution?.map((item, i) => (
              <div key={i} className="px-5 py-3 bg-slate-50 border border-slate-100 rounded-2xl flex items-center gap-3 hover:border-indigo-200 transition-all">
                <span className="font-bold text-slate-800">{item.word}</span>
                <span className="px-2 py-0.5 bg-white text-indigo-600 text-[10px] font-black rounded-lg border border-slate-100">{item.count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* TRANSCRIPT */}
      <div className="bg-white rounded-[3rem] p-12 border border-slate-200 shadow-sm">
        <h3 className="text-xl font-bold text-slate-900 mb-8 flex items-center gap-3">
          <Info className="w-6 h-6 text-slate-400" />
          Full Transcript Analysis
        </h3>
        <div className="bg-slate-50 p-10 rounded-[2.5rem] border border-slate-100 leading-relaxed text-slate-700 text-lg italic relative">
          <div className="absolute top-6 left-6 text-6xl text-slate-200 font-serif opacity-50">"</div>
          <p className="relative z-10">{transcript}</p>
        </div>
      </div>

    </div>
  );
}

function KPIBox({ title, value, icon }) {
  return (
    <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm hover:shadow-md transition-all">
      <div className="w-12 h-12 bg-slate-50 rounded-2xl flex items-center justify-center mb-4">
        {icon}
      </div>
      <p className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-1">{title}</p>
      <h4 className="text-3xl font-black text-slate-900">{value}</h4>
    </div>
  );
}

function QuickStat({ label, value, color }) {
  return (
    <div className="text-center">
      <div className={`text-2xl font-black ${color}`}>{value}</div>
      <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">{label}</div>
    </div>
  );
}

function AnalysisSection({ title, items, type }) {
  const isStrength = type === 'strength';
  return (
    <div className={`p-8 rounded-[2.5rem] border ${isStrength ? 'bg-emerald-50/50 border-emerald-100' : 'bg-rose-50/50 border-rose-100'} h-full`}>
      <div className="flex items-center gap-3 mb-6">
        {isStrength ? <CheckCircle2 className="w-6 h-6 text-emerald-600" /> : <AlertTriangle className="w-6 h-6 text-rose-600" />}
        <h3 className={`text-lg font-bold ${isStrength ? 'text-emerald-900' : 'text-rose-900'}`}>{title}</h3>
      </div>
      <div className="space-y-3">
        {items?.map((item, i) => (
          <div key={i} className={`flex items-start gap-3 p-3 rounded-2xl ${isStrength ? 'bg-white/60 border border-emerald-100' : 'bg-white/60 border border-rose-100'}`}>
            <div className={`w-1.5 h-1.5 rounded-full mt-2 shrink-0 ${isStrength ? 'bg-emerald-500' : 'bg-rose-500'}`}></div>
            <p className="text-sm font-medium text-slate-700">{item}</p>
          </div>
        ))}
      </div>
    </div>
  );
}