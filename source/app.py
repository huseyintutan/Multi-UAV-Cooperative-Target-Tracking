from flask import Flask, render_template
from MachineDevice import AircraftIAControlDevice

app = Flask(__name__)
control_device = AircraftIAControlDevice(name="MyAircraftIAControlDevice", machine="MyMachine", inputs_mapping_file="input_mappings.json")

@app.route('/')
def index():
    lidar_measurement = control_device.calculate_lidar_measurement()  
    gyro_data = control_device.calculate_gyro()  
    gps_data = control_device.calculate_gps()  
    return render_template('index.html', lidar_measurement=lidar_measurement, gyro_data=gyro_data, gps_data=gps_data)

if __name__ == '__main__':
    app.run(debug=True)
