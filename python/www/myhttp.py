import socket
import signal

L = "UTF-8"

signal.signal(signal.SIGINT, signal.SIG_DFL)
MY_ADDRESS = ""
MY_PORT = 50000

BUFSIZE = 1024

WAIT_TIME = 1

statusline = "HTTP/1.1 200 OK\r\n"
blank_line = "\r\n"
contents = "にゃんにゃん(((三^・ω・^三)))"

def recv_crlf(sock_c):
    BUFSIZE_CRLF = 1

    req = ""
    while req.find("\r\n") < 0:
        data = sock_c.recv(BUFSIZE_CRLF)
        if not data:
            break
        req += data.decode(L)
    
    return req

def get_request(sock_c):
    sock_c.settimeout(WAIT_TIME)

    req_l = req_h = req_m = None

    try:
        req = recv_crlf(sock_c)
        i_CRLF = req.find("\r\n")
        if i_CRLF < 0:
            print("No Request Line")
            return (None, None, None)
        
        req_l = req[:i_CRLF]

        req_h = {}
        key_value = recv_crlf(sock_c)
        while key_value != "\r\n":
            k, v = key_value.split(": ")
            req_h[k] = v[:-2]
            key_value = recv_crlf(sock_c)

        if "Content-Length" in req_h:
            req_m = sock_c.recv(BUFSIZE).decode(L)
            while len(req_m) < int(req_h["Content-Length"]):
                data = socl_c.recv(BUFSIZE)
                if not data:
                    break
                req_m += data.decode(L)
    except:
        req_m = None

    return (req_l, req_h, req_m)

def send_response(sock_c, code, phrase, f):
    statusline = "{} {} {}".format("HTTP/1.1", code, phrase)

    dt_now = datetime.datetime.now()
    header = dt_now.strftime("Date: %a, %d %m %Y %H:%M:%S JST\r\n")

    if f != None:
        body = f.read()
        header += "Content-Length: {}\r\n".format(len(body))

        extention_index = f.name.rindex(".")
        extension = f.name[-extention_index + 1:].lower()

        if extension == "html" or extension == "htm":
            header += "Content-Type: {}\r\n".format("text/html")
        elif extension == "txt":
            header += "Content-Type: {}\r\n".format("text/plain")
        elif extension == "gif":
            header += "Content-Type: {}\r\n".format("image/gif")
        elif extension == "png":
            header += "Content-Type: {}\r\n".format("image/png")

    sock_c.sendall(statusline.encode(L))
    sock_c.sendall(header.encode(L))
    sock_c.sendall("\r\n".encode(L))
    if body != None:
        sock_c.sendall(body)
    
    else:
        body = None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((MY_ADDRESS, MY_PORT))

sock.listen()

while True:
    sock_c, addr = sock.accept()

    line, header, body = get_request(sock_c)
    print("request line: {}".format(line))
    print("request header: {}".format(header))
    print("message body: {}".format(body))

    sock_c.close()

sock.close()
