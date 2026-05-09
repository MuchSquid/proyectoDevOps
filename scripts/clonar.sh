#!/bin/bash
# Automatización de Clonación/Actualización del Proyecto

REPO_URL="https://github.com/MuchSquid/proyectoDevOps.git"
DEST_DIR="proyecto_biblioteca"

echo "======================================"
echo "   CLONACIÓN / ACTUALIZACIÓN"
echo "======================================"

if [ -d ".git" ]; then
    echo "✅ Ya estás dentro de un repositorio Git. Actualizando..."
    git pull origin main
else
    echo "🚀 Clonando repositorio en: $DEST_DIR"
    git clone $REPO_URL $DEST_DIR
fi

echo "======================================"
echo "   PROCESO FINALIZADO"
echo "======================================"
