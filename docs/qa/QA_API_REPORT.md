# Reporte de QA - proyectoDevOps / Uteblo

## 1. Objetivo del reporte

El presente reporte documenta las actividades de aseguramiento de calidad realizadas sobre el proyecto **Uteblo - Sistema de Reservas de Biblioteca**, con el objetivo de validar el funcionamiento general del sistema, la disponibilidad de sus servicios, el comportamiento de sus APIs principales, la ejecución de pruebas automatizadas y la trazabilidad del desarrollo mediante Git.

El proyecto corresponde a un monorepo que integra frontend, backend, pruebas, scripts de automatización y despliegue con Docker Compose. Según la estructura documentada del proyecto, el sistema utiliza **React + Vite** para el frontend, **FastAPI** para el backend, **PostgreSQL** como base de datos y herramientas de prueba como **Vitest** y **Pytest**. :contentReference[oaicite:0]{index=0}

Además, el trabajo de QA responde a los criterios solicitados en la evaluación del proyecto parcial, donde se exige evidencia de pruebas unitarias, Dockerización, control de versiones con Conventional Commits, historial mínimo de commits y análisis detallado de una muestra de commits. :contentReference[oaicite:1]{index=1}

---

## 2. Alcance del QA realizado

El alcance de las pruebas realizadas cubrió los siguientes aspectos:

| Área evaluada | Actividad realizada |
|---|---|
| Disponibilidad del backend | Validación de respuesta HTTP del backend en `/docs` |
| Disponibilidad del frontend | Validación de respuesta HTTP del frontend en el puerto local |
| Docker Compose | Verificación de contenedores activos: backend, frontend y base de datos |
| Swagger/OpenAPI | Revisión de endpoints expuestos por la API |
| API Smoke Testing | Validación automatizada de endpoints principales |
| Validación de errores | Pruebas con bodies inválidos y recursos inexistentes |
| Pruebas unitarias frontend | Ejecución de suite Vitest con 9 pruebas aprobadas |
| Pruebas backend | Verificación de Pytest; no se detectaron pruebas backend existentes |
| Evidencia documental | Creación de archivos en `docs/qa/` |
| Trazabilidad Git | Generación de historial de commits para análisis |

---

## 3. Entorno de prueba

Las pruebas se ejecutaron en un entorno local dockerizado.

| Componente | Tecnología / valor |
|---|---|
| Sistema | Uteblo - Sistema de Reservas de Biblioteca |
| Backend | FastAPI |
| Frontend | React + Vite |
| Base de datos | PostgreSQL 16.3 |
| Contenedores | Docker Compose |
| Documentación API | Swagger / OpenAPI |
| Backend URL | `http://localhost:8000` |
| Swagger URL | `http://localhost:8000/docs` |
| Frontend URL | `http://localhost:5173` |
| Rama QA | `qa/api-testing` |
| Herramientas QA | Python, Vitest, Pytest, curl, Docker Compose |

---

## 4. Estado de servicios

Durante la validación, los servicios principales fueron levantados mediante Docker Compose.

### 4.1 Servicios activos

Se verificó que los siguientes contenedores se encontraban en estado `Up`:

| Servicio | Contenedor | Puerto | Estado |
|---|---|---|---|
| Backend | `biblioteca_backend` | `8000:8000` | Activo |
| Base de datos | `biblioteca_db` | `5432:5432` | Activo |
| Frontend | `biblioteca_frontend` | `5173:5173` | Activo |

### 4.2 Validación HTTP del backend

Se ejecutó una validación HTTP sobre Swagger:

