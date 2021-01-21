import socket
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

HOST = input("ホスト名を入力：")
PORT = input("ポート番号を入力：")

BUFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, int(PORT)))
except:
    exit()

req_line = "GET / HTTP/1.1\r\n"
req_head = "Host: {}\r\n".format(HOST)
blank_line = "\r\n"

try:
    sock.sendall(req_line.encode("UTF-8"))
    sock.sendall(req_head.encode("UTF-8"))
    sock.sendall(blank_line.encode("UTF-8"))

    while True:
        data = sock.recv(BUFSIZE)
        if not data:
            break
        print(data.decode("UTF-8"))

except:
    print("error")

sock.close()