import React, { useEffect, useState } from 'react';
import clinicalApi from '../api/clinical';
import { Activity, Clock, CheckCircle, Bed } from 'lucide-react';
import { LoadingView, ErrorView, EmptyView } from '../components/common/StateViews';

const PATIENTS = {
  1: 'John Doe',
  2: 'Jane Smith',
  3: 'Robert Johnson',
  4: 'Emily Davis'
};

const DEPARTMENTS = {
  1: 'Cardiology',
  2: 'Neurology',
  3: 'Orthopedics',
  4: 'Emergency',
  5: 'Pediatrics'
};

export default function Admissions() {
  const [admissions, setAdmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAdmissions = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await clinicalApi.getAdmissions();
      setAdmissions(data || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch inpatient admissions.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdmissions();
  }, []);

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12">
      <div className="flex justify-between items-center border-b border-[var(--ts-border)] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <Activity className="w-6 h-6 text-cyan-400" />
            Inpatient Admissions
          </h1>
          <p className="text-xs text-[var(--ts-text-secondary)] mt-0.5">Active Inpatients & Discharge Logs</p>
        </div>
      </div>

      {loading ? (
        <LoadingView title="Loading admission records..." />
      ) : error ? (
        <ErrorView error={error} onRetry={fetchAdmissions} />
      ) : admissions.length === 0 ? (
        <EmptyView title="No active admissions" description="No inpatient admission records registered." />
      ) : (
        <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-2xl overflow-hidden shadow-lg">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[var(--ts-border)] text-[var(--ts-text-muted)] text-[11px] uppercase tracking-wider bg-[var(--ts-bg-subtle)]">
                  <th className="py-3 px-4 font-bold">Admission ID</th>
                  <th className="py-3 px-4 font-bold">Patient Name</th>
                  <th className="py-3 px-4 font-bold">Department / Bed</th>
                  <th className="py-3 px-4 font-bold">Admission Date</th>
                  <th className="py-3 px-4 font-bold">Discharge Date</th>
                  <th className="py-3 px-4 font-bold">Status</th>
                  <th className="py-3 px-4 font-bold">Diagnosis / Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--ts-border)] text-xs">
                {admissions.map((adm) => {
                  const patientName = adm.patient_name || adm.patient?.name || PATIENTS[adm.patient_id] || `Patient #${adm.patient_id}`;
                  const deptName = adm.department_name || DEPARTMENTS[adm.department_id] || `Dept #${adm.department_id}`;
                  return (
                    <tr key={adm.id} className="hover:bg-[var(--ts-card-hover)] transition-colors">
                      <td className="py-3.5 px-4 font-mono font-bold text-cyan-400">ADM-{String(adm.id).padStart(4, '0')}</td>
                      <td className="py-3.5 px-4 font-semibold text-[var(--ts-text-primary)]">{patientName}</td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-secondary)] font-mono">
                        <span className="flex items-center gap-1.5"><Bed className="w-3.5 h-3.5 text-cyan-400" /> {deptName} (Bed #{adm.bed_id || 'Auto'})</span>
                      </td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-secondary)]">
                        {new Date(adm.admission_date).toLocaleString()}
                      </td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-muted)]">
                        {adm.discharge_date ? new Date(adm.discharge_date).toLocaleString() : 'Currently Admitted'}
                      </td>
                      <td className="py-3.5 px-4">
                        {adm.status?.toUpperCase() === 'DISCHARGED' ? (
                          <span className="ts-badge ts-badge-success text-[10px]"><CheckCircle className="w-3 h-3" /> Discharged</span>
                        ) : (
                          <span className="ts-badge ts-badge-warning text-[10px]"><Clock className="w-3 h-3" /> Admitted</span>
                        )}
                      </td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-muted)]">{adm.diagnosis || adm.reason || 'Observations'}</td>
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
