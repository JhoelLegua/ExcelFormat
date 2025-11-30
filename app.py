from flask import Flask, request, render_template, send_file, flash, redirect, url_for, jsonify
import os
import shutil
from datetime import datetime
import subprocess
import sys
from werkzeug.utils import secure_filename
import zipfile
import glob
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
# Usar variable de entorno para la clave secreta en producción
app.secret_key = os.environ.get('SECRET_KEY', 'procesador_planillas_excel_2024_render_secure')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB máximo

# Configuración de directorios
UPLOAD_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# Crear directorios si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def limpiar_directorio(directorio):
    """Limpia todos los archivos de un directorio"""
    for filename in os.listdir(directorio):
        file_path = os.path.join(directorio, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error eliminando {file_path}: {e}")

def formatear_bytes(bytes_size):
    """Convierte bytes a formato legible"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

@app.route('/')
def index():
    """Página principal"""
    # Verificar archivos existentes en input
    existing_files = []
    if os.path.exists(UPLOAD_FOLDER):
        for file in os.listdir(UPLOAD_FOLDER):
            if file.lower().endswith(('.xls', '.xlsx')):
                file_path = os.path.join(UPLOAD_FOLDER, file)
                file_size = os.path.getsize(file_path)
                existing_files.append({
                    'name': file,
                    'size': formatear_bytes(file_size),
                    'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d/%m/%Y %H:%M')
                })
    
    return render_template('index.html', uploaded_files=existing_files)

@app.route('/upload', methods=['POST'])
def upload_files():
    """Manejar la subida de archivos"""
    try:
        # Verificar si se enviaron archivos
        if 'files' not in request.files:
            flash('No se seleccionaron archivos', 'error')
            return redirect(url_for('index'))
        
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            flash('No se seleccionaron archivos válidos', 'error')
            return redirect(url_for('index'))
        
        # Opción de limpiar directorio antes de subir
        clear_before = request.form.get('clear_before', False)
        if clear_before:
            limpiar_directorio(UPLOAD_FOLDER)
        
        # Guardar archivos subidos
        uploaded_files = []
        total_size = 0
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                # Verificar si el archivo ya existe
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(file_path) and not clear_before:
                    # Agregar timestamp para evitar conflictos
                    name, ext = os.path.splitext(filename)
                    timestamp = datetime.now().strftime('%H%M%S')
                    filename = f"{name}_{timestamp}{ext}"
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                
                file.save(file_path)
                file_size = os.path.getsize(file_path)
                total_size += file_size
                
                uploaded_files.append({
                    'name': filename,
                    'size': formatear_bytes(file_size)
                })
            else:
                flash(f'Archivo no válido: {file.filename}. Solo se permiten archivos .xls y .xlsx', 'warning')
        
        if not uploaded_files:
            flash('No se pudieron cargar archivos válidos', 'error')
            return redirect(url_for('index'))
        
        flash(f'✅ Se cargaron {len(uploaded_files)} archivos correctamente ({formatear_bytes(total_size)} total)', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'❌ Error cargando archivos: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/process', methods=['POST'])
def process_files():
    """Procesar los archivos usando el script original"""
    try:
        # Obtener nombre personalizado del archivo
        custom_name = request.form.get('custom_name', '').strip()
        
        # Verificar que hay archivos en input
        input_files = glob.glob(os.path.join(UPLOAD_FOLDER, '*.xls*'))
        
        if not input_files:
            flash('❌ No hay archivos para procesar. Por favor, carga archivos primero.', 'error')
            return redirect(url_for('index'))
        
        # Limpiar directorio de salida
        limpiar_directorio(OUTPUT_FOLDER)
        
        # Información de inicio
        start_time = datetime.now()
        flash(f'🚀 Iniciando procesamiento de {len(input_files)} archivos...', 'info')
        
        print(f"🚀 Iniciando procesamiento via Flask de {len(input_files)} archivos...")
        
        # Ejecutar el script original con codificación UTF-8
        result = subprocess.run([sys.executable, 'script.py'], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.getcwd(),
                              encoding='utf-8',
                              errors='replace',
                              env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        if result.returncode != 0:
            error_msg = result.stderr or "Error desconocido en el procesamiento"
            print(f"❌ Error en script.py: {error_msg}")
            flash(f'❌ Error procesando archivos: {error_msg}', 'error')
            return redirect(url_for('index'))
        
        # Verificar que se generó el archivo de salida
        output_file = os.path.join(OUTPUT_FOLDER, 'Planilla_Unificada_Final.xlsx')
        
        if not os.path.exists(output_file):
            flash('❌ El procesamiento no generó archivo de salida', 'error')
            return redirect(url_for('index'))
        
        # Renombrar archivo si se especificó nombre personalizado
        final_filename = 'Planilla_Unificada_Final.xlsx'
        if custom_name:
            # Sanitizar nombre personalizado
            safe_name = secure_filename(custom_name)
            if not safe_name.lower().endswith('.xlsx'):
                safe_name += '.xlsx'
            
            final_path = os.path.join(OUTPUT_FOLDER, safe_name)
            shutil.copy2(output_file, final_path)
            final_filename = safe_name
        
        # Información del procesamiento
        file_size = os.path.getsize(os.path.join(OUTPUT_FOLDER, final_filename))
        
        file_info = {
            'filename': final_filename,
            'size': file_size,
            'size_formatted': formatear_bytes(file_size),
            'processed_files': len(input_files),
            'processing_time': f"{processing_time:.2f}",
            'timestamp': end_time.strftime('%d/%m/%Y %H:%M:%S'),
            'console_output': result.stdout,
            'input_files': [os.path.basename(f) for f in input_files]
        }
        
        print(f"✅ Procesamiento completado: {final_filename}")
        flash(f'✅ ¡Procesamiento completado exitosamente en {processing_time:.1f} segundos!', 'success')
        
        # Programar limpieza de archivos de entrada después de un tiempo
        def cleanup_input_files():
            try:
                import time
                time.sleep(300)  # Esperar 5 minutos
                limpiar_directorio(UPLOAD_FOLDER)
                print("🧹 Limpieza automática de archivos de entrada completada")
            except Exception as e:
                print(f"⚠️ Error en limpieza automática de entrada: {e}")
        
        import threading
        cleanup_thread = threading.Thread(target=cleanup_input_files)
        cleanup_thread.daemon = True
        cleanup_thread.start()
        
        return render_template('result.html', file_info=file_info)
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {str(e)}")
        flash(f'❌ Error durante el procesamiento: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Descargar archivo procesado y limpiar automáticamente"""
    try:
        safe_filename = secure_filename(filename)
        file_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        
        if not os.path.exists(file_path):
            flash('❌ El archivo no existe o ha expirado', 'error')
            return redirect(url_for('index'))
        
        # Programar limpieza después de la descarga
        def cleanup_after_download():
            try:
                # Esperar un poco para asegurar que la descarga termine
                import time
                time.sleep(2)
                # Limpiar todos los archivos temporales
                limpiar_directorio(UPLOAD_FOLDER)
                limpiar_directorio(OUTPUT_FOLDER)
                print("🧹 Limpieza automática completada después de descarga")
            except Exception as e:
                print(f"⚠️ Error en limpieza automática: {e}")
        
        # Ejecutar limpieza en segundo plano
        import threading
        cleanup_thread = threading.Thread(target=cleanup_after_download)
        cleanup_thread.daemon = True
        cleanup_thread.start()
        
        return send_file(file_path, as_attachment=True, download_name=safe_filename)
        
    except Exception as e:
        flash(f'❌ Error descargando archivo: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Eliminar archivo individual cargado"""
    try:
        safe_filename = secure_filename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        
        if os.path.exists(file_path):
            os.unlink(file_path)
            flash(f'🗑️ Archivo eliminado: {safe_filename}', 'success')
        else:
            flash(f'❌ Archivo no encontrado: {safe_filename}', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'❌ Error eliminando archivo: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/preview/<filename>')
def preview_file(filename):
    """Vista previa básica del archivo Excel (solo información)"""
    try:
        safe_filename = secure_filename(filename)
        file_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        # Información básica del archivo
        file_stats = os.stat(file_path)
        info = {
            'filename': safe_filename,
            'size': formatear_bytes(file_stats.st_size),
            'created': datetime.fromtimestamp(file_stats.st_ctime).strftime('%d/%m/%Y %H:%M:%S'),
            'modified': datetime.fromtimestamp(file_stats.st_mtime).strftime('%d/%m/%Y %H:%M:%S')
        }
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear')
def clear_files():
    """Limpiar todos los archivos temporales"""
    try:
        # Contar archivos antes de limpiar
        input_count = len([f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.xls', '.xlsx'))])
        output_count = len([f for f in os.listdir(OUTPUT_FOLDER) if f.lower().endswith('.xlsx')])
        
        limpiar_directorio(UPLOAD_FOLDER)
        limpiar_directorio(OUTPUT_FOLDER)
        
        flash(f'🧹 Archivos eliminados: {input_count} de entrada, {output_count} de salida', 'info')
    except Exception as e:
        flash(f'❌ Error limpiando archivos: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/status')
def status():
    """API endpoint para verificar el estado del sistema"""
    try:
        input_files = len([f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.xls', '.xlsx'))])
        output_files = len([f for f in os.listdir(OUTPUT_FOLDER) if f.lower().endswith('.xlsx')])
        
        return jsonify({
            'status': 'ok',
            'input_files': input_files,
            'output_files': output_files,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Manejar archivos demasiado grandes"""
    flash('❌ Archivo demasiado grande. Máximo 50MB permitido.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    """Página no encontrada"""
    flash('❌ Página no encontrada', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    """Error interno del servidor"""
    flash('❌ Error interno del servidor. Intenta nuevamente.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Configuración para producción o desarrollo
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0' if is_production else '127.0.0.1'
    
    print("🌐 Iniciando Procesador de Planillas Excel...")
    print(f"📁 Directorio de trabajo: {os.getcwd()}")
    print(f"📥 Directorio de entrada: {UPLOAD_FOLDER}")
    print(f"📤 Directorio de salida: {OUTPUT_FOLDER}")
    print(f"🚀 Servidor Flask iniciado en {host}:{port}")
    print(f"🔧 Entorno: {'Producción' if is_production else 'Desarrollo'}")
    
    # Configuración según el entorno
    if is_production:
        # Configuración para Render (producción)
        app.run(host=host, port=port, debug=False)
    else:
        # Configuración para desarrollo local
        app.run(host=host, port=port, debug=True)
    
    