```bash
curl -I http://localhost:8000/docs



### 4.2 Validación HTTP del backend

Se ejecutó una validación HTTP sobre Swagger para confirmar que el backend se encontraba disponible y respondiendo correctamente.

Comando ejecutado:

```bash
curl -I http://localhost:8000/docs
```

Resultado obtenido:

```text
HTTP/1.1 200 OK
server: uvicorn
content-type: text/html; charset=utf-8
```

Este resultado confirma que el backend se encontraba activo y que la documentación interactiva de la API, generada mediante Swagger/OpenAPI, estaba disponible correctamente en el entorno local.

---

### 4.3 Validación HTTP del frontend

También se validó la disponibilidad del frontend ejecutando una solicitud HTTP al puerto donde se encontraba desplegada la aplicación React/Vite.

Comando ejecutado:

```bash
curl -I http://localhost:5173
```

Resultado obtenido:

```text
HTTP/1.1 200 OK
content-type: text/html
```

Este resultado confirma que la interfaz web del sistema Uteblo estaba disponible localmente y podía ser accedida desde el navegador.

---

## 5. Observación técnica durante el arranque

Durante el arranque inicial de los servicios Docker se observó el siguiente mensaje en los logs del backend:

```text
connection to server at "db", port 5432 failed: Connection refused
```

Este error corresponde a una condición temporal de arranque. Es decir, el backend intentó conectarse al servicio de PostgreSQL antes de que la base de datos estuviera completamente lista para aceptar conexiones.

Sin embargo, este hallazgo no bloqueó el proceso de QA, ya que posteriormente se verificó lo siguiente:

- Los contenedores quedaron en estado `Up`.
- El backend respondió correctamente en `/docs` con `HTTP 200 OK`.
- El frontend respondió correctamente con `HTTP 200 OK`.
- El smoke test de APIs finalizó correctamente con `20/20 tests passed`.

Por lo tanto, este comportamiento se registra como un hallazgo técnico de severidad media, pero no como un error bloqueante para la validación funcional del sistema.

### Recomendación técnica

Se recomienda mejorar el archivo `docker-compose.yml` agregando un `healthcheck` al servicio de PostgreSQL y configurando el backend para depender de una base de datos saludable antes de iniciar completamente.

Ejemplo conceptual:

```yaml
depends_on:
  db:
    condition: service_healthy
```

Esto permitiría reducir errores temporales durante el arranque y haría más robusto el proceso de despliegue local.

---

## 6. Endpoints identificados en Swagger

La API del sistema expone diferentes módulos funcionales relacionados con la gestión de biblioteca. Los endpoints fueron identificados desde la documentación Swagger disponible en:

```text
http://localhost:8000/docs
```

A continuación, se listan los endpoints principales encontrados.

---

### 6.1 Books

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/books/` | Listar libros |
| POST | `/books/` | Crear libro |
| GET | `/books/{book_id}` | Obtener libro por ID |
| PUT | `/books/{book_id}` | Actualizar libro |
| DELETE | `/books/{book_id}` | Eliminar libro |

---

### 6.2 Users

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/users/` | Listar usuarios |
| POST | `/users/` | Crear usuario |
| GET | `/users/{user_id}` | Obtener usuario por ID |
| PUT | `/users/{user_id}` | Actualizar usuario |
| DELETE | `/users/{user_id}` | Eliminar usuario |

---

### 6.3 Loans

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/loans/` | Listar préstamos |
| POST | `/loans/` | Crear préstamo |
| GET | `/loans/{loan_id}` | Obtener préstamo por ID |
| DELETE | `/loans/{loan_id}` | Eliminar préstamo |
| GET | `/loans/user/{user_id}` | Obtener préstamos por usuario |
| PATCH | `/loans/{loan_id}/return` | Retornar préstamo |
| PATCH | `/loans/{loan_id}/cancel` | Cancelar préstamo |

---

### 6.4 Reservations

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/reservations/` | Listar reservas |
| POST | `/reservations/` | Crear reserva |
| GET | `/reservations/{reservation_id}` | Obtener reserva por ID |
| DELETE | `/reservations/{reservation_id}` | Eliminar reserva |
| GET | `/reservations/user/{user_id}` | Obtener reservas por usuario |
| PATCH | `/reservations/{reservation_id}/cancel` | Cancelar reserva |
| PATCH | `/reservations/{reservation_id}/complete` | Completar reserva |

---

### 6.5 Fines

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/fines/` | Listar multas |
| POST | `/fines/` | Crear multa |
| GET | `/fines/user/{user_id}` | Obtener multas por usuario |
| GET | `/fines/{fine_id}` | Obtener multa por ID |
| PATCH | `/fines/{fine_id}/pay` | Marcar multa como pagada |
| PATCH | `/fines/{fine_id}/cancel` | Cancelar multa |

