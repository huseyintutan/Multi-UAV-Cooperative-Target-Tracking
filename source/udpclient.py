import socket

class UdpSocket:
    def __init__(self, host='localhost', port1=1234, port2=1235, port3=1236):
        self.host = host
        self.port1 = port1
        self.port2 = port2
        self.port3 = port3
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock1.bind((self.host, self.port1))
        self.sock2.bind((self.host, self.port2))
        self.sock3.bind((self.host, self.port3))

    def recv_from_port1(self):
        return self.sock1.recv(1024).decode()

    def recv_from_port2(self):
        return self.sock2.recv(1024).decode()
    
    def recv_from_port3(self):
        return self.sock3.recv(1024).decode()

    def close(self):
        self.sock1.close()
        self.sock2.close()
        self.sock3.close()


if __name__ == '__main__':
    udp_socket = UdpSocket()

    try:
        while True:
            print("Port 1234:", udp_socket.recv_from_port1())
            print("Port 1235:", udp_socket.recv_from_port2())
            print("Port 1236:", udp_socket.recv_from_port3())
    except KeyboardInterrupt:
        pass
    finally:
        udp_socket.close()