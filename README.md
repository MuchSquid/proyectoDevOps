# Biblioteca Reservas - Monorepo

Sistema de gestión de reservas de biblioteca con arquitectura de monorepo, automatización y despliegue con Docker.

## Estructura del Proyecto

```plaintext
biblioteca-reservas
├── /frontend               # React + Vite
├── /backend                # Python (FastAPI)
├── /tests                  # Pruebas Unitarias
│   ├── /frontend_tests     # Vitest
│   └── /backend_tests      # Pytest
├── scripts/
│   └── automatizacion.sh   # Script de automatización
├── docker-compose.yml      # Orquestación de servicios
└── README.md               # Documentación
```

## Prerrequisitos

- Docker y Docker Compose
- Node.js (opcional para ejecución local sin Docker)
- Python 3.11 (opcional para ejecución local sin Docker)

## Comandos de Ejecución

El proyecto incluye un script de automatización en la raíz:

```bash
# Dar permisos de ejecución (si no los tiene)
chmod +x scripts/automatizacion.sh

# Ejecutar el menú interactivo
./scripts/automatizacion.sh

# O usar argumentos directos:
./scripts/automatizacion.sh --test   # Ejecutar pruebas
./scripts/automatizacion.sh --run    # Lanzar con Docker Compose
```

## Estrategia de Git

- **Metodología**: GitFlow (main, develop, feature/*, fix/*).
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).

## Tecnologías Utilizadas

- **Frontend**: React, Vite, Vitest.
- **Backend**: FastAPI, Pytest, SQLAlchemy.
- **Base de Datos**: PostgreSQL 16.3.
- **Contenedores**: Docker, Docker Compose.
# proyectoDevOps
