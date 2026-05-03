import React from 'react';

const BookCard = ({ book }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'available': return 'var(--status-available)';
      case 'reserved': return 'var(--status-reserved)';
      case 'maintenance': return 'var(--status-maintenance)';
      default: return 'var(--text-muted)';
    }
  };

  return (
    <div className="glass book-card">
      <div className="book-cover-container">
        <img src={book.cover} alt={book.title} className="book-cover" />
        <div className="availability-badge" style={{ backgroundColor: getStatusColor(book.availability) }}>
          {book.availability}
        </div>
      </div>
      <div className="book-info">
        <h3>{book.title}</h3>
        <p className="author">by {book.author}</p>
        <div className="metadata">
          <span>{book.genre}</span>
          <span>•</span>
          <span>{book.year}</span>
        </div>
        <p className="description">{book.description}</p>
        <button className="reserve-btn">
          {book.availability === 'available' ? 'Reserve Now' : 'View Details'}
        </button>
      </div>
    </div>
  );
};

export default BookCard;
