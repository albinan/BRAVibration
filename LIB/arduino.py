import serial
import time
import numpy as np
import matplotlib.pyplot as plt

class arduino_potentiometer_paralell():
    def __init__(self, COM='COM4', baudrate=9600):
        print('Initializing arduino board')
        self.ser = serial.Serial('COM4', 9600, timeout=3)
        #self.R1AB = 92100
        self.R1AB = 91700
        self.R1W = 122.9
        self.R1S = (self.R1AB-self.R1W)/255
        # self.R2AB = 92500
        self.R2AB = 92200
        self.R2W = 121.6
        self.R2S = (self.R2AB - self.R2W)/255
        time.sleep(3)

    def set_pot1res(self, resistance):
        print('hello')
        n = int(np.round((resistance-self.R1W)/self.R1S))
        if n > 255:
            n = 255
        elif n < 0:
            n = 0
        n = str(n).encode('utf-8')
        self.ser.write(n)
        print(self.ser.readline().decode('ascii'))

    def set_pot2res(self, resistance):
        print('hello')
        n = int(np.round((resistance-self.R1W)/self.R1S))
        if n > 255:
            n = 255
        elif n < 0:
            n = 0
        n = str(n+1000).encode('utf-8')
        self.ser.write(n)
        print(self.ser.readline().decode('ascii'))

    def set_tot_res(self, resistance):
        # Setting R1 = R2 is the optimal solution for minimizing stepsize.
        # See figures in Arduino folder
        R1 = 2*resistance
        R2 = R1
        self.set_pot1res(R1)
        self.set_pot2res(R2)

    def loop_resistance(Rstart, Rstop, Rstep):
        print('OK')

    def terminate(self):
        self.ser.close()


class arduino_potentiometer_single():
    def __init__(self, COM='COM4', baudrate=9600, Rmin=200):
        print('Initializing arduino board')
        self.ser = serial.Serial('COM4', 9600, timeout=3)
        #self.R1AB = 92100
        self.R_calib_high = 6.8+3.3
        self.Rmax = 10188.58 + Rmin
        self.R_calib_low = 150
        self.Rmin = Rmin
        self.RS = (self.Rmax-self.Rmin)/255
        print('R1S', self.RS)
        #self.R_calib = np.loadtxt('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB/Arduino/potentiometer_single/calib.csv', delimiter=',')
        #self.n_calib = np.arange()
        #self.R_delta = np.mean(self.R_calib[1:]-self.R_calib[:-1])
        #plt.plot(self.R_calib)
        #plt.show()
        #print(self.R_calib)
        time.sleep(3)

    def get_WiperValue(self, resistance):
        n = int(np.round(255*(resistance-self.Rmin)/self.Rmax))
        if n > 255:
            n = 255
        elif n < 0:
            n = 0
        return n

    def get_loop_vector(self, Rstart, Rstop, Rstep):
        n_start = self.get_WiperValue(Rstart)
        n_stop = self.get_WiperValue(Rstop)
        n_step = int(np.round(Rstep/self.RS))

        if n_step == 0:
            n_step = 1

        n = np.arange(n_start, n_stop, n_step)
        if n_start == n_stop:
            n = np.asarray([n_start])
        R_vec = n*(self.Rmax - self.Rmin)/255 + self.Rmin
        print('loop vector')
        print(R_vec)
        return R_vec

    def set_WiperValue(self, value):
        n = value
        if n > 255:
            n = 255
        elif n < 0:
            n = 0
        n = str(n).encode('utf-8')
        self.ser.write(n)
        print(self.ser.readline().decode('ascii'))

    def set_resistance(self, resistance):
        n = int(np.round(255*(resistance - self.Rmin)/(self.Rmax-self.Rmin)))
        if n > 255:
            n = 255
        elif n < 0:
            n = 0
        print('Setting resistance to', n*(self.Rmax-self.Rmin)/255 + self.Rmin, 'Ohm')
        n = str(n).encode('utf-8')
        self.ser.write(n)
        print(self.ser.readline().decode('ascii'))

    def read_A0analog_voltage(self):
        self.ser.write(str(266).encode('utf-8'))
        return float(self.ser.readline().decode('ascii'))/1024

    def read_A1analog_voltage(self):
        self.ser.write(str(267).encode('utf-8'))
        return float(self.ser.readline().decode('ascii'))/1024

    def calibrate_one(self, n, R_calib):

        self.set_WiperValue(n)
        time.sleep(3)
        V_1 = 0
        V_2 = 0
        print('Calculating Resistance')
        for j in range(15):
            print((j/15)*100, ' %')
            V_1 = V_1 + self.read_A0analog_voltage()
            V_2 = V_2 + self.read_A1analog_voltage()
        V_1 = V_1/15
        V_2 = V_2/15
        print('V_1', V_1)
        print('V_2', V_2)
        V_calib = V_1 - V_2
        I_calib = V_calib/R_calib

        R = V_2/I_calib
        print('Calibration for n=' + str(n) + ' R=' + str(R))

    def calibrate_whole(self):
        R = [0]*256
        R_calib = 974
        for i in range(256):
            print(i)
            self.set_WiperValue(i)
            time.sleep(1)
            V_1 = 0
            V_2 = 0
            for j in range(3):
                V_1 = V_1 + self.read_A0analog_voltage()
                V_2 = V_2 + self.read_A1analog_voltage()
            V_1 = V_1/3
            V_2 = V_2/3
            print('V_1', V_1)
            print('V_2', V_2)
            V_calib = V_1 - V_2
            I_calib = V_calib/R_calib

            R[i] = V_2/I_calib
            print(R)
            if i > 0:
                print('deltaR', R[i] - R[i-1])
                print(R[i-1])
            print('resistance', R[i])

        np.savetxt('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB/Arduino/potentiometer_single/calib.csv', np.transpose(np.asarray(R)), delimiter=',')

    def terminate(self):
        self.ser.close()
#ard = arduino_potentiometer_single()
#ard.calibrate_one(255, ard.R_calib_high)
#ard.set_resistance(60)
