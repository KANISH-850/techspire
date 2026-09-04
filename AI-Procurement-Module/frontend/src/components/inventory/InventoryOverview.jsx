import React from 'react';
import { Package, AlertTriangle, Clock, ArchiveX, ShoppingCart, Activity } from 'lucide-react';

export default function InventoryOverview({ status }) {
  if (!status) return <div className="text-slate-500 p-4">Loading overview...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div className="bg-blue-100 p-3 rounded-lg text-blue-600">
          <Package className="w-6 h-6" />
        </div>
        <div>
          <p className="text-sm font-medium text-slate-500">Total Inventory Items</p>
          <p className="text-2xl font-bold text-slate-800">{status.total_items}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div className="bg-amber-100 p-3 rounded-lg text-amber-600">
          <Activity className="w-6 h-6" />
        </div>
        <div>
          <p className="text-sm font-medium text-slate-500">Low Stock</p>
          <p className="text-2xl font-bold text-slate-800">{status.low_stock}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div className="bg-red-100 p-3 rounded-lg text-red-600">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <div>
          <p className="text-sm font-medium text-slate-500">Critical Stock</p>
          <p className="text-2xl font-bold text-slate-800">{status.critical_stock}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div className="bg-orange-100 p-3 rounded-lg text-orange-600">
          <Clock className="w-6 h-6" />
        </div>
        <div>
          <p className="text-sm font-medium text-slate-500">Expiring Soon</p>
          <p className="text-2xl font-bold text-slate-800">{status.expiring_soon}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div className="bg-rose-100 p-3 rounded-lg text-rose-600">
          <ArchiveX className="w-6 h-6" />
        </div>
        <div>
          <p className="text-sm font-medium text-slate-500">Expired</p>
          <p className="text-2xl font-bold text-slate-800">{status.expired}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div className="bg-emerald-100 p-3 rounded-lg text-emerald-600">
          <ShoppingCart className="w-6 h-6" />
        </div>
        <div>
          <p className="text-sm font-medium text-slate-500">Pending Purchase Orders</p>
          <p className="text-2xl font-bold text-slate-800">{status.pending_pos}</p>
        </div>
      </div>

    </div>
  );
}
