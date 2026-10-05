import React, { useEffect, useState } from 'react';
import predictiveApi from '../api/predictive';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts';
import { 
  LineChart as LineChartIcon, Activity, Database, Sparkles, ShieldCheck, CheckCircle2 
} from 'lucide-react';
import { LoadingView, ErrorView } from '../components/common/StateViews';

export default function PredictiveAnalytics() {
  const [activeTab, setActiveTab] = useState('revenue');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      let res;
      if (activeTab === 'revenue') res = await predictiveApi.getRevenueForecast();
      else if (activeTab === 'admissions') res = await predictiveApi.getAdmissionsForecast();
      else if (activeTab === 'beds') res = await predictiveApi.getBedsForecast();
      else if (activeTab === 'medicines') res = await predictiveApi.getMedicinesDemand();
      else if (activeTab === 'inventory') res = await predictiveApi.getInventoryForecast();
      
      setData(res);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch ML forecaster calculations.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const tabs = [
    { id: 'revenue', label: 'Revenue Forecast' },
    { id: 'admissions', label: 'Admissions Forecast' },
    { id: 'beds', label: 'Bed Occupancy' },
    { id: 'medicines', label: 'Medicine Demand' },
    { id: 'inventory', label: 'Inventory Demand' },
  ];

  const dataSource = Array.isArray(data) ? (data[0]?.data_source || "POSTGRESQL_DB") : (data?.data_source || "POSTGRESQL_DB");
  const dataQuality = Array.isArray(data) ? "HISTORICAL" : (data?.data_quality || "HISTORICAL");
  const isPostgres = dataSource === "POSTGRESQL_DB";

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12">
      {/* Header & Dynamic Data Source Badge */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[var(--ts-border)] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <LineChartIcon className="w-6 h-6 text-cyan-400" />
            Predictive AI Analytics
          </h1>
          <p className="text-xs text-[var(--ts-text-secondary)] mt-0.5">Scikit-Learn Machine Learning Forecast Engine</p>
        </div>

        {/* Dynamic Data Source Badge */}
        <div className={`border px-3.5 py-1.5 rounded-xl flex items-center gap-2 text-xs font-bold ${
          isPostgres
            ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
            : 'bg-amber-500/10 border-amber-500/30 text-amber-400'
        }`}>
          <Database className="w-4 h-4" />
          <span>DATA SOURCE: {dataSource}</span>
          <span className="text-[10px] opacity-80 font-normal hidden lg:inline">({dataQuality})</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-2 border-b border-[var(--ts-border)] pb-2 overflow-x-auto">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === tab.id
                ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-md'
                : 'text-[var(--ts-text-secondary)] hover:bg-[var(--ts-card-hover)]'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {loading ? (
        <LoadingView title={`Training ML model & calculating holdout test metrics for ${activeTab}...`} />
      ) : error ? (
        <ErrorView error={error} onRetry={fetchData} />
      ) : !data ? (
        <LoadingView title="Loading..." />
      ) : Array.isArray(data) ? (
        /* List View (Medicine / Inventory Demand) */
        <div className="space-y-4">
          <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl flex justify-between items-center text-xs">
            <span className="font-semibold text-[var(--ts-text-muted)]">Subsystem Model: <strong className="text-[var(--ts-text-primary)]">Item Stock & Consumption Rate Analysis</strong></span>
            <span className="ts-badge ts-badge-cyan text-[10px]">Data Source: {dataSource}</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.map((item, idx) => (
              <div key={idx} className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-5 rounded-2xl space-y-3">
                <div className="flex justify-between items-start">
                  <h4 className="font-bold text-sm text-[var(--ts-text-primary)]">{item.name}</h4>
                  <span className="ts-badge ts-badge-cyan text-[10px]">{item.category}</span>
                </div>

                {item.current_stock !== undefined ? (
                  <div className="text-xs space-y-1 text-[var(--ts-text-secondary)]">
                    <div><span className="text-[var(--ts-text-muted)] font-medium">Current Stock:</span> {item.current_stock}</div>
                    <div><span className="text-[var(--ts-text-muted)] font-medium">Min Threshold:</span> {item.minimum_stock}</div>
                    <div><span className="text-[var(--ts-text-muted)] font-medium">Daily Consumption:</span> {item.daily_consumption}/day</div>
                    <div><span className="text-[var(--ts-text-muted)] font-medium">Est. Stockout:</span> <strong className="text-amber-400">{item.days_until_stockout} days</strong></div>
                    <div className="pt-2 flex justify-between items-center">
                      <span className={`ts-badge text-[10px] ${item.risk_level === 'CRITICAL' ? 'ts-badge-danger' : 'ts-badge-success'}`}>
                        {item.risk_level} RISK
                      </span>
                      {item.recommended_reorder_qty > 0 && (
                        <span className="text-[11px] font-bold text-cyan-400">Reorder: +{item.recommended_reorder_qty}</span>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="text-xs space-y-1 text-[var(--ts-text-secondary)]">
                    <div><span className="text-[var(--ts-text-muted)] font-medium">Hist. Daily Avg:</span> {item.historical_daily_avg}</div>
                    <div><span className="text-[var(--ts-text-muted)] font-medium">Proj. Daily Demand:</span> {item.projected_daily_demand}</div>
                    <div><span className="text-[var(--ts-text-muted)] font-medium">30-Day Demand Total:</span> <strong className="text-cyan-400">{item.predicted_30day_total}</strong></div>
                    <div className="pt-2 text-cyan-400 font-semibold">{item.recommendation}</div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : (
        /* Time Series Machine Learning Forecast View */
        <div className="space-y-6">
          {/* Metrics & Algorithm Meta */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl">
              <span className="text-[11px] text-[var(--ts-text-muted)] font-semibold uppercase">Machine Learning Model</span>
              <p className="text-base font-bold text-[var(--ts-text-primary)] mt-1">{data.algorithm || 'Scikit-learn LinearRegression'}</p>
            </div>
            <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl">
              <span className="text-[11px] text-[var(--ts-text-muted)] font-semibold uppercase">Mean Absolute Error (MAE)</span>
              <p className="text-lg font-bold text-cyan-400 mt-1">{data.metrics?.mae ?? '0.0'}</p>
              <span className="text-[10px] text-[var(--ts-text-muted)]">Evaluated on holdout test split</span>
            </div>
            <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl">
              <span className="text-[11px] text-[var(--ts-text-muted)] font-semibold uppercase">Root Mean Squared Error (RMSE)</span>
              <p className="text-lg font-bold text-cyan-400 mt-1">{data.metrics?.rmse ?? '0.0'}</p>
              <span className="text-[10px] text-[var(--ts-text-muted)]">Evaluated on holdout test split</span>
            </div>
            <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl">
              <span className="text-[11px] text-[var(--ts-text-muted)] font-semibold uppercase">R² Determination Score</span>
              <p className="text-lg font-bold text-emerald-400 mt-1">{data.metrics?.r2 ?? '0.0'}</p>
              <span className="text-[10px] text-[var(--ts-text-muted)]">Chronological 80/20 train/test</span>
            </div>
          </div>

          {/* Generative AI Explanation Box */}
          {data.explanation && (
            <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-5 rounded-2xl space-y-2">
              <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyan-400" /> Generative AI Analysis & Strategic Summary
              </h3>
              <p className="text-xs text-[var(--ts-text-secondary)] leading-relaxed">
                {typeof data.explanation === 'string' ? data.explanation : JSON.stringify(data.explanation)}
              </p>
            </div>
          )}

          {/* Machine Learning Chart View */}
          {(() => {
            const chartData = (data.forecast && data.forecast.length > 0) 
              ? data.forecast 
              : (data.historical && data.historical.length > 0)
                ? data.historical
                : (data.predictions || []);
            return (
              <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-6 rounded-2xl shadow-sm space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-base font-bold text-[var(--ts-text-primary)]">
                    Machine Learning Time-Series Forecast ({activeTab.toUpperCase()})
                  </h3>
                  <span className="text-xs text-[var(--ts-text-muted)] font-semibold">
                    Trend: <span className="text-cyan-400 font-bold uppercase">{data.trend || 'Stable'}</span>
                  </span>
                </div>

                <div className="h-[340px] w-full">
                  <ResponsiveContainer>
                    <LineChart data={chartData} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                      <XAxis dataKey="date" stroke="#64748B" axisLine={false} tickLine={false} tick={{ fontSize: 11 }} />
                      <YAxis stroke="#64748B" axisLine={false} tickLine={false} tick={{ fontSize: 11 }} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', color: '#FFF' }}
                        itemStyle={{ color: '#38BDF8' }}
                      />
                      <Line type="monotone" dataKey="value" name="Calculated Metric" stroke="#0EA5E9" strokeWidth={3} dot={{ r: 4, fill: '#0EA5E9' }} activeDot={{ r: 6 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            );
          })()}
        </div>
      )}
    </div>
  );
}

