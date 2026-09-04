import React, { useState } from 'react';
import { FileText, Download, FileSpreadsheet, Sparkles, Loader2 } from 'lucide-react';

const ReportBuilder = () => {
  const [loading, setLoading] = useState(false);
  const [reportType, setReportType] = useState('financial');
  const [format, setFormat] = useState('pdf');

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/reports/generate?type=${reportType}&format=${format}`);
      if (!response.ok) throw new Error("Failed to generate report");
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${reportType}_report.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert("Error generating report. Ensure backend is running and dependencies are installed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-[1200px] mx-auto space-y-8 bg-[#F8FAFC] min-h-screen">
      <div>
        <h1 className="text-2xl font-bold text-[#0F172A] flex items-center gap-2">
          <FileText className="w-6 h-6 text-[#2563EB]" />
          AI Report Builder
        </h1>
        <p className="text-sm text-[#64748B] mt-1">Generate comprehensive hospital reports with AI Executive Summaries.</p>
      </div>

      <div className="bg-white p-8 rounded-2xl shadow-sm border border-[#E2E8F0] max-w-2xl">
        <h2 className="text-lg font-bold text-[#0F172A] mb-6">Configure Report</h2>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-[#334155] mb-2">Report Type</label>
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => setReportType('financial')}
                className={`p-4 rounded-xl border-2 text-left flex items-start gap-3 transition-colors ${
                  reportType === 'financial' 
                    ? 'border-[#2563EB] bg-blue-50' 
                    : 'border-[#E2E8F0] hover:border-[#CBD5E1]'
                }`}
              >
                <div className={`p-2 rounded-lg ${reportType === 'financial' ? 'bg-[#2563EB] text-white' : 'bg-[#F1F5F9] text-[#64748B]'}`}>
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <div className={`font-bold ${reportType === 'financial' ? 'text-[#1E40AF]' : 'text-[#334155]'}`}>Financial Performance</div>
                  <div className="text-xs text-[#64748B] mt-1">Revenue, expenses, and transaction summaries.</div>
                </div>
              </button>
              
              <button
                onClick={() => setReportType('clinical')}
                className={`p-4 rounded-xl border-2 text-left flex items-start gap-3 transition-colors ${
                  reportType === 'clinical' 
                    ? 'border-[#2563EB] bg-blue-50' 
                    : 'border-[#E2E8F0] hover:border-[#CBD5E1]'
                }`}
              >
                <div className={`p-2 rounded-lg ${reportType === 'clinical' ? 'bg-[#2563EB] text-white' : 'bg-[#F1F5F9] text-[#64748B]'}`}>
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <div className={`font-bold ${reportType === 'clinical' ? 'text-[#1E40AF]' : 'text-[#334155]'}`}>Clinical Overview</div>
                  <div className="text-xs text-[#64748B] mt-1">Patient admissions, status, and demographics.</div>
                </div>
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-[#334155] mb-2">Export Format</label>
            <div className="flex gap-4">
              <button
                onClick={() => setFormat('pdf')}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors ${
                  format === 'pdf' 
                    ? 'bg-[#0F172A] text-white' 
                    : 'bg-[#F1F5F9] text-[#64748B] hover:bg-[#E2E8F0]'
                }`}
              >
                <Download className="w-4 h-4" /> PDF Document
              </button>
              <button
                onClick={() => setFormat('excel')}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors ${
                  format === 'excel' 
                    ? 'bg-[#10B981] text-white' 
                    : 'bg-[#F1F5F9] text-[#64748B] hover:bg-[#E2E8F0]'
                }`}
              >
                <FileSpreadsheet className="w-4 h-4" /> Excel Spreadsheet
              </button>
            </div>
          </div>

          <div className="pt-6 border-t border-[#E2E8F0]">
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold py-4 px-8 rounded-xl shadow-sm transition-colors disabled:opacity-70"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generating AI Insights & Compiling...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Generate Report
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportBuilder;
