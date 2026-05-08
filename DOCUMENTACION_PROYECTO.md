# Proyecto: Biblioteca Uteblo 📚

## a) Título y descripción del proyecto y del equipo

**Nombre del producto/servicio:** Biblioteca Uteblo - Sistema de Gestión de Reservas

**Breve explicación del problema y la solución propuesta:**
Las bibliotecas tradicionales a menudo enfrentan dificultades para gestionar eficientemente los préstamos, devoluciones y multas de forma transparente para el usuario. **Biblioteca Uteblo** ofrece una plataforma moderna basada en web que centraliza la administración de libros, usuarios y notificaciones, permitiendo un seguimiento en tiempo real de los estados de reserva y una interfaz profesional que mejora la experiencia del bibliotecario y del lector.

**Integrantes y roles:**
*   **Esteban:** Product Owner & Lead Developer.
*   **Antigravity (AI):** Arquitecto de Software y Especialista DevOps.

---

## b) Justificación de la elección del tema

**Contexto del proyecto:**
El proyecto surge en un entorno académico/profesional donde se requiere demostrar el dominio de un stack tecnológico completo (Fullstack) integrando buenas prácticas de ingeniería de software.

**Motivación y relevancia:**
La gestión de inventarios y usuarios es un problema clásico que permite explorar múltiples facetas del desarrollo:
*   Persistencia de datos relacionales (PostgreSQL).
*   Desarrollo de APIs robustas (FastAPI).
*   Interfaces de usuario reactivas y profesionales (React + Tailwind + Heroicons).
*   Automatización y calidad (Docker + Pytest).

---

## c) Aplicación de Git con Conventional Commits

**Explicación de Conventional Commits:**
Utilizamos el estándar de **Conventional Commits** para mantener un historial de cambios legible y facilitar la generación automática de versiones. Este estándar añade contexto a los mensajes de commit mediante tipos (feat, fix, style, etc.).

**Guía de tipos principales:**
*   `feat`: Nueva funcionalidad.
*   `fix`: Corrección de errores.
*   `docs`: Cambios en la documentación.
*   `style`: Cambios de formato o UI que no afectan la lógica.
*   `test`: Adición o modificación de pruebas.
*   `chore`: Tareas de mantenimiento o actualización de dependencias.

**Análisis de historial de commits (Muestra de 6 commits):**

1.  `c66415a` - **docs: add project documentation and fix unit tests**: Documentación técnica y estabilidad de pruebas.
2.  `24b0bd9` - **feat: implemetación del backend 2.0**: Integración final de servicios y repositorios.
3.  `616de1a` - **fix: connect frontend to backend**: Corrección de discrepancias en nombres de campos y estados.
4.  `7264d9f` - **test: update tests to match Uteblo brand**: Actualización de pruebas unitarias para reflejar el cambio de marca.
5.  `9790145` - **feat: rename system to Uteblo in sidebar**: Cambio de branding en la interfaz de usuario.
6.  `acac4bd` - **style: rewrite index.css with warm library glassmorphism**: Rediseño visual premium con estética de biblioteca moderna.

---

## d) Pruebas Unitarias

Se han implementado **9 pruebas unitarias** para asegurar la calidad y estabilidad del backend. Las pruebas cubren desde la salud del API hasta la validación de endpoints clave.

**Lista de Pruebas Implementadas:**
1.  `test_read_root`: Verifica que el punto de entrada principal responda correctamente.
2.  `test_health_check`: Valida el estado de salud del sistema.
3.  `test_not_found`: Asegura que los errores 404 se manejen adecuadamente.
4.  `test_api_title`: Confirma que el título de la aplicación sea el correcto.
5.  `test_api_version`: Verifica la existencia de metadatos de versión.
6.  `test_books_endpoint_exists`: Comprueba la disponibilidad del recurso de libros.
7.  `test_users_endpoint_exists`: Comprueba la disponibilidad del recurso de usuarios.
8.  `test_loans_endpoint_exists`: Comprueba la disponibilidad del recurso de préstamos.
9.  `test_fines_endpoint_exists`: Comprueba la disponibilidad del recurso de multas.

---

## e) Dockerizar su aplicación

La aplicación está completamente dockerizada mediante un flujo de orquestación con **Docker Compose**.

**Estructura de Servicios:**
1.  **db (PostgreSQL 16.3):** Almacenamiento persistente de datos con volumen dedicado.
2.  **backend (FastAPI):** Aplicación de servidor que expone la lógica de negocio y se conecta a la DB.
3.  **frontend (React/Vite + Nginx):** Interfaz de usuario construida con Node y servida de forma optimizada mediante **Nginx** (puerto 5173 mapeado al 80 del contenedor). Utiliza un **multi-stage build** para reducir el tamaño de la imagen.

**Comando de ejecución:**
```bash
docker-compose up --build
```

---

*Documentación generada el 8 de mayo de 2026.*
