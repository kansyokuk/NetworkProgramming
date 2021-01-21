import socket
import signal
import multiprocessing as mp
import json

signal.signal(signal.SIGINT, signal.SIG_DFL)

L = "UTF-8"

MY_ADDRESS = ""
MY_PORT = 50000

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

def server_login(json_read):
	print(Color.PURPLE + json_read["Message"]["Login"]["title"] + Color.END)
	json_read["User_Info"]["Myself"]["name"] = input("[name]: ")
	json_read["User_Info"]["Myself"]["code"] = input("[code]: ")
	print(json_read["Message"]["Narration"]["msg_1"])

def client_login(sock_c, json_read):
	sock_c.sendall((Color.PURPLE + json_read["Message"]["Login"]["title"] + Color.END).encode(L))
	sock_c.sendall((json_read["Message"]["Login"]["msg_0"]).encode(L))
	json_read["User_Info"]["Partner"]["name"] = decode(sock_c.recv(BUFSIZE))
	json_read["User_Info"]["Partner"]["code"] = decode(sock_c.recv(BUFSIZE))
	if json_read["User_Info"]["Partner"]["code"] == json_read["User_Info"]["Myself"]["code"]:
		sock_c.sendall(("0").encode(L))
		sock_c.sendall((json_read["Message"]["Narration"]["msg_2"]).encode(L))
	else:
		sock_c.sendall(("1").encode(L))
		sock_c.sendall((json_read["Message"]["Login"]["msg_1"]).encode(L))

def send_name(sock_c, json_read):
	sock_c.sendall((json_read["User_Info"]["Myself"]["name"]).encode(L))

def conversation(sock_c, json_read):
	print(json_read["Message"]["Narration"]["msg_3"])
	sock_c.sendall(json_read["Message"]["Narration"]["msg_3"].encode(L))

	while True:
		msg = input("[you]: ")
		sock_c.sendall(msg.encode(L))
		if msg == json_read["Message"]["Narration"]["msg_4"]:
			exit()

def base2(sock_c, json_read):
	try:
		while True:
			box = decode(sock_c.recv(BUFSIZE))
			if box == json_read["Message"]["Narration"]["msg_4"]:
				sock_c.sendall((json_read["User_Info"]["Myself"]["code"]).encode(L))
				exit()
			else:
				print(Color.GREEN + "[{}]: ".format(json_read["User_Info"]["Partner"]["name"] + Color.END) + box)
	except:
		commun_error_msg(json_read)

def base1(sock_c, json_read):
	try:
		client_login(sock_c, json_read)
		conversation(sock_c, json_read)
	except:
		commun_error_msg(json_read)

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((MY_ADDRESS, MY_PORT))
	sock.listen()

	jsonfile_open = open("./communicate_server.json", "r")
	json_read = json.load(jsonfile_open)
	jsonfile_open.close()

	server_login(json_read)

	while True:
		sock_c = sock.accept()[0]
		p1 = mp.Process(target = base1, args = (sock_c, json_read))
		p1.start()
		p2 = mp.Process(target = base2, args = (sock_c, json_read))
		p2.start()

if __name__ == "__main__":
	main()
