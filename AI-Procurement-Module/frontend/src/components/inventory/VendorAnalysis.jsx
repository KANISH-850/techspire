import React from 'react';
import { Star } from 'lucide-react';

export default function VendorAnalysis({ vendors }) {
  if (!vendors || vendors.length === 0) return <div className="text-slate-500 p-4">No vendors found.</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {vendors.map(vendor => (
        <div key={vendor.id} className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h3 className="text-lg font-bold text-slate-900">{vendor.name}</h3>
              <p className="text-sm text-slate-500">{vendor.contact_person}</p>
            </div>
            <div className="flex items-center text-amber-500">
              <Star className="w-4 h-4 fill-current" />
              <span className="ml-1 text-sm font-medium">{vendor.rating}</span>
            </div>
          </div>
          
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-500">Items Supplied:</span>
              <span className="font-medium text-slate-900">{vendor.supplied_items}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-500">Avg Delivery:</span>
              <span className="font-medium text-slate-900">{vendor.average_delivery_days} days</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-500">Reliability Score:</span>
              <span className="font-medium text-emerald-600">{vendor.reliability_score}%</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-500">Total PO Value:</span>
              <span className="font-medium text-blue-600">${vendor.total_value.toLocaleString()}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-500">Active Orders:</span>
              <span className="font-medium text-slate-900">{vendor.active_orders}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