---

### 6.6 Notifications

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/notifications/` | Listar notificaciones |
| POST | `/notifications/` | Crear notificación |
| GET | `/notifications/user/{user_id}/unread` | Obtener notificaciones no leídas por usuario |
| GET | `/notifications/user/{user_id}` | Obtener notificaciones por usuario |
| GET | `/notifications/{notification_id}` | Obtener notificación por ID |
| PATCH | `/notifications/{notification_id}/read` | Marcar notificación como leída |

---

### 6.7 Default

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Endpoint raíz |
| GET | `/health` | Health check del backend |

---

## 7. API Smoke Test

Para validar rápidamente la disponibilidad y el comportamiento básico de las APIs, se creó el archivo:

```text
docs/qa/api_smoke_test.py
```

Este script ejecuta pruebas automáticas contra los endpoints principales del backend. La validación incluye:

1. Endpoints exitosos con respuesta `200 OK`.
2. Peticiones `POST` inválidas para verificar respuestas controladas `400` o `422`.
3. Consultas a recursos inexistentes para verificar respuestas `404` o `422`.

El objetivo de este smoke test no fue reemplazar pruebas unitarias profundas, sino confirmar que los módulos principales del backend respondían de forma estable y controlada.

---

### 7.1 Resultado del smoke test

Comando ejecutado:

```bash
python docs/qa/api_smoke_test.py
```

Resultado obtenido:

```text
Summary: 20/20 tests passed
```

Este resultado evidencia que todas las validaciones automáticas ejecutadas sobre la API fueron satisfactorias.

---

### 7.2 Casos cubiertos por el smoke test

| ID | Método | Endpoint | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|---|
| API-01 | GET | `/` | 200 | 200 | Aprobado |
| API-02 | GET | `/health` | 200 | 200 | Aprobado |
| API-03 | GET | `/books/` | 200 | 200 | Aprobado |
| API-04 | GET | `/users/` | 200 | 200 | Aprobado |
| API-05 | GET | `/loans/` | 200 | 200 | Aprobado |
| API-06 | GET | `/reservations/` | 200 | 200 | Aprobado |
| API-07 | GET | `/fines/` | 200 | 200 | Aprobado |
| API-08 | GET | `/notifications/` | 200 | 200 | Aprobado |
| API-09 | POST | `/books/` con `{}` | 400/422 | 422 | Aprobado |
| API-10 | POST | `/users/` con `{}` | 400/422 | 422 | Aprobado |
| API-11 | POST | `/loans/` con `{}` | 400/422 | 422 | Aprobado |
| API-12 | POST | `/reservations/` con `{}` | 400/422 | 422 | Aprobado |
| API-13 | POST | `/fines/` con `{}` | 400/422 | 422 | Aprobado |
| API-14 | POST | `/notifications/` con `{}` | 400/422 | 422 | Aprobado |
| API-15 | GET | `/books/999999` | 404/422 | 404 | Aprobado |
| API-16 | GET | `/users/999999` | 404/422 | 404 | Aprobado |
| API-17 | GET | `/loans/999999` | 404/422 | 404 | Aprobado |
| API-18 | GET | `/reservations/999999` | 404/422 | 404 | Aprobado |
| API-19 | GET | `/fines/999999` | 404/422 | 404 | Aprobado |
| API-20 | GET | `/notifications/999999` | 404/422 | 404 | Aprobado |

---

### 7.3 Interpretación del smoke test

El resultado `20/20 tests passed` permite concluir que:

- El backend está disponible.
- Los endpoints principales responden correctamente.
- Las validaciones de entrada funcionan para datos inválidos.
- Los recursos inexistentes no generan errores internos.
- La API responde con códigos HTTP controlados.
- No se observaron errores `500 Internal Server Error` durante el smoke test.

Esto aporta evidencia importante de estabilidad funcional básica sobre los módulos principales del backend.

---

## 8. Pruebas unitarias frontend

Se ejecutaron pruebas unitarias sobre el frontend utilizando **Vitest**.

Inicialmente, el frontend contaba con 3 pruebas existentes. Para cumplir el mínimo requerido de 9 pruebas unitarias, se agregó un nuevo archivo de pruebas:

```text
frontend/src/tests/App.qa.test.jsx
```

Este archivo añadió 6 pruebas adicionales orientadas a validar elementos principales de la interfaz.

---

### 8.1 Comando ejecutado

Desde la carpeta `frontend`, se ejecutó:

```bash
npx vitest run
```

---

### 8.2 Resultado obtenido

El resultado final de la ejecución fue:

```text
Test Files  2 passed (2)
Tests       9 passed (9)
```

Este resultado confirma que la suite de pruebas frontend alcanzó el mínimo de 9 pruebas unitarias exigido para la entrega.

---

### 8.3 Pruebas frontend validadas

Las pruebas frontend verificaron aspectos relevantes de la interfaz principal del sistema:

| ID | Prueba | Propósito |
|---|---|---|
| UI-01 | Renderizado del nombre Uteblo | Validar identidad principal del sistema |
| UI-02 | Renderizado del subtítulo Sistema de Reservas | Confirmar propósito visible de la aplicación |
| UI-03 | Visualización de módulos de navegación | Confirmar estructura general de la interfaz |
| UI-04 | Visualización de la sección Libros | Validar módulo principal |
| UI-05 | Visualización del contador de catálogo | Confirmar información de estado del catálogo |
| UI-06 | Visualización del campo de búsqueda | Validar elemento de interacción |
| UI-07 | Escritura en el campo de búsqueda | Validar interacción del usuario |
| UI-08 | Visualización del botón Agregar libro | Validar acción principal del módulo libros |
| UI-09 | Visualización de módulos: Usuarios, Préstamos, Reservas, Multas y Notificaciones | Validar navegación general del sistema |

---

### 8.4 Interpretación

El resultado `9 passed` permite concluir que el frontend cumple con el mínimo de pruebas unitarias solicitado para esta etapa del proyecto.

Estas pruebas no reemplazan pruebas end-to-end completas, pero validan que los elementos principales de la interfaz se renderizan correctamente y que existe una base automatizada para prevenir regresiones visuales básicas.

---

## 9. Pruebas backend con Pytest

También se intentó ejecutar pruebas backend mediante Pytest.

---

### 9.1 Preparación del entorno

Se creó un entorno virtual dentro del backend y se instalaron las dependencias necesarias desde `requirements.txt`.

Comandos ejecutados:

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pytest httpx
```

