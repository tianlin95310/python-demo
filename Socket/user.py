class UserVo:
    def __init__(self):
        print(self)
    def setSocket(self, socket, addr):
        self.socket = socket
        self.addr = addr
    def setInfo(self, username, gender, id):
        self.username = username
        self.gender = gender
        self.id = id