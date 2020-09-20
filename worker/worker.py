import asyncio
import logging
from socket import socket
from config import Config


async def worker_job(client_socket: socket, worker_name: str):
    if Config.log_worker_verbose:
        logging.debug('WORKER_{worker_name}: spawned'.format(worker_name=worker_name))

    reader, writer = await asyncio.open_connection(sock=client_socket)

    request_line = (await reader.readline()).decode()
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

    writer.close()
    if Config.log_worker_verbose:
        logging.debug('WORKER_{worker_name}: closed slave writer'.format(worker_name=worker_name))

    if Config.log_worker_verbose:
        logging.debug('WORKER_{worker_name}: done'.format(worker_name=worker_name))
