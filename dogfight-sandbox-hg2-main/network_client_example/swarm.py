import dogfight_client as df
import time

# Bağlantı oluşturma
df.connect("192.168.56.1", 50888)

time.sleep(2)

# Uçakları listeleme
planes = df.get_planes_list()

# İlk üç uçağı kontrol etmek için bir döngü oluşturma
for i in range(3,6):
    # Her uçak için bir ID seçme
    plane_id = planes[i]
    
    # Uçağı başlangıç durumuna getirme
    df.reset_machine(plane_id)
    # Uçağın motor gücünü 1'e yükseltme
    df.set_plane_thrust(plane_id, 1)
    df.set_client_update_mode(True)

    time.sleep(1.5)
    df.retract_gear(plane_id)
    # Otomatik pilotu etkinleştirme
    df.activate_autopilot(plane_id)   

    # Otomatik pilot ayarları
    df.set_plane_autopilot_speed(plane_id, 300)  # Hızı 500 km/s'ye ayarla
    df.set_plane_autopilot_heading(plane_id, 90)  # Yönü 270 derece (batı) olarak ayarla
    df.set_plane_autopilot_altitude(plane_id, 500)  # İrtifayı 200 metre olarak ayarla
    df.stabilize_plane(plane_id)

    time.sleep(0.5)

    

    


# Bağlantıyı kesme
df.disconnect()
