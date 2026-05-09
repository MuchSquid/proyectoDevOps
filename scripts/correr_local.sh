#!/bin/bash
# Automatización para Correr el Proyecto en Modo Local

# Obtener directorio raíz
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "======================================"
echo "   DESPLIEGUE LOCAL CON DOCKER"
echo "======================================"

# Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no parece estar en ejecución. Por favor, inícialo."
    exit 1
fi

echo "📦 Construyendo y levantando servicios..."
docker-compose up --build -d

echo "======================================"
echo "   SISTEMA LISTO"
echo "======================================"
echo "🌐 Frontend: http://localhost:5173"
echo "⚙️  Backend:  http://localhost:8000"
echo "📊 Database: Puerto 5432"
echo "======================================"
echo "Para ver los logs usa: docker-compose logs -f"
echo "Para detenerlo usa: docker-compose down"
