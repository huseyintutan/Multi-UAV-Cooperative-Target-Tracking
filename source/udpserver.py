import socket

class UdpSocket:
    def __init__(self, host='localhost', port=1234):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        self.sock.sendto(data, (self.host, self.port))

    def close(self):
        self.sock.close()


if __name__ == '__main__':
    udp = UdpSocket()

    while True:
        data = input('Enter data to send: ')

        if data == 'exit':
            break

        udp.send(data)

    udp.close()