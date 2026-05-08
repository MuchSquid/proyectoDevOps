# Uteblo — Rediseño UI: Biblioteca Moderna con Glassmorphism Apple

**Fecha:** 2026-05-08  
**Estado:** Aprobado  
**Alcance:** Solo CSS (index.css, components.css) + Sidebar.jsx nombre + reemplazo de emojis por react-icons

---

## 1. Objetivo

Rediseñar completamente la interfaz visual del sistema de reservas de biblioteca para que adopte una estética de biblioteca moderna con glassmorphism estilo Apple. El cambio es puramente visual — cero modificaciones a la lógica de negocio o estructura de componentes JSX (excepto el Sidebar y reemplazo de emojis por react-icons).

---

## 2. Nombre del sistema

El sistema pasa a llamarse **Uteblo**. Subtítulo: *Sistema de Reservas*.

---

## 3. Tipografía

**Fuente única:** `Plus Jakarta Sans` (Google Fonts)  
Pesos: 300, 400, 500, 600, 700, 800

| Uso | Peso | Tamaño | Letter-spacing |
|-----|------|--------|----------------|
| Título de página (`page-title`) | 800 | 1.7rem | -0.04em |
| Brand name sidebar | 800 | 1rem | -0.02em |
| Subtítulos, nav activo | 600 | — | -0.02em |
| Cuerpo, metadata | 400 | 0.875rem | -0.01em |
| Labels uppercase / badges | 700 | 0.6rem | 0.08em |

Reemplaza `Inter` completamente. Import en `index.css`:
```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');
```

---

## 4. Paleta de colores

### Variables CSS (`:root`)

```css
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

/* Sombras */
--shadow-warm: 0 10px 44px rgba(70,35,8,0.13), 0 2px 0 rgba(255,255,255,0.88) inset;
--shadow-dark: 0 10px 44px rgba(0,0,0,0.28),   0 1.5px 0 rgba(255,255,255,0.07) inset;

/* Texto */
--text-primary:   #221004;
--text-secondary: #6b3f20;
--text-muted:     #a87048;

/* Acento */
--accent-primary: #8b4513;
--accent-amber:   #c08840;
--accent-gradient: linear-gradient(145deg, #a05018, #7a3410);

/* Semánticos */
--success: #187038;
--warning: #c08840;
--danger:  #9a1c1c;
--info:    #1a4a8a;

/* Status (mismos nombres, nuevos colores cálidos) */
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
```

### Fondo del body

```css
body {
  background:
    radial-gradient(ellipse 75% 55% at 12%  8%,  rgba(200,150,60,0.22) 0%, transparent 58%),
    radial-gradient(ellipse 55% 50% at 88% 88%,  rgba(140,75,25,0.17)  0%, transparent 58%),
    radial-gradient(ellipse 45% 38% at 55% 38%,  rgba(230,195,125,0.11) 0%, transparent 48%),
    linear-gradient(148deg, #ede3d0 0%, #e3d4b8 55%, #d8c8a2 100%);
}
```

---

## 5. Sistema Glassmorphism

Tres niveles de glass, usados según contexto:

| Clase | Blur | Saturate | Background | Uso |
|-------|------|----------|------------|-----|
| `.glass` | 52px | 180% | rgba(255,249,238, 0.60) | Cards, stat cards, tabla |
| `.glass-strong` | 64px | 200% | rgba(255,250,240, 0.80) | Panel principal (main-content) |
| `.glass-dark` | 56px | 155% | rgba(28,13,4, 0.84) | Sidebar |
| `.glass-modal` | 72px | 220% | rgba(255,249,235, 0.88) | Modales |

Todos comparten:
- `brightness()`: light +5–7%, dark sin cambio
- `border`: 1px solid con tinte dorado cálido
- `border-radius`: 18–20px
- Sombra con **inset blanco** para efecto de borde iluminado superior (clave del estilo Apple)

---

## 6. Componentes — cambios CSS

### Sidebar
- Background: `var(--glass-dark)` con backdrop-filter
- Brand: logo con gradiente caoba, nombre **Uteblo** en 800 weight
- Nav items activos: background con tinte ámbar, borde sutil, glow suave

### Main content
- Background: `var(--glass-strong)`
- Page title: 1.7rem 800 weight, letter-spacing -0.04em

### Stat cards
- `.glass` con padding 0.9rem 1rem
- Valor: 1.8rem 800 weight, letter-spacing -0.045em

### Book cards
- `.glass` con hover: `translateY(-4px) scale(1.01)` + sombra amplificada
- Reflejo superior en cover via `::after` pseudo-elemento

### Tablas
- Header con `rgba(255,249,235,0.45)`
- Filas hover: `rgba(205,162,88,0.07)`
- Borders cálidos

