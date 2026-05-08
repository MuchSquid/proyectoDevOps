import React, { useState, useEffect } from 'react';
import { getFines, createFine, payFine, cancelFine } from '../api/api-fines';
import { getUsers } from '../api/api-users';
import { getLoans } from '../api/api-loans';
import { 
  HiOutlineBanknotes, 
  HiOutlinePlus, 
  HiOutlineClock, 
  HiOutlineCheckCircle, 
  HiOutlineChartBar, 
  HiOutlineExclamationTriangle, 
  HiOutlineCreditCard, 
  HiOutlineXMark 
} from 'react-icons/hi2';

const emptyForm = { user_id: '', loan_id: '', amount: '', reason: '' };

const Modal = ({ title, onClose, children }) => (
  <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
    <div className="modal">
      <div className="modal-header">
        <span className="modal-title">{title}</span>
        <button className="modal-close btn" onClick={onClose}><HiOutlineXMark /></button>
      </div>
      {children}
    </div>
  </div>
);

const statusBadge = status => {
  const s = (status || 'cancelled').toLowerCase();
  return <span className={`badge badge-${s}`}>{s}</span>;
};

const FinesPage = () => {
  const [fines, setFines] = useState([]);
  const [users, setUsers] = useState([]);
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  const load = async () => {
    setLoading(true); setError(null);
    try {
      const [f, u, l] = await Promise.all([
        getFines({ limit: 100 }),
        getUsers({ limit: 100 }),
        getLoans({ limit: 100 }),
      ]);
      setFines(f); setUsers(u); setLoans(l);
    } catch { setError('No se pudo conectar al backend'); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const getUserName = id => { const u = users.find(u => u.id === id); return u ? `${u.first_name} ${u.last_name}` : `User #${id}`; };

  const filtered = fines.filter(f => {
    const q = search.toLowerCase();
    return getUserName(f.user_id).toLowerCase().includes(q) || f.reason?.toLowerCase().includes(q);
  });

  const totalPending = fines.filter(f => f.status === 'pending').reduce((acc, f) => acc + parseFloat(f.amount || 0), 0);
  const totalPaid = fines.filter(f => f.status === 'paid').reduce((acc, f) => acc + parseFloat(f.amount || 0), 0);

  const handleCreate = async e => {
    e.preventDefault(); setSaving(true);
    try {
      await createFine({ user_id: +form.user_id, loan_id: +form.loan_id, amount: form.amount, reason: form.reason });
      setShowModal(false); await load();
    } catch (err) { alert(err.response?.data?.detail || 'Error al crear multa'); }
    finally { setSaving(false); }
  };

  const handlePay = async id => {
    try { await payFine(id); await load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error'); }
  };

  const handleCancel = async id => {
    if (!confirm('¿Cancelar multa?')) return;
    try { await cancelFine(id); await load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error'); }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <div className="page-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <HiOutlineBanknotes /> Multas
          </div>
          <div className="page-subtitle">{fines.length} multas registradas</div>
        </div>
        <button className="btn btn-primary" onClick={() => { setForm(emptyForm); setShowModal(true); }}>
          <HiOutlinePlus style={{ marginRight: '0.4rem' }} /> Nueva multa
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon"><HiOutlineClock /></div>
          <div className="stat-label">Pendiente</div>
          <div className="stat-value" style={{ color: 'var(--warning)' }}>${totalPending.toFixed(2)}</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon"><HiOutlineCheckCircle /></div>
          <div className="stat-label">Cobrado</div>
          <div className="stat-value" style={{ color: 'var(--success)' }}>${totalPaid.toFixed(2)}</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon"><HiOutlineChartBar /></div>
          <div className="stat-label">Total multas</div>
          <div className="stat-value">{fines.length}</div>
        </div>
      </div>

      <div className="toolbar">
        <input placeholder="Buscar por usuario o razón…" value={search} onChange={e => setSearch(e.target.value)} />
      </div>

      {loading && <div className="loading-wrapper"><div className="spinner" /><span>Cargando multas…</span></div>}
      {error && (
        <div className="empty-state">
          <HiOutlineExclamationTriangle style={{ fontSize: '2.5rem', color: 'var(--danger)' }} />
          <h3>Error</h3>
          <p>{error}</p>
          <button className="btn btn-ghost" style={{ marginTop: '1rem' }} onClick={load}>Reintentar</button>
        </div>
      )}

      {!loading && !error && (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Usuario</th>
                <th>Préstamo</th>
                <th>Monto</th>
                <th>Razón</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr><td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>Sin resultados</td></tr>
              )}
              {filtered.map(f => (
                <tr key={f.id}>
                  <td style={{ color: 'var(--text-muted)' }}>#{f.id}</td>
                  <td>{getUserName(f.user_id)}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>#{f.loan_id}</td>
                  <td><strong style={{ color: 'var(--warning)' }}>${parseFloat(f.amount).toFixed(2)}</strong></td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.82rem' }}>{f.reason}</td>
                  <td>{statusBadge(f.status)}</td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.4rem' }}>
                      {f.status === 'PENDING' && (
                        <>
                          <button className="btn btn-success btn-sm" onClick={() => handlePay(f.id)}>
                            <HiOutlineCreditCard style={{ marginRight: '0.3rem' }} /> Pagar
                          </button>
                          <button className="btn btn-danger btn-sm" onClick={() => handleCancel(f.id)}>
                            <HiOutlineXMark />
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <Modal title="Nueva multa" onClose={() => setShowModal(false)}>
          <form className="form-grid" onSubmit={handleCreate}>
            <div className="form-group">
              <label className="form-label">Usuario *</label>
              <select required value={form.user_id} onChange={e => setForm(f => ({ ...f, user_id: e.target.value }))}>
                <option value="">Seleccionar usuario…</option>
                {users.map(u => <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Préstamo *</label>
              <select required value={form.loan_id} onChange={e => setForm(f => ({ ...f, loan_id: e.target.value }))}>
                <option value="">Seleccionar préstamo…</option>
                {loans.map(l => <option key={l.id} value={l.id}>#{l.id} — {getUserName(l.user_id)} ({l.status})</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Monto *</label>
              <input required type="number" step="0.01" min="0" value={form.amount} onChange={e => setForm(f => ({ ...f, amount: e.target.value }))} placeholder="0.00" />
            </div>
            <div className="form-group">
              <label className="form-label">Razón *</label>
              <textarea required rows={2} value={form.reason} onChange={e => setForm(f => ({ ...f, reason: e.target.value }))} style={{ resize: 'vertical' }} />
            </div>
            <div className="form-actions">
              <button type="button" className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancelar</button>
              <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Creando…' : 'Crear multa'}</button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};

export default FinesPage;
