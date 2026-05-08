import React, { useState, useEffect } from 'react';
import {
  HiOutlineBookOpen,
  HiOutlineExclamationTriangle,
  HiOutlinePencilSquare,
  HiOutlineTrash,
  HiOutlinePlus,
  HiOutlineXMark
} from 'react-icons/hi2';
import { getBooks, createBook, updateBook, deleteBook } from '../api/api-books';

const emptyForm = { 
  title: '', 
  description: '', 
  publication_year: new Date().getFullYear(), 
  language: 'Español',
  pages: 0,
  publisher: '',
  cover_image: '', 
  available_copies: 1 
};

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

const BooksPage = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editBook, setEditBook] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  const load = async () => {
    setLoading(true); setError(null);
    try { setBooks(await getBooks({ limit: 100 })); }
    catch { setError('No se pudo conectar al backend'); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const filtered = books.filter(b => {
    const q = search.toLowerCase();
    return b.title?.toLowerCase().includes(q) || b.publisher?.toLowerCase().includes(q);
  });

  const openCreate = () => { setEditBook(null); setForm(emptyForm); setShowModal(true); };
  const openEdit = (b) => { 
    setEditBook(b); 
    setForm({ 
      title: b.title, 
      description: b.description || '', 
      publication_year: b.publication_year || '', 
      language: b.language || '',
      pages: b.pages || 0,
      publisher: b.publisher || '',
      cover_image: b.cover_image || '', 
      available_copies: b.available_copies || 0 
    }); 
    setShowModal(true); 
  };

  const handleSave = async e => {
    e.preventDefault(); setSaving(true);
    try {
      if (editBook) await updateBook(editBook.id, form);
      else await createBook(form);
      setShowModal(false); await load();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al guardar');
    } finally { setSaving(false); }
  };

  const handleDelete = async (id) => {
    if (!confirm('¿Eliminar este libro?')) return;
    try { await deleteBook(id); await load(); }
    catch (err) { alert(err.response?.data?.detail || 'Error al eliminar'); }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <div className="page-title">
            <HiOutlineBookOpen style={{ marginRight: '0.75rem' }} /> Libros
          </div>
          <div className="page-subtitle">{books.length} libros en el catálogo</div>
        </div>
        <button className="btn btn-primary" onClick={openCreate}>
          <HiOutlinePlus style={{ marginRight: '0.5rem' }} /> Agregar libro
        </button>
      </div>

      <div className="toolbar">
        <input placeholder="Buscar por título o editorial…" value={search} onChange={e => setSearch(e.target.value)} />
      </div>

      {loading && <div className="loading-wrapper"><div className="spinner" /><span>Cargando libros…</span></div>}
      {error && (
        <div className="empty-state">
          <HiOutlineExclamationTriangle size={48} color="var(--error)" />
          <h3>Error</h3>
          <p>{error}</p>
          <button className="btn btn-ghost" onClick={load}>Reintentar</button>
        </div>
      )}

      {!loading && !error && (
        <div className="books-grid">
          {filtered.map(book => (
            <div key={book.id} className="book-card">
              <div className="book-cover-container">
                {book.cover_image
                  ? <img src={book.cover_image} alt={book.title} className="book-cover" />
                  : <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--bg-card)' }}>
                      <HiOutlineBookOpen size={48} opacity={0.3} />
                    </div>
                }
                <div className="book-availability-badge">
                  <span className={`badge badge-${book.available_copies > 0 ? 'available' : 'overdue'}`}>
                    {book.available_copies > 0 ? `${book.available_copies} disponibles` : 'Agotado'}
                  </span>
                </div>
              </div>
              <div className="book-info">
                <div className="book-title">{book.title}</div>
                <div className="book-author">{book.publisher || 'Editorial desconocida'}</div>
                <div className="book-meta">
                  {book.language && <span>{book.language}</span>}
                  <span>•</span>
                  {book.publication_year && <span>{book.publication_year}</span>}
                </div>
                {book.description && <div className="book-desc">{book.description}</div>}
                <div className="book-actions">
                  <button className="btn btn-ghost btn-sm" onClick={() => openEdit(book)}>
                    <HiOutlinePencilSquare style={{ marginRight: '0.4rem' }} /> Editar
                  </button>
                  <button className="btn btn-danger btn-sm" onClick={() => handleDelete(book.id)}>
                    <HiOutlineTrash />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <Modal title={editBook ? 'Editar libro' : 'Nuevo libro'} onClose={() => setShowModal(false)}>
          <form className="form-grid" onSubmit={handleSave}>
            <div className="form-group">
              <label className="form-label">Título *</label>
              <input required value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Editorial</label>
                <input value={form.publisher} onChange={e => setForm(f => ({ ...f, publisher: e.target.value }))} />
              </div>
              <div className="form-group">
                <label className="form-label">Año</label>
                <input type="number" value={form.publication_year} onChange={e => setForm(f => ({ ...f, publication_year: +e.target.value }))} />
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Idioma</label>
                <input value={form.language} onChange={e => setForm(f => ({ ...f, language: e.target.value }))} />
              </div>
              <div className="form-group">
                <label className="form-label">Páginas</label>
                <input type="number" value={form.pages} onChange={e => setForm(f => ({ ...f, pages: +e.target.value }))} />
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Copias disponibles</label>
              <input type="number" value={form.available_copies} onChange={e => setForm(f => ({ ...f, available_copies: +e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">URL de portada</label>
              <input value={form.cover_image} onChange={e => setForm(f => ({ ...f, cover_image: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Descripción</label>
              <textarea rows={3} value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} />
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

export default BooksPage;
