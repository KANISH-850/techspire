import React from 'react';

export default function ExpiryAlerts({ items }) {
  if (!items || items.length === 0) return <div className="text-slate-500 p-4">No expiring items found.</div>;

  const getStatusColor = (status) => {
    if (status === "Expired") return "bg-rose-100 text-rose-800";
    if (status.includes("7 days")) return "bg-orange-100 text-orange-800";
    return "bg-amber-100 text-amber-800";
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <table className="min-w-full divide-y divide-slate-200">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Item</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Batch</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Expiry Date</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Days Remaining</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Stock</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Status</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-slate-200">
          {items.map((item, idx) => (
            <tr key={idx} className="hover:bg-slate-50">
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">{item.name}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{item.batch_number || "N/A"}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{item.expiry_date}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900 font-bold">{item.days_remaining}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{item.current_stock}</td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(item.status)}`}>
                  {item.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
