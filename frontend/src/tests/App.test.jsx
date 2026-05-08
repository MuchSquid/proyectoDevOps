import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Sidebar from '../components/Sidebar.jsx';
import React from 'react';

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, NavLink: ({ children, className }) => <a className={typeof className === 'function' ? className({ isActive: false }) : className}>{children}</a> };
});

describe('Uteblo Sidebar', () => {
  it('muestra el nombre Uteblo', () => {
    render(
      <MemoryRouter>
        <Sidebar />
      </MemoryRouter>
    );
    expect(screen.getByText('Uteblo')).toBeInTheDocument();
  });

  it('muestra el subtítulo Sistema de Reservas', () => {
    render(
      <MemoryRouter>
        <Sidebar />
      </MemoryRouter>
    );
    expect(screen.getByText('Sistema de Reservas')).toBeInTheDocument();
  });

  it('muestra todos los módulos de navegación', () => {
    render(
      <MemoryRouter>
        <Sidebar />
      </MemoryRouter>
    );
    expect(screen.getByText('Libros')).toBeInTheDocument();
    expect(screen.getByText('Usuarios')).toBeInTheDocument();
    expect(screen.getByText('Préstamos')).toBeInTheDocument();
    expect(screen.getByText('Reservas')).toBeInTheDocument();
    expect(screen.getByText('Multas')).toBeInTheDocument();
    expect(screen.getByText('Notificaciones')).toBeInTheDocument();
  });
});
