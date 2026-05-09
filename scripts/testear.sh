#!/bin/bash
# Automatización de Ejecución de Tests

# Obtener directorio raíz
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "======================================"
echo "   EJECUCIÓN DE TESTS (CI/CD)"
echo "======================================"

# 1. Tests del Backend
echo "🐍 [BACKEND] Ejecutando Pytest..."
export PYTHONPATH=$PYTHONPATH:.
pytest tests/backend_tests
BACKEND_EXIT=$?

# 2. Tests del Frontend
echo "⚛️ [FRONTEND] Ejecutando Vitest..."
cd frontend
npm run test -- --run
FRONTEND_EXIT=$?
cd ..

echo "======================================"
echo "   RESUMEN DE RESULTADOS"
echo "======================================"
[ $BACKEND_EXIT -eq 0 ] && echo "✅ Backend: PASSED" || echo "❌ Backend: FAILED"
[ $FRONTEND_EXIT -eq 0 ] && echo "✅ Frontend: PASSED" || echo "❌ Frontend: FAILED"
echo "======================================"

if [ $BACKEND_EXIT -ne 0 ] || [ $FRONTEND_EXIT -ne 0 ]; then
    exit 1
fi
