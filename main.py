import asyncio

from master.master import master_job


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server_coroutine = asyncio.start_server(master_job, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(server_coroutine)

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
