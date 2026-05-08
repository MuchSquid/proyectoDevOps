# Uteblo UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reemplazar completamente el tema oscuro/violeta con una estética de biblioteca moderna — fondo crema, glassmorphism Apple cálido, Plus Jakarta Sans, nombre "Uteblo".

**Architecture:** Solo reescritura de CSS (`index.css` y `components.css`) + cambios mínimos en JSX (nombre en Sidebar, reemplazar `✕` por `<HiOutlineXMark />` en BooksPage y UsersPage). Cero cambios a lógica de negocio ni APIs.

**Tech Stack:** React 19, Vite, react-icons v5 (hi2), Plus Jakarta Sans (Google Fonts), CSS nativo con custom properties.

---

## Archivos involucrados

| Archivo | Acción |
|---------|--------|
| `frontend/src/index.css` | Reescritura completa |
| `frontend/src/components/components.css` | Reescritura completa |
| `frontend/src/components/Sidebar.jsx` | Cambiar nombre brand a "Uteblo" |
| `frontend/src/pages/BooksPage.jsx` | Añadir `HiOutlineXMark` + reemplazar `✕` |
| `frontend/src/pages/UsersPage.jsx` | Añadir `HiOutlineXMark` + reemplazar `✕` |
| `frontend/src/tests/App.test.jsx` | Actualizar texto "Biblioteca Digital" → "Uteblo" |

---

## Task 1: Reescribir `index.css`

**Files:**
- Modify: `frontend/src/index.css`

- [ ] **Step 1: Reemplazar el contenido completo de `index.css`**

