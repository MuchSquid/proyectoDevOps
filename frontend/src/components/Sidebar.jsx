import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  HiOutlineBookOpen,
  HiOutlineUsers,
  HiOutlineClipboardDocumentList,
  HiOutlineBookmark,
  HiOutlineCurrencyDollar,
  HiOutlineBell,
  HiOutlineBuildingLibrary
} from 'react-icons/hi2';
import './components.css';

const navItems = [
  { to: '/',              icon: <HiOutlineBookOpen />, label: 'Libros' },
  { to: '/users',         icon: <HiOutlineUsers />, label: 'Usuarios' },
  { to: '/loans',         icon: <HiOutlineClipboardDocumentList />, label: 'Préstamos' },
  { to: '/reservations',  icon: <HiOutlineBookmark />, label: 'Reservas' },
  { to: '/fines',         icon: <HiOutlineCurrencyDollar />, label: 'Multas' },
  { to: '/notifications', icon: <HiOutlineBell />, label: 'Notificaciones' },
];

const Sidebar = () => (
  <aside className="sidebar">
    <div className="sidebar-brand">
      <div className="sidebar-logo">
        <HiOutlineBuildingLibrary size={24} />
      </div>
      <div>
        <div className="sidebar-brand-name">Uteblo</div>
        <div className="sidebar-brand-sub">Sistema de Reservas</div>
      </div>
    </div>

    <nav className="sidebar-nav">
      <div className="sidebar-section-label">Módulos</div>
      {navItems.map(({ to, icon, label }) => (
        <NavLink
          key={to}
          to={to}
          end={to === '/'}
          className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
        >
          <span className="sidebar-link-icon">{icon}</span>
          {label}
        </NavLink>
      ))}
    </nav>

    <div className="sidebar-footer">
      API: <strong>localhost:8000</strong>
    </div>
  </aside>
);

export default Sidebar;
