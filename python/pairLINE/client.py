import socket
import signal
import multiprocessing as mp
import json

signal.signal(signal.SIGINT, signal.SIG_DFL)

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

def commun_error_msg(json_read):
	print("-----")
	print(Color.GREEN + "[{}]: ".format(json_read["User_Info"]["Partner"]["name"] + Color.END))
	print(Color.YELLOW + "comunicate error. " + Color.END)

def client_login(sock, json_read):
	print(decode(sock.recv(BUFSIZE)))
	print(decode(sock.recv(BUFSIZE)))
	json_read["User_Info"]["Myself"]["name"] = input("[name]: ")
	json_read["User_Info"]["Myself"]["code"] = input("[code]: ")
	sock.sendall(json_read["User_Info"]["Myself"]["name"].encode(L))
	sock.sendall(json_read["User_Info"]["Myself"]["code"].encode(L))
	flag = int(decode(sock.recv(BUFSIZE)))
	print(decode(sock.recv(BUFSIZE)))
	if flag:
		sock.close()
		exit()

def recv_name(sock, json_read):
	json_read["User_Info"]["Myself"]["name"] = decode(sock.recv(BUFSIZE))

def conversation(sock, json_read):
	print(decode(sock.recv(BUFSIZE)))

	while True:
		msg = input("[you]: ")
		sock.sendall(msg.encode(L))
		if msg == json_read["Message"]["Narration"]["msg_0"]:
			exit()

def base2(sock, json_read):
	try:
		while True:
			box = decode(sock.recv(BUFSIZE))
			if box == json_read["Message"]["Narration"]["msg_0"]:
				exit()
			else:
				print(Color.GREEN + "[{}]: ".format(json_read["User_Info"]["Partner"]["name"] + Color.END) + box)
	except:
		commun_error_msg(json_read)

def base1(sock, json_read):
	try:
		client_login(sock, json_read)
		conversation(sock, json_read)
	except:
		commun_error_msg(json_read)

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))

	jsonfile_open = open("./communicate_client.json", "r")
	json_read = json.load(jsonfile_open)
	jsonfile_open.close()

	p1 = mp.Process(target = base1, args = (sock, json_read))
	p1.start()
	p2 = mp.Process(target = base2, args = (sock, json_read))
	p2.start()

	sock.close()

if __name__ == "__main__":
    main()
