import React from 'react';
import { ShoppingCart } from 'lucide-react';

export default function LowStockTable({ items, onCreatePO }) {
  if (!items || items.length === 0) return <div className="text-slate-500 p-4">No low stock items found. Inventory is healthy!</div>;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <table className="min-w-full divide-y divide-slate-200">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Item</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Category</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Current Stock</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Min / Max</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Vendor</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Priority</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Action</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-slate-200">
          {items.map((item) => (
            <tr key={item.id} className="hover:bg-slate-50">
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">{item.name}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{item.category}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900 font-bold">{item.current_stock} {item.unit}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{item.minimum_stock} / {item.maximum_stock}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{item.vendor_name}</td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${item.priority === 'Critical' ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'}`}>
                  {item.priority}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button 
                  onClick={() => onCreatePO(item)}
                  className="text-blue-600 hover:text-blue-900 flex items-center gap-1"
                >
                  <ShoppingCart className="w-4 h-4" /> Reorder ({item.recommended_quantity})
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
