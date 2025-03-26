# Gunicorn configuration file
import multiprocessing

# Configurações básicas
bind = "0.0.0.0:8000"
workers = 2  # Reduzindo o número de workers
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Aumentando o timeout
keepalive = 2

# Configurações de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Configurações de processo
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Configurações de performance
worker_tmp_dir = "/dev/shm"
max_requests = 1000
max_requests_jitter = 50
timeout = 120
graceful_timeout = 120
keep_alive = 5 