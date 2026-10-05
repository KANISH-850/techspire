import React, { useEffect, useState } from 'react';
import clinicalApi from '../api/clinical';
import { Bed, CheckCircle, AlertTriangle, Activity } from 'lucide-react';
import { LoadingView, ErrorView, EmptyView } from '../components/common/StateViews';

const DEPARTMENTS = {
  1: 'Cardiology Ward',
  2: 'Neurology Ward',
  3: 'Orthopedics Ward',
  4: 'Emergency Ward',
  5: 'Pediatrics Ward'
};

export default function Beds() {
  const [beds, setBeds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBeds = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await clinicalApi.getBeds();
      setBeds(data || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch bed inventory and status.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBeds();
  }, []);

  const totalBeds = beds.length;
  const occupiedBeds = beds.filter(b => b.is_occupied || b.status?.toLowerCase() === 'occupied').length;
  const occupancyRate = totalBeds > 0 ? Math.round((occupiedBeds / totalBeds) * 100) : 0;

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[var(--ts-border)] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <Bed className="w-6 h-6 text-cyan-400" />
            Bed Occupancy & Allocation
          </h1>
          <p className="text-xs text-[var(--ts-text-secondary)] mt-0.5">Ward & ICU Bed Status Overview</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="bg-[var(--ts-card-bg)] px-4 py-2 rounded-xl border border-[var(--ts-border)] flex items-center gap-3 text-xs">
            <span className="text-[var(--ts-text-muted)]">Occupancy:</span>
            <span className="font-bold text-cyan-400">{occupiedBeds} / {totalBeds} ({occupancyRate}%)</span>
          </div>
        </div>
      </div>

      {loading ? (
        <LoadingView title="Loading bed capacity grid..." />
      ) : error ? (
        <ErrorView error={error} onRetry={fetchBeds} />
      ) : beds.length === 0 ? (
        <EmptyView title="No bed data available" description="No beds registered in database." />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {beds.map((b) => {
            const isOccupied = b.is_occupied || b.status?.toLowerCase() === 'occupied';
            const deptName = b.department_name || b.department?.name || DEPARTMENTS[b.department_id] || `Ward #${b.department_id}`;
            return (
              <div
                key={b.id}
                className={`p-4 rounded-2xl border transition-all space-y-3 ${
                  isOccupied
                    ? 'bg-rose-500/10 border-rose-500/30'
                    : 'bg-[var(--ts-card-bg)] border-[var(--ts-border)] hover:border-cyan-500/40'
                }`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex items-center gap-2">
                    <Bed className={`w-5 h-5 ${isOccupied ? 'text-rose-400' : 'text-emerald-400'}`} />
                    <span className="font-bold text-sm text-[var(--ts-text-primary)]">{b.bed_number}</span>
                  </div>
                  <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full border ${
                    isOccupied
                      ? 'bg-rose-500/20 text-rose-400 border-rose-500/30'
                      : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                  }`}>
                    {isOccupied ? 'Occupied' : 'Available'}
                  </span>
                </div>

                <div className="text-xs space-y-1 text-[var(--ts-text-secondary)]">
                  <div><span className="text-[var(--ts-text-muted)] font-medium">Department:</span> <span className="font-semibold text-cyan-300">{deptName}</span></div>
                  <div><span className="text-[var(--ts-text-muted)] font-medium">Bed Type:</span> {b.bed_type || 'Standard Ward'}</div>
                  {b.daily_rate && (
                    <div><span className="text-[var(--ts-text-muted)] font-medium">Daily Rate:</span> ${b.daily_rate}/day</div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
