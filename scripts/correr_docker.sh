#!/bin/bash
# Automatización para Correr el Proyecto con Docker

# Obtener directorio raíz
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "======================================"
echo "   DESPLIEGUE CON DOCKER"
echo "======================================"

if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no parece estar en ejecución."
    exit 1
fi

echo "📦 Construyendo y levantando contenedores..."
docker-compose up --build -d

echo "======================================"
echo "   SISTEMA LISTO EN DOCKER"
echo "======================================"
echo "🌐 Frontend: http://localhost:5173"
echo "⚙️  Backend:  http://localhost:8000"
echo "======================================"
