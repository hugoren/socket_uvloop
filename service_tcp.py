import asyncio
import uvloop
import socketserver
from collections import deque
from blinker import signal
from concurrent.futures import ThreadPoolExecutor
from config import HOST, PORT
from utils import log
# from utils import rpush_redis
import redis
import time

q = deque()
queue_signal = signal("queue_signal")
q_num = 0


@queue_signal.connect
def rpush_data(data_list):
    try:
        msg_key = "log-msg"
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, max_connections=10)
        r = redis.StrictRedis(connection_pool=pool)
        [r.rpush(msg_key, i) for i in data_list]
    except Exception as e:
        log('error', str(e))


def is_list_max(list_max=3000):

    if q.__len__() >= list_max:
        start_time = time.time()
        data_list = [q.pop() for i in range(list_max)]
        # rpush_data(data_list)
        queue_signal.send(data_list)
        print(time.time() - start_time)
    else:
        global q_num
        if q_num == q.__len__() and q_num >=1:
            data_list = [q.pop() for i in range(q_num)]
            queue_signal.send(data_list)
        q_num = q.__len__()
        print(q_num)


class TCPHandler(socketserver.BaseRequestHandler):
    def setup(self):
        ip = self.client_address[0].strip()
        port = self.client_address[1]
        print(ip, port)

    def handle(self):
        #  keep alive
        while 1:
            data = self.request.recv(1024)
            if data:
                q.appendleft(data)
                is_list_max()
                self.request.sendall(b"recev success!")

    def finish(self):
        print("client is disconnect")


async def handler():
    print("Socket tcp server begin.....")
    log('info', 'Socket tcp server begin.....')
    try:
        s = socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler)
        s.serve_forever()
    except Exception as e:
        log('error', str(e))
        print(e)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(loop.run_until_complete(handler()))


