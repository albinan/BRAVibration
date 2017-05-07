import numpy as np
import visa
from set_timescale import set_timescale
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':
    oscillResource = 'USB0::0x1AB1::0x04CE::DS1ZD171500380::INSTR'
    rm = visa.ResourceManager()
    print("List of possible resources:")
    print(rm.list_resources())
    inst = rm.open_resource(oscillResource)
    print("Using resource:")
    print(inst.query("*IDN?"))

    #timeWindow = 50

    #set_timescale(timeWindow, inst)

    inst.write('STOP')
    t_win = float(inst.query(':TIMebase:MAIN:SCALe?')) # Time window
    fs = float(inst.query(':ACQuire:SRATe?')) # Sample rate
    timestep = float(inst.query(':WAVeform:XINCrement?'))
    n = t_win*fs  # number of samples
    print('Samplerate: ' + str(fs) + ' [1/s]')
    print('Window size: ' + str(t_win) + ' [s]')
    print('Samples: ' + str(n) + ' [-]')
    print('Timestep: ' + str(timestep) + '| ' + str(1/timestep))
    batchsize = 10000
    batches = int(np.floor(n/batchsize))

    inst.write(':WAV:SOUR CHAN1')
    inst.write(':WAV:MODE NORM')
    inst.write(':WAV:FORM ASCii')
    V_chan1 = []
    for i in range(0, batches):
        inst.write(':WAV:STAR ' + str(i*batchsize + 1))
        inst.write(':WAV:STOP ' + str((i+1)*batchsize + 1))
        V_chan1_str = inst.query(':WAV:DATA?')
        V_chan1_str = V_chan1_str[11:].split(',')
        V_chan1.extend([float(i) for i in V_chan1_str])

    inst.write(':WAV:SOUR CHAN2')
    inst.write(':WAV:MODE NORM')
    inst.write(':WAV:FORM ASCii')
    V_chan2 = []
    for i in range(0, batches):
        inst.write(':WAV:STAR ' + str(i*batchsize + 1))
        inst.write(':WAV:STOP ' + str((i+1)*batchsize + 1))
        V_chan2_str = inst.query(':WAV:DATA?')
        V_chan2_str = V_chan2_str[11:].split(',')
        V_chan2.extend([float(i) for i in V_chan2_str])



    #plt.figure(1)
    #plt.subplot(211)
    #plt.plot(V_chan1)
    #plt.title('Channel 1')
    #plt.subplot(212)
    #plt.plot(V_chan2)
    #plt.title('Channel 2')
    n = np.size(V_chan1)
    HEADER = 'fs\n' + str(fs) + '\nV_chan1,V_chan2'
    output = np.transpose(np.vstack((V_chan1, V_chan2)))
    np.savetxt('test.csv', output, delimiter=',', newline='\n', header=HEADER)

    plt.show()

    #inst.write(':WAV_MODE NORM')
