import React, { useEffect, useState } from 'react';
import reportsApi from '../api/reports';
import { 
  FileText, Download, Play, History, CheckCircle, Clock, AlertCircle, FileSpreadsheet, FileCode 
} from 'lucide-react';
import { LoadingView, ErrorView } from '../components/common/StateViews';

export default function Reports() {
  const [reportTypes, setReportTypes] = useState([]);
  const [history, setHistory] = useState([]);
  const [selectedType, setSelectedType] = useState('executive_summary');
  const [scope, setScope] = useState('monthly');
  const [generating, setGenerating] = useState(false);
  const [activeReport, setActiveReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchInitial = async () => {
    try {
      setLoading(true);
      setError(null);
      const [typesRes, histRes] = await Promise.all([
        reportsApi.getReportTypes(),
        reportsApi.getHistory()
      ]);
      setReportTypes(typesRes.report_types || typesRes || []);
      setHistory(histRes || []);
    } catch (err) {
      console.error(err);
      setError("Failed to connect to report generator engine.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInitial();
  }, []);

  const handleGenerate = async (e) => {
    e.preventDefault();
    try {
      setGenerating(true);
      const res = await reportsApi.generateReport({
        report_type: selectedType,
        scope: scope,
        format: 'json'
      });
      setActiveReport(res);
      const histRes = await reportsApi.getHistory();
      setHistory(histRes || []);
    } catch (err) {
      alert("Failed to generate report.");
    } finally {
      setGenerating(false);
    }
  };

  const handleDownloadPdf = async (id) => {
    try {
      await reportsApi.downloadPdf(id);
    } catch (e) {
      alert("Failed to download PDF.");
    }
  };

  const handleDownloadExcel = async (id) => {
    try {
      await reportsApi.downloadExcel(id);
    } catch (e) {
      alert("Failed to download Excel file.");
    }
  };

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12">
      <div className="flex justify-between items-center border-b border-[var(--ts-border)] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <FileText className="w-6 h-6 text-cyan-400" />
            AI Report Builder
          </h1>
          <p className="text-xs text-[var(--ts-text-secondary)] mt-0.5">Automated Executive & Clinical PDF/Excel Report Generator</p>
        </div>
      </div>

      {loading ? (
        <LoadingView title="Loading report builder configurations..." />
      ) : error ? (
        <ErrorView error={error} onRetry={fetchInitial} />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Controls */}
          <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-6 rounded-2xl space-y-4">
            <h3 className="text-base font-bold text-[var(--ts-text-primary)]">Configure Report</h3>
            
            <form onSubmit={handleGenerate} className="space-y-4 text-xs">
              <div>
                <label className="block text-[var(--ts-text-muted)] font-semibold mb-1.5">Report Type</label>
                <select
                  value={selectedType}
                  onChange={(e) => setSelectedType(e.target.value)}
                  className="w-full bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] text-[var(--ts-text-primary)] px-3 py-2.5 rounded-xl focus:outline-none focus:border-cyan-500"
                >
                  <option value="executive_summary">Executive Summary Report</option>
                  <option value="department_performance">Department Performance Report</option>
                  <option value="patient_census">Patient Census & Admissions Report</option>
                  <option value="financial_summary">Financial & Revenue Report</option>
                  <option value="inventory_audit">Inventory & Procurement Audit</option>
                </select>
              </div>

              <div>
                <label className="block text-[var(--ts-text-muted)] font-semibold mb-1.5">Scope / Time Horizon</label>
                <select
                  value={scope}
                  onChange={(e) => setScope(e.target.value)}
                  className="w-full bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] text-[var(--ts-text-primary)] px-3 py-2.5 rounded-xl focus:outline-none focus:border-cyan-500"
                >
                  <option value="weekly">Weekly (Last 7 Days)</option>
                  <option value="monthly">Monthly (Last 30 Days)</option>
                  <option value="quarterly">Quarterly (Last 90 Days)</option>
                  <option value="annual">Annual (Last 365 Days)</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={generating}
                className="w-full ts-btn-primary justify-center py-3 text-xs"
              >
                <Play className="w-4 h-4" />
                <span>{generating ? 'Compiling AI Analysis...' : 'Generate New Report'}</span>
              </button>
            </form>

            <div className="pt-4 border-t border-[var(--ts-border)] space-y-2">
              <h4 className="text-xs font-bold text-[var(--ts-text-muted)] uppercase tracking-wider flex items-center gap-1.5">
                <History className="w-3.5 h-3.5" /> Recent Generated Reports
              </h4>
              <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                {history.map((h) => (
                  <div key={h.id} className="p-3 bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] rounded-xl text-xs space-y-1">
                    <div className="flex justify-between font-bold text-[var(--ts-text-primary)]">
                      <span>{h.title || h.report_type}</span>
                      <span className="text-[10px] text-cyan-400">#{h.id}</span>
                    </div>
                    <div className="flex gap-2 pt-1">
                      <button
                        onClick={() => handleDownloadPdf(h.id)}
                        className="px-2 py-1 bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 border border-rose-500/30 rounded text-[10px] flex items-center gap-1 font-bold"
                      >
                        <Download className="w-3 h-3" /> PDF
                      </button>
                      <button
                        onClick={() => handleDownloadExcel(h.id)}
                        className="px-2 py-1 bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/30 rounded text-[10px] flex items-center gap-1 font-bold"
                      >
                        <FileSpreadsheet className="w-3 h-3" /> Excel
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Report Active Preview */}
          <div className="lg:col-span-2 bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-6 rounded-2xl shadow-sm space-y-4">
            <h3 className="text-base font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
              <FileCode className="w-5 h-5 text-cyan-400" />
              Report Live Preview
            </h3>

            {!activeReport ? (
              <div className="text-center py-16 text-[var(--ts-text-muted)]">
                <FileText className="w-12 h-12 mx-auto mb-2 opacity-50 text-cyan-400" />
                <p className="text-xs">Select parameters and click "Generate New Report" to compile instant insights.</p>
              </div>
            ) : (
              <div className="space-y-4 text-xs">
                <div className="p-4 bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] rounded-xl flex justify-between items-center">
                  <div>
                    <h4 className="font-bold text-sm text-[var(--ts-text-primary)]">{activeReport.title}</h4>
                    <p className="text-[11px] text-[var(--ts-text-muted)]">Generated at {new Date(activeReport.created_at || Date.now()).toLocaleString()}</p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleDownloadPdf(activeReport.id)}
                      className="ts-btn-primary px-3 py-1.5 text-xs bg-gradient-to-r from-rose-600 to-pink-600"
                    >
                      <Download className="w-3.5 h-3.5" /> Export PDF
                    </button>
                    <button
                      onClick={() => handleDownloadExcel(activeReport.id)}
                      className="ts-btn-primary px-3 py-1.5 text-xs bg-gradient-to-r from-emerald-600 to-teal-600"
                    >
                      <FileSpreadsheet className="w-3.5 h-3.5" /> Export Excel
                    </button>
                  </div>
                </div>

                <div className="bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] p-4 rounded-xl space-y-2">
                  <h4 className="font-bold text-cyan-400 uppercase text-[11px] tracking-wider">Executive Summary</h4>
                  <p className="text-[var(--ts-text-secondary)] leading-relaxed">
                    {activeReport.summary || activeReport.content?.executive_summary || "Report generated successfully using live hospital database aggregations."}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
