import psutil
import time
import bluetooth
from datetime import datetime

def log(message):
    with open("/home/josep/batterystatus.txt", "a") as f:
        f.write(str(datetime.now())+ " | " + str(message) + '\n')
        f.close()



counter = 0

while True:  
    try:  
        batteryProtectorAddress = '4c:11:ae:a0:17:4e'
        port = 1
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((batteryProtectorAddress, port))
        log("connected " + str(counter))
        counter = counter + 1
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        battery_percent = battery.percent
        log(str(plugged) + "|" + str(battery_percent) + "|check" )
        if battery_percent > 83:
            s.send('0')
            log(str(plugged) + "|" + str(battery_percent) + "|off" )
        if battery_percent < 83:
            s.send('1')
            log(str(plugged) + "|" + str(battery_percent) + "|on")
        s.close()
        log("disconnected")
        time.sleep(60)
    except Exception as e:
        log("Exception")
        log(str(e))
        time.sleep(60)

