import React, { useState, useEffect } from 'react';
import { Package, AlertCircle, ShoppingCart, TrendingDown } from 'lucide-react';

const Procurement = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/inventory/status');
        if (!response.ok) throw new Error("Failed to fetch inventory status");
        const json = await response.json();
        setData(json);
      } catch (err) {
        console.error(err);
        setError("Failed to load inventory data.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center min-h-screen">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-[#0F172A] border-t-transparent rounded-full animate-spin"></div>
          <div className="text-xl font-medium text-[#0F172A]">Analyzing Inventory...</div>
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

  return (
    <div className="p-8 max-w-[1600px] mx-auto space-y-8 bg-[#F8FAFC] min-h-screen">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-[#0F172A] flex items-center gap-2">
            <Package className="w-6 h-6 text-[#F59E0B]" />
            AI Procurement & Inventory
          </h1>
          <p className="text-sm text-[#64748B] mt-1">Smart inventory management and AI-driven purchase recommendations.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-[#E2E8F0]">
          <p className="text-[#64748B] font-semibold text-sm">Total Items Tracked</p>
          <p className="text-3xl font-bold text-[#0F172A] mt-2">{data.summary.total_items}</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-[#E2E8F0]">
          <p className="text-[#64748B] font-semibold text-sm">Healthy Stock</p>
          <p className="text-3xl font-bold text-[#10B981] mt-2">{data.summary.healthy_stock_count}</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-rose-200 bg-rose-50">
          <p className="text-rose-700 font-semibold text-sm">Low Stock Alerts</p>
          <p className="text-3xl font-bold text-rose-600 mt-2">{data.summary.low_stock_count}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        
        <div className="xl:col-span-2 space-y-8">
          {/* Low Stock Items */}
          <div className="bg-white border border-[#E2E8F0] p-6 rounded-2xl shadow-sm">
            <h3 className="text-lg font-bold text-[#0F172A] mb-6 flex items-center gap-2">
              <TrendingDown className="w-5 h-5 text-rose-500" /> Critical Low Stock
            </h3>
            
            {data.low_stock_items.length === 0 ? (
              <div className="text-[#64748B] py-4">No low stock items. Everything is healthy.</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b-2 border-[#F1F5F9] text-[#64748B] text-xs uppercase tracking-wider">
                      <th className="py-3 px-4 font-bold">Item Name</th>
                      <th className="py-3 px-4 font-bold">Category</th>
                      <th className="py-3 px-4 font-bold">Current Stock</th>
                      <th className="py-3 px-4 font-bold">Minimum</th>
                      <th className="py-3 px-4 font-bold">Vendor</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.low_stock_items.map((item) => (
                      <tr key={item.id} className="border-b border-[#F1F5F9]">
                        <td className="py-4 px-4 font-medium text-[#0F172A]">{item.name}</td>
                        <td className="py-4 px-4 text-[#64748B]">{item.category}</td>
                        <td className="py-4 px-4 font-bold text-rose-500">{item.current_stock}</td>
                        <td className="py-4 px-4 text-[#64748B]">{item.minimum_stock}</td>
                        <td className="py-4 px-4 text-[#64748B]">{item.vendor}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* AI Recommendations */}
        <div className="xl:col-span-1">
          <div className="bg-[#0F172A] border border-[#1E293B] rounded-2xl shadow-sm overflow-hidden h-full">
            <div className="p-6">
              <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                <ShoppingCart className="w-5 h-5 text-[#38BDF8]" /> AI Purchase Suggestions
              </h3>
              
              {data.ai_recommendations.length === 0 ? (
                <div className="text-[#94A3B8] italic">No active recommendations. Stock levels are sufficient.</div>
              ) : (
                <div className="space-y-4">
                  {data.ai_recommendations.map((rec, idx) => (
                    <div key={idx} className="bg-[#1E293B] p-4 rounded-xl border border-[#334155]">
                      <div className="flex justify-between items-start mb-2">
                        <span className={`text-[10px] font-bold px-2 py-1 rounded uppercase ${
                          rec.priority === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400' : 'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {rec.priority} PRIORITY
                        </span>
                      </div>
                      <h4 className="text-white font-bold mb-2">{rec.title}</h4>
                      <p className="text-sm text-[#94A3B8] mb-3">{rec.reason}</p>
                      <button className="w-full bg-[#38BDF8] hover:bg-[#0284C7] text-white font-bold py-2 px-4 rounded-lg transition-colors text-sm">
                        Create Purchase Order
                      </button>
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

export default Procurement;
