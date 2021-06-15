import socket
import json
import _thread
import time
from user import UserVo

userList = []

def login(data3, what, conn, addr):
    userVo = UserVo()
    userVo.setSocket(conn, addr)
    
    userVo.setInfo(data3['username'], data3['gender'], data3['id'])
    userList.append(userVo)
    print(data3['username'], '登录系统', len(userList))
    for user in userList:
        print(user.username)
    responseList = []
    responseData = {}
    response = {}
    
    for u in userList:
        user = {}
        user['username'] = u.username
        user['gender'] = u.gender
        user['id'] = u.id
        responseList.append(user)
    print('返回给客户端的数据', responseList)    
    responseData['list'] = responseList
    responseData['whoFirst'] = 0
    response['content'] = responseData
    response['what'] = what
    for user in userList:
        jsonstr = json.dumps(response) + '\n'
        user.socket.send(jsonstr.encode('utf-8'))
def dispatchEvent(data):
    for user in userList:
        print('返回给客户端的数据', data.decode())
        user.socket.send(data)
def dealwithConn(client, addr):
    print('子线程循环开始')
    with client:
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    for user in userList:
                        if user.socket == client:
                            userList.remove(user)
                    print('某用户退出系统，剩余用户个数', len(userList), '剩余用户如下：')
                    for user in userList:
                        print(user.username)
                    break
                data2 = json.loads(data.decode())
                data3 = data2['content']
                print('receive form client：', data2)
                what = data2['what']
                if what == 1:
                    login(data3, what, client, addr)
                if what == 2:
                    dispatchEvent(data)
            except ConnectionResetError as reset:
                client.close()
                print('关闭了正在占线的链接！', reset)
                break
            except ConnectionAbortedError as aborted:
                client.close()
                print('客户端断开链接！', aborted)
                break
            except OSError as oserror:
                client.close()
                print('OSError', oserror)
                break
            except BaseException as unknown:
                client.close()
                print('----未知错误----', unknown)
                break
    print('子线程循环结束')

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
  host = socket.gethostname()
  port = 10005
  server.bind((host, port))
  server.listen(5)
  while True:
      print('等待客户端连接...')
      conn,addr = server.accept()
      _thread.start_new_thread(dealwithConn, (conn, addr))
        
