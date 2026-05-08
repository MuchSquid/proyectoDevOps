import React, { useState, useEffect } from 'react';
import { getLoans, createLoan, returnLoan, cancelLoan } from '../api/api-loans';
import { getUsers } from '../api/api-users';
import { getBooks } from '../api/api-books';
import { 
  HiOutlineClipboardDocumentList, 
  HiOutlinePlus, 
  HiOutlineExclamationTriangle, 
  HiOutlineArrowUturnLeft, 
  HiOutlineXMark 
} from 'react-icons/hi2';

const emptyForm = { user_id: '', book_id: '', due_date: '' };

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

const LoansPage = () => {
  const [loans, setLoans] = useState([]);
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
      const [l, u, b] = await Promise.all([
        getLoans({ limit: 100 }),
        getUsers({ limit: 100 }),
        getBooks({ limit: 100 }),
      ]);
      setLoans(l); setUsers(u); setBooks(b);
    } catch { setError('No se pudo conectar al backend'); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const getUserName = id => { const u = users.find(u => u.id === id); return u ? `${u.first_name} ${u.last_name}` : `User #${id}`; };
  const getBookTitle = id => books.find(b => b.id === id)?.title || `Book #${id}`;

  const filtered = loans.filter(l => {
    const q = search.toLowerCase();
    return getUserName(l.user_id).toLowerCase().includes(q) || getBookTitle(l.book_id).toLowerCase().includes(q);
  });

  const handleCreate = async e => {
    e.preventDefault(); setSaving(true);
    try {
      await createLoan({ user_id: +form.user_id, book_id: +form.book_id, due_date: form.due_date || undefined });
      setShowModal(false); await load();
    } catch (err) { alert(err.response?.data?.detail || 'Error al crear préstamo'); }
    finally { setSaving(false); }
  };

  const handleReturn = async id => {
    try { await returnLoan(id); await load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error'); }
  };

  const handleCancel = async id => {
    if (!confirm('¿Cancelar préstamo?')) return;
    try { await cancelLoan(id); await load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error'); }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <div className="page-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <HiOutlineClipboardDocumentList /> Préstamos
          </div>
          <div className="page-subtitle">{loans.length} préstamos registrados</div>
        </div>
        <button className="btn btn-primary" onClick={() => { setForm(emptyForm); setShowModal(true); }}>
          <HiOutlinePlus style={{ marginRight: '0.4rem' }} /> Nuevo préstamo
        </button>
      </div>

      <div className="toolbar">
        <input placeholder="Buscar por usuario o libro…" value={search} onChange={e => setSearch(e.target.value)} />
      </div>

      {loading && <div className="loading-wrapper"><div className="spinner" /><span>Cargando préstamos…</span></div>}
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
                <th>Fecha préstamo</th>
                <th>Fecha vencimiento</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr><td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>Sin resultados</td></tr>
              )}
              {filtered.map(l => (
                <tr key={l.id}>
                  <td style={{ color: 'var(--text-muted)' }}>#{l.id}</td>
                  <td>{getUserName(l.user_id)}</td>
                  <td>{getBookTitle(l.book_id)}</td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.82rem' }}>{l.loan_date ? new Date(l.loan_date).toLocaleDateString() : '—'}</td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.82rem' }}>{l.due_date ? new Date(l.due_date).toLocaleDateString() : '—'}</td>
                  <td>{statusBadge(l.status)}</td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.4rem' }}>
                      {l.status === 'ACTIVE' && (
                        <>
                          <button className="btn btn-success btn-sm" onClick={() => handleReturn(l.id)}>
                            <HiOutlineArrowUturnLeft style={{ marginRight: '0.3rem' }} /> Devolver
                          </button>
                          <button className="btn btn-danger btn-sm" onClick={() => handleCancel(l.id)}>
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
        <Modal title="Nuevo préstamo" onClose={() => setShowModal(false)}>
          <form className="form-grid" onSubmit={handleCreate}>
            <div className="form-group">
              <label className="form-label">Usuario *</label>
              <select required value={form.user_id} onChange={e => setForm(f => ({ ...f, user_id: e.target.value }))}>
                <option value="">Seleccionar usuario…</option>
                {users.map(u => <option key={u.id} value={u.id}>{u.first_name} {u.last_name} ({u.email})</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Libro *</label>
              <select required value={form.book_id} onChange={e => setForm(f => ({ ...f, book_id: e.target.value }))}>
                <option value="">Seleccionar libro…</option>
                {books.filter(b => b.available_copies > 0).map(b => <option key={b.id} value={b.id}>{b.title} ({b.available_copies} disp.)</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Fecha de vencimiento</label>
              <input type="date" value={form.due_date} onChange={e => setForm(f => ({ ...f, due_date: e.target.value }))} />
            </div>
            <div className="form-actions">
              <button type="button" className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancelar</button>
              <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Creando…' : 'Crear préstamo'}</button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};

export default LoansPage;
