import asyncio
import logging
import socket
import multiprocessing as mp
from asyncio.streams import StreamReader, StreamWriter

from config import Config
from worker.worker_spawner import WorkerSpawner


class Master:
    def __init__(self, address, port):
        self._address = address
        self._port = port
        self._request_queue = mp.Queue()

    def start_server(self):
        loop = asyncio.get_event_loop()
        server_coroutine = asyncio.start_server(self._master_job,
                                                host=self._address,
                                                port=self._port,
                                                backlog=Config.max_connections)
        server = loop.run_until_complete(server_coroutine)
        logging.info('MASTER: serving on {}'.format(server.sockets[0].getsockname()))

        for i in range(Config.workers_process_amount):
            p = mp.Process(target=WorkerSpawner(self._request_queue, i).start)
            p.start()
            logging.info('MASTER: Started worker spawner {}'.format(i))

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logging.warning('MASTER: stopped by user')

        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
        logging.info('MASTER: stopped')

    async def _master_job(self, reader: StreamReader, writer: StreamWriter):
        request_line_encoded = await reader.readline()
        request_line = request_line_encoded.decode()

        # TODO: debug
        socket_obj: socket.socket
        socket_obj = writer.get_extra_info('socket')

        # TODO: debug
        print('send masterW message')
        writer.write(b'masterW ')
        await writer.drain()
        print('send masterS message')
        socket_obj.send(b'masterS ')

        socket_fd = socket_obj.fileno()

        socket_obj_new = socket.socket(fileno=socket_fd)
        print('send masterSNew message')
        socket_obj_new.send(b'masterSNew ')

        logging.warning('MASTER: socket_fd {}'.format(socket_fd))

        self._request_queue.put((request_line, socket_fd))