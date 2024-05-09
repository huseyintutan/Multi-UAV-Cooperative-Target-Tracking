from flask import Flask, render_template
import socket
import threading
from udpclient import UdpSocket

app = Flask(__name__)

# Global değişken verileri saklamak için
gps_data = "No data received yet."

def listen_for_gps_data():
    global gps_data
    # UDP soketi oluştur
    udp_socket = UdpSocket()
    # UDP soketinden sürekli veri al
    while True:
        gps_data = udp_socket.recv()
        print(gps_data)




@app.route('/')
def index():
    # Global değişkeni kullanarak son alınan GPS verisini sayfada göster
    return render_template('index.html', gps_data=gps_data)

if __name__ == '__main__':
    # Soket dinleme işlemini başlatan bir thread
    thread = threading.Thread(target=listen_for_gps_data)
    thread.daemon = True
    thread.start()
    # Flask uygulamasını çalıştır
    app.run(debug=True, use_reloader=False,port=8181)