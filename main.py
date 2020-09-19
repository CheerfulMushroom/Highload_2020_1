import logging

import coloredlogs

from config import Config
from master.master import Master

if __name__ == "__main__":
    coloredlogs.install(
        level=Config.log_level,
        fmt=Config.log_format,
        datefmt=Config.log_date_format,
    )

    logging.info('Starting webserver')
    master = Master('127.0.0.1', 8888)
    master.start_server()
