import socket
import signal
import json

signal.signal(signal.SIGINT, signal.SIG_DFL)

json_open = open("./client.json", "r")
json_read = json.load(json_open)

L = "UTF-8"

HOST = "127.0.0.1"
PORT = 50000

BUFSIZE = 100000

class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

def decode(data):
    return data.decode(L)

def func_write(sock):
    print(decode(sock.recv(BUFSIZE)))
    print(decode(sock.recv(BUFSIZE)))
    msg = input("[message]: ")
    sock.sendall(msg.encode(L))
    
    print(decode(sock.recv(BUFSIZE)))
    json_read["My_Info"]["menu_selection"] = input("[your selection]: ")
    sock.sendall(json_read["My_Info"]["menu_selection"].encode(L))
    if json_read["My_Info"]["menu_selection"] == "Y":
        func_write(sock)
    else:
        menu(sock)

def func_read(sock):
    print(decode(sock.recv(BUFSIZE)))
    print(decode(sock.recv(BUFSIZE)))
    
    json_read["My_Info"]["menu_selection"] = input("[your selection]: ")
    sock.sendall(json_read["My_Info"]["menu_selection"].encode(L))
    if json_read["My_Info"]["menu_selection"] == "Y":
        func_read(sock)
    else:
        menu(sock)

def func_delete(sock):
    print(decode(sock.recv(BUFSIZE)))
    print(decode(sock.recv(BUFSIZE)))
    num = input("[thread number]: ")
    code = input("[password]: ")
    sock.sendall(num.encode(L))
    sock.sendall(code.encode(L))
    print(decode(sock.recv(BUFSIZE)))

    print(decode(sock.recv(BUFSIZE)))
    json_read["My_Info"]["menu_selection"] = input("[your selection]: ")
    sock.sendall(json_read["My_Info"]["menu_selection"].encode(L))
    if json_read["My_Info"]["menu_selection"] == "Y":
        func_delete(sock)
    else:
        menu(sock)

def func_exit(sock):
    print(decode(sock.recv(BUFSIZE)))
    print(decode(sock.recv(BUFSIZE)))

def judge(sock):
    if json_read["My_Info"]["menu_selection"] == "W":
        func_write(sock)
    elif json_read["My_Info"]["menu_selection"] == "R":
        func_read(sock)
    elif json_read["My_Info"]["menu_selection"] == "D":
        func_delete(sock)
    else:
        func_exit(sock)

def menu(sock):
    print(decode(sock.recv(BUFSIZE)))
    print(decode(sock.recv(BUFSIZE)))
    json_read["My_Info"]["menu_selection"] = input("[your selection]: ")
    sock.sendall(json_read["My_Info"]["menu_selection"].encode(L))
    judge(sock)

def login(sock):
    print(decode(sock.recv(BUFSIZE)))
    print(decode(sock.recv(BUFSIZE)))
    json_read["My_Info"]["name"] = input("[name]: ")
    json_read["My_Info"]["code"] = input("[code]: ")
    sock.sendall(json_read["My_Info"]["name"].encode(L))
    sock.sendall(json_read["My_Info"]["code"].encode(L))

def base(sock):
    login(sock)
    menu(sock)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    base(sock)

    sock.close()

if __name__ == "__main__":
    main()