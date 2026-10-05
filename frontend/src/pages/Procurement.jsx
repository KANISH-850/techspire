import React, { useEffect, useState } from 'react';
import procurementApi from '../api/procurement';
import { 
  ShoppingCart, Users, Bot, Layers, Plus, CheckCircle, Clock, AlertTriangle, Sparkles 
} from 'lucide-react';
import { LoadingView, ErrorView, EmptyView } from '../components/common/StateViews';

export default function Procurement() {
  const [activeTab, setActiveTab] = useState('pos');
  const [vendors, setVendors] = useState([]);
  const [pos, setPos] = useState([]);
  const [aiRecs, setAiRecs] = useState(null);
  const [loading, setLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showPOModal, setShowPOModal] = useState(false);

  const [poForm, setPoForm] = useState({
    vendor_id: 1,
    status: 'Draft',
    total_amount: 500,
    items: [
      { inventory_item_id: 1, quantity: 50, unit_price: 10, total_price: 500 }
    ]
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [vRes, pRes] = await Promise.all([
        procurementApi.getVendors(),
        procurementApi.getPurchaseOrders()
      ]);
      setVendors(vRes || []);
      setPos(pRes || []);
    } catch (err) {
      console.error(err);
      setError("Failed to load procurement and vendor records.");
    } finally {
      setLoading(false);
    }
  };

  const fetchAIRecommendations = async () => {
    try {
      setAiLoading(true);
      setActiveTab('ai');
      const data = await procurementApi.getAIRecommendations();
      setAiRecs(data);
    } catch (err) {
      console.error(err);
    } finally {
      setAiLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreatePO = async (e) => {
    e.preventDefault();
    try {
      await procurementApi.createPurchaseOrder(poForm);
      setShowPOModal(false);
      fetchData();
    } catch (err) {
      alert("Failed to draft purchase order.");
    }
  };

  const handleUpdateStatus = async (id, newStatus) => {
    try {
      await procurementApi.updatePurchaseOrderStatus(id, newStatus);
      fetchData();
    } catch (err) {
      alert("Failed to update status.");
    }
  };

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[var(--ts-border)] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <ShoppingCart className="w-6 h-6 text-cyan-400" />
            AI Procurement & Vendor Management
          </h1>
          <p className="text-xs text-[var(--ts-text-secondary)] mt-0.5">Automated Purchase Orders & AI Supply Chain Insights</p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchAIRecommendations}
            className="ts-btn-primary text-xs px-3.5 py-2"
          >
            <Bot className="w-4 h-4 text-cyan-300" /> Generate AI Order Recommendations
          </button>
          <button
            onClick={() => setShowPOModal(true)}
            className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] text-xs text-[var(--ts-text-primary)] hover:border-cyan-500 font-semibold px-3.5 py-2 rounded-xl transition"
          >
            <Plus className="w-4 h-4 inline mr-1 text-cyan-400" /> Create PO
          </button>
        </div>
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex space-x-2 border-b border-[var(--ts-border)] pb-2">
        <button
          onClick={() => setActiveTab('pos')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'pos'
              ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white'
              : 'text-[var(--ts-text-secondary)] hover:bg-[var(--ts-card-hover)]'
          }`}
        >
          Purchase Orders ({pos.length})
        </button>
        <button
          onClick={() => setActiveTab('vendors')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'vendors'
              ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white'
              : 'text-[var(--ts-text-secondary)] hover:bg-[var(--ts-card-hover)]'
          }`}
        >
          Vendors ({vendors.length})
        </button>
        <button
          onClick={fetchAIRecommendations}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition flex items-center gap-1.5 ${
            activeTab === 'ai'
              ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white'
              : 'text-[var(--ts-text-secondary)] hover:bg-[var(--ts-card-hover)]'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" /> AI Recommendations
        </button>
      </div>

      {loading ? (
        <LoadingView title="Fetching procurement records..." />
      ) : error ? (
        <ErrorView error={error} onRetry={fetchData} />
      ) : activeTab === 'pos' ? (
        <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-2xl overflow-hidden shadow-lg">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[var(--ts-border)] text-[var(--ts-text-muted)] text-[11px] uppercase tracking-wider bg-[var(--ts-bg-subtle)]">
                  <th className="py-3 px-4 font-bold">PO Code</th>
                  <th className="py-3 px-4 font-bold">Vendor ID</th>
                  <th className="py-3 px-4 font-bold">Total Amount</th>
                  <th className="py-3 px-4 font-bold">Status</th>
                  <th className="py-3 px-4 font-bold">Created Date</th>
                  <th className="py-3 px-4 font-bold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--ts-border)] text-xs">
                {pos.map((po) => (
                  <tr key={po.id} className="hover:bg-[var(--ts-card-hover)] transition-colors">
                    <td className="py-3.5 px-4 font-mono font-bold text-cyan-400">PO-{po.po_number || po.id}</td>
                    <td className="py-3.5 px-4 font-semibold text-[var(--ts-text-primary)]">Vendor #{po.vendor_id}</td>
                    <td className="py-3.5 px-4 font-bold text-[var(--ts-text-primary)]">${po.total_amount}</td>
                    <td className="py-3.5 px-4">
                      <span className={`ts-badge text-[10px] ${
                        po.status === 'Approved' || po.status === 'Completed'
                          ? 'ts-badge-success'
                          : po.status === 'Draft'
                          ? 'ts-badge-cyan'
                          : 'ts-badge-warning'
                      }`}>
                        {po.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-[var(--ts-text-muted)]">
                      {new Date(po.created_at || Date.now()).toLocaleDateString()}
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="flex gap-2">
                        {po.status === 'Draft' && (
                          <button
                            onClick={() => handleUpdateStatus(po.id, 'Approved')}
                            className="px-2 py-1 bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/30 rounded text-[10px] font-bold"
                          >
                            Approve PO
                          </button>
                        )}
                        {po.status === 'Approved' && (
                          <button
                            onClick={() => handleUpdateStatus(po.id, 'Received')}
                            className="px-2 py-1 bg-cyan-500/10 text-cyan-400 hover:bg-cyan-500/20 border border-cyan-500/30 rounded text-[10px] font-bold"
                          >
                            Mark Received
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : activeTab === 'vendors' ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {vendors.map((v) => (
            <div key={v.id} className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl space-y-2">
              <div className="flex justify-between items-start">
                <h3 className="font-bold text-sm text-[var(--ts-text-primary)]">{v.name}</h3>
                <span className="ts-badge ts-badge-cyan text-[10px]">{v.rating ? `${v.rating}/5` : 'Active'}</span>
              </div>
              <p className="text-xs text-[var(--ts-text-secondary)]"><span className="text-[var(--ts-text-muted)] font-medium">Contact:</span> {v.contact_person || v.email || 'N/A'}</p>
              <p className="text-xs text-[var(--ts-text-secondary)]"><span className="text-[var(--ts-text-muted)] font-medium">Phone:</span> {v.phone || 'N/A'}</p>
              <p className="text-xs text-[var(--ts-text-muted)]"><span className="font-medium">Lead Time:</span> {v.lead_time_days || 3} days</p>
            </div>
          ))}
        </div>
      ) : (
        /* AI Recommendations View */
        <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-6 rounded-2xl space-y-4">
          <h3 className="text-base font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <Bot className="w-5 h-5 text-cyan-400" />
            AI Purchase Order Recommendations
          </h3>

          {aiLoading ? (
            <LoadingView title="Running supply chain optimization model..." />
          ) : !aiRecs ? (
            <EmptyView title="No AI recommendations compiled" description="Click 'Generate AI Order Recommendations' above." />
          ) : (
            <div className="space-y-4">
              <p className="text-xs text-[var(--ts-text-secondary)] leading-relaxed">
                {aiRecs.summary || aiRecs.executive_summary || "AI recommends drafting purchase orders for critical items approaching minimum stock thresholds."}
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {(aiRecs.recommendations || aiRecs.items || []).map((item, idx) => (
                  <div key={idx} className="p-4 bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] rounded-xl space-y-2 text-xs">
                    <div className="flex justify-between font-bold text-[var(--ts-text-primary)]">
                      <span>{item.name || item.item_name}</span>
                      <span className="text-cyan-400">Rec. Qty: {item.recommended_quantity || item.suggested_qty || 100}</span>
                    </div>
                    <p className="text-[var(--ts-text-muted)]">Reason: {item.reason || "Stock approaching safety threshold"}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* PO Creation Modal */}
      {showPOModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] p-6 rounded-2xl max-w-lg w-full space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
              <Plus className="w-5 h-5 text-cyan-400" />
              Draft Purchase Order
            </h3>

            <form onSubmit={handleCreatePO} className="space-y-3 text-xs">
              <div>
                <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Select Vendor</label>
                <select
                  value={poForm.vendor_id}
                  onChange={(e) => setPoForm({...poForm, vendor_id: parseInt(e.target.value) || 1})}
                  className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                >
                  {vendors.map(v => (
                    <option key={v.id} value={v.id}>{v.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Total Amount ($)</label>
                <input
                  type="number"
                  step="0.01"
                  required
                  value={poForm.total_amount}
                  onChange={(e) => setPoForm({...poForm, total_amount: parseFloat(e.target.value) || 0})}
                  className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowPOModal(false)}
                  className="px-4 py-2 rounded-xl border border-[var(--ts-border)] text-[var(--ts-text-muted)]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="ts-btn-primary px-4 py-2"
                >
                  Save Draft PO
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
