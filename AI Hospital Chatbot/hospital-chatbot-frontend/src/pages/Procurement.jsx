import React, { useState, useEffect } from 'react';
import { 
  Package, AlertCircle, ShoppingCart, TrendingDown, Clock, 
  Building2, RefreshCw, CheckCircle2, Plus, X, Calendar
} from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const Procurement = () => {
  const [statusData, setStatusData] = useState(null);
  const [expiringData, setExpiringData] = useState(null);
  const [vendorsData, setVendorsData] = useState([]);
  const [reorderData, setReorderData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Active Tab: 'overview', 'reorder', 'expiring', 'vendors'
  const [activeTab, setActiveTab] = useState('overview');

  // Purchase Order Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedVendorId, setSelectedVendorId] = useState('');
  const [selectedItemId, setSelectedItemId] = useState('');
  const [orderQuantity, setOrderQuantity] = useState(100);
  const [unitPrice, setUnitPrice] = useState(1.0);
  const [submittingPO, setSubmittingPO] = useState(false);
  const [poSuccessMessage, setPoSuccessMessage] = useState(null);
  const [poErrorMessage, setPoErrorMessage] = useState(null);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [statusRes, expiringRes, vendorsRes, reorderRes] = await Promise.all([
        fetch(`${API_BASE_URL}/inventory/status`).then(res => res.json()),
        fetch(`${API_BASE_URL}/inventory/expiring`).then(res => res.json()),
        fetch(`${API_BASE_URL}/inventory/vendors`).then(res => res.json()),
        fetch(`${API_BASE_URL}/inventory/reorder`).then(res => res.json()),
      ]);

      setStatusData(statusRes);
      setExpiringData(expiringRes);
      setVendorsData(vendorsRes || []);
      setReorderData(reorderRes || []);

      if (vendorsRes && vendorsRes.length > 0) {
        setSelectedVendorId(vendorsRes[0].id.toString());
      }
      if (statusRes && statusRes.all_items && statusRes.all_items.length > 0) {
        setSelectedItemId(statusRes.all_items[0].id.toString());
        setUnitPrice(statusRes.all_items[0].price || 1.0);
      }

      setLoading(false);
    } catch (err) {
      console.error("Procurement Data Load Error:", err);
      setError("Failed to load inventory data. Ensure backend is running.");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  const handleOpenPOModal = (vendorId = null, itemId = null, suggestedQty = null) => {
    if (vendorId) setSelectedVendorId(vendorId.toString());
    if (itemId) {
      setSelectedItemId(itemId.toString());
      const matched = statusData?.all_items?.find(i => i.id.toString() === itemId.toString());
      if (matched) setUnitPrice(matched.price || 1.0);
    }
    if (suggestedQty) setOrderQuantity(suggestedQty);

    setPoSuccessMessage(null);
    setPoErrorMessage(null);
    setIsModalOpen(true);
  };

  const handleCreatePurchaseOrder = async (e) => {
    e.preventDefault();
    if (!selectedVendorId) {
      setPoErrorMessage("Please select a valid vendor.");
      return;
    }

    const qty = parseInt(orderQuantity, 10);
    const price = parseFloat(unitPrice);
    if (isNaN(qty) || qty <= 0) {
      setPoErrorMessage("Quantity must be greater than zero.");
      return;
    }

    const totalAmount = qty * price;

    try {
      setSubmittingPO(true);
      setPoErrorMessage(null);

      const payload = {
        vendor_id: parseInt(selectedVendorId, 10),
        items: [
          {
            item_id: parseInt(selectedItemId, 10) || 1,
            quantity: qty,
            unit_price: price
          }
        ],
        total_amount: round(totalAmount, 2)
      };

      const res = await fetch(`${API_BASE_URL}/inventory/purchase-orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const errorDetail = await res.json().catch(() => ({ detail: 'Failed to create PO' }));
        throw new Error(errorDetail.detail || "Server error while creating Purchase Order.");
      }

      const createdPO = await res.json();
      setPoSuccessMessage(`Purchase Order #${createdPO.id} successfully created and committed to Database! Status: ${createdPO.status}`);
      setSubmittingPO(false);
      
      // Refresh inventory data after PO creation
      setTimeout(() => {
        fetchAllData();
      }, 1500);

    } catch (err) {
      console.error("PO Creation Error:", err);
      setPoErrorMessage(err.message || "Failed to create Purchase Order.");
      setSubmittingPO(false);
    }
  };

  const round = (num, decimals) => Number(Math.round(num + "e" + decimals) + "e-" + decimals);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#F8FAFC]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-[#0F172A] border-t-transparent rounded-full animate-spin"></div>
          <div className="text-xl font-medium text-[#0F172A]">Analyzing Inventory & Vendor Data...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#F8FAFC] p-4">
        <div className="bg-white border-l-4 border-rose-500 p-8 rounded-xl shadow-lg max-w-md text-center">
          <AlertCircle className="w-12 h-12 text-rose-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-[#0F172A] mb-2">{error}</h2>
          <button onClick={fetchAllData} className="mt-4 px-4 py-2 bg-[#0F172A] text-white rounded-lg text-sm font-semibold">
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  const lowStockItems = statusData?.low_stock_items || [];
  const allItems = statusData?.all_items || [];
  const aiRecs = statusData?.ai_recommendations || [];
  const expiringSoon = expiringData?.expiring_soon_items || [];
  const expiredItems = expiringData?.expired_items || [];

  return (
    <div className="p-8 max-w-[1600px] mx-auto space-y-8 bg-[#F8FAFC] min-h-screen font-sans">
      {/* Top Title Bar */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-[#0F172A] flex items-center gap-2">
            <Package className="w-6 h-6 text-[#F59E0B]" />
            AI Procurement & Inventory Assistant
          </h1>
          <p className="text-sm text-[#64748B] mt-1">
            Smart Stock Management, Vendor Reliability Analytics, and AI Purchase Order Recommendations
          </p>
        </div>
        <button
          onClick={() => handleOpenPOModal()}
          className="flex items-center gap-2 bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold px-5 py-2.5 rounded-xl shadow-sm transition-colors text-sm"
        >
          <Plus className="w-4 h-4" /> Create Purchase Order
        </button>
      </div>

      {/* Metric Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-[#E2E8F0]">
          <p className="text-[#64748B] font-semibold text-xs uppercase tracking-wider">Total Tracked Items</p>
          <p className="text-3xl font-bold text-[#0F172A] mt-2">{statusData?.summary?.total_items || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-[#E2E8F0]">
          <p className="text-[#64748B] font-semibold text-xs uppercase tracking-wider">Healthy Stock</p>
          <p className="text-3xl font-bold text-[#10B981] mt-2">{statusData?.summary?.healthy_stock_count || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-rose-200 bg-rose-50">
          <p className="text-rose-700 font-semibold text-xs uppercase tracking-wider">Low Stock Alerts</p>
          <p className="text-3xl font-bold text-rose-600 mt-2">{statusData?.summary?.low_stock_count || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-amber-200 bg-amber-50">
          <p className="text-amber-700 font-semibold text-xs uppercase tracking-wider">Expiring (30 Days)</p>
          <p className="text-3xl font-bold text-amber-600 mt-2">{expiringSoon.length + expiredItems.length}</p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-[#E2E8F0] gap-4">
        <button
          onClick={() => setActiveTab('overview')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'overview' ? 'border-[#2563EB] text-[#2563EB]' : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
          }`}
        >
          <TrendingDown className="w-4 h-4" /> Low Stock & AI Recs
        </button>
        <button
          onClick={() => setActiveTab('reorder')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'reorder' ? 'border-[#2563EB] text-[#2563EB]' : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
          }`}
        >
          <RefreshCw className="w-4 h-4" /> Reorder Suggestions ({reorderData.length})
        </button>
        <button
          onClick={() => setActiveTab('expiring')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'expiring' ? 'border-[#2563EB] text-[#2563EB]' : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
          }`}
        >
          <Clock className="w-4 h-4" /> Expiring Items ({expiringSoon.length})
        </button>
        <button
          onClick={() => setActiveTab('vendors')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'vendors' ? 'border-[#2563EB] text-[#2563EB]' : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
          }`}
        >
          <Building2 className="w-4 h-4" /> Vendor Performance ({vendorsData.length})
        </button>
      </div>

      {/* TAB 1: OVERVIEW & AI RECOMMENDATIONS */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          <div className="xl:col-span-2 space-y-8">
            <div className="bg-white border border-[#E2E8F0] p-6 rounded-2xl shadow-sm">
              <h3 className="text-lg font-bold text-[#0F172A] mb-6 flex items-center gap-2">
                <TrendingDown className="w-5 h-5 text-rose-500" /> Critical Low Stock Items
              </h3>
              
              {lowStockItems.length === 0 ? (
                <div className="text-[#64748B] py-8 text-center bg-[#F8FAFC] rounded-xl border border-dashed border-[#E2E8F0]">
                  <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
                  No low stock items. All inventory items are above minimum threshold.
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="border-b-2 border-[#F1F5F9] text-[#64748B] text-xs uppercase tracking-wider">
                        <th className="py-3 px-4 font-bold">Item Name</th>
                        <th className="py-3 px-4 font-bold">Category</th>
                        <th className="py-3 px-4 font-bold">Current Stock</th>
                        <th className="py-3 px-4 font-bold">Min Target</th>
                        <th className="py-3 px-4 font-bold">Vendor</th>
                        <th className="py-3 px-4 font-bold">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {lowStockItems.map((item) => (
                        <tr key={item.id} className="border-b border-[#F1F5F9] hover:bg-[#F8FAFC]">
                          <td className="py-4 px-4 font-semibold text-[#0F172A]">{item.name}</td>
                          <td className="py-4 px-4 text-[#64748B] text-sm">{item.category}</td>
                          <td className="py-4 px-4 font-bold text-rose-600">{item.current_stock}</td>
                          <td className="py-4 px-4 text-[#64748B] text-sm">{item.minimum_stock}</td>
                          <td className="py-4 px-4 text-[#64748B] text-sm">{item.vendor}</td>
                          <td className="py-4 px-4">
                            <button
                              onClick={() => handleOpenPOModal(null, item.id, item.minimum_stock - item.current_stock + 100)}
                              className="px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-[#2563EB] font-bold rounded-lg text-xs transition-colors"
                            >
                              Reorder Item
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>

          {/* AI Recommendations Column */}
          <div className="xl:col-span-1">
            <div className="bg-[#0F172A] border border-[#1E293B] rounded-2xl shadow-sm overflow-hidden h-full">
              <div className="p-6">
                <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                  <ShoppingCart className="w-5 h-5 text-[#38BDF8]" /> AI Purchase Suggestions
                </h3>
                
                {aiRecs.length === 0 ? (
                  <div className="text-[#94A3B8] italic text-sm">
                    No active AI recommendations. Stock levels are currently sufficient.
                  </div>
                ) : (
                  <div className="space-y-4">
                    {aiRecs.map((rec, idx) => (
                      <div key={idx} className="bg-[#1E293B] p-4 rounded-xl border border-[#334155]">
                        <div className="flex justify-between items-start mb-2">
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${
                            rec.priority === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                          }`}>
                            {rec.priority} PRIORITY
                          </span>
                        </div>
                        <h4 className="text-white font-bold text-sm mb-2">{rec.title}</h4>
                        <p className="text-xs text-[#94A3B8] mb-3 leading-relaxed">{rec.reason}</p>
                        <button 
                          onClick={() => handleOpenPOModal()}
                          className="w-full bg-[#38BDF8] hover:bg-[#0284C7] text-white font-bold py-2 px-4 rounded-lg transition-colors text-xs"
                        >
                          Generate Purchase Order
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: REORDER SUGGESTIONS */}
      {activeTab === 'reorder' && (
        <div className="bg-white border border-[#E2E8F0] p-6 rounded-2xl shadow-sm">
          <h3 className="text-lg font-bold text-[#0F172A] mb-6 flex items-center gap-2">
            <RefreshCw className="w-5 h-5 text-[#2563EB]" /> Dynamic Reorder Suggestions
          </h3>
          {reorderData.length === 0 ? (
            <div className="text-[#64748B] py-8 text-center">No items currently approaching minimum stock threshold.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b-2 border-[#F1F5F9] text-[#64748B] text-xs uppercase tracking-wider">
                    <th className="py-3 px-4 font-bold">Item</th>
                    <th className="py-3 px-4 font-bold">Current Stock</th>
                    <th className="py-3 px-4 font-bold">Min Threshold</th>
                    <th className="py-3 px-4 font-bold">Recommended Quantity</th>
                    <th className="py-3 px-4 font-bold">Reason</th>
                    <th className="py-3 px-4 font-bold">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {reorderData.map((s, idx) => (
                    <tr key={idx} className="border-b border-[#F1F5F9] hover:bg-[#F8FAFC]">
                      <td className="py-4 px-4 font-semibold text-[#0F172A]">{s.item?.name || 'Item'}</td>
                      <td className="py-4 px-4 text-[#0F172A] font-bold">{s.current_stock}</td>
                      <td className="py-4 px-4 text-[#64748B]">{s.minimum_stock}</td>
                      <td className="py-4 px-4 font-bold text-emerald-600">{s.recommended_quantity} units</td>
                      <td className="py-4 px-4 text-xs text-[#64748B] font-medium">{s.reason}</td>
                      <td className="py-4 px-4">
                        <button
                          onClick={() => handleOpenPOModal(s.item?.vendor_id, s.item?.id, s.recommended_quantity)}
                          className="px-3 py-1.5 bg-[#2563EB] text-white font-bold rounded-lg text-xs hover:bg-[#1D4ED8]"
                        >
                          Create Order
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* TAB 3: EXPIRING ITEMS */}
      {activeTab === 'expiring' && (
        <div className="bg-white border border-[#E2E8F0] p-6 rounded-2xl shadow-sm space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
              <Clock className="w-5 h-5 text-amber-500" /> Expiration Tracking (30-Day Rule)
            </h3>
          </div>

          {expiringSoon.length === 0 && expiredItems.length === 0 ? (
            <div className="text-[#64748B] py-8 text-center bg-[#F8FAFC] rounded-xl border border-dashed border-[#E2E8F0]">
              <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
              No expired or expiring items found within 30 days.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b-2 border-[#F1F5F9] text-[#64748B] text-xs uppercase tracking-wider">
                    <th className="py-3 px-4 font-bold">Item Name</th>
                    <th className="py-3 px-4 font-bold">Category</th>
                    <th className="py-3 px-4 font-bold">Expiry Date</th>
                    <th className="py-3 px-4 font-bold">Days Remaining</th>
                    <th className="py-3 px-4 font-bold">Stock</th>
                    <th className="py-3 px-4 font-bold">Severity</th>
                  </tr>
                </thead>
                <tbody>
                  {[...expiredItems, ...expiringSoon].map((exp, idx) => (
                    <tr key={idx} className="border-b border-[#F1F5F9] hover:bg-[#F8FAFC]">
                      <td className="py-4 px-4 font-semibold text-[#0F172A]">{exp.item?.name}</td>
                      <td className="py-4 px-4 text-[#64748B] text-sm">{exp.item?.category}</td>
                      <td className="py-4 px-4 text-[#0F172A] text-sm font-medium">{exp.expiry_date}</td>
                      <td className="py-4 px-4 font-bold text-amber-600">{exp.days_remaining} days</td>
                      <td className="py-4 px-4 font-semibold text-[#0F172A]">{exp.item?.current_stock}</td>
                      <td className="py-4 px-4">
                        <span className={`text-[10px] font-bold px-2.5 py-1 rounded uppercase ${
                          exp.severity === 'EXPIRED' ? 'bg-rose-100 text-rose-700' : 'bg-amber-100 text-amber-700'
                        }`}>
                          {exp.severity}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* TAB 4: VENDOR PERFORMANCE ANALYSIS */}
      {activeTab === 'vendors' && (
        <div className="bg-white border border-[#E2E8F0] p-6 rounded-2xl shadow-sm">
          <h3 className="text-lg font-bold text-[#0F172A] mb-6 flex items-center gap-2">
            <Building2 className="w-5 h-5 text-[#2563EB]" /> Vendor Reliability & Performance Metrics
          </h3>
          {vendorsData.length === 0 ? (
            <div className="text-[#64748B] py-8 text-center">No vendors registered in database.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b-2 border-[#F1F5F9] text-[#64748B] text-xs uppercase tracking-wider">
                    <th className="py-3 px-4 font-bold">Vendor Name</th>
                    <th className="py-3 px-4 font-bold">Contact Email</th>
                    <th className="py-3 px-4 font-bold">Delivery Lead Time</th>
                    <th className="py-3 px-4 font-bold">Reliability Score</th>
                    <th className="py-3 px-4 font-bold">Rating</th>
                    <th className="py-3 px-4 font-bold">Total Orders</th>
                    <th className="py-3 px-4 font-bold">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {vendorsData.map((v) => (
                    <tr key={v.id} className="border-b border-[#F1F5F9] hover:bg-[#F8FAFC]">
                      <td className="py-4 px-4 font-bold text-[#0F172A]">{v.name}</td>
                      <td className="py-4 px-4 text-[#64748B] text-sm">{v.contact_email}</td>
                      <td className="py-4 px-4 text-[#0F172A] text-sm font-medium">{v.delivery_time_days} days</td>
                      <td className="py-4 px-4 font-bold text-emerald-600">{v.reliability_score} / 10</td>
                      <td className="py-4 px-4 font-bold text-amber-500">★ {v.rating}</td>
                      <td className="py-4 px-4 font-bold text-[#0F172A]">{v.purchase_orders_count} POs (${v.total_purchase_value?.toLocaleString()})</td>
                      <td className="py-4 px-4">
                        <button
                          onClick={() => handleOpenPOModal(v.id)}
                          className="px-3 py-1.5 bg-[#0F172A] text-white font-bold rounded-lg text-xs hover:bg-[#334155]"
                        >
                          New PO
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* CREATE PURCHASE ORDER MODAL */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden border border-[#E2E8F0]">
            <div className="bg-[#0F172A] p-5 text-white flex justify-between items-center">
              <h3 className="font-bold text-lg flex items-center gap-2">
                <ShoppingCart className="w-5 h-5 text-[#38BDF8]" /> Create Purchase Order
              </h3>
              <button onClick={() => setIsModalOpen(false)} className="text-white/70 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreatePurchaseOrder} className="p-6 space-y-4">
              {poSuccessMessage && (
                <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-semibold flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  {poSuccessMessage}
                </div>
              )}

              {poErrorMessage && (
                <div className="p-3 bg-rose-50 border border-rose-200 text-rose-800 rounded-xl text-xs font-semibold flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
                  {poErrorMessage}
                </div>
              )}

              <div>
                <label className="block text-xs font-bold text-[#334155] uppercase tracking-wider mb-1">Select Vendor</label>
                <select
                  value={selectedVendorId}
                  onChange={(e) => setSelectedVendorId(e.target.value)}
                  className="w-full p-2.5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl text-sm font-semibold text-[#0F172A]"
                  required
                >
                  {vendorsData.map(v => (
                    <option key={v.id} value={v.id}>{v.name} (Rating: {v.rating}★)</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#334155] uppercase tracking-wider mb-1">Target Inventory Item</label>
                <select
                  value={selectedItemId}
                  onChange={(e) => {
                    setSelectedItemId(e.target.value);
                    const matched = allItems.find(i => i.id.toString() === e.target.value);
                    if (matched) setUnitPrice(matched.price || 1.0);
                  }}
                  className="w-full p-2.5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl text-sm font-semibold text-[#0F172A]"
                  required
                >
                  {allItems.map(item => (
                    <option key={item.id} value={item.id}>{item.name} (${item.price}/unit)</option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#334155] uppercase tracking-wider mb-1">Quantity</label>
                  <input
                    type="number"
                    min="1"
                    value={orderQuantity}
                    onChange={(e) => setOrderQuantity(e.target.value)}
                    className="w-full p-2.5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl text-sm font-semibold text-[#0F172A]"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#334155] uppercase tracking-wider mb-1">Unit Price ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={unitPrice}
                    onChange={(e) => setUnitPrice(e.target.value)}
                    className="w-full p-2.5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl text-sm font-semibold text-[#0F172A]"
                    required
                  />
                </div>
              </div>

              <div className="p-3 bg-[#F1F5F9] rounded-xl border border-[#E2E8F0] flex justify-between items-center">
                <span className="text-xs font-bold text-[#64748B] uppercase">Calculated Total Amount:</span>
                <span className="text-lg font-bold text-[#2563EB]">
                  ${round((parseInt(orderQuantity, 10) || 0) * (parseFloat(unitPrice) || 0), 2).toLocaleString()}
                </span>
              </div>

              <div className="pt-2 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-sm font-semibold text-[#64748B] hover:text-[#0F172A]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submittingPO}
                  className="px-6 py-2.5 bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold rounded-xl text-sm disabled:opacity-50 flex items-center gap-2"
                >
                  {submittingPO ? 'Committing to DB...' : 'Submit & Create PO'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Procurement;