```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

:root {
  /* Fondos */
  --bg-main:    #ede3d0;
  --bg-surface: #e3d4b8;
  --bg-deep:    #d8c8a2;

  /* Glass */
  --glass-light:  rgba(255, 249, 238, 0.60);
  --glass-strong: rgba(255, 250, 240, 0.80);
  --glass-dark:   rgba(28, 13, 4,   0.84);
  --glass-modal:  rgba(255, 249, 235, 0.88);

  /* Bordes */
  --glass-border:      rgba(205, 162, 88, 0.38);
  --glass-border-dark: rgba(200, 158, 78, 0.20);
  --glass-border-hover: rgba(205, 162, 88, 0.60);

  /* Sombras */
  --shadow-warm: 0 10px 44px rgba(70,35,8,0.13), 0 2px 0 rgba(255,255,255,0.88) inset;
  --shadow-dark: 0 10px 44px rgba(0,0,0,0.28),   0 1.5px 0 rgba(255,255,255,0.07) inset;

  /* Texto */
  --text-primary:   #221004;
  --text-secondary: #6b3f20;
  --text-muted:     #a87048;

  /* Acento */
  --accent-primary:  #8b4513;
  --accent-amber:    #c08840;
  --accent-glow:     rgba(139, 69, 19, 0.25);
  --accent-light:    rgba(139, 69, 19, 0.12);

  /* Semánticos */
  --success: #187038;
  --warning: #c08840;
  --danger:  #9a1c1c;
  --info:    #1a4a8a;

  /* Status */
  --status-available:   #187038;
  --status-reserved:    #8a3e08;
  --status-overdue:     #9a1c1c;
  --status-active:      #1a4a8a;
  --status-returned:    #187038;
  --status-cancelled:   #6b5040;
  --status-completed:   #5a3090;
  --status-pending:     #8a3e08;
  --status-paid:        #187038;
  --status-maintenance: #9a1c1c;

  --sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  font-family: var(--sans);
  font-size: 16px;
  line-height: 1.5;
  font-weight: 400;
  color: var(--text-primary);
  background-color: var(--bg-main);
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(ellipse 75% 55% at 12%  8%,  rgba(200,150,60,0.22) 0%, transparent 58%),
    radial-gradient(ellipse 55% 50% at 88% 88%,  rgba(140,75,25,0.17)  0%, transparent 58%),
    radial-gradient(ellipse 45% 38% at 55% 38%,  rgba(230,195,125,0.11) 0%, transparent 48%),
    linear-gradient(148deg, #ede3d0 0%, #e3d4b8 55%, #d8c8a2 100%);
  overflow-x: hidden;
}

#root { width: 100%; min-height: 100vh; display: flex; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(170,115,55,0.28); border-radius: 3px; }

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-12px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}

/* Glass utilities */
.glass {
  background: var(--glass-light);
  backdrop-filter: blur(52px) saturate(180%) brightness(105%);
  -webkit-backdrop-filter: blur(52px) saturate(180%) brightness(105%);
  border: 1px solid var(--glass-border);
  border-radius: 18px;
  box-shadow: var(--shadow-warm);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.glass:hover {
  border-color: var(--glass-border-hover);
}
.glass-strong {
  background: var(--glass-strong);
  backdrop-filter: blur(64px) saturate(200%) brightness(107%);
  -webkit-backdrop-filter: blur(64px) saturate(200%) brightness(107%);
  border: 1px solid rgba(215, 175, 108, 0.52);
  border-radius: 18px;
  box-shadow: var(--shadow-warm);
}
.glass-dark {
  background: var(--glass-dark);
  backdrop-filter: blur(56px) saturate(155%);
  -webkit-backdrop-filter: blur(56px) saturate(155%);
  border: 1px solid var(--glass-border-dark);
  border-radius: 18px;
  box-shadow: var(--shadow-dark);
}

/* Typography */
h1, h2, h3, h4 { margin: 0; font-weight: 700; letter-spacing: -0.025em; }
h1 { font-size: 2.25rem; }
h2 { font-size: 1.5rem; }
h3 { font-size: 1.125rem; }
p  { margin: 0; }

/* Buttons */
button { cursor: pointer; border: none; outline: none; font-family: inherit; }

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.55rem 1.1rem;
  border-radius: 11px;
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  transition: all 0.2s ease;
}
.btn-primary {
  background: linear-gradient(145deg, #a05018, #7a3410);
  color: rgba(255, 238, 210, 0.95);
  box-shadow: 0 5px 18px rgba(100,38,8,0.30), 0 1px 0 rgba(255,255,255,0.14) inset;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(100,38,8,0.38);
}
.btn-ghost {
  background: rgba(205, 162, 88, 0.12);
  color: var(--text-secondary);
  border: 1px solid var(--glass-border);
}
.btn-ghost:hover {
  background: rgba(205, 162, 88, 0.22);
  color: var(--text-primary);
  border-color: var(--glass-border-hover);
}
.btn-danger {
  background: rgba(154, 28, 28, 0.12);
  color: var(--danger);
  border: 1px solid rgba(154, 28, 28, 0.25);
}
.btn-danger:hover { background: rgba(154, 28, 28, 0.22); }
.btn-success {
  background: rgba(24, 112, 56, 0.12);
  color: var(--success);
  border: 1px solid rgba(24, 112, 56, 0.25);
}
.btn-success:hover { background: rgba(24, 112, 56, 0.22); }
.btn-sm { padding: 0.32rem 0.75rem; font-size: 0.8rem; border-radius: 8px; }

/* Inputs */
input, select, textarea {
  font-family: inherit;
  font-size: 0.875rem;
  color: var(--text-primary);
  background: rgba(255, 249, 235, 0.60);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 1px solid var(--glass-border);
  border-radius: 11px;
  padding: 0.55rem 0.9rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  width: 100%;
  box-shadow: 0 1.5px 0 rgba(255,255,255,0.90) inset;
}
input:focus, select:focus, textarea:focus {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px var(--accent-light), 0 1.5px 0 rgba(255,255,255,0.90) inset;
}
select option { background: #f5ede0; color: var(--text-primary); }

/* Status badges */
.badge {
  display: inline-block;
  padding: 0.2rem 0.65rem;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.badge-available   { background: rgba(24,112,56,0.13);  color: var(--status-available);   border: 1px solid rgba(24,112,56,0.22); }
.badge-reserved    { background: rgba(138,62,8,0.12);   color: var(--status-reserved);    border: 1px solid rgba(138,62,8,0.22); }
.badge-maintenance { background: rgba(154,28,28,0.12);  color: var(--status-maintenance); border: 1px solid rgba(154,28,28,0.22); }
.badge-active      { background: rgba(26,74,138,0.12);  color: var(--status-active);      border: 1px solid rgba(26,74,138,0.22); }
.badge-returned    { background: rgba(24,112,56,0.13);  color: var(--status-returned);    border: 1px solid rgba(24,112,56,0.22); }
.badge-overdue     { background: rgba(154,28,28,0.12);  color: var(--status-overdue);     border: 1px solid rgba(154,28,28,0.22); }
.badge-cancelled   { background: rgba(107,80,64,0.12);  color: var(--status-cancelled);   border: 1px solid rgba(107,80,64,0.22); }
.badge-completed   { background: rgba(90,48,144,0.12);  color: var(--status-completed);   border: 1px solid rgba(90,48,144,0.22); }
.badge-pending     { background: rgba(192,136,64,0.14); color: var(--status-pending);     border: 1px solid rgba(192,136,64,0.22); }
.badge-paid        { background: rgba(24,112,56,0.13);  color: var(--status-paid);        border: 1px solid rgba(24,112,56,0.22); }

/* Spinner */
.spinner {
  width: 2rem; height: 2rem;
  border: 3px solid rgba(205,162,88,0.25);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
.loading-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem;
  color: var(--text-muted);
  animation: fadeIn 0.3s ease;
}

/* Error / empty state */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: var(--text-muted);
  animation: fadeIn 0.3s ease;
}
.empty-state h3 { color: var(--text-secondary); margin-bottom: 0.5rem; font-size: 1rem; }

/* Table */
.table-wrapper { overflow-x: auto; border-radius: 16px; border: 1px solid var(--glass-border); }
table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
thead tr { background: rgba(255,249,235,0.45); border-bottom: 1px solid var(--glass-border); }
th { padding: 0.85rem 1.25rem; text-align: left; font-weight: 700; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.07em; color: var(--text-muted); white-space: nowrap; }
td { padding: 0.85rem 1.25rem; border-bottom: 1px solid rgba(205,162,88,0.10); color: var(--text-primary); }
tbody tr:last-child td { border-bottom: none; }
tbody tr { transition: background 0.15s ease; }
tbody tr:hover { background: rgba(205,162,88,0.07); }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(34, 16, 4, 0.35);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
  padding: 1rem;
}
.modal {
  background: var(--glass-modal);
  backdrop-filter: blur(72px) saturate(220%) brightness(110%);
  -webkit-backdrop-filter: blur(72px) saturate(220%) brightness(110%);
  border: 1px solid rgba(215, 175, 108, 0.55);
  border-radius: 20px;
  padding: 2rem;
  width: 100%;
  max-width: 480px;
  animation: fadeIn 0.25s ease;
  box-shadow: 0 20px 60px rgba(70,35,8,0.22), 0 2px 0 rgba(255,255,255,0.95) inset;
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}
.modal-title { font-size: 1rem; font-weight: 800; color: var(--text-primary); letter-spacing: -0.02em; }
.modal-close {
  background: rgba(205, 162, 88, 0.12);
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1;
  padding: 0.3rem 0.5rem;
  border-radius: 8px;
  border: 1px solid var(--glass-border);
  transition: color 0.2s, background 0.2s;
}
.modal-close:hover { color: var(--text-primary); background: rgba(205,162,88,0.22); }

/* Form */
.form-grid { display: grid; gap: 1rem; }
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-label { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); }
.form-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 0.5rem; }

/* Page layout */
.page-container {
  flex: 1;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
  min-height: 100vh;
}
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.75rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.page-title {
  font-size: 1.7rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.04em;
  line-height: 1.1;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.page-subtitle { font-size: 0.875rem; color: var(--text-muted); margin-top: 0.2rem; font-weight: 400; }

/* Toolbar */
.toolbar {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}
.toolbar input { max-width: 300px; }

/* Stats cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1.75rem;
}
.stat-card {
  background: var(--glass-light);
  backdrop-filter: blur(52px) saturate(180%) brightness(105%);
  -webkit-backdrop-filter: blur(52px) saturate(180%) brightness(105%);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 1.1rem 1.4rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  box-shadow: var(--shadow-warm);
  transition: border-color 0.2s;
}
.stat-card:hover { border-color: var(--glass-border-hover); }
.stat-label { font-size: 0.62rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; }
.stat-value { font-size: 1.8rem; font-weight: 800; color: var(--text-primary); line-height: 1; letter-spacing: -0.045em; }
.stat-icon { font-size: 1.25rem; margin-bottom: 0.2rem; color: var(--text-secondary); display: flex; align-items: center; }
```

