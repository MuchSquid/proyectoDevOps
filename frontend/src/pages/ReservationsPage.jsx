import React, { useState, useEffect } from 'react';
import { getReservations, createReservation, cancelReservation, completeReservation } from '../api/api-reservations';
import { getUsers } from '../api/api-users';
import { getBooks } from '../api/api-books';
import { 
  HiOutlineBookmark, 
  HiOutlinePlus, 
  HiOutlineExclamationTriangle, 
  HiOutlineCheck, 
  HiOutlineXMark 
} from 'react-icons/hi2';

const emptyForm = { user_id: '', book_id: '', reservation_date: '', expiry_date: '' };

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
  const cls = s === 'expired' ? 'overdue' : s;
  return <span className={`badge badge-${cls}`}>{s}</span>;
};

const ReservationsPage = () => {
  const [reservations, setReservations] = useState([]);
  const [users, setUsers] = useState([]);
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  const load = async () => {
    setLoading(true); setError(null);
    try {
      const [r, u, b] = await Promise.all([
        getReservations({ limit: 100 }),
        getUsers({ limit: 100 }),
        getBooks({ limit: 100 }),
      ]);
      setReservations(r); setUsers(u); setBooks(b);
    } catch { setError('No se pudo conectar al backend'); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const getUserName = id => { const u = users.find(u => u.id === id); return u ? `${u.first_name} ${u.last_name}` : `User #${id}`; };
  const getBookTitle = id => books.find(b => b.id === id)?.title || `Book #${id}`;

  const filtered = reservations.filter(r => {
    const q = search.toLowerCase();
    return getUserName(r.user_id).toLowerCase().includes(q) || getBookTitle(r.book_id).toLowerCase().includes(q);
  });

  const handleCreate = async e => {
    e.preventDefault(); setSaving(true);
    try {
      const payload = { user_id: +form.user_id, book_id: +form.book_id };
      if (form.expiry_date) payload.expiration_date = new Date(form.expiry_date).toISOString();
      await createReservation(payload);
      setShowModal(false); await load();
    } catch (err) { alert(err.response?.data?.detail || 'Error al crear reserva'); }
    finally { setSaving(false); }
  };

  const handleCancel = async id => {
    if (!confirm('¿Cancelar reserva?')) return;
    try { await cancelReservation(id); await load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error'); }
  };

  const handleComplete = async id => {
    try { await completeReservation(id); await load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error'); }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <div className="page-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <HiOutlineBookmark /> Reservas
          </div>
          <div className="page-subtitle">{reservations.length} reservas registradas</div>
        </div>
        <button className="btn btn-primary" onClick={() => { setForm(emptyForm); setShowModal(true); }}>
          <HiOutlinePlus style={{ marginRight: '0.4rem' }} /> Nueva reserva
        </button>
      </div>

      <div className="toolbar">
        <input placeholder="Buscar por usuario o libro…" value={search} onChange={e => setSearch(e.target.value)} />
      </div>

      {loading && <div className="loading-wrapper"><div className="spinner" /><span>Cargando reservas…</span></div>}
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
                <th>Libro</th>
                <th>Fecha reserva</th>
                <th>Vencimiento</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr><td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>Sin resultados</td></tr>
              )}
              {filtered.map(r => (
                <tr key={r.id}>
                  <td style={{ color: 'var(--text-muted)' }}>#{r.id}</td>
                  <td>{getUserName(r.user_id)}</td>
                  <td>{getBookTitle(r.book_id)}</td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.82rem' }}>{r.reservation_date ? new Date(r.reservation_date).toLocaleDateString() : '—'}</td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.82rem' }}>{r.expiration_date ? new Date(r.expiration_date).toLocaleDateString() : '—'}</td>
                  <td>{statusBadge(r.status)}</td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.4rem' }}>
                      {r.status === 'ACTIVE' && (
                        <>
                          <button className="btn btn-success btn-sm" onClick={() => handleComplete(r.id)}>
                            <HiOutlineCheck style={{ marginRight: '0.3rem' }} /> Completar
                          </button>
                          <button className="btn btn-danger btn-sm" onClick={() => handleCancel(r.id)}>
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
        <Modal title="Nueva reserva" onClose={() => setShowModal(false)}>
          <form className="form-grid" onSubmit={handleCreate}>
            <div className="form-group">
              <label className="form-label">Usuario *</label>
              <select required value={form.user_id} onChange={e => setForm(f => ({ ...f, user_id: e.target.value }))}>
                <option value="">Seleccionar usuario…</option>
                {users.map(u => <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Libro *</label>
              <select required value={form.book_id} onChange={e => setForm(f => ({ ...f, book_id: e.target.value }))}>
                <option value="">Seleccionar libro…</option>
                {books.map(b => <option key={b.id} value={b.id}>{b.title} ({b.available_copies} disp.)</option>)}
              </select>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Fecha reserva</label>
                <input type="date" value={form.reservation_date} onChange={e => setForm(f => ({ ...f, reservation_date: e.target.value }))} />
              </div>
              <div className="form-group">
                <label className="form-label">Vencimiento</label>
                <input type="date" value={form.expiry_date} onChange={e => setForm(f => ({ ...f, expiry_date: e.target.value }))} />
              </div>
            </div>
            <div className="form-actions">
              <button type="button" className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancelar</button>
              <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Creando…' : 'Crear reserva'}</button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};

export default ReservationsPage;
