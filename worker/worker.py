import asyncio
import logging
from socket import socket
from config import Config


async def worker_job(request_line: str,
                     socket_obj: socket,
                     worker_name: str):
    if Config.log_worker_verbose:
        logging.debug('WORKER_{worker_name}: spawned'.format(worker_name=worker_name))

    logging.warning('WORKER_{}: socket_fd {}'.format(worker_name, socket_obj.fileno()))
    _, writer = await asyncio.open_connection(sock=socket_obj)

    request_line_words = request_line.split(' ')
    if len(request_line_words) < 2:
        # FIXME(Alex): Error handling
        logging.error('WORKER_{worker_name}: NO ERROR HANDLING'.format(worker_name=worker_name))

    method, path = request_line_words[:2]

    # TODO(Alex): check method, check path
    logging.info('WORKER_{worker_name}: {method} {path}'.format(worker_name=worker_name, method=method, path=path))

    writer.write(request_line.encode())
    await writer.drain()
    if Config.log_worker_verbose:
        logging.debug('WORKER_{worker_name}: drained data'.format(worker_name=worker_name))

    await asyncio.sleep(0.01)
    writer.close()
    if Config.log_worker_verbose:
        logging.debug('WORKER_{worker_name}: closed slave writer'.format(worker_name=worker_name))

    # socket_obj.close()

    if Config.log_worker_verbose:
        logging.debug('WORKER_{worker_name}: done'.format(worker_name=worker_name))
