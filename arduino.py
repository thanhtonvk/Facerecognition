import serial
import time
dataSerial = serial.Serial('COM4', 280301, timeout=.1)
def send_data(id):
    time.sleep(3)
    dataSerial.write(str(id).encode())
    print('mo khoa ',id)
    time.sleep(3)
