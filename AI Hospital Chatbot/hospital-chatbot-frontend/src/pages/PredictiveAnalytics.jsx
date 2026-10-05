import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { TrendingUp, Users, BedDouble, Pill, Package, AlertCircle, Sparkles, Cpu, Database, CheckCircle2 } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const PredictiveAnalytics = () => {
  const [revenueData, setRevenueData] = useState(null);
  const [admissionsData, setAdmissionsData] = useState(null);
  const [bedsData, setBedsData] = useState(null);
  const [medicinesData, setMedicinesData] = useState(null);
  const [inventoryData, setInventoryData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const [rev, adm, beds, meds, inv] = await Promise.all([
          fetch(`${API_BASE_URL}/predictive/revenue?days_ahead=30`).then(res => res.json()),
          fetch(`${API_BASE_URL}/predictive/admissions?days_ahead=30`).then(res => res.json()),
          fetch(`${API_BASE_URL}/predictive/beds?days_ahead=30`).then(res => res.json()),
          fetch(`${API_BASE_URL}/predictive/medicines?days_ahead=30`).then(res => res.json()),
          fetch(`${API_BASE_URL}/predictive/inventory?days_ahead=30`).then(res => res.json()),
        ]);

        setRevenueData(rev);
        setAdmissionsData(adm);
        setBedsData(beds);
        setMedicinesData(meds);
        setInventoryData(inv);
        setLoading(false);
      } catch (err) {
        console.error("Predictive Analytics Error:", err);
        setError("Failed to load predictive models. Ensure backend server is running.");
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#F8FAFC]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-[#0F172A] border-t-transparent rounded-full animate-spin"></div>
          <div className="text-xl font-medium text-[#0F172A]">Running Scikit-Learn ML Forecasting Models...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#F8FAFC] p-4">
        <div className="bg-white border-l-4 border-rose-500 p-8 rounded-xl shadow-lg max-w-md text-center">
          <AlertCircle className="w-12 h-12 text-rose-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-[#0F172A] mb-2">{error}</h2>
          <button onClick={() => window.location.reload()} className="mt-4 px-4 py-2 bg-[#0F172A] text-white rounded-lg text-sm font-semibold">
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  // Combine historical and forecast for charting
  const processChartData = (data) => {
    if (!data || !data.historical || !data.forecast) return [];
    
    const hist = data.historical.map(d => ({
      date: d.date,
      historical: d.value,
      forecast: null
    }));
    
    const lastHist = hist.length > 0 ? { ...hist[hist.length - 1], forecast: hist[hist.length - 1].historical } : null;
    
    const forc = data.forecast.map(d => ({
      date: d.date,
      historical: null,
      forecast: d.predicted_value
    }));

    return lastHist ? [...hist, lastHist, ...forc] : [...hist, ...forc];
  };

  const revChartData = processChartData(revenueData);
  const admChartData = processChartData(admissionsData);
  const bedsChartData = processChartData(bedsData);
  const medsChartData = processChartData(medicinesData);
  const invChartData = processChartData(inventoryData);

  const ForecastCard = ({ 
    title, 
    icon: Icon, 
    color, 
    strokeColor, 
    chartData, 
    modelMeta, 
    aiAnalysis, 
    yFormatter 
  }) => {
    const dataQuality = modelMeta?.data_quality || 'historical';
    const dataSource = modelMeta?.data_source || 'PostgreSQL';
    const metrics = modelMeta?.metrics;

    const qualityBadgeColor = {
      historical: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
      approximated: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
      reconstructed: 'bg-blue-500/20 text-blue-300 border-blue-500/30'
    }[dataQuality] || 'bg-slate-500/20 text-slate-300 border-slate-500/30';

    return (
      <div className="bg-white border border-[#E2E8F0] rounded-2xl shadow-sm overflow-hidden flex flex-col justify-between">
        <div>
          <div className="bg-[#1E293B] p-4 flex flex-wrap justify-between items-center gap-2">
            <h2 className="text-white font-bold flex items-center gap-2 text-base">
              <Icon className="w-5 h-5" style={{ color }} /> {title}
            </h2>
            <div className="flex items-center gap-2">
              <span className={`text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded border ${qualityBadgeColor}`}>
                Data Quality: {dataQuality}
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-white/10 text-white border border-white/20">
                Scikit-Learn ML
              </span>
            </div>
          </div>

          <div className="p-6 space-y-4">
            {/* Metadata Bar */}
            <div className="flex flex-wrap items-center justify-between gap-3 text-xs bg-[#F8FAFC] p-3 rounded-xl border border-[#E2E8F0]">
              <div className="flex items-center gap-1.5">
                <Database className="w-3.5 h-3.5 text-[#64748B]" />
                <span className="font-semibold text-[#64748B]">Source:</span>
                <span className="font-medium text-[#0F172A]">{dataSource}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-[#64748B]" />
                <span className="font-semibold text-[#64748B]">Model:</span>
                <span className="font-medium text-[#0F172A]">{modelMeta?.algorithm || 'LinearRegression'}</span>
              </div>
              {metrics && typeof metrics === 'object' ? (
                <div className="flex items-center gap-3 font-mono text-[11px] bg-white px-2 py-1 rounded border border-[#E2E8F0]">
                  <span className="text-emerald-600 font-semibold">R²: {metrics.r2}</span>
                  <span className="text-slate-600">MAE: {metrics.mae}</span>
                  <span className="text-slate-600">RMSE: {metrics.rmse}</span>
                </div>
              ) : (
                <span className="text-[11px] text-slate-400 italic">Metrics: {typeof metrics === 'string' ? metrics : 'Evaluation pending'}</span>
              )}
            </div>

            <div className="h-[280px] w-full">
              <ResponsiveContainer>
                <LineChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                  <XAxis dataKey="date" stroke="#94A3B8" axisLine={false} tickLine={false} tick={{ fontSize: 10 }} />
                  <YAxis stroke="#94A3B8" axisLine={false} tickLine={false} tick={{ fontSize: 10 }} tickFormatter={yFormatter} />
                  <Tooltip contentStyle={{ backgroundColor: '#0F172A', border: 'none', borderRadius: '8px', color: '#FFF' }} />
                  <Legend />
                  <Line type="monotone" dataKey="historical" name="Historical Actual" stroke="#94A3B8" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="forecast" name="ML Predicted" stroke={strokeColor} strokeWidth={3} strokeDasharray="5 5" dot={false} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {aiAnalysis && aiAnalysis.executive_summary ? (
              <div className="bg-[#F8FAFC] rounded-xl p-4 border border-[#E2E8F0]">
                <h3 className="text-xs font-bold text-[#64748B] uppercase tracking-wider mb-1">AI Analytical Insight</h3>
                <p className="text-sm text-[#334155] leading-relaxed">{aiAnalysis.executive_summary}</p>
              </div>
            ) : (
              <div className="bg-[#F8FAFC] rounded-xl p-3 border border-[#E2E8F0] text-xs text-[#94A3B8] italic">
                AI commentary offline (Ollama service unavailable). Chart displays Scikit-Learn linear regression forecast data.
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="p-8 max-w-[1600px] mx-auto space-y-8 bg-[#F8FAFC] min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-[#0F172A] flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-[#8B5CF6]" />
            Predictive AI Analytics
          </h1>
          <p className="text-sm text-[#64748B] mt-1">
            Formalized Machine Learning Time-Series Forecasting powered by Scikit-Learn Linear Regression & PostgreSQL
          </p>
        </div>
        <div className="flex items-center gap-2 bg-purple-50 border border-purple-200 px-4 py-2 rounded-xl text-purple-700 font-bold text-xs">
          <CheckCircle2 className="w-4 h-4 text-purple-600" />
          <span>ML Models Active: 5 / 5</span>
        </div>
      </div>

      {/* Grid of 4 Forecast Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 1. Revenue Forecast */}
        <ForecastCard 
          title="Revenue Forecast" 
          icon={TrendingUp} 
          color="#38BDF8" 
          strokeColor="#0284C7"
          chartData={revChartData} 
          modelMeta={revenueData}
          aiAnalysis={revenueData?.ai_analysis}
          yFormatter={v => `$${v >= 1000 ? `${(v/1000).toFixed(0)}k` : v}`}
        />

        {/* 2. Admissions Forecast */}
        <ForecastCard 
          title="Patient Admissions Forecast" 
          icon={Users} 
          color="#34D399" 
          strokeColor="#059669"
          chartData={admChartData} 
          modelMeta={admissionsData}
          aiAnalysis={admissionsData?.ai_analysis}
          yFormatter={v => Math.round(v)}
        />

        {/* 3. Bed Occupancy Forecast */}
        <ForecastCard 
          title="Bed Occupancy Forecast" 
          icon={BedDouble} 
          color="#F59E0B" 
          strokeColor="#D97706"
          chartData={bedsChartData} 
          modelMeta={bedsData}
          aiAnalysis={bedsData?.ai_analysis}
          yFormatter={v => `${Math.round(v)} beds`}
        />

        {/* 4. Medicine Demand Forecast */}
        <ForecastCard 
          title="Medicine Demand Forecast" 
          icon={Pill} 
          color="#EC4899" 
          strokeColor="#DB2777"
          chartData={medsChartData} 
          modelMeta={medicinesData}
          aiAnalysis={medicinesData?.ai_analysis}
          yFormatter={v => Math.round(v)}
        />
      </div>

      {/* 5. Inventory Forecast (Full Width) */}
      <div className="w-full">
        <ForecastCard 
          title="Overall Inventory Level Forecast" 
          icon={Package} 
          color="#8B5CF6" 
          strokeColor="#7C3AED"
          chartData={invChartData} 
          modelMeta={inventoryData}
          aiAnalysis={inventoryData?.ai_analysis}
          yFormatter={v => Math.round(v)}
        />
      </div>

      {/* ML Model Architecture & Classification Section */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-center gap-2 border-b border-[#E2E8F0] pb-3">
          <Cpu className="w-5 h-5 text-indigo-600" />
          <h2 className="text-lg font-bold text-[#0F172A]">AI & ML System Architecture Classification</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-[#F8FAFC] p-4 rounded-xl border border-[#E2E8F0] space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-indigo-100 text-indigo-700">
              Machine Learning
            </span>
            <h3 className="font-bold text-sm text-[#0F172A]">Scikit-Learn Regressors</h3>
            <p className="text-xs text-[#64748B]">
              5 Scikit-Learn <code className="bg-slate-200 px-1 py-0.5 rounded text-[11px]">LinearRegression</code> models for time-series trend forecasting with R², MAE, RMSE metrics.
            </p>
          </div>

          <div className="bg-[#F8FAFC] p-4 rounded-xl border border-[#E2E8F0] space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-purple-100 text-purple-700">
              Generative AI
            </span>
            <h3 className="font-bold text-sm text-[#0F172A]">Qwen3:4B LLM (Ollama)</h3>
            <p className="text-xs text-[#64748B]">
              Natural language generation for analytical summaries, dashboard recommendations, and chatbot answers.
            </p>
          </div>

          <div className="bg-[#F8FAFC] p-4 rounded-xl border border-[#E2E8F0] space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-100 text-emerald-700">
              RAG Vector Engine
            </span>
            <h3 className="font-bold text-sm text-[#0F172A]">ChromaDB & Embeddings</h3>
            <p className="text-xs text-[#64748B]">
              <code className="bg-slate-200 px-1 py-0.5 rounded text-[11px]">nomic-embed-text</code> embeddings stored in ChromaDB for FAQ & policy similarity search.
            </p>
          </div>

          <div className="bg-[#F8FAFC] p-4 rounded-xl border border-[#E2E8F0] space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-slate-200 text-slate-700">
              Database & Rules
            </span>
            <h3 className="font-bold text-sm text-[#0F172A]">PostgreSQL & SQL</h3>
            <p className="text-xs text-[#64748B]">
              Relational tables, SQL queries for patient lookups, regex for navigation, and 30-day date thresholds.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictiveAnalytics;