- [ ] **Step 2: Verificar que la app arranca sin errores CSS**

```bash
cd frontend && npm run dev
```
Abrir `http://localhost:5173`. El fondo debe ser crema cálido (no negro).

- [ ] **Step 3: Commit**

```bash
git add frontend/src/index.css
git commit -m "style: rewrite index.css with warm library glassmorphism theme"
```

---

## Task 2: Reescribir `components.css`

**Files:**
- Modify: `frontend/src/components/components.css`

- [ ] **Step 1: Reemplazar el contenido completo de `components.css`**

```css
/* ===== LAYOUT ===== */
.layout { display: flex; min-height: 100vh; width: 100%; }

/* ===== SIDEBAR ===== */
.sidebar {
  width: 240px;
  min-height: 100vh;
  background: var(--glass-dark);
  backdrop-filter: blur(56px) saturate(155%);
  -webkit-backdrop-filter: blur(56px) saturate(155%);
  border-right: 1px solid var(--glass-border-dark);
  box-shadow: var(--shadow-dark);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  z-index: 100;
}

.sidebar-brand {
  padding: 1.5rem 1.25rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid var(--glass-border-dark);
  margin-bottom: 0.75rem;
}
.sidebar-logo {
  width: 38px; height: 38px;
  background: linear-gradient(145deg, #d4935a, #8b4010);
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: rgba(255,238,210,0.95);
  box-shadow: 0 4px 14px rgba(0,0,0,0.36), 0 1px 0 rgba(255,255,255,0.18) inset;
  flex-shrink: 0;
}
.sidebar-brand-name {
  font-size: 1rem;
  font-weight: 800;
  color: #ecd898;
  line-height: 1.15;
  letter-spacing: -0.02em;
}
.sidebar-brand-sub {
  font-size: 0.6rem;
  font-weight: 500;
  color: rgba(210, 170, 88, 0.42);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.sidebar-section-label {
  padding: 0.5rem 1.25rem 0.25rem;
  font-size: 0.58rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: rgba(210, 170, 78, 0.36);
}

.sidebar-nav { flex: 1; padding: 0 0.75rem 1rem; }

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.58rem 0.75rem;
  border-radius: 12px;
  color: rgba(228, 196, 132, 0.62);
  text-decoration: none;
  font-size: 0.835rem;
  font-weight: 500;
  transition: all 0.18s ease;
  margin-bottom: 0.12rem;
  letter-spacing: -0.005em;
}
.sidebar-link:hover {
  background: rgba(205, 158, 68, 0.10);
  color: rgba(228, 196, 132, 0.94);
}
.sidebar-link.active {
  background: rgba(200, 138, 58, 0.22);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  color: #f2cc78;
  border: 1px solid rgba(200, 138, 58, 0.30);
  box-shadow: 0 2px 10px rgba(0,0,0,0.18), 0 1px 0 rgba(255,255,255,0.08) inset;
}
.sidebar-link-icon { font-size: 1rem; width: 1.25rem; text-align: center; display: flex; align-items: center; justify-content: center; }

.sidebar-footer {
  padding: 0.85rem 1.25rem;
  border-top: 1px solid var(--glass-border-dark);
  font-size: 0.62rem;
  font-weight: 500;
  color: rgba(210, 170, 78, 0.30);
  letter-spacing: 0.04em;
}

/* ===== MAIN CONTENT ===== */
.main-content {
  flex: 1;
  overflow-y: auto;
  min-width: 0;
  background: var(--glass-strong);
  backdrop-filter: blur(64px) saturate(200%) brightness(107%);
  -webkit-backdrop-filter: blur(64px) saturate(200%) brightness(107%);
  border-left: 1px solid rgba(215, 175, 108, 0.25);
  box-shadow: var(--shadow-warm);
}

/* ===== BOOKS ===== */
.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
}
.book-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 16px;
  border: 1px solid var(--glass-border);
  background: var(--glass-light);
  backdrop-filter: blur(52px) saturate(180%) brightness(105%);
  -webkit-backdrop-filter: blur(52px) saturate(180%) brightness(105%);
  box-shadow: var(--shadow-warm);
  transition: all 0.25s ease;
  animation: fadeIn 0.4s ease;
}
.book-card:hover {
  border-color: var(--glass-border-hover);
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 18px 50px rgba(70,32,8,0.20), 0 2px 0 rgba(255,255,255,0.92) inset;
}
.book-cover-container {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: rgba(205, 162, 88, 0.12);
}
.book-cover-container::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.12) 0%, transparent 65%);
  pointer-events: none;
}
.book-cover { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.book-card:hover .book-cover { transform: scale(1.05); }
.book-availability-badge { position: absolute; top: 0.75rem; right: 0.75rem; }
.book-info { padding: 1.25rem; display: flex; flex-direction: column; gap: 0.5rem; flex: 1; }
.book-title { font-size: 0.95rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.015em; }
.book-author { font-size: 0.8rem; color: var(--text-muted); font-weight: 400; }
.book-meta { display: flex; gap: 0.5rem; align-items: center; font-size: 0.78rem; color: var(--text-muted); }
.book-meta span { color: var(--text-secondary); }
.book-desc { font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5; flex: 1; }
.book-actions { margin-top: auto; padding-top: 0.75rem; display: flex; gap: 0.5rem; }
.book-actions .btn { flex: 1; justify-content: center; }
```

