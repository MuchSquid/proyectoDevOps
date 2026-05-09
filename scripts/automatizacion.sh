#!/bin/bash

# Script de Automatización para Biblioteca Uteblo 📚
# Este script facilita las tareas comunes de desarrollo y despliegue.

# Obtener el directorio raíz del proyecto
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

function show_menu() {
    echo "======================================"
    echo "   MENU DE AUTOMATIZACION - UTEBLO"
    echo "======================================"
    echo "1. Actualizar Repositorio (git pull)"
    echo "2. Ejecutar Pruebas Unitarias (Backend & Frontend)"
    echo "3. Ejecutar Smoke Test (API en ejecución)"
    echo "4. Levantar Entorno con Docker (Full Stack)"
    echo "5. Detener y Limpiar Docker"
    echo "6. Salir"
    echo "======================================"
}

function update_repo() {
    echo "🔄 Actualizando repositorio..."
    git pull
}

function run_tests() {
    echo "🧪 Ejecutando pruebas del Backend (Pytest)..."
    export PYTHONPATH=$PYTHONPATH:.
    pytest tests/backend_tests
    
    echo "🧪 Ejecutando pruebas del Frontend (Vitest)..."
    cd frontend && npm run test -- --run && cd ..
}

function run_smoke_test() {
    echo "🔥 Ejecutando API Smoke Test..."
    python3 docs/qa/api_smoke_test.py
}

function run_docker() {
    echo "🐳 Levantando contenedores con Docker Compose..."
    docker-compose up --build -d
    echo "✅ Sistema levantado. Backend en :8000, Frontend en :5173"
}

function stop_docker() {
    echo "🛑 Deteniendo contenedores..."
    docker-compose down
}

# Lógica principal
if [ $# -eq 0 ]; then
    show_menu
    read -p "Seleccione una opción: " choice
else
    choice=$1
fi

case $choice in
    1) update_repo ;;
    2) run_tests ;;
    3) run_smoke_test ;;
    4) run_docker ;;
    5) stop_docker ;;
    6) exit 0 ;;
    *) echo "❌ Opción no válida." ;;
esac