### Modales
- `.glass-modal` (blur 72px) — el más denso
- Overlay: `rgba(34,16,4,0.35)` con `blur(8px)`

### Inputs / Search
- Glass suave, borde cálido, inset blanco
- `font-style: italic` para el placeholder del buscador

### Botón primario
- `var(--accent-gradient)` con `box-shadow` cálida y lift en hover

### Badges
- Disponible: verde cálido `#187038`
- Reservado: caoba `#8a3e08`  
- Vencido: rojo `#9a1c1c`
- Cancelado: marrón neutro

### Scrollbar
- Track: transparente
- Thumb: `rgba(170,115,55,0.28)` — cálido, discreto

---

## 7. Iconos (react-icons)

Reemplazar todos los emojis de UI por iconos de `react-icons/hi2` (Heroicons 2). Los emojis de portada de libros (📕📗📘) se mantienen como placeholder hasta tener imágenes reales.

| Ubicación | Emoji actual | Ícono react-icons |
|-----------|-------------|-------------------|
| Sidebar brand | — | `HiOutlineLibrary` (ya existe en hi2) |
| Nav: Libros | — | `HiOutlineBookOpen` (ya existe) |
| Nav: Usuarios | — | `HiOutlineUsers` (ya existe) |
| Nav: Préstamos | — | `HiOutlineClipboardDocumentList` (ya existe) |
| Nav: Reservas | — | `HiOutlineBookmark` (ya existe) |
| Nav: Multas | — | `HiOutlineCurrencyDollar` (ya existe) |
| Nav: Notificaciones | — | `HiOutlineBell` (ya existe) |
| Page title Libros | 📖 | `HiOutlineBookOpen` |
| Page title Usuarios | 👤 | `HiOutlineUsers` |
| Page title Préstamos | 📋 | `HiOutlineClipboardDocumentList` |
| Page title Reservas | 🔖 | `HiOutlineBookmark` |
| Page title Multas | 💰 | `HiOutlineCurrencyDollar` |
| Page title Notificaciones | 🔔 | `HiOutlineBell` |
| Botón agregar | ＋ | `HiOutlinePlus` (ya existe) |
| Stat: Total libros | 📚 | `HiOutlineBookOpen` |
| Stat: Disponibles | ✅ | `HiOutlineCheckCircle` |
| Stat: Prestados | 🔖 | `HiOutlineArrowPathRoundedSquare` |
| Stat: Vencidos | ⏰ | `HiOutlineClock` |
| Search | 🔍 | `HiOutlineMagnifyingGlass` |
| Modal título nuevo | ✦ | `HiOutlinePlusCircle` |
| Modal título editar | — | `HiOutlinePencilSquare` (ya existe) |
| Empty state error | — | `HiOutlineExclamationTriangle` (ya existe) |

---

## 8. Archivos modificados

| Archivo | Tipo de cambio |
|---------|---------------|
| `frontend/src/index.css` | **Reescritura completa** — variables, body, buttons, inputs, badges, table, modal, spinner, layout |
| `frontend/src/components/components.css` | **Reescritura completa** — sidebar, main, book cards, stats |
| `frontend/src/components/Sidebar.jsx` | Cambio de nombre a **Uteblo**, icono brand actualizado |
| `frontend/src/pages/BooksPage.jsx` | Reemplazar emojis por react-icons hi2 |
| `frontend/src/pages/LoansPage.jsx` | Reemplazar emojis por react-icons hi2 |
| `frontend/src/pages/UsersPage.jsx` | Reemplazar emojis por react-icons hi2 |
| `frontend/src/pages/ReservationsPage.jsx` | Reemplazar emojis por react-icons hi2 |
| `frontend/src/pages/FinesPage.jsx` | Reemplazar emojis por react-icons hi2 |
| `frontend/src/pages/NotificationsPage.jsx` | Reemplazar emojis por react-icons hi2 |

**No se modifican:** `App.jsx`, `main.jsx`, archivos de API, lógica de negocio.

---

## 9. Criterios de aceptación

- [ ] Fondo crema con gradiente radial visible en toda la app
- [ ] Sidebar oscuro translúcido con efecto glass, nombre "Uteblo"
- [ ] Contenido principal con glass-strong (blur 64px)
- [ ] Cards de libros con hover elevado y reflejo en cover
- [ ] Tablas con fondo glass y filas hover cálidas
- [ ] Modales con blur máximo (72px) y overlay oscuro-cálido
- [ ] Botón primario caoba con gradiente y sombra
- [ ] Fuente Plus Jakarta Sans aplicada en toda la UI
- [ ] Cero emojis en elementos de navegación, títulos y stat cards (solo en portadas de libros placeholder)
- [ ] Badges de estado con colores cálidos correctos
- [ ] Scrollbar cálido y discreto
