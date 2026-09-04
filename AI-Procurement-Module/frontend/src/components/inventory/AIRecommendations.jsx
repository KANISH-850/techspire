import React from 'react';
import { Bot, Lightbulb, ArrowRight, TrendingDown } from 'lucide-react';

export default function AIRecommendations({ recommendations, loading }) {
  if (loading) return (
    <div className="flex flex-col items-center justify-center p-12 text-slate-500">
      <Bot className="w-12 h-12 text-blue-500 animate-pulse mb-4" />
      <p>Ollama is analyzing inventory data...</p>
    </div>
  );

  if (!recommendations) return <div className="text-slate-500 p-4">No AI recommendations available.</div>;

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 p-6 rounded-xl shadow-sm">
        <h3 className="text-lg font-bold text-blue-900 flex items-center gap-2 mb-3">
          <Bot className="w-5 h-5" /> Executive Summary
        </h3>
        <p className="text-blue-800 leading-relaxed">
          {recommendations.executive_summary}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2 mb-4">
            <ArrowRight className="w-5 h-5 text-rose-500" /> Immediate Actions
          </h3>
          <ul className="space-y-3">
            {recommendations.immediate_actions.map((action, idx) => (
              <li key={idx} className="flex items-start gap-2 text-slate-700">
                <span className="w-1.5 h-1.5 bg-rose-500 rounded-full mt-2 shrink-0"></span>
                <span>{action}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2 mb-4">
            <TrendingDown className="w-5 h-5 text-emerald-500" /> Cost Optimization
          </h3>
          <ul className="space-y-3">
            {recommendations.cost_optimization.map((action, idx) => (
              <li key={idx} className="flex items-start gap-2 text-slate-700">
                <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full mt-2 shrink-0"></span>
                <span>{action}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
