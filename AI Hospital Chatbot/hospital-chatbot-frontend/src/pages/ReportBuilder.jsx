import React, { useState } from 'react';
import { FileText, Download, FileSpreadsheet, Sparkles, Loader2, Package, ShoppingCart, Calendar, AlertCircle } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const ReportBuilder = () => {
  const [loading, setLoading] = useState(false);
  const [reportType, setReportType] = useState('financial');
  const [format, setFormat] = useState('pdf');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [dateError, setDateError] = useState(null);

  const handleGenerate = async () => {
    if (startDate && endDate && startDate > endDate) {
      setDateError("Start Date must be before or equal to End Date.");
      return;
    }
    setDateError(null);
    setLoading(true);

    try {
      let url = `${API_BASE_URL}/reports/generate?type=${reportType}&format=${format}`;
      if (startDate) url += `&start_date=${encodeURIComponent(startDate)}`;
      if (endDate) url += `&end_date=${encodeURIComponent(endDate)}`;

      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to generate report from server.");

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = `${reportType}_report.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(downloadUrl);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Report Generation Error:", error);
      alert("Error generating report. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const templates = [
    {
      id: 'financial',
      name: 'Financial Performance',
      desc: 'Revenue, expenses, and transaction summaries.',
      icon: FileText
    },
    {
      id: 'clinical',
      name: 'Clinical Overview',
      desc: 'Patient admissions, status, and demographics.',
      icon: Sparkles
    },
    {
      id: 'inventory',
      name: 'Inventory Summary',
      desc: 'Current stock levels, thresholds, and unit pricing.',
      icon: Package
    },
    {
      id: 'procurement',
      name: 'Procurement Summary',
      desc: 'Vendor performance ratings and purchase orders.',
      icon: ShoppingCart
    }
  ];

  return (
    <div className="p-8 max-w-[1200px] mx-auto space-y-8 bg-[#F8FAFC] min-h-screen font-sans">
      <div>
        <h1 className="text-2xl font-bold text-[#0F172A] flex items-center gap-2">
          <FileText className="w-6 h-6 text-[#2563EB]" />
          AI Report Builder
        </h1>
        <p className="text-sm text-[#64748B] mt-1">
          Generate comprehensive hospital reports in PDF & Excel formats with AI Executive Summaries.
        </p>
      </div>

      <div className="bg-white p-8 rounded-2xl shadow-sm border border-[#E2E8F0] max-w-3xl space-y-8">
        <h2 className="text-lg font-bold text-[#0F172A] border-b border-[#F1F5F9] pb-4">Configure Report Parameters</h2>

        {/* 1. Report Type Selection */}
        <div>
          <label className="block text-xs font-bold text-[#334155] uppercase tracking-wider mb-3">
            Select Report Template
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {templates.map((tpl) => {
              const Icon = tpl.icon;
              const isSelected = reportType === tpl.id;
              return (
                <button
                  key={tpl.id}
                  type="button"
                  onClick={() => setReportType(tpl.id)}
                  className={`p-4 rounded-xl border-2 text-left flex items-start gap-3 transition-all ${
                    isSelected 
                      ? 'border-[#2563EB] bg-blue-50/50 shadow-sm' 
                      : 'border-[#E2E8F0] hover:border-[#CBD5E1] bg-white'
                  }`}
                >
                  <div className={`p-2.5 rounded-lg ${isSelected ? 'bg-[#2563EB] text-white' : 'bg-[#F1F5F9] text-[#64748B]'}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <div className={`font-bold text-sm ${isSelected ? 'text-[#1E40AF]' : 'text-[#334155]'}`}>{tpl.name}</div>
                    <div className="text-xs text-[#64748B] mt-1 leading-relaxed">{tpl.desc}</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* 2. Date Filter Selection */}
        <div>
          <label className="block text-xs font-bold text-[#334155] uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <Calendar className="w-4 h-4 text-[#64748B]" /> Date Range Filter (Optional)
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <span className="block text-xs text-[#64748B] mb-1 font-medium">Start Date</span>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full p-2.5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl text-sm font-semibold text-[#0F172A]"
              />
            </div>
            <div>
              <span className="block text-xs text-[#64748B] mb-1 font-medium">End Date</span>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full p-2.5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl text-sm font-semibold text-[#0F172A]"
              />
            </div>
          </div>
          {dateError && (
            <div className="mt-2 text-xs font-bold text-rose-600 flex items-center gap-1">
              <AlertCircle className="w-3.5 h-3.5" /> {dateError}
            </div>
          )}
        </div>

        {/* 3. Export Format Selection */}
        <div>
          <label className="block text-xs font-bold text-[#334155] uppercase tracking-wider mb-3">
            Export Format
          </label>
          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => setFormat('pdf')}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-sm transition-colors ${
                format === 'pdf' 
                  ? 'bg-[#0F172A] text-white shadow-md' 
                  : 'bg-[#F1F5F9] text-[#64748B] hover:bg-[#E2E8F0]'
              }`}
            >
              <Download className="w-4 h-4" /> PDF Document (.pdf)
            </button>
            <button
              type="button"
              onClick={() => setFormat('excel')}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-sm transition-colors ${
                format === 'excel' 
                  ? 'bg-[#10B981] text-white shadow-md' 
                  : 'bg-[#F1F5F9] text-[#64748B] hover:bg-[#E2E8F0]'
              }`}
            >
              <FileSpreadsheet className="w-4 h-4" /> Excel Spreadsheet (.xlsx)
            </button>
          </div>
        </div>

        {/* 4. Action Button */}
        <div className="pt-4 border-t border-[#E2E8F0]">
          <button
            type="button"
            onClick={handleGenerate}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold py-4 px-8 rounded-xl shadow-md transition-colors disabled:opacity-70 text-base"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating AI Executive Summary & Exporting File...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Generate & Export {reportType.toUpperCase()} Report
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReportBuilder;
