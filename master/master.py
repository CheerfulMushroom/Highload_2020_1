from asyncio.streams import StreamReader, StreamWriter


async def master_job(reader: StreamReader, writer: StreamWriter):
    request_line_encoded = await reader.readline()
    request_line = request_line_encoded.decode()
    request_line_words = request_line.split(' ')
    if len(request_line_words) < 2:
        # FIXME(Alex): Error handling
        pass

    method, path = request_line_words[:2]

    addr = writer.get_extra_info('peername')
    print("{addr}:\t{method} {path}".format(addr=addr, method=method, path=path))

    writer.write(request_line_encoded)
    await writer.drain()
    writer.close()

    print("=========================================")
