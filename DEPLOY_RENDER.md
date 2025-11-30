# 🚀 Guía de Despliegue en Render

## Procesador de Planillas Excel - Despliegue en Producción

Esta guía te ayudará a desplegar tu aplicación de procesamiento de planillas Excel en Render, una plataforma de hosting moderna y confiable.

---

## 📋 Prerequisitos

1. **Cuenta en Render**: Crear cuenta gratuita en [render.com](https://render.com)
2. **Repositorio Git**: Tu código debe estar en GitHub, GitLab o Bitbucket
3. **Archivos preparados**: ✅ Ya están listos en tu proyecto

---

## 🗂️ Archivos de Configuración Creados

### ✅ Archivos Listos para Despliegue:

- **`render.yaml`** - Configuración específica de Render
- **`requirements.txt`** - Dependencias optimizadas para producción
- **`start.sh`** - Script de inicialización
- **`.gitignore`** - Archivos a ignorar en Git
- **`app.py`** - Actualizado para producción con variables de entorno

---

## 🚀 Pasos de Despliegue

### 1. **Preparar Repositorio Git**

```bash
# Inicializar Git (si no existe)
git init

# Agregar archivos
git add .

# Hacer commit
git commit -m "Preparado para despliegue en Render"

# Conectar con tu repositorio remoto
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git

# Subir código
git push -u origin main
```

### 2. **Configurar en Render**

#### A. Crear Nuevo Web Service

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio Git

#### B. Configuración del Servicio

- **Name**: `procesador-planillas-excel`
- **Region**: `Oregon (US West)`
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

#### C. Variables de Entorno

En la sección **Environment Variables**, agregar:

| Variable | Valor |
|----------|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | `tu-clave-super-secreta-aqui-2024` |
| `PYTHONPATH` | `/opt/render/project/src` |

### 3. **Plan de Servicio**

- **Free Plan**: Perfecto para empezar
  - 512 MB RAM
  - Se duerme después de 15 min de inactividad
  - 750 horas gratis al mes

- **Starter Plan**: Para uso intensivo ($7/mes)
  - 512 MB RAM
  - Sin suspensión
  - SSL automático

---

## 🛠️ Configuración Avanzada (Opcional)

### A. Usar render.yaml (Automático)

Si tienes el archivo `render.yaml` en la raíz, Render lo detectará automáticamente.

### B. Script de Inicialización Personalizado

Si prefieres usar `start.sh`:
```bash
# En Start Command, usar:
bash start.sh
```

### C. Variables de Entorno con .env

Para desarrollo local, crear `.env`:
```env
SECRET_KEY=tu-clave-secreta-desarrollo
FLASK_ENV=development
```

---

## 🔧 Verificación del Despliegue

### 1. **URLs Importantes**

Una vez desplegado, tendrás:
- **App URL**: `https://tu-app-name.onrender.com`
- **Health Check**: `https://tu-app-name.onrender.com/status`

### 2. **Pruebas Post-Despliegue**

✅ **Verificar que funciona**:
1. Acceder a la URL principal
2. Subir un archivo Excel de prueba
3. Procesar y descargar resultado
4. Verificar endpoint de estado

### 3. **Monitoreo de Logs**

En Render Dashboard → Tu servicio → **Logs**:
```
🌐 Iniciando Procesador de Planillas Excel...
📁 Directorio de trabajo: /opt/render/project/src
📥 Directorio de entrada: input
📤 Directorio de salida: output
🚀 Servidor Flask iniciado en 0.0.0.0:10000
🔧 Entorno: Producción
```

---

## ⚡ Optimizaciones de Rendimiento

### 1. **Configuración Gunicorn**

El archivo usa configuración optimizada:
```bash
gunicorn --bind 0.0.0.0:$PORT \
         --workers 4 \
         --timeout 120 \
         --keep-alive 2 \
         --max-requests 1000 \
         app:app
```

### 2. **Gestión de Memoria**

- Workers optimizados para el plan Free
- Timeout de 120s para procesos largos
- Limpieza automática de archivos temporales

### 3. **Caching y CDN** (Plan Paid)

Para mejor rendimiento:
- Habilitar Redis para caché
- CDN automático para archivos estáticos
- Health checks avanzados

---

## 🚨 Solución de Problemas

### Error: "Application Failed to Start"

**Verificar**:
- `requirements.txt` está completo
- Variables de entorno configuradas
- Puerto configurado correctamente (`$PORT`)

### Error: "Module Not Found"

**Solución**:
```bash
# Asegurar que todas las dependencias están en requirements.txt
pip freeze > requirements.txt
```

### Error: "Permission Denied"

**Verificar**:
- Directorios `input/` y `output/` existen
- Script `start.sh` tiene permisos de ejecución

### App Se Duerme (Plan Free)

**Comportamiento Normal**:
- Se suspende tras 15 min sin actividad
- Se reactiva automáticamente en ~30 segundos
- Actualiza a plan pagado para evitarlo

---

## 🎯 URL Final del Proyecto

Una vez desplegado, tu aplicación estará disponible en:
```
https://procesador-planillas-excel.onrender.com
```

### 🔗 Endpoints Disponibles:

- **Inicio**: `/`
- **Subir archivos**: `/upload`
- **Procesar**: `/process`
- **Estado**: `/status`
- **Descargas**: `/download/<filename>`

---

## 🎉 ¡Felicidades!

Tu **Procesador de Planillas Excel** ahora está en producción:

✅ **Accesible desde cualquier lugar del mundo**  
✅ **Interfaz web profesional**  
✅ **SSL automático (HTTPS)**  
✅ **Escalable y confiable**  
✅ **Monitoreo incluido**

---

## 📞 Soporte

- **Documentación Render**: [docs.render.com](https://docs.render.com)
- **Community**: [community.render.com](https://community.render.com)
- **Status Page**: [status.render.com](https://status.render.com)

---

## 🔄 Actualizaciones

Para nuevas versiones:

```bash
# Hacer cambios en el código
git add .
git commit -m "Nueva funcionalidad agregada"
git push origin main

# Render auto-desplegará automáticamente
```

---

**🎊 ¡Tu aplicación ya está lista para el mundo!** 🎊