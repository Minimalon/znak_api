from multiprocessing import cpu_count
from src.config import dir_path

bind = "10.8.16.18:8180"

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
logs_dir = dir_path / 'logs'
accesslog = logs_dir / 'access_log.log'
errorlog = logs_dir / 'errorlog.log'
