import logging
import pathlib


class Config:
    base_dir = ''
    index_filename = 'index.html'

    # CONNECTION
    addr = 'localhost'
    port = 3000
    max_connections = 100
    bytes_per_recv = 1024
    bytes_per_send = 1024

    # WORKERS
    workers_process_amount = 4

    # LOGGING
    log_level = logging.DEBUG
    log_format = '%(asctime)s %(levelname)s\t%(name)s[%(process)d]\t\t%(message)s'
    log_date_format = '%H:%M:%S'

    log_worker_spawner_verbose = False
    log_worker_verbose = False
