import React, { useEffect, useState } from 'react';
import { predictiveApi } from '../services/api';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar
} from 'recharts';
import { AlertCircle, TrendingUp, TrendingDown, Pill, Activity, Users, DollarSign } from 'lucide-react';

const Card = ({ title, children, icon: Icon, className = "" }) => (
  <div className={`bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden ${className}`}>
    <div className="p-5 border-b border-gray-50 flex items-center justify-between">
      <h3 className="font-semibold text-gray-800">{title}</h3>
      {Icon && <Icon className="text-gray-400 w-5 h-5" />}
    </div>
    <div className="p-5">{children}</div>
  </div>
);

const PredictionCard = ({ title, forecastData, type = "line", unit = "" }) => {
  if (!forecastData || !forecastData.historical) return null;
  
  const data = [
    ...forecastData.historical.map(d => ({ ...d, type: 'Historical' })),
    ...forecastData.forecast.map(d => ({ ...d, type: 'Forecast' }))
  ];

  return (
    <Card title={title} className="h-[400px] flex flex-col">
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          {type === "line" ? (
            <LineChart data={data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
              <XAxis dataKey="date" tick={{fontSize: 12}} tickFormatter={(val) => val.substring(5)} />
              <YAxis tick={{fontSize: 12}} width={40} />
              <Tooltip labelStyle={{color: '#374151'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
              <Legend wrapperStyle={{fontSize: '12px'}} />
              <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} dot={false} name={`Value ${unit}`} />
            </LineChart>
          ) : (
            <BarChart data={data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
              <XAxis dataKey="date" tick={{fontSize: 12}} tickFormatter={(val) => val.substring(5)} />
              <YAxis tick={{fontSize: 12}} width={40} />
              <Tooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
              <Legend wrapperStyle={{fontSize: '12px'}} />
              <Bar dataKey="value" fill="#8b5cf6" name={`Value ${unit}`} />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
      <div className="mt-4 pt-4 border-t border-gray-100 flex items-start gap-3 bg-blue-50/50 -mx-5 -mb-5 p-5 rounded-b-xl">
        <AlertCircle className="w-5 h-5 text-blue-500 shrink-0 mt-0.5" />
        <p className="text-sm text-blue-900 leading-relaxed font-medium">
          {forecastData.explanation}
        </p>
      </div>
    </Card>
  );
};

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState({
    summary: null,
    revenue: null,
    admissions: null,
    bedOccupancy: null,
    inventory: null,
  });
  const [horizon, setHorizon] = useState(30);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const [sum, rev, adm, bed, inv] = await Promise.all([
          predictiveApi.getSummary(),
          predictiveApi.getRevenue(horizon),
          predictiveApi.getAdmissions(horizon),
          predictiveApi.getBedOccupancy(7),
          predictiveApi.getInventory()
        ]);
        setData({ summary: sum, revenue: rev, admissions: adm, bedOccupancy: bed, inventory: inv });
      } catch (err) {
        setError(err.message || 'Failed to fetch predictions');
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [horizon]);

  if (loading) return (
    <div className="flex items-center justify-center h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );

  if (error) return (
    <div className="p-8">
      <div className="bg-red-50 text-red-600 p-4 rounded-lg flex items-center gap-3">
        <AlertCircle />
        <p>Error loading predictions: {error}</p>
      </div>
    </div>
  );

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Predictive AI Analytics</h1>
          <p className="text-gray-500 mt-1">AI-003 Module • Scikit-learn Models • Data Horizon: {horizon} Days</p>
        </div>
        <select 
          className="bg-white border border-gray-200 text-gray-700 rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500 transition-all font-medium"
          value={horizon}
          onChange={e => setHorizon(Number(e.target.value))}
        >
          <option value={7}>7 Days Forecast</option>
          <option value={30}>30 Days Forecast</option>
          <option value={90}>90 Days Forecast</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card title="Revenue Trend" icon={DollarSign} className="bg-gradient-to-br from-blue-500 to-blue-600 !text-white border-none shadow-blue-500/20">
          <div className="flex items-end gap-3 text-white">
            <span className="text-3xl font-bold capitalize">{data.summary?.revenue_trend}</span>
            {data.summary?.revenue_trend === 'increasing' ? <TrendingUp className="text-blue-200 w-8 h-8 pb-1" /> : <TrendingDown className="text-blue-200 w-8 h-8 pb-1" />}
          </div>
        </Card>
        <Card title="Admissions Trend" icon={Users}>
          <div className="flex items-end gap-3 text-gray-800">
            <span className="text-3xl font-bold capitalize">{data.summary?.admissions_trend}</span>
            {data.summary?.admissions_trend === 'increasing' ? <TrendingUp className="text-green-500 w-8 h-8 pb-1" /> : <TrendingDown className="text-red-500 w-8 h-8 pb-1" />}
          </div>
        </Card>
        <Card title="Peak Bed Occupancy" icon={Activity}>
          <div className="flex items-end gap-3 text-gray-800">
            <span className="text-3xl font-bold">{(data.summary?.bed_occupancy_peak * 100).toFixed(1)}%</span>
            <span className="text-sm text-gray-500 font-medium pb-1.5 uppercase tracking-wide">Next 7 Days</span>
          </div>
        </Card>
        <Card title="Inventory Alerts" icon={Pill}>
          <div className="flex items-end gap-3 text-gray-800">
            <span className="text-3xl font-bold text-rose-500">
              {data.inventory?.filter(i => i.risk === 'HIGH').length || 0}
            </span>
            <span className="text-sm text-gray-500 font-medium pb-1.5 uppercase tracking-wide">High Risk Items</span>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <PredictionCard title="Revenue Forecast (₹)" forecastData={data.revenue} />
        <PredictionCard title="Patient Admissions Forecast" forecastData={data.admissions} type="bar" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <PredictionCard title="Bed Occupancy Rate Forecast" forecastData={data.bedOccupancy} />
        
        <Card title="Inventory Depletion Risk" className="h-[400px]">
          <div className="overflow-auto h-[320px] -mx-5 px-5">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-gray-500 uppercase bg-gray-50 sticky top-0">
                <tr>
                  <th className="px-4 py-3 font-semibold">Medicine</th>
                  <th className="px-4 py-3 font-semibold text-right">Stock</th>
                  <th className="px-4 py-3 font-semibold text-right">Days Left</th>
                  <th className="px-4 py-3 font-semibold">Risk</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {data.inventory?.map((item, i) => (
                  <tr key={i} className="hover:bg-gray-50/50 transition-colors">
                    <td className="px-4 py-3 font-medium text-gray-900">{item.medicine}</td>
                    <td className="px-4 py-3 text-right text-gray-600">{item.current_stock.toLocaleString()}</td>
                    <td className="px-4 py-3 text-right font-medium">{item.days_until_stockout === 999 ? '∞' : item.days_until_stockout}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                        item.risk === 'HIGH' ? 'bg-rose-100 text-rose-700' :
                        item.risk === 'MEDIUM' ? 'bg-amber-100 text-amber-700' :
                        'bg-emerald-100 text-emerald-700'
                      }`}>
                        {item.risk}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  );
}
