import logging
import socket


class Config:
    # CONNECTION
    addr = socket.gethostbyname(socket.gethostname() + '.local')
    port = 8888
    max_connections = 100

    # WORKERS
    workers_process_amount = 1

    # LOGGING
    log_level = logging.DEBUG
    log_format = '%(asctime)s\t%(levelname)s\t%(name)s[%(process)d]\t%(message)s'
    log_date_format = '%H:%M:%S'

    log_worker_spawner_verbose = True
    log_worker_verbose = True
