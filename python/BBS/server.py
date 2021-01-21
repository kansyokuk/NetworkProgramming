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

def memory_read():    
    jsonfile_open = open("./log.json", "r")
    json_read = json.load(jsonfile_open)
    jsonfile_open.close()
    return json_read

def memory_write(data):
    json_dic = data
    jsonfile_open = open("./log.json", "w", encoding = L)
    json.dump(json_dic, jsonfile_open, ensure_ascii = False, indent = 4)
    jsonfile_open.close()

def commun_error_msg(json_read):
    print("-----")
    print(Color.GREEN + "[User_Name]: " + Color.END + "{}".format(json_read["User_Info"]["name"]))
    print(Color.YELLOW + "comunicate error." + Color.END)

def login_msg(json_read):
    print("-----")
    print(Color.GREEN + "[User_Name]: " + Color.END + "{}".format(json_read["User_Info"]["name"]))
    print(Color.GREEN + "[User_Code]: " + Color.END + "{}".format(json_read["User_Info"]["code"]))
    print("Logged in.")

def logout_msg(json_read):
    print("-----")
    print(Color.GREEN + "[User_Name]: " + Color.END + "{}".format(json_read["User_Info"]["name"]))
    print(Color.GREEN + "[User_Code]: " + Color.END + "{}".format(json_read["User_Info"]["code"]))
    print("Logged out.")

def write_msg(json_read):
    print("-----")
    print(Color.GREEN + "[User_Name]: " + Color.END + "{}".format(json_read["User_Info"]["name"]))
    print(Color.GREEN + "[User_Code]: " + Color.END + "{}".format(json_read["User_Info"]["code"]))
    print("Writing now.")

def read_msg(json_read):
    print("-----")
    print(Color.GREEN + "[User_Name]: " + Color.END + "{}".format(json_read["User_Info"]["name"]))
    print(Color.GREEN + "[User_Code]: " + Color.END + "{}".format(json_read["User_Info"]["code"]))
    print("Reading now.")

def delete_msg(json_read):
    print("-----")
    print(Color.GREEN + "[User_Name]: " + Color.END + "{}".format(json_read["User_Info"]["name"]))
    print(Color.GREEN + "[User_Code]: " + Color.END + "{}".format(json_read["User_Info"]["code"]))
    print("Deleting now.")

def decode(data):
    return data.decode(L)

def func_write(sock_c, addr, data, json_read):
    write_msg(json_read)
    data = memory_read()
    sock_c.sendall((Color.PURPLE + json_read["Message"]["Write"]["title"] + Color.END).encode(L))
    sock_c.sendall(json_read["Message"]["Write"]["msg_0"].encode(L))
    msg = decode(sock_c.recv(BUFSIZE))
    data["log"].append([json_read["User_Info"]["name"], json_read["User_Info"]["code"], msg])
    memory_write(data)

    sock_c.sendall(json_read["Message"]["Write"]["msg_1"].encode(L))
    json_read["User_Info"]["menu_selection"] = decode(sock_c.recv(BUFSIZE))
    if json_read["User_Info"]["menu_selection"] == "Y":
        func_write(sock_c, addr, data, json_read)
    else:
        menu(sock_c, addr, data, json_read)

def func_read(sock_c, addr, data, json_read):
    read_msg(json_read)
    data = memory_read()
    sock_c.sendall((Color.PURPLE + json_read["Message"]["Read"]["title"] + Color.END).encode(L))
    sock_c.sendall(json_read["Message"]["Read"]["msg_0"].encode(L))
    msg = "-----\n"
    for i in range(len(data["log"])):
        if data["log"][i] == None:
            continue
        msg = msg + Color.GREEN + "[thread number]: " + Color.END + "{}\n".format(i)
        msg = msg + Color.GREEN + "[name]: " + Color.END + "{}\n".format(data["log"][i][0])
        msg = msg + "{}\n".format(data["log"][i][2])
        msg = msg + "-----\n"
    sock_c.sendall(msg.encode(L))

    sock_c.sendall(json_read["Message"]["Read"]["msg_1"].encode(L))
    json_read["User_Info"]["menu_selection"] = decode(sock_c.recv(BUFSIZE))
    if json_read["User_Info"]["menu_selection"] == "Y":
        func_read(sock_c, addr, data, json_read)
    else:
        menu(sock_c, addr, data, json_read)

