import asyncio
import logging
from socket import socket
from utils.request import Request
from utils.response import Response
from config import Config
import os.path


async def worker_job(client_socket: socket, worker_name: str):
    if Config.log_worker_verbose:
        logging.debug(f'WORKER_{worker_name}: spawned')

    # GET REQUEST

    loop = asyncio.get_event_loop()
    request_raw = ""
    while True:
        request_part = (await loop.sock_recv(client_socket, Config.bytes_per_recv)).decode()
        request_raw += request_part
        if '\r\n' in request_raw:
            break

    request = Request(request_raw)

    # GET FILENAME

    filepath: str
    search_folder = request.url.endswith('/')
    if search_folder:
        filepath = Config.base_dir + request.url + Config.index_filename
    else:
        filepath = Config.base_dir + request.url
    file_exists = os.path.exists(filepath)

    # CREATE RESPONSE

    response: Response
    if request.method not in ['GET', 'HEAD']:
        response = Response(method=request.method, protocol=request.protocol, status=405)
    elif '/..' in request.url or (search_folder and not file_exists):
        response = Response(method=request.method, protocol=request.protocol, status=403)
    elif (not file_exists) or (not request.is_valid):
        response = Response(method=request.method, protocol=request.protocol, status=404)
    else:
        response = Response(method=request.method, protocol=request.protocol, status=200, filepath=filepath)

    logging.info(f'WORKER_{worker_name}: {response.status} {request.method} {request.url}')

    # SEND RESPONSE

    await response.send(client_socket)

    # END WORKER

    client_socket.close()

    if Config.log_worker_verbose:
        logging.debug(f'WORKER_{worker_name}: closed client socket')

    if Config.log_worker_verbose:
        logging.debug(f'WORKER_{worker_name}: done')
