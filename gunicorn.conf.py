# Configuración de Gunicorn para Render
# gunicorn.conf.py

import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = 4
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Log to stdout so logs will be visible in Render
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'procesador_planillas_excel'

# Server mechanics
preload_app = True
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8192