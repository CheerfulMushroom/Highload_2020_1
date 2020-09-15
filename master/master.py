import asyncio

async def master_job(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received message from {addr}".format(addr=addr))

    print("Send: {message}".format(message=message))

    await asyncio.sleep(10)
    writer.write(data)
    await writer.drain()

    print("Close the client socket")
    writer.close()

    print("=========================================")
