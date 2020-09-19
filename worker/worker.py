import asyncio
import logging
from socket import socket


async def worker_job(request_line: str,
                     socket_obj: socket,
                     worker_name: str):
    logging.debug('WORKER_{worker_name}: spawned'.format(worker_name=worker_name))

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
    logging.debug('WORKER_{worker_name}: drained data'.format(worker_name=worker_name))

    await asyncio.sleep(1)
    writer.close()
    logging.debug('WORKER_{worker_name}: closed slave writer'.format(worker_name=worker_name))

    # socket_obj.close()

    logging.debug('WORKER_{worker_name}: done'.format(worker_name=worker_name))
