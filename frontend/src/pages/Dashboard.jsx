import React, { useEffect, useState } from 'react';
import dashboardApi from '../api/dashboard';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts';
import { 
  AlertCircle, TrendingUp, TrendingDown, Users, Activity, CheckCircle, 
  Clock, Heart, ShieldAlert, Star, Filter, Calendar, ActivitySquare
} from 'lucide-react';
import { LoadingView, ErrorView } from '../components/common/StateViews';

export default function Dashboard() {
  const [kpis, setKpis] = useState(null);
  const [revenue, setRevenue] = useState(null);
  const [departments, setDepartments] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [aiInsights, setAiInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [aiLoading, setAiLoading] = useState(true);

  // Filters state
  const [dateRange, setDateRange] = useState('30');
  const [departmentFilter, setDepartmentFilter] = useState('');

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const filters = {};
      if (dateRange !== 'all') {
        const end = new Date();
        const start = new Date();
        start.setDate(end.getDate() - parseInt(dateRange));
        filters.start_date = start.toISOString();
        filters.end_date = end.toISOString();
      }
      if (departmentFilter) {
        filters.department_id = departmentFilter;
      }

      const [kpiData, revData, deptData, alertData] = await Promise.all([
        dashboardApi.getKPIs(filters),
        dashboardApi.getRevenue(filters),
        dashboardApi.getDepartments(filters),
        dashboardApi.getAlerts()
      ]);
      
      setKpis(kpiData);
      setRevenue(revData);
      setDepartments(deptData || []);
      setAlerts(alertData.alerts || alertData || []);
      setLoading(false);
      
      fetchAIInsights();
    } catch (err) {
      console.error(err);
      setError("Failed to load executive dashboard data. Verify backend server.");
      setLoading(false);
    }
  };

  const fetchAIInsights = async () => {
    try {
      setAiLoading(true);
      const insights = await dashboardApi.getAIInsights();
      setAiInsights(insights);
    } catch (err) {
      console.error("AI Insights Error:", err);
      setAiInsights(null);
    } finally {
      setAiLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, [dateRange, departmentFilter]);

  if (loading && !kpis) {
    return <LoadingView title="Loading Executive AI Overview..." />;
  }

  if (error) {
    return <ErrorView error={error} onRetry={fetchDashboardData} />;
  }

  // Helper Badge Components
  const TrendBadge = ({ value }) => {
    if (value === undefined || value === null) return null;
    const isPos = value >= 0;
    return (
      <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1 ${isPos ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/15 text-rose-400 border border-rose-500/30'}`}>
        {isPos ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
        {Math.abs(value)}%
      </span>
    );
  };

  const SeverityBadge = ({ severity }) => {
    const colors = {
      CRITICAL: 'bg-rose-500/20 text-rose-400 border-rose-500/30',
      HIGH: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      MEDIUM: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
      LOW: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    };
    return (
      <span className={`text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded-md border ${colors[severity] || colors.LOW}`}>
        {severity}
      </span>
    );
  };

  const KPICard = ({ title, value, subtitle, icon: Icon, growth }) => (
    <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-5 rounded-2xl shadow-sm hover:border-[var(--ts-border-strong)] transition-all">
      <div className="flex justify-between items-start mb-3">
        <div className="p-2.5 bg-cyan-500/10 rounded-xl text-cyan-400">
          <Icon className="w-5 h-5" />
        </div>
        <TrendBadge value={growth} />
      </div>
      <div>
        <p className="text-2xl font-black text-[var(--ts-text-primary)] tracking-tight">{value}</p>
        <h3 className="text-xs font-semibold text-[var(--ts-text-secondary)] mt-1">{title}</h3>
        {subtitle && <p className="text-[11px] text-[var(--ts-text-muted)] mt-0.5">{subtitle}</p>}
      </div>
    </div>
  );

  // Helper helper to extract numerical value whether scalar or object {value: ...}
  const getVal = (item, fallback = 0) => {
    if (item === null || item === undefined) return fallback;
    if (typeof item === 'object') return item.value ?? fallback;
    return item;
  };

  const getGrowth = (item) => {
    if (item === null || item === undefined) return undefined;
    if (typeof item === 'object') return item.change_percent;
    return undefined;
  };

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12">
      {/* Top Header Controls */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[var(--ts-border)] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <ActivitySquare className="w-6 h-6 text-cyan-400" />
            CEO Executive AI Dashboard
          </h1>
          <p className="text-xs text-[var(--ts-text-secondary)] mt-0.5">Real-Time Hospital Operations & Financial Overview</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-[var(--ts-card-bg)] px-3 py-1.5 rounded-xl border border-[var(--ts-border)]">
            <Calendar className="w-4 h-4 text-[var(--ts-text-muted)]" />
            <select 
              className="bg-transparent text-xs font-semibold text-[var(--ts-text-primary)] focus:outline-none cursor-pointer"
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
            >
              <option value="7">Last 7 Days</option>
              <option value="30">Last 30 Days</option>
              <option value="90">Last 90 Days</option>
              <option value="180">Last 6 Months</option>
              <option value="all">All Time</option>
            </select>
          </div>
          
          <div className="flex items-center gap-2 bg-[var(--ts-card-bg)] px-3 py-1.5 rounded-xl border border-[var(--ts-border)]">
            <Filter className="w-4 h-4 text-[var(--ts-text-muted)]" />
            <select 
              className="bg-transparent text-xs font-semibold text-[var(--ts-text-primary)] focus:outline-none cursor-pointer"
              value={departmentFilter}
              onChange={(e) => setDepartmentFilter(e.target.value)}
            >
              <option value="">All Departments</option>
              {departments.map(d => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* 1. KPI Grid (8 Cards) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Total Revenue" value={`$${getVal(kpis?.total_revenue).toLocaleString()}`} icon={TrendingUp} growth={getGrowth(kpis?.total_revenue) ?? kpis?.revenue_growth} />
        <KPICard title="Total Patients" value={getVal(kpis?.total_patients).toLocaleString()} icon={Users} growth={getGrowth(kpis?.total_patients) ?? kpis?.patient_growth} />
        <KPICard title="Bed Occupancy Rate" value={`${getVal(kpis?.bed_occupancy)}%`} icon={Clock} subtitle="Current Utilization" />
        <KPICard title="Patient Satisfaction" value={`${getVal(kpis?.patient_satisfaction || kpis?.average_patient_satisfaction)}/10`} icon={Star} subtitle="Average Score" />
        <KPICard title="Total Admissions" value={getVal(kpis?.total_admissions).toLocaleString()} icon={Activity} />
        <KPICard title="Total Discharges" value={getVal(kpis?.total_discharges).toLocaleString()} icon={CheckCircle} />
        <KPICard title="Emergency Cases" value={getVal(kpis?.emergency_cases).toLocaleString()} icon={Heart} subtitle="Selected Period" />
        <KPICard title="Appt. Completion" value={`${getVal(kpis?.appointment_completion_rate, 95)}%`} icon={CheckCircle} subtitle={`${getVal(kpis?.cancellation_rate, 5)}% Cancellation`} />
      </div>

      {/* Executive AI Insights & Recommendations */}
      <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-2xl overflow-hidden shadow-lg">
        <div className="bg-gradient-to-r from-cyan-900/40 via-blue-900/40 to-indigo-900/40 px-6 py-4 border-b border-[var(--ts-border)] flex justify-between items-center">
          <h2 className="text-slate-100 font-bold text-base flex items-center gap-2">
            <span className="text-cyan-400">✨</span> Executive AI Insights
          </h2>
          {(aiInsights?.hospital_status || aiInsights?.status) && (
            <span className="ts-badge ts-badge-cyan text-xs font-bold uppercase">
              Status: {aiInsights.hospital_status || aiInsights.status || 'Nominal'}
            </span>
          )}
        </div>
        
        <div className="p-6">
          {aiLoading ? (
            <div className="animate-pulse space-y-3">
              <div className="h-4 bg-[var(--ts-border)] rounded w-3/4"></div>
              <div className="h-4 bg-[var(--ts-border)] rounded w-1/2"></div>
            </div>
          ) : !aiInsights ? (
            <div className="text-[var(--ts-text-muted)] italic text-sm">AI Insights currently unavailable. Ensure LLM engine is configured.</div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Summary & Insights */}
              <div className="lg:col-span-1 space-y-5">
                <div>
                  <h3 className="text-xs font-bold text-[var(--ts-text-muted)] uppercase tracking-wider mb-2">Executive Summary</h3>
                  <p className="text-[var(--ts-text-secondary)] leading-relaxed text-sm">
                    {aiInsights.executive_summary || aiInsights.summary || "Real-time AI monitoring shows active hospital operations."}
                  </p>
                </div>
                <div>
                  <h3 className="text-xs font-bold text-[var(--ts-text-muted)] uppercase tracking-wider mb-2">Key Insights</h3>
                  <ul className="space-y-2">
                    {(aiInsights.key_insights || aiInsights.key_observations || []).map((insight, idx) => (
                      <li key={idx} className="flex gap-2.5 text-xs text-[var(--ts-text-secondary)]">
                        <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-1.5 shrink-0"></div>
                        <span>{insight}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Recommendations */}
              <div className="lg:col-span-2">
                <h3 className="text-xs font-bold text-[var(--ts-text-muted)] uppercase tracking-wider mb-3">AI Executive Recommendations</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {(aiInsights.recommendations || []).map((rec, idx) => {
                    const title = typeof rec === 'string' ? rec : rec.title || rec.action || 'Optimization';
                    const priority = rec.priority || 'HIGH';
                    const reason = rec.reason || rec.justification || 'Maintains operational efficiency.';
                    const impact = rec.expected_impact || rec.impact || 'Positive outcome';
                    return (
                      <div key={idx} className="bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] p-4 rounded-xl space-y-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-[10px] font-bold tracking-wide uppercase text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded">
                            {priority} PRIORITY
                          </span>
                        </div>
                        <p className="text-xs font-bold text-[var(--ts-text-primary)]">
                          {title}
                        </p>
                        <p className="text-xs text-[var(--ts-text-secondary)]">
                          <span className="font-semibold text-[var(--ts-text-muted)]">Reason:</span> {reason}
                        </p>
                        <p className="text-xs text-cyan-400 font-semibold pt-1">
                          Impact: {impact}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Charts & Department Table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Revenue Chart */}
          <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-6 rounded-2xl shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-base font-bold text-[var(--ts-text-primary)]">Revenue Trend</h3>
              {revenue?.highest_revenue_department && (
                <div className="text-xs text-[var(--ts-text-muted)]">
                  Top Dept: <span className="font-bold text-cyan-400">{revenue.highest_revenue_department.department || revenue.highest_revenue_department}</span>
                </div>
              )}
            </div>
            <div className="h-[280px] w-full">
              <ResponsiveContainer>
                <LineChart data={revenue?.monthly || []} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="month" stroke="#64748B" axisLine={false} tickLine={false} tick={{ fontSize: 11 }} />
                  <YAxis stroke="#64748B" axisLine={false} tickLine={false} tick={{ fontSize: 11 }} tickFormatter={(val) => `$${val/1000}k`} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', color: '#FFF' }}
                    itemStyle={{ color: '#38BDF8' }}
                    formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']}
                  />
                  <Line type="monotone" dataKey="revenue" stroke="#0EA5E9" strokeWidth={3} dot={{ r: 4, fill: '#0EA5E9', strokeWidth: 2, stroke: '#FFF' }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Department Performance Table */}
          <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-6 rounded-2xl shadow-sm">
            <h3 className="text-base font-bold text-[var(--ts-text-primary)] mb-4">Department Performance</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-[var(--ts-border)] text-[var(--ts-text-muted)] text-[11px] uppercase tracking-wider">
                    <th className="py-2.5 px-3 font-bold">Department</th>
                    <th className="py-2.5 px-3 font-bold">Revenue</th>
                    <th className="py-2.5 px-3 font-bold">Patients</th>
                    <th className="py-2.5 px-3 font-bold">Occupancy</th>
                    <th className="py-2.5 px-3 font-bold">Score</th>
                    <th className="py-2.5 px-3 font-bold">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--ts-border)] text-xs">
                  {departments.map((dept) => {
                    const occ = dept.occupancy ?? dept.bed_occupancy_rate ?? 50;
                    const rev = dept.revenue ?? 0;
                    const score = dept.performance_score ?? dept.avg_satisfaction ?? 9.0;
                    const severity = dept.alert_status ?? (occ > 80 ? 'HIGH' : 'LOW');
                    return (
                      <tr key={dept.id} className="hover:bg-[var(--ts-card-hover)] transition-colors">
                        <td className="py-3 px-3 font-semibold text-[var(--ts-text-primary)]">{dept.name}</td>
                        <td className="py-3 px-3 font-medium text-cyan-400">${rev.toLocaleString()}</td>
                        <td className="py-3 px-3 text-[var(--ts-text-secondary)]">{(dept.patient_count || 0).toLocaleString()}</td>
                        <td className="py-3 px-3">
                          <div className="flex items-center gap-2">
                            <span className="font-medium text-[var(--ts-text-primary)] w-8">{occ}%</span>
                            <div className="w-16 bg-[var(--ts-bg-subtle)] h-1.5 rounded-full overflow-hidden">
                              <div className={`h-full ${occ > 90 ? 'bg-rose-500' : 'bg-cyan-500'}`} style={{ width: `${occ}%` }}></div>
                            </div>
                          </div>
                        </td>
                        <td className="py-3 px-3 font-bold text-[var(--ts-text-primary)]">{score}</td>
                        <td className="py-3 px-3">
                          <SeverityBadge severity={severity} />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Active Alerts */}
        <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-6 rounded-2xl shadow-sm flex flex-col h-full">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-base font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-rose-400" />
              Active System Alerts
            </h3>
            <span className="ts-badge ts-badge-danger text-xs">
              {alerts.length} Active
            </span>
          </div>
          
          {alerts.length === 0 ? (
            <div className="text-center py-12 text-[var(--ts-text-muted)] my-auto">
              <CheckCircle className="w-10 h-10 mx-auto mb-2 text-emerald-400 opacity-50" />
              <p className="text-xs">All hospital systems nominal.</p>
            </div>
          ) : (
            <div className="space-y-3 overflow-y-auto pr-1 flex-1 max-h-[600px]">
              {alerts.map((alert, i) => (
                <div key={i} className="p-3.5 rounded-xl border border-[var(--ts-border)] bg-[var(--ts-bg-subtle)] space-y-2">
                  <div className="flex justify-between items-start">
                    <SeverityBadge severity={alert.severity} />
                    <span className="text-[10px] text-[var(--ts-text-muted)]">
                      {alert.timestamp || alert.created_at ? new Date(alert.timestamp || alert.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : 'Recent'}
                    </span>
                  </div>
                  <h4 className="font-bold text-[var(--ts-text-primary)] text-xs">{alert.title}</h4>
                  <p className="text-[11px] text-[var(--ts-text-secondary)] leading-relaxed">{alert.message || alert.description}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
