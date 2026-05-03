#!/bin/bash

# Script de Automatización para Biblioteca Reservas

REPO_URL="https://github.com/tu-usuario/biblioteca-reservas.git"

function show_menu() {
    echo "======================================"
    echo "   MENU DE AUTOMATIZACION"
    echo "======================================"
    echo "1. Clonar/Actualizar Repositorio"
    echo "2. Ejecutar Pruebas (Frontend & Backend)"
    echo "3. Ejecutar Localmente (Docker)"
    echo "4. Salir"
    echo "======================================"
}

function clone_update() {
    if [ -d ".git" ]; then
        echo "Actualizando repositorio..."
        git pull origin develop
    else
        echo "Clonando repositorio..."
        git clone $REPO_URL .
    fi
}

function run_tests() {
    echo "Ejecutando pruebas del Backend..."
    # Añadimos el directorio raíz al PYTHONPATH para que encuentre el módulo backend
    export PYTHONPATH=$PYTHONPATH:.
    pytest tests/backend_tests
    
    echo "Ejecutando pruebas del Frontend..."
    cd frontend && npm run test -- --run && cd ..
}

function run_local() {
    echo "Lanzando Docker Compose..."
    docker-compose up --build
}

if [ $# -eq 0 ]; then
    show_menu
    read -p "Seleccione una opción: " choice
else
    choice=$1
fi

case $choice in
    1|--clone) clone_update ;;
    2|--test) run_tests ;;
    3|--run) run_local ;;
    4) exit 0 ;;
    *) echo "Opción no válida." ;;
esac
