import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
buf_size = 1024
addr = ("127.0.0.1", 5454)
data = 'socket_1'

while 1:
    s.sendto(bytes(data[:buf_size], encoding="utf-8"), addr)
    print(data[:buf_size])
s.close()