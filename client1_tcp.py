import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('127.0.0.1', 5454))
    while 1:
        sock.sendall(b"test6666666666666666")
        response = str(sock.recv(1024), 'ascii')