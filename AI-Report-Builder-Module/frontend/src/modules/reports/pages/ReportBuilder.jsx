import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  FileText, Download, Printer, Loader2, 
  TrendingUp, Activity, Box, ShoppingCart, DollarSign
} from 'lucide-react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const API_URL = 'http://localhost:8002/api/v1/reports';
const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function ReportBuilder() {
  const [reportType, setReportType] = useState('financial');
  const [startDate, setStartDate] = useState('2026-01-01');
  const [endDate, setEndDate] = useState('2026-12-31');
  const [department, setDepartment] = useState('all');
  
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [error, setError] = useState(null);

  const generateReport = async (format = 'preview') => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/generate`, {
        report_type: reportType,
        start_date: startDate,
        end_date: endDate,
        department: department,
        format: format
      });
      
      if (format === 'preview') {
        setReportData(response.data);
      } else {
        // Trigger download
        const url = `http://localhost:8002${response.data.download_url}`;
        window.open(url, '_blank');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate report.');
    } finally {
      setLoading(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const renderChart = (chart) => {
    if (chart.type === 'line') {
      const keys = Object.keys(chart.data[0] || {}).filter(k => k !== 'month');
      return (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chart.data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            {keys.map((k, i) => (
              <Line key={k} type="monotone" dataKey={k} stroke={COLORS[i % COLORS.length]} />
            ))}
          </LineChart>
        </ResponsiveContainer>
      );
    }
    if (chart.type === 'bar') {
      const xKey = Object.keys(chart.data[0] || {})[0];
      const valKey = Object.keys(chart.data[0] || {})[1];
      return (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chart.data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={xKey} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey={valKey} fill={COLORS[0]} />
          </BarChart>
        </ResponsiveContainer>
      );
    }
    if (chart.type === 'pie') {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie data={chart.data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100}>
              {chart.data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      );
    }
    return null;
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6 print-container">
      {/* Controls / Filter Section */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 no-print">
        <h2 className="text-lg font-semibold text-slate-800 mb-4">Report Parameters</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Report Type</label>
            <select 
              value={reportType} 
              onChange={(e) => setReportType(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="financial">Financial Report</option>
              <option value="clinical">Clinical Report</option>
              <option value="operational">Operational Report</option>
              <option value="inventory">Inventory Report</option>
              <option value="procurement">Procurement Report</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Start Date</label>
            <input 
              type="date" 
              value={startDate} 
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">End Date</label>
            <input 
              type="date" 
              value={endDate} 
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Department</label>
            <select 
              value={department} 
              onChange={(e) => setDepartment(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Departments</option>
              <option value="Cardiology">Cardiology</option>
              <option value="Neurology">Neurology</option>
              <option value="Orthopedics">Orthopedics</option>
              <option value="General">General</option>
              <option value="Emergency">Emergency</option>
            </select>
          </div>
        </div>
        
        <div className="mt-6 flex gap-3">
          <button 
            onClick={() => generateReport('preview')}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <FileText className="w-4 h-4" />}
            Generate Preview
          </button>
          <button 
            onClick={() => generateReport('pdf')}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-slate-100 text-slate-700 border border-slate-300 rounded-md hover:bg-slate-200 transition disabled:opacity-50"
          >
            <Download className="w-4 h-4" /> PDF Export
          </button>
          <button 
            onClick={() => generateReport('excel')}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-md hover:bg-emerald-100 transition disabled:opacity-50"
          >
            <Download className="w-4 h-4" /> Excel Export
          </button>
        </div>
        
        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-700 border border-red-200 rounded-md">
            {error}
          </div>
        )}
      </div>

      {/* Report Preview */}
      {reportData && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden print:border-none print:shadow-none">
          <div className="p-6 border-b border-slate-200 flex justify-between items-center print:border-b-2 print:border-black">
            <div>
              <h1 className="text-2xl font-bold text-slate-900 capitalize">
                {reportData.report_type} Report
              </h1>
              <p className="text-slate-500">
                Generated: {reportData.generated_date}
              </p>
            </div>
            <button 
              onClick={handlePrint}
              className="no-print flex items-center gap-2 px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-md transition"
            >
              <Printer className="w-5 h-5" /> Print
            </button>
          </div>
          
          <div className="p-6 space-y-8">
            
            {/* AI Executive Summary */}
            <div className="bg-blue-50 border border-blue-100 p-6 rounded-xl">
              <h3 className="text-lg font-semibold text-blue-900 mb-2 flex items-center gap-2">
                <Activity className="w-5 h-5" /> Executive Summary
              </h3>
              <p className="text-blue-800 leading-relaxed text-lg">
                {reportData.summary}
              </p>
            </div>

            {/* KPIs */}
            <div>
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Key Metrics</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(reportData.kpis).map(([key, value]) => (
                  <div key={key} className="bg-slate-50 p-4 rounded-lg border border-slate-200 print:border-black">
                    <p className="text-sm font-medium text-slate-500 mb-1 capitalize">
                      {key.replace(/_/g, ' ')}
                    </p>
                    <p className="text-2xl font-bold text-slate-900">
                      {typeof value === 'number' && key.includes('revenue') ? `$${value.toLocaleString()}` : value.toLocaleString()}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Charts */}
            {reportData.charts && reportData.charts.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-slate-800 mb-4">Analytics Visualization</h3>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 break-inside-avoid">
                  {reportData.charts.map((chart, idx) => (
                    <div key={idx} className="bg-white p-4 border border-slate-200 rounded-lg print:border-black">
                      <h4 className="text-center font-medium text-slate-700 mb-4">{chart.title}</h4>
                      {renderChart(chart)}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Table */}
            {reportData.tables && reportData.tables.Data && (
              <div className="break-inside-avoid">
                <h3 className="text-lg font-semibold text-slate-800 mb-4">Data Subset (Preview)</h3>
                <div className="overflow-x-auto border border-slate-200 rounded-lg print:border-black">
                  <table className="min-w-full divide-y divide-slate-200">
                    <thead className="bg-slate-50">
                      <tr>
                        {Object.keys(reportData.tables.Data[0] || {}).map((col) => (
                          <th key={col} className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                            {col.replace(/_/g, ' ')}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-slate-200">
                      {reportData.tables.Data.slice(0, 10).map((row, idx) => (
                        <tr key={idx}>
                          {Object.values(row).map((val, cellIdx) => (
                            <td key={cellIdx} className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">
                              {val}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
            
          </div>
        </div>
      )}
    </div>
  );
}
