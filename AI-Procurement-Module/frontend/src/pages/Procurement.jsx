import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Layers, Activity, AlertTriangle, Users, Bot, ShoppingCart } from 'lucide-react';
import InventoryOverview from '../components/inventory/InventoryOverview';
import LowStockTable from '../components/inventory/LowStockTable';
import ExpiryAlerts from '../components/inventory/ExpiryAlerts';
import VendorAnalysis from '../components/inventory/VendorAnalysis';
import AIRecommendations from '../components/inventory/AIRecommendations';
import PurchaseOrders from '../components/inventory/PurchaseOrders';

const API_URL = 'http://localhost:8003/api/v1/inventory';

export default function Procurement() {
  const [activeTab, setActiveTab] = useState('overview');
  
  const [status, setStatus] = useState(null);
  const [lowStock, setLowStock] = useState([]);
  const [expiry, setExpiry] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [pos, setPos] = useState([]);
  const [aiData, setAiData] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [resStatus, resLowStock, resExpiry, resVendors, resPos] = await Promise.all([
        axios.get(`${API_URL}/status`),
        axios.get(`${API_URL}/low-stock`),
        axios.get(`${API_URL}/expiry`),
        axios.get(`${API_URL}/vendors`),
        axios.get(`${API_URL}/purchase-orders`)
      ]);
      setStatus(resStatus.data);
      setLowStock(resLowStock.data);
      setExpiry(resExpiry.data);
      setVendors(resVendors.data);
      setPos(resPos.data);
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err);
    }
  };

  const fetchAIRecommendations = async () => {
    setAiLoading(true);
    setActiveTab('ai');
    try {
      const res = await axios.get(`${API_URL}/ai-recommendations`);
      setAiData(res.data);
    } catch (err) {
      console.error("AI failed:", err);
    } finally {
      setAiLoading(false);
    }
  };

  const handleCreatePO = async (item) => {
    try {
      const payload = {
        vendor_id: item.vendor_id || 1, // Fallback if null
        status: "Draft",
        total_amount: item.unit_price * item.recommended_quantity,
        items: [{
          inventory_item_id: item.id,
          quantity: item.recommended_quantity,
          unit_price: item.unit_price,
          total_price: item.unit_price * item.recommended_quantity
        }]
      };
      await axios.post(`${API_URL}/purchase-orders`, payload);
      alert("Purchase order drafted successfully!");
      fetchDashboardData();
      setActiveTab('pos');
    } catch (err) {
      alert("Failed to create PO.");
    }
  };

  const handleUpdatePOStatus = async (poId, newStatus) => {
    try {
      await axios.patch(`${API_URL}/purchase-orders/${poId}`, { status: newStatus });
      fetchDashboardData();
    } catch (err) {
      alert("Failed to update PO status.");
    }
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: <Layers className="w-4 h-4" /> },
    { id: 'low_stock', label: 'Low Stock', icon: <Activity className="w-4 h-4" /> },
    { id: 'expiry', label: 'Expiry Alerts', icon: <AlertTriangle className="w-4 h-4" /> },
    { id: 'vendors', label: 'Vendors', icon: <Users className="w-4 h-4" /> },
    { id: 'pos', label: 'Purchase Orders', icon: <ShoppingCart className="w-4 h-4" /> },
    { id: 'ai', label: 'AI Recommendations', icon: <Bot className="w-4 h-4" /> },
  ];

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Procurement & Inventory</h1>
          <p className="text-slate-500 mt-1">Manage stock, suppliers, and AI-driven purchase insights.</p>
        </div>
        <button 
          onClick={fetchAIRecommendations}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition shadow-sm shadow-blue-500/20"
        >
          <Bot className="w-5 h-5" /> Generate AI Insights
        </button>
      </div>

      <div className="border-b border-slate-200">
        <nav className="flex space-x-8" aria-label="Tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition
                ${activeTab === tab.id 
                  ? 'border-blue-500 text-blue-600' 
                  : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                }
              `}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="mt-6">
        {activeTab === 'overview' && <InventoryOverview status={status} />}
        {activeTab === 'low_stock' && <LowStockTable items={lowStock} onCreatePO={handleCreatePO} />}
        {activeTab === 'expiry' && <ExpiryAlerts items={expiry} />}
        {activeTab === 'vendors' && <VendorAnalysis vendors={vendors} />}
        {activeTab === 'pos' && <PurchaseOrders orders={pos} onUpdateStatus={handleUpdatePOStatus} />}
        {activeTab === 'ai' && <AIRecommendations recommendations={aiData} loading={aiLoading} />}
      </div>
    </div>
  );
}
