import React, { useState, useEffect } from 'react';
import {
  HiOutlineUsers,
  HiOutlineExclamationTriangle,
  HiOutlinePencilSquare,
  HiOutlineTrash,
  HiOutlineUserPlus,
  HiOutlineXMark
} from 'react-icons/hi2';
import { getUsers, createUser, updateUser, deleteUser } from '../api/api-users';

const emptyForm = { first_name: '', last_name: '', email: '', role: 'STUDENT', university_code: '', phone: '', password: '' };
const ROLES = ['STUDENT', 'LIBRARIAN', 'ADMIN'];

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

const UsersPage = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editUser, setEditUser] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  const load = async () => {
    setLoading(true); setError(null);
    try { setUsers(await getUsers({ limit: 100 })); }
    catch { setError('No se pudo conectar al backend'); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const filtered = users.filter(u => {
    const q = search.toLowerCase();
    return u.first_name?.toLowerCase().includes(q) || u.last_name?.toLowerCase().includes(q) || u.email?.toLowerCase().includes(q);
  });

  const openCreate = () => { setEditUser(null); setForm(emptyForm); setShowModal(true); };
  const openEdit = u => { 
    setEditUser(u); 
    setForm({ 
      first_name: u.first_name, 
      last_name: u.last_name, 
      email: u.email, 
      role: u.role, 
      university_code: u.university_code, 
      phone: u.phone || '', 
      password: '' 
    }); 
    setShowModal(true); 
  };

  const handleSave = async e => {
    e.preventDefault(); setSaving(true);
    try {
      const payload = { ...form };
      if (editUser && !payload.password) delete payload.password; // No enviar password vacío en update
      
      if (editUser) await updateUser(editUser.id, payload);
      else await createUser(payload);
      
      setShowModal(false); await load();
    } catch (err) { alert(err.response?.data?.detail || 'Error al guardar'); }
    finally { setSaving(false); }
  };

  const handleDelete = async id => {
    if (!confirm('¿Eliminar este usuario?')) return;
    try { await deleteUser(id); await load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error al eliminar'); }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <div className="page-title">
            <HiOutlineUsers style={{ marginRight: '0.75rem' }} /> Usuarios
          </div>
          <div className="page-subtitle">{users.length} usuarios registrados</div>
        </div>
        <button className="btn btn-primary" onClick={openCreate}>
          <HiOutlineUserPlus style={{ marginRight: '0.5rem' }} /> Nuevo usuario
        </button>
      </div>

      <div className="toolbar">
        <input placeholder="Buscar por nombre, apellido o email…" value={search} onChange={e => setSearch(e.target.value)} />
      </div>

      {loading && <div className="loading-wrapper"><div className="spinner" /><span>Cargando usuarios…</span></div>}
      {error && (
        <div className="empty-state">
          <HiOutlineExclamationTriangle size={48} color="var(--error)" />
          <h3>Error</h3>
          <p>{error}</p>
          <button className="btn btn-ghost" onClick={load}>Reintentar</button>
        </div>
      )}

      {!loading && !error && (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Código</th>
                <th>Nombre completo</th>
                <th>Email</th>
                <th>Rol</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr><td colSpan={6} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>Sin resultados</td></tr>
              )}
              {filtered.map(u => (
                <tr key={u.id}>
                  <td style={{ color: 'var(--text-muted)' }}>{u.university_code}</td>
                  <td><strong>{u.first_name} {u.last_name}</strong></td>
                  <td style={{ color: 'var(--text-secondary)' }}>{u.email}</td>
                  <td>
                    <span className={`badge badge-${u.role === 'ADMIN' ? 'active' : u.role === 'LIBRARIAN' ? 'completed' : 'available'}`}>
                      {u.role}
                    </span>
                  </td>
                  <td>
                    <span className={`badge badge-${u.is_active ? 'available' : 'overdue'}`}>
                      {u.is_active ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.4rem' }}>
                      <button className="btn btn-ghost btn-sm" onClick={() => openEdit(u)}>
                        <HiOutlinePencilSquare />
                      </button>
                      <button className="btn btn-danger btn-sm" onClick={() => handleDelete(u.id)}>
                        <HiOutlineTrash />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <Modal title={editUser ? 'Editar usuario' : 'Nuevo usuario'} onClose={() => setShowModal(false)}>
          <form className="form-grid" onSubmit={handleSave}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Nombre *</label>
                <input required value={form.first_name} onChange={e => setForm(f => ({ ...f, first_name: e.target.value }))} />
              </div>
              <div className="form-group">
                <label className="form-label">Apellido *</label>
                <input required value={form.last_name} onChange={e => setForm(f => ({ ...f, last_name: e.target.value }))} />
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Email *</label>
              <input required type="email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Código Universitario *</label>
              <input required value={form.university_code} onChange={e => setForm(f => ({ ...f, university_code: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Rol</label>
              <select value={form.role} onChange={e => setForm(f => ({ ...f, role: e.target.value }))}>
                {ROLES.map(r => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Contraseña {editUser ? '(opcional)' : '*'}</label>
              <input required={!editUser} type="password" value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} />
            </div>
            <div className="form-actions">
              <button type="button" className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancelar</button>
              <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Guardando…' : 'Guardar'}</button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};

export default UsersPage;
