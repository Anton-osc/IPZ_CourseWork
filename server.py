import socket

class Server:
    def __init__(self):
        self.server_ip = '192.168.0.104'
        self.server_port = 10000
        self.serverallowconn = 2
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.server_ip, self.server_port)
        self.sock.bind(self.server_address)
        self.sock.listen(self.serverallowconn)

    def connection(self):
        connection, client_address = self.sock.accept()
        try:
            pass
        finally:
            connection.close()
            self.sock.close()

            