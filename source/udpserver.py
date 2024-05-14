import socket

class UdpSocket:
    def __init__(self, host='localhost', port1=1234, port2=1235, port3=1236):
        self.host = host
        self.port1 = port1
        self.port2 = port2
        self.port3 = port3
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_to_port1(self, data):
        self.sock.sendto(data, (self.host, self.port1))

    def send_to_port2(self, data):
        self.sock.sendto(data, (self.host, self.port2))

    def send_to_port3(self, data):
        self.sock.sendto(data, (self.host, self.port3))

    def close(self):
        self.sock.close()


if __name__ == '__main__':
    udp_server = UdpSocket()

    try:
        while True:
            data = input('Enter data to send (format: "port1:message" or "port2:message"): ')

            if data == 'exit':
                break

            if data.startswith('port1:'):
                message = data[len('port1:'):]
                udp_server.send_to_port1(message)
            elif data.startswith('port2:'):
                message = data[len('port2:'):]
                udp_server.send_to_port2(message)
            elif data.startswith('port3:'):
                message = data[len('port3:'):]
                udp_server.send_to_port3(message)
            else:
                print("Invalid input format. Use 'port1:message' or 'port2:message'.")
    except KeyboardInterrupt:
        pass
    finally:
        udp_server.close()