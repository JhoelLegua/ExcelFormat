# Procesador de Planillas Excel - Sistema Web Flask

## 🚀 Sistema Completo Implementado

Este sistema convierte tu script de Python en una aplicación web profesional que permite a los usuarios:

- **Subir múltiples archivos Excel** mediante interfaz web moderna
- **Procesar automáticamente** usando tu lógica existente
- **Descargar resultados** con formato profesional
- **Interfaz intuitiva** con feedback visual en tiempo real

## 📁 Estructura del Proyecto

```
PROGRAMA MAPEO/
├── app.py                  # Aplicación Flask principal ✅
├── script.py              # Tu script original (sin cambios) ✅
├── templates/             # Templates HTML ✅
│   ├── index.html         # Interfaz principal ✅
│   └── result.html        # Página de resultados ✅
├── static/                # Archivos estáticos ✅
│   └── css/
│       └── style.css      # Estilos personalizados ✅
├── input/                 # Archivos de entrada ✅
├── output/                # Archivos procesados ✅
├── requirements.txt       # Dependencias ✅
└── README.md             # Este archivo
```

## 🛠️ Instalación y Configuración

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
python app.py
```

### 3. Acceder a la Aplicación

Abrir navegador en: **http://localhost:5000**

## ✨ Características Principales

### 🎨 Interfaz de Usuario Moderna
- **Diseño responsive** con Bootstrap 5
- **Drag & drop visual** para archivos
- **Feedback en tiempo real** durante procesamiento
- **Animaciones suaves** y transiciones elegantes

### 🔒 Validación y Seguridad
- **Validación de tipos de archivo** (.xls, .xlsx únicamente)
- **Límite de tamaño** (50MB máximo)
- **Sanitización de nombres** de archivos
- **Manejo robusto de errores**

### ⚡ Funcionalidades Avanzadas
- **Nombres personalizados** para archivos de salida
- **Vista previa** de información de archivos
- **Log detallado** del procesamiento
- **Limpieza automática** de archivos temporales
- **API endpoints** para integración

### 📊 Procesamiento Inteligente
- **Conserva toda la lógica** del script original
- **Formateo profesional** automático:
  - 🟢 Headers en verde, negrita, mayúsculas
  - 🟡 Campos especiales en amarillo
  - 🟠 Filas de totales en naranja
  - 📅 Fechas normalizadas (DD/MM/YYYY)

## 🎯 Flujo de Usuario

1. **📥 Subir Archivos**: Seleccionar múltiples archivos Excel
2. **✏️ Personalizar**: Opcional - definir nombre del archivo final  
3. **⚙️ Procesar**: Un clic para unificar y formatear
4. **📤 Descargar**: Obtener planilla final profesional

## 🔧 Rutas Disponibles

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Página principal |
| `/upload` | POST | Subir archivos |
| `/process` | POST | Procesar archivos |
| `/download/<filename>` | GET | Descargar archivo |
| `/clear` | GET | Limpiar archivos |
| `/status` | GET | Estado del sistema (API) |
| `/preview/<filename>` | GET | Vista previa (API) |

## 🎨 Personalización

### Colores y Estilos
Los colores se pueden personalizar en `static/css/style.css`:
- Variables CSS en `:root`
- Gradientes personalizables
- Animaciones configurables

### Configuración de la App
En `app.py` puedes modificar:
- Tamaño máximo de archivos
- Extensiones permitidas
- Directorios de trabajo
- Clave secreta

## 🚀 Ventajas sobre Script Original

| Aspecto | Script Original | Sistema Web |
|---------|----------------|-------------|
| **Interfaz** | Línea de comandos | Web moderna y intuitiva |
| **Usabilidad** | Técnico | Cualquier usuario |
| **Feedback** | Solo texto | Visual y en tiempo real |
| **Gestión archivos** | Manual | Automática con validación |
| **Accesibilidad** | Local únicamente | Acceso remoto posible |
| **Escalabilidad** | Individual | Multi-usuario potencial |

## 🔄 Mantenimiento

### Limpiar archivos temporales:
- Automático después de cada uso
- Manual desde interfaz web
- Programático via endpoint `/clear`

### Logs y monitoreo:
- Console output capturado
- Errores manejados graciosamente
- Status endpoint para health checks

## 🎉 ¡Listo para Usar!

El sistema está **100% funcional** y listo para producción. Mantiene toda la robustez de tu script original mientras proporciona una experiencia de usuario moderna y profesional.

### Para iniciar:
```bash
python app.py
```

¡Disfruta de tu nuevo sistema web de procesamiento de planillas Excel! 🎊