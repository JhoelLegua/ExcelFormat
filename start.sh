#!/bin/bash

# Script de inicialización para Render
echo "🚀 Iniciando despliegue en Render..."

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p input
mkdir -p output

# Establecer permisos
echo "🔐 Configurando permisos..."
chmod 755 input
chmod 755 output

# Verificar que el script principal existe
if [ ! -f "script.py" ]; then
    echo "❌ Error: script.py no encontrado"
    exit 1
fi

if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py no encontrado"
    exit 1
fi

# Configurar variables de entorno para producción
export FLASK_ENV=production
export PYTHONPATH=/opt/render/project/src

echo "✅ Inicialización completada"
echo "🌐 Iniciando aplicación con Gunicorn..."

# Iniciar la aplicación con Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100 app:app