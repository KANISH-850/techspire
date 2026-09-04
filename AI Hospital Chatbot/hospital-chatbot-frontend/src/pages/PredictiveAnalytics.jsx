import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { TrendingUp, Users, AlertCircle, Sparkles } from 'lucide-react';
import { dashboardService } from '../services/api';

const PredictiveAnalytics = () => {
  const [revenueData, setRevenueData] = useState(null);
  const [admissionsData, setAdmissionsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [rev, adm] = await Promise.all([
          fetch('http://localhost:8000/api/v1/predictive/revenue?days_ahead=30').then(res => res.json()),
          fetch('http://localhost:8000/api/v1/predictive/admissions?days_ahead=30').then(res => res.json())
        ]);
        setRevenueData(rev);
        setAdmissionsData(adm);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setError("Failed to load predictive models.");
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-[#0F172A] border-t-transparent rounded-full animate-spin"></div>
          <div className="text-xl font-medium text-[#0F172A]">Running AI Forecasting Models...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-full items-center justify-center p-4">
        <div className="bg-white border-l-4 border-rose-500 p-8 rounded-xl shadow-lg">
          <AlertCircle className="w-12 h-12 text-rose-500 mb-4" />
          <h2 className="text-xl font-bold text-[#0F172A]">{error}</h2>
        </div>
      </div>
    );
  }

  // Combine historical and forecast for charting
  const processChartData = (data, valueKey) => {
    if (!data) return [];
    
    // Convert historical
    const hist = data.historical.map(d => ({
      date: d.date,
      historical: d.value,
      forecast: null
    }));
    
    // Get last historical point to connect the line
    const lastHist = hist.length > 0 ? { ...hist[hist.length - 1], forecast: hist[hist.length - 1].historical } : null;
    
    // Convert forecast
    const forc = data.forecast.map(d => ({
      date: d.date,
      historical: null,
      forecast: d.predicted_value
    }));

    return lastHist ? [...hist, lastHist, ...forc] : [...hist, ...forc];
  };

  const revChartData = processChartData(revenueData, 'value');
  const admChartData = processChartData(admissionsData, 'value');

  return (
    <div className="p-8 max-w-[1600px] mx-auto space-y-8 bg-[#F8FAFC] min-h-screen">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-[#0F172A] flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-[#8B5CF6]" />
            AI Predictive Analytics
          </h1>
          <p className="text-sm text-[#64748B] mt-1">30-Day Forecasting using Machine Learning (Linear Regression)</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Revenue Forecast */}
        <div className="bg-white border border-[#E2E8F0] rounded-2xl shadow-sm overflow-hidden">
          <div className="bg-[#1E293B] p-4 flex justify-between items-center">
            <h2 className="text-white font-bold flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-[#38BDF8]" /> Revenue Forecast
            </h2>
          </div>
          <div className="p-6">
            <div className="h-[300px] w-full mb-6">
              <ResponsiveContainer>
                <LineChart data={revChartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                  <XAxis dataKey="date" stroke="#94A3B8" axisLine={false} tickLine={false} tick={{ fontSize: 10 }} />
                  <YAxis stroke="#94A3B8" axisLine={false} tickLine={false} tick={{ fontSize: 10 }} tickFormatter={v => `$${v/1000}k`} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0F172A', border: 'none', borderRadius: '8px', color: '#FFF' }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="historical" name="Historical" stroke="#94A3B8" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="forecast" name="AI Forecast" stroke="#8B5CF6" strokeWidth={3} strokeDasharray="5 5" dot={false} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {revenueData?.ai_analysis && (
              <div className="bg-[#F8FAFC] rounded-xl p-4 border border-[#E2E8F0]">
                <h3 className="text-sm font-bold text-[#0F172A] mb-2">AI Revenue Insights</h3>
                <p className="text-sm text-[#334155]">{revenueData.ai_analysis.executive_summary}</p>
              </div>
            )}
          </div>
        </div>

        {/* Admissions Forecast */}
        <div className="bg-white border border-[#E2E8F0] rounded-2xl shadow-sm overflow-hidden">
          <div className="bg-[#1E293B] p-4 flex justify-between items-center">
            <h2 className="text-white font-bold flex items-center gap-2">
              <Users className="w-5 h-5 text-[#34D399]" /> Admissions Forecast
            </h2>
          </div>
          <div className="p-6">
            <div className="h-[300px] w-full mb-6">
              <ResponsiveContainer>
                <LineChart data={admChartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                  <XAxis dataKey="date" stroke="#94A3B8" axisLine={false} tickLine={false} tick={{ fontSize: 10 }} />
                  <YAxis stroke="#94A3B8" axisLine={false} tickLine={false} tick={{ fontSize: 10 }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0F172A', border: 'none', borderRadius: '8px', color: '#FFF' }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="historical" name="Historical" stroke="#94A3B8" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="forecast" name="AI Forecast" stroke="#34D399" strokeWidth={3} strokeDasharray="5 5" dot={false} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {admissionsData?.ai_analysis && (
              <div className="bg-[#F8FAFC] rounded-xl p-4 border border-[#E2E8F0]">
                <h3 className="text-sm font-bold text-[#0F172A] mb-2">AI Admission Insights</h3>
                <p className="text-sm text-[#334155]">{admissionsData.ai_analysis.executive_summary}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictiveAnalytics;
