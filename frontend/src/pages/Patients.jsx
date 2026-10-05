import React, { useEffect, useState } from 'react';
import clinicalApi from '../api/clinical';
import { Users, UserPlus, Search, Phone, Mail, FileText } from 'lucide-react';
import { LoadingView, ErrorView, EmptyView } from '../components/common/StateViews';

export default function Patients() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    dob: '1990-01-01',
    gender: 'Male',
    phone: '',
    email: '',
    emergency_contact: ''
  });

  const fetchPatients = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await clinicalApi.getPatients();
      setPatients(data || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch patient records from backend PostgreSQL database.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const handleCreatePatient = async (e) => {
    e.preventDefault();
    try {
      await clinicalApi.createPatient(formData);
      setShowModal(false);
      setFormData({
        first_name: '',
        last_name: '',
        dob: '1990-01-01',
        gender: 'Male',
        phone: '',
        email: '',
        emergency_contact: ''
      });
      fetchPatients();
    } catch (err) {
      alert("Failed to register patient. Please check required fields.");
    }
  };

  const filteredPatients = patients.filter(p => {
    const fullName = p.name || `${p.first_name || ''} ${p.last_name || ''}`.trim();
    const mrn = p.mrn || `MRN-${String(p.id).padStart(4, '0')}`;
    const phone = p.phone || '';
    return `${fullName} ${mrn} ${phone}`.toLowerCase().includes(search.toLowerCase());
  });

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[var(--ts-border)] pb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
            <Users className="w-6 h-6 text-cyan-400" />
            Patient Registry
          </h1>
          <p className="text-xs text-[var(--ts-text-secondary)] mt-0.5">Canonical Patient Medical Records</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-[var(--ts-text-muted)] absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search MRN, name, phone..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] text-xs text-[var(--ts-text-primary)] pl-9 pr-3 py-2 rounded-xl focus:outline-none focus:border-cyan-500 w-64"
            />
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="ts-btn-primary text-xs px-3.5 py-2"
          >
            <UserPlus className="w-4 h-4" /> Register New Patient
          </button>
        </div>
      </div>

      {loading ? (
        <LoadingView title="Fetching patient database..." />
      ) : error ? (
        <ErrorView error={error} onRetry={fetchPatients} />
      ) : filteredPatients.length === 0 ? (
        <EmptyView title="No patients found" description="Register a new patient or adjust search terms." />
      ) : (
        <div className="bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-2xl overflow-hidden shadow-lg">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[var(--ts-border)] text-[var(--ts-text-muted)] text-[11px] uppercase tracking-wider bg-[var(--ts-bg-subtle)]">
                  <th className="py-3 px-4 font-bold">MRN</th>
                  <th className="py-3 px-4 font-bold">Patient Name</th>
                  <th className="py-3 px-4 font-bold">Gender & Age / DOB</th>
                  <th className="py-3 px-4 font-bold">Department / Contact</th>
                  <th className="py-3 px-4 font-bold">Emergency Contact</th>
                  <th className="py-3 px-4 font-bold">Status / Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--ts-border)] text-xs">
                {filteredPatients.map((p) => {
                  const fullName = p.name || `${p.first_name || ''} ${p.last_name || ''}`.trim() || `Patient #${p.id}`;
                  const mrn = p.mrn || `MRN-${String(p.id).padStart(4, '0')}`;
                  const ageDob = p.dob || (p.age ? `${p.age} yrs` : 'N/A');
                  const deptName = p.department?.name || (p.department_id ? `Dept #${p.department_id}` : 'General');
                  return (
                    <tr key={p.id} className="hover:bg-[var(--ts-card-hover)] transition-colors">
                      <td className="py-3.5 px-4 font-mono font-bold text-cyan-400">{mrn}</td>
                      <td className="py-3.5 px-4 font-semibold text-[var(--ts-text-primary)]">
                        {fullName}
                      </td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-secondary)]">
                        <span className="ts-badge ts-badge-cyan text-[10px] mr-2">{p.gender}</span>
                        <span>{ageDob}</span>
                      </td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-secondary)]">
                        <div className="space-y-0.5">
                          <div className="font-semibold text-cyan-300">{deptName}</div>
                          {p.phone && <div className="flex items-center gap-1.5 text-[var(--ts-text-muted)]"><Phone className="w-3 h-3" />{p.phone}</div>}
                          {p.email && <div className="flex items-center gap-1.5 text-[var(--ts-text-muted)]"><Mail className="w-3 h-3" />{p.email}</div>}
                        </div>
                      </td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-muted)]">{p.emergency_contact || 'N/A'}</td>
                      <td className="py-3.5 px-4 text-[var(--ts-text-muted)]">
                        <div className="space-y-0.5">
                          {p.status && <span className="ts-badge ts-badge-cyan text-[10px] block w-fit mb-1">{p.status}</span>}
                          <div>{p.admission_date ? new Date(p.admission_date).toLocaleDateString() : (p.created_at ? new Date(p.created_at).toLocaleDateString() : 'Active')}</div>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] p-6 rounded-2xl max-w-lg w-full space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-[var(--ts-text-primary)] flex items-center gap-2">
              <UserPlus className="w-5 h-5 text-cyan-400" />
              Register New Patient
            </h3>

            <form onSubmit={handleCreatePatient} className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">First Name</label>
                  <input
                    type="text"
                    required
                    value={formData.first_name}
                    onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                    className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Last Name</label>
                  <input
                    type="text"
                    required
                    value={formData.last_name}
                    onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                    className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Date of Birth</label>
                  <input
                    type="date"
                    required
                    value={formData.dob}
                    onChange={(e) => setFormData({...formData, dob: e.target.value})}
                    className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Gender</label>
                  <select
                    value={formData.gender}
                    onChange={(e) => setFormData({...formData, gender: e.target.value})}
                    className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Phone Number</label>
                <input
                  type="text"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-[var(--ts-text-muted)] font-semibold mb-1">Emergency Contact</label>
                <input
                  type="text"
                  value={formData.emergency_contact}
                  onChange={(e) => setFormData({...formData, emergency_contact: e.target.value})}
                  className="w-full bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-xl px-3 py-2 text-[var(--ts-text-primary)] focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl border border-[var(--ts-border)] text-[var(--ts-text-muted)] hover:text-[var(--ts-text-primary)]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="ts-btn-primary px-4 py-2"
                >
                  Save Registration
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
