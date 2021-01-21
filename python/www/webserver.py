import socket
import signal
import myhttp

# キーボードからの[ctrl]+[c]を非同期で受付
signal.signal(signal.SIGINT, signal.SIG_DFL)

# 待受に使うIPアドレスとポート番号
MY_ADDRESS = ""
MY_PORT = 50000

BASE_DIR = "."

# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 自分の情報をソケットに登録
sock.bind((MY_ADDRESS, MY_PORT))
# ソケットを待ち受け状態にする
sock.listen()

while True:
    # 接続要求→受理
    sock_c, addr = sock.accept()

    line, header, body = myhttp.get_request(sock_c)

    print("request line: {}\n".format(line))
    print("request header: {}\n".format(header))
    print("message body: {}\n".format(body))

    req1 = line.split(" ")

    if req1[0] == "GET":
        filepath = BASE_DIR + req1[1]
        try:
            with open(filepath, "rb") as f:
                myhttp.send_response(sock_c, 200, "OK", f)
        except:
            pass
        
    sock_c.close()

# 待ち受け用ソケットを閉じる
sock.close()
