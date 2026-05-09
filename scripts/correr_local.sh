#!/bin/bash
# Automatización para Correr el Proyecto en Modo Local (Modo Desarrollo)

# Obtener directorio raíz
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "======================================"
2: echo "   EJECUCIÓN LOCAL (SIN DOCKER)"
3: echo "======================================"

# Función para limpiar procesos al salir
cleanup() {
    echo -e "\n🛑 Deteniendo servidores..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# 1. Iniciar Backend
echo "🐍 Iniciando Backend (FastAPI)..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
pip install -r requirements.txt > /dev/null 2>&1
export PYTHONPATH=$PYTHONPATH:.
export DATABASE_URL="postgresql://postgres:235689@localhost:5432/biblioteca"
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# 2. Iniciar Frontend
echo "⚛️ Iniciando Frontend (Vite)..."
cd frontend
npm install > /dev/null 2>&1
npm run dev &
FRONTEND_PID=$!
cd ..

echo "======================================"
echo "   SISTEMA EN EJECUCIÓN"
echo "======================================"
echo "🌐 Frontend: http://localhost:5173"
echo "⚙️  Backend:  http://localhost:8000"
echo "👉 Presiona Ctrl+C para detener ambos"
echo "======================================"

# Mantener el script vivo para que el trap funcione
wait
