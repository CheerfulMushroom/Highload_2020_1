import asyncio
import logging
from multiprocessing import Queue

from .worker import worker_job


class WorkerSpawner:
    def __init__(self, request_queue: Queue, process_id: int):
        self._request_queue = request_queue
        self._spawner_id = process_id
        self._loop = asyncio.get_event_loop()

    def start(self):
        logging.info('SPAWNER_{spawner_id}: started'.format(spawner_id=self._spawner_id))
        try:
            self._loop.run_until_complete(self._worker_spawner())
        except KeyboardInterrupt:
            logging.warning('SPAWNER_{spawner_id}: stopped by user'.format(spawner_id=self._spawner_id))

    async def _worker_spawner(self):
        worker_num = 0

        while True:
            logging.debug('SPAWNER_{spawner_id}: awaiting data'.format(spawner_id=self._spawner_id))
            request_line, socket_obj = await self._loop.run_in_executor(None, self._request_queue.get)

            worker_name = '{spawner_id}_{worker_id}'.format(spawner_id=self._spawner_id, worker_id=worker_num)
            logging.debug('SPAWNER_{spawner_id}: spawning worker {worker_name}'.format(spawner_id=self._spawner_id,
                                                                                       worker_name=worker_name))

            self._loop.create_task(worker_job(request_line, socket_obj, worker_name))
            worker_num += 1