---

### 9.2 Resultado de Pytest

Al ejecutar:

```bash
python -m pytest -q
```

se obtuvo:

```text
no tests ran
```

---

### 9.3 Interpretación

Este resultado indica que Pytest se instaló correctamente, pero no encontró archivos de prueba backend dentro de la estructura actual del proyecto.

Por esta razón, la cobertura unitaria fue reforzada en frontend con Vitest hasta alcanzar las 9 pruebas solicitadas. Además, la validación funcional del backend fue cubierta mediante el smoke test automatizado de APIs, el cual obtuvo `20/20 tests passed`.

---

### 9.4 Recomendación

Se recomienda agregar pruebas backend formales en una futura iteración, por ejemplo:

- Prueba de `GET /health`.
- Prueba de `GET /books/`.
- Prueba de `POST /books/` con datos inválidos.
- Prueba de `GET /books/{id}` inexistente.
- Prueba de validaciones de usuarios.
- Prueba de reglas de préstamos y reservas.
- Prueba de reglas de multas y notificaciones.

Esto permitiría complementar el smoke test funcional con una cobertura unitaria más sólida sobre la lógica del backend.

---

## 10. Evidencias generadas

Durante el proceso de QA se generaron o deben adjuntarse las siguientes evidencias:

| Evidencia | Descripción |
|---|---|
| `docker compose ps` | Servicios backend, frontend y db activos |
| `curl -I http://localhost:8000/docs` | Backend respondiendo `200 OK` |
| `curl -I http://localhost:5173` | Frontend respondiendo `200 OK` |
| Swagger UI | Endpoints disponibles por módulo |
| Frontend local | Interfaz Uteblo corriendo en navegador |
| `api_smoke_test.py` | Script de validación de APIs |
| Resultado smoke test | `20/20 tests passed` |
| Resultado Vitest | `9/9 tests passed` |
| Resultado Pytest | `no tests ran`, documentado como hallazgo |
| `git_history_25_commits.txt` | Historial de commits para trazabilidad |
| Pull Request QA | Evidencia de flujo de ramas y revisión |

