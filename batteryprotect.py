import psutil
import time
import bluetooth
import logging
from systemd.journal import JournalHandler

batteryProtectorAddress = '4c:11:ae:a0:17:4e'
port = 1

def sendCommand(command):
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((batteryProtectorAddress, port))
    s.send(command)
    s.close()

log = logging.getLogger('batteryprotector')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)
log.info("Battery Protector started")

while True:  
    try:         
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        battery_percent = battery.percent
        if (plugged == True and battery_percent > 85):
            sendCommand('0')
            log.info("Charge off")
        if (plugged == False and battery_percent < 65):
            sendCommand('1')
            log.info("Charge on")
        time.sleep(60)
    except Exception as e:
        log.error(str(e))
        time.sleep(60)