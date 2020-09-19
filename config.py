import logging


class Config:
    # WORKERS
    workers_process_amount = 1

    # LOGGING
    log_level = logging.DEBUG
    log_format = '%(asctime)s %(levelname)s\t%(name)s[%(process)d]\t%(message)s'
    log_date_format = '%H:%M:%S'