- [ ] **Step 2: Verificar sidebar y contenido principal en el navegador**

Con `npm run dev` corriendo, abrir `http://localhost:5173`.
- El sidebar debe ser oscuro translúcido (marrón oscuro, no negro puro)
- El área de contenido debe tener fondo crema suave
- La navegación debe mostrar el item activo con tinte ámbar

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/components.css
git commit -m "style: rewrite components.css with warm sidebar glass and book cards"
```

---

## Task 3: Actualizar Sidebar.jsx — nombre "Uteblo"

**Files:**
- Modify: `frontend/src/components/Sidebar.jsx`

- [ ] **Step 1: Cambiar el nombre del brand de "Biblioteca" a "Uteblo"**

En `frontend/src/components/Sidebar.jsx` línea 30, reemplazar:
```jsx
        <div className="sidebar-brand-name">Biblioteca</div>
        <div className="sidebar-brand-sub">Sistema de Reservas</div>
```
Por:
```jsx
        <div className="sidebar-brand-name">Uteblo</div>
        <div className="sidebar-brand-sub">Sistema de Reservas</div>
```

- [ ] **Step 2: Verificar en navegador**

El sidebar debe mostrar "Uteblo" como nombre del sistema con el subtítulo "SISTEMA DE RESERVAS".

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/Sidebar.jsx
git commit -m "feat: rename system to Uteblo in sidebar brand"
```

