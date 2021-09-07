import psutil
import time
import bluetooth
import logging
import subprocess
from systemd.journal import JournalHandler

log = logging.getLogger('batteryprotector')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

computerBluetoothAddress = "08:5B:D6:D0:33:96"
batteryProtectorAddress = '4c:11:ae:a0:17:4e'
port = 1

def bluetoothIsActive():
    stdoutdata = subprocess.getoutput("hcitool dev")  
    if computerBluetoothAddress in stdoutdata.split():
        return True
    return False

def switchBluetoothOff():
    time.sleep(10)
    subprocess.call(["rfkill", "block", "bluetooth"]) 
    log.info("Switching bluetooth off")

def switchBluetoothOn():
    subprocess.call(["rfkill", "unblock", "bluetooth"])
    log.info("Switching bluetooth on")
    time.sleep(10)

def setCharger(chargingStatus):
    bluetoothActiveBeforeSettingChargeMode = bluetoothIsActive()
    if (not bluetoothActiveBeforeSettingChargeMode):
        switchBluetoothOn()
    try:
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((batteryProtectorAddress, port))
        log.info("Charger " + chargingStatus)
        command = '1' if chargingStatus == "On" else '0'
        s.send(command)
        s.close()
    finally:
        if (not bluetoothActiveBeforeSettingChargeMode):
            switchBluetoothOff()

log.info("Battery Protector started")

while True:  
    try:         
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        battery_percent = battery.percent
        if (plugged == True and battery_percent > 90):            
            setCharger("Off")
        if (plugged == False and battery_percent < 75):
            setCharger("On")
        time.sleep(60)
    except Exception as e:
        log.error(str(e))
        time.sleep(60)
