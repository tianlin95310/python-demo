import socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host = socket.gethostname()
host = '192.168.1.2'
# host = '27.23.227.74'
# host = 'localhost'
port = 10005
client.connect((host, port))

while True:
    try:
        data = client.recv(1024)
        print ('recv', data.decode())
        msg = '{"what":1,"content":{"username":"tianlin","gender":"male","id":"10001","socket":null}}'
        client.send(msg.encode('utf-8'))
        client.close()
    except ConnectionRefusedError as refuse:
        print('服务器拒绝连接！', refuse)
        break
    except ConnectionResetError as reset:
        print('关闭了正在占线的链接！', reset)
        break
    except ConnectionAbortedError as aborted:
        print('客户端断开链接！', aborted)
        break
    except OSError as oserror:
        print('OSError', oserror)
        break