---

## Task 4: Reemplazar `✕` por `HiOutlineXMark` en BooksPage

**Files:**
- Modify: `frontend/src/pages/BooksPage.jsx`

- [ ] **Step 1: Añadir `HiOutlineXMark` al import existente**

En `frontend/src/pages/BooksPage.jsx` línea 1–8, reemplazar:
```jsx
import { 
  HiOutlineBookOpen, 
  HiOutlineExclamationTriangle, 
  HiOutlinePencilSquare, 
  HiOutlineTrash,
  HiOutlinePlus
} from 'react-icons/hi2';
```
Por:
```jsx
import { 
  HiOutlineBookOpen, 
  HiOutlineExclamationTriangle, 
  HiOutlinePencilSquare, 
  HiOutlineTrash,
  HiOutlinePlus,
  HiOutlineXMark
} from 'react-icons/hi2';
```

- [ ] **Step 2: Reemplazar el `✕` del modal close button**

En `frontend/src/pages/BooksPage.jsx` línea 28, reemplazar:
```jsx
        <button className="modal-close btn" onClick={onClose}>✕</button>
```
Por:
```jsx
        <button className="modal-close btn" onClick={onClose}><HiOutlineXMark /></button>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/BooksPage.jsx
git commit -m "style: replace text close button with HiOutlineXMark icon in BooksPage"
```

