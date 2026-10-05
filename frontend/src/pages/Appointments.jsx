import React, { useEffect, useState } from 'react';
import clinicalApi from '../api/clinical';
import { Calendar, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { LoadingView, ErrorView, EmptyView } from '../components/common/StateViews';

const DEPARTMENTS = {
  1: 'Cardiology',
  2: 'Neurology',
  3: 'Orthopedics',
  4: 'Emergency',
  5: 'Pediatrics'
};

const PATIENTS = {
  1: 'John Doe',
  2: 'Jane Smith',
  3: 'Robert Johnson',
  4: 'Emily Davis'
};

export default function Appointments() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAppointments = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await clinicalApi.getAppointments();
      setAppointments(data || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch appointment schedules.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const StatusBadge = ({ status }) => {
    switch (status?.toUpperCase()) {
      case 'COMPLETED':
        return <span className="ts-badge ts-badge-success text-[10px]"><CheckCircle className="w-3 h-3" /> Completed</span>;
      case 'CANCELLED':
        return <span className="ts-badge ts-badge-danger text-[10px]"><XCircle className="w-3 h-3" /> Cancelled</span>;
      default:
        return <span className="ts-badge ts-badge-cyan text-[10px]"><Clock className="w-3 h-3" /> {status || 'Scheduled'}</span>;
    }
  };

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12">
      <div className="flex justify-between items-center border-b border-[var(--ts-border)] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <Calendar className="w-6 h-6 text-cyan-400" />
            Appointments Management
          </h1>
          <p className="text-xs text-[var(--ts-text-secondary)] mt-0.5">Outpatient Schedules & Status</p>
        </div>
      </div>

      {loading ? (
        <LoadingView title="Fetching appointment records..." />
      ) : error ? (
        <ErrorView error={error} onRetry={fetchAppointments} />
      ) : appointments.length === 0 ? (
        <EmptyView title="No appointments found" description="No scheduled outpatient appointments currently exist." />
      ) : (
        <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-2xl overflow-hidden shadow-lg">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[var(--ts-border)] text-[var(--ts-text-muted)] text-[11px] uppercase tracking-wider bg-[var(--ts-bg-subtle)]">
                  <th className="py-3 px-4 font-bold">Appt ID</th>
                  <th className="py-3 px-4 font-bold">Patient Name</th>
                  <th className="py-3 px-4 font-bold">Department</th>
                  <th className="py-3 px-4 font-bold">Date & Time</th>
                  <th className="py-3 px-4 font-bold">Status</th>
                  <th className="py-3 px-4 font-bold">Notes / Reason</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--ts-border)] text-xs">
                {appointments.map((a) => {
                  const patientName = a.patient_name || a.patient?.name || PATIENTS[a.patient_id] || `Patient #${a.patient_id}`;
                  const deptName = a.department_name || a.department?.name || DEPARTMENTS[a.department_id] || `Dept #${a.department_id}`;
                  return (
                    <tr key={a.id} className="hover:bg-[var(--ts-card-hover)] transition-colors">
                      <td className="py-3.5 px-4 font-mono font-bold text-cyan-400">#APT-{String(a.id).padStart(3, '0')}</td>
                      <td className="py-3.5 px-4 font-semibold text-[var(--ts-text-primary)]">{patientName}</td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-secondary)] font-medium text-cyan-300">{deptName}</td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-secondary)]">
                        {new Date(a.appointment_date).toLocaleString()}
                      </td>
                      <td className="py-3.5 px-4">
                        <StatusBadge status={a.status} />
                      </td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-muted)]">{a.notes || a.reason || 'Routine Checkup'}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
