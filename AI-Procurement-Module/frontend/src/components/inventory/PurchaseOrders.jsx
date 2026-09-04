import React from 'react';
import { FileText, CheckCircle, Clock, XCircle, ArrowRightCircle } from 'lucide-react';

export default function PurchaseOrders({ orders, onUpdateStatus }) {
  if (!orders || orders.length === 0) return <div className="text-slate-500 p-4">No purchase orders found.</div>;

  const getStatusIcon = (status) => {
    switch(status) {
      case 'Draft': return <FileText className="w-4 h-4 text-slate-500" />;
      case 'Pending': return <Clock className="w-4 h-4 text-amber-500" />;
      case 'Approved': return <CheckCircle className="w-4 h-4 text-blue-500" />;
      case 'Ordered': return <ArrowRightCircle className="w-4 h-4 text-indigo-500" />;
      case 'Received': return <CheckCircle className="w-4 h-4 text-emerald-500" />;
      case 'Cancelled': return <XCircle className="w-4 h-4 text-rose-500" />;
      default: return null;
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'Draft': return 'bg-slate-100 text-slate-800';
      case 'Pending': return 'bg-amber-100 text-amber-800';
      case 'Approved': return 'bg-blue-100 text-blue-800';
      case 'Ordered': return 'bg-indigo-100 text-indigo-800';
      case 'Received': return 'bg-emerald-100 text-emerald-800';
      case 'Cancelled': return 'bg-rose-100 text-rose-800';
      default: return 'bg-slate-100 text-slate-800';
    }
  };

  const nextStatus = {
    'Draft': 'Pending',
    'Pending': 'Approved',
    'Approved': 'Ordered',
    'Ordered': 'Received'
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <table className="min-w-full divide-y divide-slate-200">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">PO ID</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Vendor</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Date Created</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Total Amount</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Status</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-slate-200">
          {orders.map((po) => (
            <tr key={po.id} className="hover:bg-slate-50">
              <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-slate-900">PO-{po.id.toString().padStart(4, '0')}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{po.vendor_id} (ID)</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{new Date(po.created_at).toLocaleDateString()}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-slate-900">${po.total_amount.toLocaleString()}</td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className={`px-2 py-1 inline-flex items-center gap-1 text-xs font-semibold rounded-full ${getStatusColor(po.status)}`}>
                  {getStatusIcon(po.status)} {po.status}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                {nextStatus[po.status] && (
                  <button 
                    onClick={() => onUpdateStatus(po.id, nextStatus[po.status])}
                    className="text-blue-600 hover:text-blue-900 mr-3"
                  >
                    Mark {nextStatus[po.status]}
                  </button>
                )}
                {po.status !== 'Received' && po.status !== 'Cancelled' && (
                  <button 
                    onClick={() => onUpdateStatus(po.id, 'Cancelled')}
                    className="text-rose-600 hover:text-rose-900"
                  >
                    Cancel
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