---

## Task 5: Reemplazar `✕` por `HiOutlineXMark` en UsersPage

**Files:**
- Modify: `frontend/src/pages/UsersPage.jsx`

- [ ] **Step 1: Añadir `HiOutlineXMark` al import existente**

En `frontend/src/pages/UsersPage.jsx` línea 1–8, reemplazar:
```jsx
import { 
  HiOutlineUsers, 
  HiOutlineExclamationTriangle, 
  HiOutlinePencilSquare, 
  HiOutlineTrash,
  HiOutlineUserPlus
} from 'react-icons/hi2';
```
Por:
```jsx
import { 
  HiOutlineUsers, 
  HiOutlineExclamationTriangle, 
  HiOutlinePencilSquare, 
  HiOutlineTrash,
  HiOutlineUserPlus,
  HiOutlineXMark
} from 'react-icons/hi2';
```

- [ ] **Step 2: Reemplazar el `✕` del modal close button**

En `frontend/src/pages/UsersPage.jsx` línea 19, reemplazar:
```jsx
        <button className="modal-close btn" onClick={onClose}>✕</button>
```
Por:
```jsx
        <button className="modal-close btn" onClick={onClose}><HiOutlineXMark /></button>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/UsersPage.jsx
git commit -m "style: replace text close button with HiOutlineXMark icon in UsersPage"
```

---

## Task 6: Actualizar test con nuevo nombre

**Files:**
- Modify: `frontend/src/tests/App.test.jsx`

El test existente busca el texto "Biblioteca Digital" que ya no existe en la app. El componente `App` ahora carga `Sidebar` con el nombre "Uteblo".

- [ ] **Step 1: Ejecutar los tests para confirmar que fallan**

```bash
cd frontend && npm test
```
Resultado esperado: FAIL — `Unable to find an element with the text: /Biblioteca Digital/i`

- [ ] **Step 2: Reemplazar el contenido completo de `App.test.jsx`**

```jsx
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
```

- [ ] **Step 3: Correr tests y verificar que pasan**

```bash
cd frontend && npm test
```
Resultado esperado: PASS — 3 tests passing

- [ ] **Step 4: Commit**

```bash
git add frontend/src/tests/App.test.jsx
git commit -m "test: update tests to match Uteblo brand and sidebar structure"
```

---

## Task 7: Verificación visual final

- [ ] **Step 1: Levantar el servidor de desarrollo**

```bash
cd frontend && npm run dev
```

- [ ] **Step 2: Verificar cada criterio de aceptación en `http://localhost:5173`**

| Criterio | Cómo verificar |
|----------|---------------|
| Fondo crema con gradiente | El body debe ser beige cálido con manchas de luz ámbar en las esquinas |
| Sidebar oscuro translúcido | El sidebar debe ser marrón muy oscuro con borde dorado sutil, semi-transparente |
| "Uteblo" en el brand | Visible en la parte superior del sidebar |
| Glass en contenido principal | El área blanca debe tener un leve blur sobre el fondo del body |
| Cards de libros con glass | Las cards deben elevarse al hacer hover con sombra cálida |
| Tablas con fondo glass | Páginas Préstamos/Usuarios deben tener tabla con glass sutil |
| Modal con blur denso | Al abrir un modal, el fondo se oscurece con blur y el modal tiene vidrio denso |
| Botón primario caoba | Marrón caoba con gradiente oscuro, sombra cálida |
| Plus Jakarta Sans | Abrir DevTools → Elements → inspeccionar body, ver font-family |
| Badges colores cálidos | Verde para disponible, marrón para reservado, rojo para vencido |
| Botón X en modales | Los botones de cerrar modal deben mostrar el ícono `×` de Heroicons, no el caracter de texto |
| Scrollbar cálido | En páginas con mucho contenido, el scrollbar debe ser marrón suave |

- [ ] **Step 3: Verificar con build de producción**

```bash
cd frontend && npm run build
```
Resultado esperado: build exitoso sin errores.

- [ ] **Step 4: Commit final y tag**

```bash
git add -A
git commit -m "chore: verify Uteblo redesign complete — all acceptance criteria met"
```
