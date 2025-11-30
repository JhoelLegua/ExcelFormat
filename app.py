from flask import Flask, request, render_template, send_file, flash, redirect, url_for, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from script import procesar_archivos_en_memoria

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
# Usar variable de entorno para la clave secreta en producción
app.secret_key = os.environ.get('SECRET_KEY', 'procesador_planillas_excel_2024_render_secure')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB máximo

# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')



@app.route('/process', methods=['POST'])
def process_files():
    """Procesar los archivos usando procesamiento en memoria"""
    try:
        # Obtener archivos subidos directamente del formulario
        uploaded_files = request.files.getlist('files')
        custom_name = request.form.get('custom_name', '').strip()
        
        # Filtrar archivos válidos
        archivos_validos = [f for f in uploaded_files if f.filename != '' and 
                          allowed_file(f.filename)]
        
        if not archivos_validos:
            flash('❌ No se encontraron archivos Excel válidos para procesar', 'error')
            return redirect(url_for('index'))
        
        # Información de inicio
        start_time = datetime.now()
        print(f"🚀 Iniciando procesamiento en memoria de {len(archivos_validos)} archivos...")
        
        # Procesar archivos en memoria usando la función optimizada
        resultado_stream = procesar_archivos_en_memoria(archivos_validos)
        
        if resultado_stream is None:
            flash('❌ El procesamiento no generó archivo de salida', 'error')
            return redirect(url_for('index'))
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Generar nombre de archivo
        if custom_name:
            safe_name = secure_filename(custom_name)
            if not safe_name.lower().endswith('.xlsx'):
                safe_name += '.xlsx'
            final_filename = safe_name
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_filename = f'Planilla_Unificada_{timestamp}.xlsx'
        
        print(f"✅ Procesamiento completado en {processing_time:.1f} segundos: {final_filename}")
        
        # Enviar archivo directamente desde memoria
        return send_file(
            resultado_stream,
            as_attachment=True,
            download_name=final_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {str(e)}")
        flash(f'❌ Error durante el procesamiento: {str(e)}', 'error')
        return redirect(url_for('index'))



@app.route('/status')
def status():
    """API endpoint para verificar el estado del sistema"""
    try:
        return jsonify({
            'status': 'ok',
            'message': 'Procesador de Planillas Excel funcionando correctamente',
            'timestamp': datetime.now().isoformat(),
            'memory_processing': True
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
    print(f"🚀 Servidor Flask iniciado en {host}:{port}")
    print(f"🔧 Entorno: {'Producción' if is_production else 'Desarrollo'}")
    print("💾 Procesamiento en memoria habilitado")
    
    # Configuración según el entorno
    if is_production:
        # Configuración para Render (producción)
        app.run(host=host, port=port, debug=False)
    else:
        # Configuración para desarrollo local
        app.run(host=host, port=port, debug=True)
    
    