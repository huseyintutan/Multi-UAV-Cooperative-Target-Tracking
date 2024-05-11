from flask import Flask, render_template
import socket
import threading
from udpclient import UdpSocket

app = Flask(__name__)

gps_data = "No data received yet."

def listen_for_gps_data():
    global gps_data
    udp_socket = UdpSocket()
    while True:
        gps_data = udp_socket.recv()
        #print(gps_data)

@app.route('/')
def index():
    return render_template('dashboard.html', gps_data=gps_data)

@app.route('/get_gps_data')
def get_gps_data():

    return gps_data

if __name__ == '__main__':
    thread = threading.Thread(target=listen_for_gps_data)
    thread.daemon = True
    thread.start()
    app.run(debug=True, use_reloader=False,port=8181)