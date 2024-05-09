import socket

# create a udp socket class for receiving string stream

class UdpSocket:
    def __init__(self, host='localhost', port=1234):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def recv(self):
        return self.sock.recv(1024).decode()

    def close(self):
        self.sock.close()


if __name__ == '__main__':
    udp_socket = UdpSocket()

    while True:
        print(udp_socket.recv())

    udp_socket.close()  