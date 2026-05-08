import React, { useState, useEffect } from 'react';
import { getNotifications, createNotification, markAsRead } from '../api/api-notifications';
import { getUsers } from '../api/api-users';
import { 
  HiOutlineBell, 
  HiOutlinePlus, 
  HiOutlineExclamationTriangle, 
  HiOutlineInformationCircle, 
  HiOutlineCheckCircle, 
  HiOutlineXCircle, 
  HiOutlineCheck, 
  HiOutlineXMark 
} from 'react-icons/hi2';

const emptyForm = { user_id: '', title: '', message: '', type: 'info' };
const TYPES = ['info', 'warning', 'success', 'error'];

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

const TypeIcon = ({ type }) => {
  const icons = {
    info: <HiOutlineInformationCircle style={{ color: 'var(--primary)' }} />,
    warning: <HiOutlineExclamationTriangle style={{ color: 'var(--warning)' }} />,
    success: <HiOutlineCheckCircle style={{ color: 'var(--success)' }} />,
    error: <HiOutlineXCircle style={{ color: 'var(--danger)' }} />,
    default: <HiOutlineBell />
  };
  return icons[type] || icons.default;
};

const typeBadge = type => {
  const map = { info: 'active', warning: 'pending', success: 'paid', error: 'overdue' };
  return (
    <span className={`badge badge-${map[type] || 'active'}`} style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
      <TypeIcon type={type} /> {type}
    </span>
  );
};

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [filterRead, setFilterRead] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  const load = async () => {
    setLoading(true); setError(null);
    try {
      const [n, u] = await Promise.all([
        getNotifications({ limit: 100 }),
        getUsers({ limit: 100 }),
      ]);
      setNotifications(n); setUsers(u);
    } catch { setError('No se pudo conectar al backend'); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const getUserName = id => { const u = users.find(u => u.id === id); return u ? `${u.first_name} ${u.last_name}` : `User #${id}`; };

  const unread = notifications.filter(n => !n.is_read).length;

  const filtered = notifications.filter(n => {
    const q = search.toLowerCase();
    const matchQ = n.title?.toLowerCase().includes(q) || n.message?.toLowerCase().includes(q) || getUserName(n.user_id).toLowerCase().includes(q);
    const matchR = filterRead === 'all' || (filterRead === 'unread' && !n.is_read) || (filterRead === 'read' && n.is_read);
    return matchQ && matchR;
  });

  const handleCreate = async e => {
    e.preventDefault(); setSaving(true);
    try {
      await createNotification({ ...form, user_id: +form.user_id });
      setShowModal(false); await load();
    } catch (err) { alert(err.response?.data?.detail || 'Error al crear notificación'); }
    finally { setSaving(false); }
  };

  const handleMarkRead = async id => {
    try { await markAsRead(id); await load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error'); }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <div className="page-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <HiOutlineBell /> Notificaciones
          </div>
          <div className="page-subtitle">
            {notifications.length} total
            {unread > 0 && <span style={{ marginLeft: '0.5rem', color: 'var(--warning)' }}>· {unread} sin leer</span>}
          </div>
        </div>
        <button className="btn btn-primary" onClick={() => { setForm(emptyForm); setShowModal(true); }}>
          <HiOutlinePlus style={{ marginRight: '0.4rem' }} /> Nueva notificación
        </button>
      </div>

      <div className="toolbar">
        <input placeholder="Buscar…" value={search} onChange={e => setSearch(e.target.value)} />
        <select value={filterRead} onChange={e => setFilterRead(e.target.value)} style={{ width: 'auto' }}>
          <option value="all">Todas</option>
          <option value="unread">Sin leer</option>
          <option value="read">Leídas</option>
        </select>
      </div>

      {loading && <div className="loading-wrapper"><div className="spinner" /><span>Cargando notificaciones…</span></div>}
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
                <th>Título</th>
                <th>Mensaje</th>
                <th>Tipo</th>
                <th>Leída</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr><td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>Sin resultados</td></tr>
              )}
              {filtered.map(n => (
                <tr key={n.id} style={{ opacity: n.is_read ? 0.65 : 1 }}>
                  <td style={{ color: 'var(--text-muted)' }}>#{n.id}</td>
                  <td>{getUserName(n.user_id)}</td>
                  <td><strong>{n.title}</strong></td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', maxWidth: '250px' }}>{n.message}</td>
                  <td>{typeBadge(n.type)}</td>
                  <td>
                    {n.is_read
                      ? <span className="badge badge-available" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}><HiOutlineCheck /> Leída</span>
                      : <span className="badge badge-pending">Pendiente</span>}
                  </td>
                  <td>
                    {!n.is_read && (
                      <button className="btn btn-ghost btn-sm" onClick={() => handleMarkRead(n.id)}>Marcar leída</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <Modal title="Nueva notificación" onClose={() => setShowModal(false)}>
          <form className="form-grid" onSubmit={handleCreate}>
            <div className="form-group">
              <label className="form-label">Usuario *</label>
              <select required value={form.user_id} onChange={e => setForm(f => ({ ...f, user_id: e.target.value }))}>
                <option value="">Seleccionar usuario…</option>
                {users.map(u => <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Título *</label>
              <input required value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Tipo</label>
              <select value={form.type} onChange={e => setForm(f => ({ ...f, type: e.target.value }))}>
                {TYPES.map(t => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Mensaje *</label>
              <textarea required rows={3} value={form.message} onChange={e => setForm(f => ({ ...f, message: e.target.value }))} style={{ resize: 'vertical' }} />
            </div>
            <div className="form-actions">
              <button type="button" className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancelar</button>
              <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Enviando…' : 'Enviar'}</button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};

export default NotificationsPage;