---

## 11. Archivos creados o modificados

Como parte del trabajo QA se trabajó con los siguientes archivos:

| Archivo | Propósito |
|---|---|
| `docs/qa/api_smoke_test.py` | Script automatizado para probar endpoints principales |
| `docs/qa/test_summary.md` | Resumen de resultados QA |
| `docs/qa/git_history_25_commits.txt` | Evidencia del historial de commits |
| `docs/qa/QA_API_REPORT.md` | Reporte profesional de QA |
| `frontend/src/tests/App.qa.test.jsx` | Nuevas pruebas unitarias frontend |
| `.gitignore` | Prevención de subida de entornos locales y dependencias innecesarias |

Antes del commit se debe verificar que no se incluyan carpetas innecesarias o generadas localmente, tales como:

```text
backend/.venv/
frontend/node_modules/
__pycache__/
.pytest_cache/
```

---

## 12. Hallazgos QA

| ID | Hallazgo | Severidad | Impacto | Recomendación |
|---|---|---|---|---|
| QA-01 | El backend mostró inicialmente un error de conexión con PostgreSQL durante el arranque. | Media | Puede generar confusión al iniciar el entorno. | Agregar `healthcheck` y dependencia por servicio saludable en Docker Compose. |
| QA-02 | La base de datos Docker inició sin datos de catálogo. | Baja | El frontend puede mostrar `0 libros en el catálogo`. | Agregar script de seed para entorno local. |
| QA-03 | Pytest no detectó pruebas backend. | Media | No existe cobertura unitaria backend formal. | Agregar pruebas con Pytest y FastAPI TestClient. |
| QA-04 | La cobertura unitaria actual se concentra en frontend. | Media | El backend depende del smoke test funcional. | Complementar con pruebas unitarias backend en futuras iteraciones. |
| QA-05 | El warning `version is obsolete` aparece en Docker Compose. | Baja | No bloquea ejecución, pero puede generar ruido en consola. | Retirar el atributo `version` del archivo `docker-compose.yml`. |

---

## 13. Evaluación frente a requisitos del proyecto

| Requisito | Estado | Evidencia |
|---|---|---|
| Proyecto dockerizado | Cumplido | `docker compose ps` con servicios activos |
| Backend funcionando | Cumplido | `/docs` responde `200 OK` |
| Frontend funcionando | Cumplido | Frontend responde `200 OK` |
| Swagger disponible | Cumplido | Endpoints visibles en `/docs` |
| Mínimo 9 pruebas unitarias | Cumplido | Vitest: `9 passed` |
| Evidencia de ejecución de tests | Cumplido | Captura de Vitest y smoke test |
| Validación de APIs | Cumplido | Smoke test: `20/20 passed` |
| Historial mínimo de commits | Cumplido si se adjunta captura | Repositorio muestra más de 9 commits |
| Análisis de 6 commits | Pendiente de completar con hashes reales | Usar `git log` y `git show --stat` |
| Pull Request según branching | Cumplido si se adjunta PR | Crear PR desde `qa/api-testing` hacia `main` |

