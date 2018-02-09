import asyncio
import uvloop
import socketserver

# async def socket_server():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_add = ('0.0.0.0', 5454)
#     s.bind(server_add)
#     print(server_add)
#     while 1:
#         data, addr = s.recvfrom(1024)
#         print(data.decode())
#     s.close()
#
#
# if __name__ == "__main__":
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
#     loop = uvloop.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(socket_server())


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        print(data)


async def handler():
    addr = ('127.0.0.1', 5454)
    print("begin")
    try:
        s = socketserver.ThreadingUDPServer(addr, MyUDPHandler)
        s.serve_forever()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # from concurrent.futures import ThreadPoolExecutor
    #
    # with ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.submit(handler)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(handler())
