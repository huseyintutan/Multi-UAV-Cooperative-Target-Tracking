from flask import Flask, render_template
import socket
import threading

app = Flask(__name__)

# Global değişken verileri saklamak için
gps_data = "No data received yet."

def listen_for_gps_data():
    global gps_data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 8080))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    gps_data = data.decode('utf-8')
                    print("Received:", gps_data)

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