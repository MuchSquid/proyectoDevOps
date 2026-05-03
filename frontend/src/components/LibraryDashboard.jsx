import React, { useState } from 'react';
import { MOCK_BOOKS } from '../data/mockData';
import BookCard from './BookCard';
import './components.css';

const LibraryDashboard = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');

  const filteredBooks = MOCK_BOOKS.filter(book => {
    const matchesSearch = book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         book.author.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || book.availability === filter;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="title-section">
          <h1>Biblioteca Digital</h1>
          <p className="subtitle">Explora nuestra colección y reserva tu próxima lectura</p>
        </div>
        
        <div className="controls-section glass">
          <input 
            type="text" 
            placeholder="Buscar libros o autores..." 
            className="search-input"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <select 
            className="filter-select"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="all">Todos</option>
            <option value="available">Disponibles</option>
            <option value="reserved">Reservados</option>
            <option value="maintenance">Mantenimiento</option>
          </select>
        </div>
      </header>

      <main className="books-grid">
        {filteredBooks.length > 0 ? (
          filteredBooks.map(book => (
            <BookCard key={book.id} book={book} />
          ))
        ) : (
          <div className="no-results glass">
            <p>No se encontraron libros que coincidan con tu búsqueda.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default LibraryDashboard;
