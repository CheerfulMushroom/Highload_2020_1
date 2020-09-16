import asyncio
import socket

from asyncio.streams import StreamWriter
from multiprocessing import Queue


class Worker:
    def __init__(self, request_queue: Queue):
        self._request_queue = request_queue

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._worker_job())
        loop.run_forever()

    async def _worker_job(self):
        while True:
            request_line: str
            writer: StreamWriter

            request_line: str
            socket_obj: socket.socket
            request_line, socket_obj = self._request_queue.get()

            _, writer = await asyncio.open_connection(sock=socket_obj)

            request_line_words = request_line.split(' ')
            if len(request_line_words) < 2:
                # FIXME(Alex): Error handling
                pass

            method, path = request_line_words[:2]

            # TODO(Alex): check method, check path
            addr = writer.get_extra_info('peername')
            print("{addr}:\t{method} {path}".format(addr=addr, method=method, path=path))

            writer.write(request_line.encode())
            await writer.drain()

            await asyncio.sleep(3)
            writer.close()
            print('Closed slave writer')

            # socket_obj.close()

            print("=========================================")
