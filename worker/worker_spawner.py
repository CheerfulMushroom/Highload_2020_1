import asyncio
import logging
from socket import socket

from config import Config
from .worker import worker_job


class WorkerSpawner:
    def __init__(self, server_socket: socket, spawner_id: int):
        self._server_socket = server_socket
        self._spawner_id = spawner_id
        self._loop: asyncio.AbstractEventLoop = None

    def start(self):
        self._loop = asyncio.get_event_loop()

        logging.info('SPAWNER_{}: started'.format(self._spawner_id))

        try:
            self._loop.run_until_complete(self._worker_spawner())
        except KeyboardInterrupt:
            logging.warning('SPAWNER_{}: stopped by user'.format(self._spawner_id))

    async def _worker_spawner(self):
        worker_num = 0

        while True:
            if Config.log_worker_spawner_verbose:
                logging.debug('SPAWNER_{spawner_id}: awaiting data'.format(spawner_id=self._spawner_id))

            client_socket, _ = await self._loop.sock_accept(self._server_socket)

            worker_name = '{spawner_id}_{worker_id}'.format(spawner_id=self._spawner_id, worker_id=worker_num)
            if Config.log_worker_spawner_verbose:
                logging.debug('SPAWNER_{spawner_id}: spawning worker {worker_name}'.format(spawner_id=self._spawner_id,
                                                                                           worker_name=worker_name))

            self._loop.create_task(worker_job(client_socket, worker_name))
            worker_num += 1
