from flask import Flask, render_template
import socket
import threading
from udpclient import UdpSocket

app = Flask(__name__)

gps_data1 = "No data received yet."
gps_data2 = "No data received yet."
gps_data3 = "No data received yet."

def listen_for_gps_data():
    global gps_data1
    global gps_data2
    global gps_data3

    udp_socket = UdpSocket()
    while True:
        gps_data1 = udp_socket.recv_from_port1()
        gps_data2 = udp_socket.recv_from_port2()
        gps_data3 = udp_socket.recv_from_port3()
        #print(gps_data)

@app.route('/')
def index():
    return render_template('dashboard.html', gps_data1=gps_data1,gps_data2=gps_data2,gps_data3=gps_data3)

@app.route('/get_data1')
def get_gps_data1():

    return gps_data1

@app.route('/get_data2')
def get_gps_data2():

    return gps_data2

@app.route('/get_data3')
def get_gps_data3():

    return gps_data3

if __name__ == '__main__':
    thread = threading.Thread(target=listen_for_gps_data)
    thread.daemon = True
    thread.start()
    app.run(debug=True, use_reloader=False,port=8181)