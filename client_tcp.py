import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('127.0.0.1', 5454))
    while 1:
        sock.send(b"test6666666666666666")
        print(sock.recv(1024))


# def tcp_client():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(('127.0.0.1', 5454))
#     while 1:
#         s.sendall(b"test66666666666")
#         s.recv(1024)
#     # s.sendall(b"fafdasfafa")
#     # print(s.recv(1024))
#
#
# if __name__ == "__main__":
#     tcp_client()