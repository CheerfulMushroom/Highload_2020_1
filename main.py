import asyncio

from master.master import Master


if __name__ == "__main__":
    master = Master('127.0.0.1', 8888)
    master.start_server()
