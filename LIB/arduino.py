import serial
import time
import numpy as np

class arduino_potentiometer():
    def __init__(self, COM='COM4', baudrate=9600):
        print('Initializing arduino board')
        self.ser = serial.Serial('COM4', 9600, timeout=3)
        self.R1AB = 92100
        self.R1S = self.R1AB/255
        self.R1W = 127
        time.sleep(3)

    def set_pot1(self, resistance):
        print('hello')
        n = str(int(np.round((resistance-self.R1W)/self.R1S))).encode('utf-8')
        print(n)
        self.ser.write(n)
        print(self.ser.readline().decode('ascii'))

    def terminate(self):
        self.ser.close()

arduino = arduino_potentiometer()
arduino.set_pot1(400)
arduino.terminate()
