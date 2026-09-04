import React, { useEffect, useState } from 'react';
import { dashboardService } from '../services/api';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { 
  AlertCircle, TrendingUp, TrendingDown, Users, Activity, CheckCircle, 
  Clock, Heart, ShieldAlert, Star, Filter, Calendar, ActivitySquare
} from 'lucide-react';

const Dashboard = () => {
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
        dashboardService.getKPIs(filters),
        dashboardService.getRevenue(filters),
        dashboardService.getDepartments(filters),
        dashboardService.getAlerts()
      ]);
      
      setKpis(kpiData);
      setRevenue(revData);
      setDepartments(deptData);
      setAlerts(alertData.alerts || []);
      setLoading(false);
      
      fetchAIInsights();
    } catch (err) {
      console.error(err);
      setError("Failed to load dashboard data. Ensure backend is running.");
      setLoading(false);
    }
  };

  const fetchAIInsights = async () => {
    try {
      setAiLoading(true);
      const insights = await dashboardService.getAIInsights();
      setAiInsights(insights);
    } catch (err) {
      console.error("AI Error:", err);
      setAiInsights(null);
    } finally {
      setAiLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, [dateRange, departmentFilter]);

  if (loading && !kpis) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#F8FAFC]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-[#0F172A] border-t-transparent rounded-full animate-spin"></div>
          <div className="text-xl font-medium text-[#0F172A]">Loading Executive Overview...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#F8FAFC] p-4">
        <div className="bg-white border-l-4 border-rose-500 p-8 rounded-xl shadow-lg max-w-lg w-full text-center">
          <AlertCircle className="w-16 h-16 text-rose-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-[#0F172A] mb-2">Connection Error</h2>
          <p className="text-[#64748B] mb-6">{error}</p>
          <button onClick={fetchDashboardData} className="px-6 py-2.5 bg-[#0F172A] hover:bg-[#334155] text-white rounded-lg transition-colors font-medium">
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  // Helper Components
  const TrendBadge = ({ value }) => {
    if (value === undefined || value === null) return null;
    const isPos = value >= 0;
    return (
      <span className={`text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1 ${isPos ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
        {isPos ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
        {Math.abs(value)}%
      </span>
    );
  };

  const SeverityBadge = ({ severity }) => {
    const colors = {
      CRITICAL: 'bg-rose-100 text-rose-700 border-rose-200',
      HIGH: 'bg-orange-100 text-orange-700 border-orange-200',
      MEDIUM: 'bg-yellow-100 text-yellow-700 border-yellow-200',
      LOW: 'bg-blue-100 text-blue-700 border-blue-200',
    };
    return (
      <span className={`text-[10px] uppercase tracking-wider font-bold px-2 py-1 rounded-md border ${colors[severity] || colors.LOW}`}>
        {severity}
      </span>
    );
  };

  const KPICard = ({ title, value, subtitle, icon: Icon, growth }) => (
    <div className="bg-white border border-[#E2E8F0] p-5 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="p-2.5 bg-[#F1F5F9] rounded-xl">
          <Icon className="w-5 h-5 text-[#0F172A]" />
        </div>
        <TrendBadge value={growth} />
      </div>
      <div>
        <p className="text-3xl font-bold text-[#0F172A] tracking-tight">{value}</p>
        <h3 className="text-sm font-semibold text-[#64748B] mt-1">{title}</h3>
        {subtitle && <p className="text-xs text-[#94A3B8] mt-1">{subtitle}</p>}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-[#0F172A] font-sans pb-12">
      {/* Top Navigation / Header */}
      <div className="bg-white border-b border-[#E2E8F0] sticky top-0 z-20">
        <div className="px-8 py-4 max-w-[1600px] mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-[#0F172A] flex items-center gap-2">
              <ActivitySquare className="w-6 h-6 text-[#2563EB]" />
              Executive AI Dashboard
            </h1>
            <p className="text-sm text-[#64748B] mt-0.5">Hospital Operations & Financial Overview</p>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-[#F1F5F9] p-1 rounded-lg border border-[#E2E8F0]">
              <Calendar className="w-4 h-4 text-[#64748B] ml-2" />
              <select 
                className="bg-transparent text-sm font-medium text-[#0F172A] border-none focus:ring-0 cursor-pointer py-1.5 pr-8"
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
            
            <div className="flex items-center gap-2 bg-[#F1F5F9] p-1 rounded-lg border border-[#E2E8F0]">
              <Filter className="w-4 h-4 text-[#64748B] ml-2" />
              <select 
                className="bg-transparent text-sm font-medium text-[#0F172A] border-none focus:ring-0 cursor-pointer py-1.5 pr-8"
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
      </div>

      <div className="p-8 max-w-[1600px] mx-auto space-y-8">
        {loading && <div className="absolute inset-0 bg-white/50 z-10 flex items-center justify-center">Loading...</div>}

        {/* 1. KPI Grid (8 Cards) */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <KPICard title="Total Revenue" value={`$${(kpis?.total_revenue || 0).toLocaleString()}`} icon={TrendingUp} growth={kpis?.revenue_growth} />
          <KPICard title="Total Patients" value={kpis?.total_patients?.toLocaleString()} icon={Users} growth={kpis?.patient_growth} />
          <KPICard title="Bed Occupancy Rate" value={`${kpis?.bed_occupancy || 0}%`} icon={Clock} subtitle="Current Utilization" />
          <KPICard title="Patient Satisfaction" value={`${kpis?.average_patient_satisfaction || 0}/10`} icon={Star} subtitle="Average Score" />
          <KPICard title="Total Admissions" value={kpis?.total_admissions?.toLocaleString()} icon={Activity} />
          <KPICard title="Total Discharges" value={kpis?.total_discharges?.toLocaleString()} icon={CheckCircle} />
          <KPICard title="Emergency Cases" value={kpis?.emergency_cases?.toLocaleString()} icon={Heart} subtitle="In Selected Period" />
          <KPICard title="Appt. Completion" value={`${kpis?.appointment_completion_rate || 0}%`} icon={CheckCircle} subtitle={`${kpis?.cancellation_rate}% Cancellation`} />
        </div>

        {/* Executive AI Insights & Recommendations */}
        <div className="bg-white border border-[#E2E8F0] rounded-2xl overflow-hidden shadow-sm">
          <div className="bg-[#0F172A] px-6 py-4 flex justify-between items-center">
            <h2 className="text-white font-bold text-lg flex items-center gap-2">
              <span className="text-[#38BDF8]">✨</span> Executive AI Insights
            </h2>
            {aiInsights?.hospital_status && (
              <span className="bg-white/20 text-white text-xs px-3 py-1 rounded-full font-bold uppercase tracking-wider">
                Status: {aiInsights.hospital_status}
              </span>
            )}
          </div>
          
          <div className="p-6">
            {aiLoading ? (
              <div className="animate-pulse space-y-4">
                <div className="h-4 bg-[#E2E8F0] rounded w-3/4"></div>
                <div className="h-4 bg-[#E2E8F0] rounded w-1/2"></div>
              </div>
            ) : !aiInsights || !aiInsights.executive_summary ? (
              <div className="text-[#64748B] italic">AI Insights unavailable. Ensure API key is configured.</div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                
                {/* Summary & Insights */}
                <div className="lg:col-span-1 space-y-6">
                  <div>
                    <h3 className="text-sm font-bold text-[#64748B] uppercase tracking-wider mb-2">Executive Summary</h3>
                    <p className="text-[#334155] leading-relaxed text-sm">
                      {aiInsights.executive_summary}
                    </p>
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-[#64748B] uppercase tracking-wider mb-3">Key Insights</h3>
                    <ul className="space-y-3">
                      {aiInsights.key_insights?.map((insight, idx) => (
                        <li key={idx} className="flex gap-3 text-sm text-[#334155]">
                          <div className="w-1.5 h-1.5 rounded-full bg-[#2563EB] mt-1.5 shrink-0"></div>
                          {insight}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Recommendations */}
                <div className="lg:col-span-2">
                  <h3 className="text-sm font-bold text-[#64748B] uppercase tracking-wider mb-4">AI Executive Recommendations</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {aiInsights.recommendations?.map((rec, idx) => {
                      let emoji = '🔵';
                      if (rec.priority === 'CRITICAL' || rec.priority === 'HIGH') emoji = '🔴';
                      else if (rec.priority === 'MEDIUM') emoji = '🟠';
                      else if (rec.priority === 'LOW') emoji = '🟢';

                      return (
                        <div key={idx} className="bg-transparent mb-4">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-sm font-bold tracking-wide uppercase">
                              {emoji} {rec.priority} PRIORITY
                            </span>
                          </div>
                          <p className="text-[#0F172A] font-bold mb-1">
                            {rec.title}
                          </p>
                          <p className="text-sm text-[#4A5568] mb-1">
                            <span className="font-semibold">Reason:</span> {rec.reason}
                          </p>
                          {rec.supporting_metric && (
                            <p className="text-sm text-[#4A5568] mb-1">
                              <span className="font-semibold">Metric:</span> {rec.supporting_metric}
                            </p>
                          )}
                          <p className="text-sm text-[#4A5568]">
                            <span className="font-semibold text-[#2563EB]">Impact:</span> {rec.expected_impact}
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

        {/* Charts & Tables Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Revenue Insights */}
          <div className="lg:col-span-2 space-y-8">
            
            <div className="bg-white border border-[#E2E8F0] p-6 rounded-2xl shadow-sm">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-bold text-[#0F172A]">Revenue Trend</h3>
                {revenue?.highest_revenue_department && (
                  <div className="text-sm text-[#64748B]">
                    Top Dept: <span className="font-bold text-[#0F172A]">{revenue.highest_revenue_department.department}</span>
                  </div>
                )}
              </div>
              <div className="h-[300px] w-full">
                <ResponsiveContainer>
                  <LineChart data={revenue?.monthly || []} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                    <XAxis dataKey="month" stroke="#94A3B8" axisLine={false} tickLine={false} tick={{ fontSize: 12 }} />
                    <YAxis stroke="#94A3B8" axisLine={false} tickLine={false} tick={{ fontSize: 12 }} tickFormatter={(val) => `$${val/1000}k`} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0F172A', border: 'none', borderRadius: '8px', color: '#FFF' }}
                      itemStyle={{ color: '#38BDF8' }}
                      formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']}
                    />
                    <Line type="monotone" dataKey="revenue" stroke="#2563EB" strokeWidth={3} dot={{ r: 4, fill: '#2563EB', strokeWidth: 2, stroke: '#FFF' }} activeDot={{ r: 6 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white border border-[#E2E8F0] p-6 rounded-2xl shadow-sm">
              <h3 className="text-lg font-bold text-[#0F172A] mb-6">Department Performance</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b-2 border-[#F1F5F9] text-[#64748B] text-xs uppercase tracking-wider">
                      <th className="py-3 px-4 font-bold">Department</th>
                      <th className="py-3 px-4 font-bold">Revenue</th>
                      <th className="py-3 px-4 font-bold">Patients</th>
                      <th className="py-3 px-4 font-bold">Occupancy</th>
                      <th className="py-3 px-4 font-bold">Score</th>
                      <th className="py-3 px-4 font-bold">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {departments.map((dept) => (
                      <tr key={dept.id} className="border-b border-[#F1F5F9] hover:bg-[#F8FAFC] transition-colors">
                        <td className="py-4 px-4 font-medium text-[#0F172A]">{dept.name}</td>
                        <td className="py-4 px-4 font-semibold text-[#0F172A]">${dept.revenue.toLocaleString()}</td>
                        <td className="py-4 px-4 text-[#64748B]">{dept.patient_count.toLocaleString()}</td>
                        <td className="py-4 px-4">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium text-[#0F172A] w-9">{dept.occupancy}%</span>
                            <div className="w-16 bg-[#F1F5F9] h-2 rounded-full overflow-hidden">
                              <div className={`h-full ${dept.occupancy > 90 ? 'bg-rose-500' : 'bg-[#2563EB]'}`} style={{ width: `${dept.occupancy}%` }}></div>
                            </div>
                          </div>
                        </td>
                        <td className="py-4 px-4">
                          <span className="font-bold text-[#0F172A]">{dept.performance_score}</span>
                        </td>
                        <td className="py-4 px-4">
                          <SeverityBadge severity={dept.alert_status} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Critical Alerts */}
          <div className="space-y-6">
            <div className="bg-white border border-[#E2E8F0] p-6 rounded-2xl shadow-sm h-full">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
                  <ShieldAlert className="w-5 h-5 text-rose-500" />
                  Active Alerts
                </h3>
                <span className="bg-[#0F172A] text-white text-xs px-2.5 py-1 rounded-full font-bold">
                  {alerts.length}
                </span>
              </div>
              
              {alerts.length === 0 ? (
                <div className="text-center py-12 text-[#94A3B8]">
                  <CheckCircle className="w-12 h-12 mx-auto mb-3 text-emerald-400 opacity-50" />
                  <p>All systems normal. No critical alerts.</p>
                </div>
              ) : (
                <div className="space-y-4 max-h-[700px] overflow-y-auto pr-2">
                  {alerts.map((alert, i) => (
                    <div key={i} className={`p-4 rounded-xl border ${alert.severity === 'CRITICAL' ? 'bg-rose-50 border-rose-200' : alert.severity === 'HIGH' ? 'bg-orange-50 border-orange-200' : 'bg-yellow-50 border-yellow-200'}`}>
                      <div className="flex justify-between items-start mb-2">
                        <SeverityBadge severity={alert.severity} />
                        <span className="text-[10px] text-[#64748B] font-medium">
                          {new Date(alert.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                        </span>
                      </div>
                      <h4 className="font-bold text-[#0F172A] text-sm mb-1">{alert.title}</h4>
                      <p className="text-xs text-[#334155] mb-3 leading-relaxed">{alert.message}</p>
                      
                      {alert.recommended_action && (
                        <div className="mt-3 pt-3 border-t border-black/5">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-[#64748B] block mb-1">Action Required</span>
                          <p className="text-xs font-medium text-[#0F172A]">{alert.recommended_action}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Dashboard;