---

## 14. Análisis de commits

Para cumplir con la trazabilidad del desarrollo, se generó el archivo:

```text
docs/qa/git_history_25_commits.txt
```

Este archivo contiene el historial reciente del repositorio y debe utilizarse para seleccionar 6 commits representativos.

La siguiente tabla debe completarse con los hashes reales obtenidos mediante:

```bash
git log --oneline --decorate -n 25
git show --stat HASH
```

| Commit | Tipo | Mensaje | Propósito | Impacto QA |
|---|---|---|---|---|
| `HASH-01` | `feat` | Implementación de estructura backend para Book | Añade o mejora el módulo de libros | Requiere validar CRUD de libros |
| `HASH-02` | `feat(backend)` | Implementación del módulo User | Añade funcionalidad relacionada con usuarios | Requiere pruebas de creación, listado y validación de usuarios |
| `HASH-03` | `feat` | Implementación del backend 2.0 | Integra nueva versión o mejoras del backend | Requiere smoke testing general de APIs |
| `HASH-04` | `docs` | Documentación o plan de implementación | Mejora trazabilidad documental | No impacta ejecución, pero mejora mantenibilidad |
| `HASH-05` | `feat` | Setup inicial del proyecto | Crea estructura base del monorepo | Base para Docker, pruebas y automatización |
| `HASH-06` | `test` | Evidencia o pruebas QA | Añade pruebas y documentación de calidad | Evidencia directa para evaluación QA |

---

## 15. Checklist de capturas sugeridas

Para el informe final o presentación se recomienda adjuntar las siguientes capturas:

- [ ] Repositorio GitHub mostrando más de 9 commits.
- [ ] Historial de commits en terminal con `git log --oneline -n 25`.
- [ ] Pull Request desde `qa/api-testing` hacia `main`.
- [ ] `docker compose ps` mostrando backend, db y frontend en estado `Up`.
- [ ] `curl -I http://localhost:8000/docs` con `HTTP/1.1 200 OK`.
- [ ] `curl -I http://localhost:5173` con `HTTP/1.1 200 OK`.
- [ ] Swagger mostrando endpoints de Books, Users, Loans, Reservations, Fines y Notifications.
- [ ] Frontend corriendo en `localhost:5173`.
- [ ] Smoke test API con `20/20 tests passed`.
- [ ] Vitest con `9 passed`.
- [ ] Pytest mostrando `no tests ran`, documentado como hallazgo.
- [ ] Archivo `docs/qa/QA_API_REPORT.md` creado dentro del repositorio.

---

## 16. Conclusión

El proceso de QA realizado permitió validar que el sistema **Uteblo - Biblioteca Reservas** se encuentra operativo en un entorno local dockerizado. Se confirmó que tanto el backend como el frontend responden correctamente, que la documentación Swagger está disponible y que los endpoints principales de la API funcionan de manera estable.

El smoke test automatizado obtuvo un resultado de **20/20 pruebas aprobadas**, cubriendo endpoints exitosos, validaciones con datos inválidos y recursos inexistentes. Además, se reforzó la suite de pruebas frontend hasta alcanzar **9 pruebas unitarias aprobadas con Vitest**, cumpliendo el mínimo solicitado por la rúbrica del proyecto.

Como hallazgos principales, se identificó un error temporal de conexión entre backend y PostgreSQL durante el arranque, la ausencia de datos seed en la base de datos Docker y la falta de pruebas backend detectadas por Pytest. Estos hallazgos no bloquearon la validación funcional del sistema, pero deben ser considerados como mejoras para futuras iteraciones.

En conclusión, el proyecto cuenta con evidencia suficiente de ejecución dockerizada, validación funcional de APIs, pruebas unitarias frontend y documentación QA organizada dentro de `docs/qa/`, fortaleciendo la calidad, trazabilidad y mantenibilidad del sistema.