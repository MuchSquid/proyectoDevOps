import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../App.jsx';
import React from 'react';

describe('Biblioteca Digital Dashboard', () => {
  it('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Biblioteca Digital/i)).toBeInTheDocument();
  });

  it('renders mock books from synthetic data', () => {
    render(<App />);
    // "The Art of Automation" is the first book in mockData.js
    expect(screen.getByText(/The Art of Automation/i)).toBeInTheDocument();
    expect(screen.getByText(/Alex Rivera/i)).toBeInTheDocument();
  });

  it('filters books by search term', () => {
    render(<App />);
    const searchInput = screen.getByPlaceholderText(/Buscar libros o autores/i);
    
    fireEvent.change(searchInput, { target: { value: 'FastAPI' } });
    
    expect(screen.getByText(/FastAPI Mastery/i)).toBeInTheDocument();
    // "The Art of Automation" should be filtered out
    expect(screen.queryByText(/The Art of Automation/i)).not.toBeInTheDocument();
  });

  it('shows "no results" message when search fails', () => {
    render(<App />);
    const searchInput = screen.getByPlaceholderText(/Buscar libros o autores/i);
    
    fireEvent.change(searchInput, { target: { value: 'NonExistentBook123' } });
    
    expect(screen.getByText(/No se encontraron libros/i)).toBeInTheDocument();
  });
});
