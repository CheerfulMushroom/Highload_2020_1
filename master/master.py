import asyncio
import multiprocessing as mp

from asyncio.streams import StreamReader, StreamWriter
from worker.worker import Worker
import socket


class Master:
    def __init__(self, address, port):
        self._address = address
        self._port = port
        self._request_queue = mp.Queue()

    def start_server(self):
        loop = asyncio.get_event_loop()
        server_coroutine = asyncio.start_server(self._master_job, self._address, self._port)
        server = loop.run_until_complete(server_coroutine)

        for i in range(1):
            p = mp.Process(target=Worker(self._request_queue).start)
            p.start()

        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    async def _master_job(self, reader: StreamReader, writer: StreamWriter):
        request_line_encoded = await reader.readline()
        request_line = request_line_encoded.decode()

        socket_obj = writer.get_extra_info('socket')

        self._request_queue.put((request_line, socket_obj))

        await asyncio.sleep(1)
        writer.close()
        print('Closed master writer')
