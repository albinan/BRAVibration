import numpy as np
import visa
import time
import os


def snapsnot(outputFileLoc, channels):
    print('waht')
    oscillResource = 'USB0::0x1AB1::0x04CE::DS1ZD171500380::INSTR'
    rm = visa.ResourceManager()
    print("List of possible resources:")
    print(rm.list_resources())
    inst = rm.open_resource(oscillResource)
    print("Using resource:")
    print(inst.query("*IDN?"))

    #timeWindow = 50

    #set_timescale(timeWindow, inst)

    #inst.write('STOP')
    t_win = float(inst.query(':TIMebase:MAIN:SCALe?')) # Time window
    fs = float(inst.query(':ACQuire:SRATe?')) # Sample rate
    print('Samplerate: ' + str(fs) + ' [1/s]')
    print('Window size: ' + str(t_win) + ' [s]')
    print('Sampling frequency: ' + str(fs))
    print('Time increment: ' + str(1/fs))
    inst.write(':WAV:MODE NORM')
    print(inst.query('WAV:MODE?'))
    inst.write(':WAV:FORM ASCii')
    V_chan = []
    channels = channels.split(',')
    header = 'time,'
    for channel in channels:
        print(channel)
        V_chan_tmp = []
        inst.write(':WAV:SOUR CHAN' + channel)
        V_chan_str = inst.query(':WAV:DATA?')
        V_chan_str = V_chan_str[11:].split(',')
        V_chan_tmp.extend([float(i) for i in V_chan_str])
        V_chan.append(V_chan_tmp)
        header = header + 'Voltage_channel_' + channel +','

    header = header[:-1]
    n = np.size(V_chan[0])

    t = []
    t.append(np.asarray(range(0, n))*(1/fs))
    os.makedirs(outputFileLoc + '/snapshots', exist_ok=True)
    print(outputFileLoc + '/snapshots')
    data = np.transpose(np.vstack((t, V_chan)))
    fileLoc = outputFileLoc + '/snapshots/oscillsnapshot' + time.strftime('%S-%M-%d-%m-%Y') + '.csv'
    np.savetxt(fileLoc, data, delimiter=',', newline='\n', header=header)

    return data, header, fileLoc

def hotsnap():
    print('whatwhat')

    #inst.write(':WAV_MODE NORM')
