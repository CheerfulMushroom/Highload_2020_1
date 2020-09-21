import logging
import socket


class Config:
    base_dir = '/home/shroomoffun/Programs/main_program/semestr_3/highload/Highload_2020_1'
    index_filename = '/index.html'

    # CONNECTION
    addr = socket.gethostbyname(socket.gethostname() + '.local')
    port = 8888
    max_connections = 100
    bytes_per_recv = 128
    bytes_per_send = 1024

    # WORKERS
    workers_process_amount = 8

    # LOGGING
    log_level = logging.DEBUG
    log_format = '%(asctime)s\t%(levelname)s\t%(name)s[%(process)d]\t%(message)s'
    log_date_format = '%H:%M:%S'

    log_worker_spawner_verbose = True
    log_worker_verbose = True
