import socket
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

HOST = "127.0.0.1"
PORT = 50000

BUFSIZE = 100000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))

data = sock.recv(BUFSIZE)
print(data.decode("UTF-8"))
print("「0」～「3」以外の入力は「3」になるよ")
print("【1回戦】　どの手にする？")

while True:
    num = input("あなたの手：")
    if num != "0" and num != "1" and num != "2" and num != "3":
        num = "3"

    try:
        sock.sendall(num.encode("UTF-8"))
    except:
        print("送信に失敗しました")

    if num == "3":
        data = sock.recv(BUFSIZE)
        print(data.decode("UTF-8"))
        sock.close()
        break

    data = sock.recv(BUFSIZE)
    print(data.decode("UTF-8"))