def func_delete(sock_c, addr, data, json_read):
    delete_msg(json_read)
    data = memory_read()
    sock_c.sendall((Color.PURPLE + json_read["Message"]["Delete"]["title"] + Color.END).encode(L))
    sock_c.sendall(json_read["Message"]["Delete"]["msg_0"].encode(L))
    num = decode(sock_c.recv(BUFSIZE))
    code = decode(sock_c.recv(BUFSIZE))
    if len(data["log"]) <= int(num):
        sock_c.sendall(json_read["Message"]["Delete"]["msg_1"].encode(L))
    else:
        if data["log"][int(num)][1] == code:
            data["log"][int(num)][2] = Color.RED + "This message has been deleted." + Color.END
            memory_write(data)
            sock_c.sendall(json_read["Message"]["Delete"]["msg_2"].encode(L))
        else:
            sock_c.sendall(json_read["Message"]["Delete"]["msg_3"].encode(L))
    
    sock_c.sendall(json_read["Message"]["Delete"]["msg_4"].encode(L))
    json_read["User_Info"]["menu_selection"] = decode(sock_c.recv(BUFSIZE))
    if json_read["User_Info"]["menu_selection"] == "Y":
        func_delete(sock_c, addr, data, json_read)
    else:
        menu(sock_c, addr, data, json_read)

def func_exit(sock_c, addr, json_read):
    sock_c.sendall((Color.PURPLE + json_read["Message"]["Exit"]["title"] + Color.END).encode(L))
    sock_c.sendall(json_read["Message"]["Exit"]["msg_0"].encode(L))
    logout_msg(json_read)

def judge(sock_c, addr, data, json_read):
    if json_read["User_Info"]["menu_selection"] == "W":
        func_write(sock_c, addr, data, json_read)
    elif json_read["User_Info"]["menu_selection"] == "R":
        func_read(sock_c, addr, data, json_read)
    elif json_read["User_Info"]["menu_selection"] == "D":
        func_delete(sock_c, addr, data, json_read)
    else:
        func_exit(sock_c, addr, json_read)
    
def menu(sock_c, addr, data, json_read):
    sock_c.sendall((Color.PURPLE + json_read["Message"]["Menu"]["title"] + Color.END).encode(L))
    sock_c.sendall(json_read["Message"]["Menu"]["msg_0"].encode(L))
    json_read["User_Info"]["menu_selection"] = decode(sock_c.recv(BUFSIZE))
    judge(sock_c, addr, data, json_read)

def login(sock_c, addr, data, json_read):
    sock_c.sendall((Color.PURPLE + json_read["Message"]["Login"]["title"] + Color.END).encode(L))
    sock_c.sendall(json_read["Message"]["Login"]["msg_0"].encode(L))
    json_read["User_Info"]["name"] = decode(sock_c.recv(BUFSIZE))
    json_read["User_Info"]["code"] = decode(sock_c.recv(BUFSIZE))
    login_msg(json_read)

def base(sock_c, addr):
    try:
        data = memory_read()

        jsonfile_open = open("./server.json", "r")
        json_read = json.load(jsonfile_open)
        jsonfile_open.close()

        login(sock_c, addr, data, json_read)
        menu(sock_c, addr, data, json_read)
    except:
        commun_error_msg(json_read)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((MY_ADDRESS, MY_PORT))
    sock.listen()

    while True:
        sock_c, addr = sock.accept()
        p = mp.Process(target = base, args = (sock_c, addr))
        p.start()
    
if __name__ == "__main__":
    main()