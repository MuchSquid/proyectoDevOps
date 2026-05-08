import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import BooksPage from './pages/BooksPage';
import UsersPage from './pages/UsersPage';
import LoansPage from './pages/LoansPage';
import ReservationsPage from './pages/ReservationsPage';
import FinesPage from './pages/FinesPage';
import NotificationsPage from './pages/NotificationsPage';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <div className="layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/"              element={<BooksPage />} />
            <Route path="/users"         element={<UsersPage />} />
            <Route path="/loans"         element={<LoansPage />} />
            <Route path="/reservations"  element={<ReservationsPage />} />
            <Route path="/fines"         element={<FinesPage />} />
            <Route path="/notifications" element={<NotificationsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
