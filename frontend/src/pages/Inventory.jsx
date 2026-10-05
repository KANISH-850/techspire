import React, { useEffect, useState } from 'react';
import inventoryApi from '../api/inventory';
import { 
  Package, AlertTriangle, Clock, Plus, Activity, CheckCircle, Search 
} from 'lucide-react';
import { LoadingView, ErrorView, EmptyView } from '../components/common/StateViews';

export default function Inventory() {
  const [status, setStatus] = useState(null);
  const [items, setItems] = useState([]);
  const [lowStock, setLowStock] = useState([]);
  const [expiry, setExpiry] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [search, setSearch] = useState('');

  const [formData, setFormData] = useState({
    name: '',
    category: 'Pharmaceutical',
    quantity: 100,
    unit: 'boxes',
    unit_price: 15.5,
    min_stock_level: 20,
    vendor_id: 1,
    expiration_date: '2026-12-31'
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [statusRes, itemsRes, lowRes, expRes] = await Promise.all([
        inventoryApi.getStatus(),
        inventoryApi.getItems(),
        inventoryApi.getLowStock(),
        inventoryApi.getExpiryAlerts()
      ]);
      setStatus(statusRes);
      setItems(itemsRes || []);
      setLowStock(lowRes || []);
      setExpiry(expRes || []);
    } catch (err) {
      console.error(err);
      setError("Failed to load hospital inventory status.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreateItem = async (e) => {
    e.preventDefault();
    try {
      await inventoryApi.createItem(formData);
      setShowModal(false);
      fetchData();
    } catch (err) {
      alert("Failed to add inventory item.");
    }
  };

  const filteredItems = items.filter(i => 
    `${i.name} ${i.category} ${i.sku}`.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[var(--ts-border)] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <Package className="w-6 h-6 text-cyan-400" />
            Hospital Inventory Management
          </h1>
          <p className="text-xs text-[var(--ts-text-secondary)] mt-0.5">Medicine Stock, Medical Supplies & Expiration Alerts</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-[var(--ts-text-muted)] absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search item name, category..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] text-xs text-[var(--ts-text-primary)] pl-9 pr-3 py-2 rounded-xl focus:outline-none focus:border-cyan-500 w-64"
            />
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="ts-btn-primary text-xs px-3.5 py-2"
          >
            <Plus className="w-4 h-4" /> Add Inventory Item
          </button>
        </div>
      </div>

      {loading ? (
        <LoadingView title="Fetching inventory records..." />
      ) : error ? (
        <ErrorView error={error} onRetry={fetchData} />
      ) : (
        <div className="space-y-6">
          {/* Overview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl">
              <span className="text-[11px] text-[var(--ts-text-muted)] font-semibold uppercase">Total Items</span>
              <p className="text-2xl font-black text-[var(--ts-text-primary)] mt-1">{status?.total_items || items.length}</p>
            </div>
            <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl">
              <span className="text-[11px] text-[var(--ts-text-muted)] font-semibold uppercase">Low Stock Alerts</span>
              <p className="text-2xl font-black text-amber-400 mt-1">{lowStock.length}</p>
            </div>
            <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl">
              <span className="text-[11px] text-[var(--ts-text-muted)] font-semibold uppercase">Expiring Items</span>
              <p className="text-2xl font-black text-rose-400 mt-1">{expiry.length}</p>
            </div>
            <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] p-4 rounded-2xl">
              <span className="text-[11px] text-[var(--ts-text-muted)] font-semibold uppercase">Total Inventory Value</span>
              <p className="text-2xl font-black text-cyan-400 mt-1">${(status?.total_value || 0).toLocaleString()}</p>
            </div>
          </div>

          {/* Table */}
          <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-2xl overflow-hidden shadow-lg">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-[var(--ts-border)] text-[var(--ts-text-muted)] text-[11px] uppercase tracking-wider bg-[var(--ts-bg-subtle)]">
                    <th className="py-3 px-4 font-bold">Item Name</th>
                    <th className="py-3 px-4 font-bold">Category</th>
                    <th className="py-3 px-4 font-bold">In Stock</th>
                    <th className="py-3 px-4 font-bold">Min Stock</th>
                    <th className="py-3 px-4 font-bold">Unit Price</th>
                    <th className="py-3 px-4 font-bold">Expiry Date</th>
                    <th className="py-3 px-4 font-bold">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--ts-border)] text-xs">
                  {filteredItems.map((item) => {
                    const isLow = item.quantity <= item.min_stock_level;
                    return (
                      <tr key={item.id} className="hover:bg-[var(--ts-card-hover)] transition-colors">
                        <td className="py-3.5 px-4 font-semibold text-[var(--ts-text-primary)]">{item.name}</td>
                        <td className="py-3.5 px-4 text-[var(--ts-text-secondary)]">{item.category}</td>
                        <td className="py-3.5 px-4 font-bold text-cyan-400">{item.quantity} {item.unit}</td>
                        <td className="py-3.5 px-4 text-[var(--ts-text-muted)]">{item.min_stock_level}</td>
                        <td className="py-3.5 px-4 font-medium text-[var(--ts-text-primary)]">${item.unit_price}</td>
                        <td className="py-3.5 px-4 text-[var(--ts-text-muted)]">{item.expiration_date || 'N/A'}</td>
                        <td className="py-3.5 px-4">
                          {isLow ? (
                            <span className="ts-badge ts-badge-warning text-[10px]">Low Stock</span>
                          ) : (
                            <span className="ts-badge ts-badge-success text-[10px]">Optimal</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] p-6 rounded-2xl max-w-lg w-full space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
              <Plus className="w-5 h-5 text-cyan-400" />
              Add Inventory Item
            </h3>

            <form onSubmit={handleCreateItem} className="space-y-3 text-xs">
              <div>
                <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Item Name</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Category</label>
                  <input
                    type="text"
                    required
                    value={formData.category}
                    onChange={(e) => setFormData({...formData, category: e.target.value})}
                    className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Quantity</label>
                  <input
                    type="number"
                    required
                    value={formData.quantity}
                    onChange={(e) => setFormData({...formData, quantity: parseInt(e.target.value) || 0})}
                    className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Unit Price ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={formData.unit_price}
                    onChange={(e) => setFormData({...formData, unit_price: parseFloat(e.target.value) || 0})}
                    className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Min Stock Level</label>
                  <input
                    type="number"
                    required
                    value={formData.min_stock_level}
                    onChange={(e) => setFormData({...formData, min_stock_level: parseInt(e.target.value) || 0})}
                    className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl border border-[var(--ts-border)] text-[var(--ts-text-muted)]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="ts-btn-primary px-4 py-2"
                >
                  Save Item
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
