# NOTE  CHANNEL1 HAS TO MEASSURE VOLTAGE OVER HARVESTER
#       CHANNEL2 HAS TO MEASSURE VOLTAGE OVER G

import numpy as np
import visa
from V2G import V2G
# from G2V import G2V
import sys
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB')
from arduino import arduino_potentiometer_single
from set_timescale import set_timescale
from set_voltagescale import set_voltagescale
from set_g import set_g
import time
import matplotlib.pyplot as plt
import os
from createArray import createArray
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def createDir(folderLoc):
    # Make directories for saving data
    if not os.path.exists(folderLoc+'/figures'):
        os.makedirs(folderLoc+'/figures')
        print('Creating folder: '+folderLoc+'/figures')
    if not os.path.exists(folderLoc+'/data'):
        os.makedirs(folderLoc+'/data')
        print('Creating folder: '+folderLoc+'/data')

def createLoopArrays(arduino, fs, gs, Rs):
    f_vec = createArray(fs, isFreqency=True)
    g_vec = createArray(gs, isFreqency=False)
    R_vec = arduino.get_loop_vector(Rs[0], Rs[1], Rs[2])
    return (f_vec, g_vec, R_vec)

def checkAmplifier(inst, channel, f_vec, g_vec, sf_vg, g_err, k_p, s_handle, num_periods, num_tbox):
# Check if amplifier spans the needed g levels
    iterations_test = 25  # More iterations needed when going from max(g_vec) to gmin
    print('Checking if amplifier is set high enough...')
    inst.write(channel + 'OUTput 1')
    inst.write(channel + 'FREQuency ' + str(max(f_vec)))
    set_timescale((num_periods/num_tbox)/max(f_vec), inst)
    print(g_vec)
    err = set_g(max(g_vec)*1.1, inst, sf_vg, s_handle, g_err, iterations_test, k_p, checkAmplifier=True)
    if err == 0:
        print("***Checking amplifier level: Failed, too many iterations***")
        return 0
    print('High test: OK')

    print('Lowering g level...')
    set_g(min(g_vec)*0.9, inst, sf_vg, s_handle, g_err, iterations_test, k_p, checkAmplifier=True)

    print('Checking if amplifier is set low enough...')
    inst.write(channel + 'FREQuency ' + str(min(f_vec)))
    set_timescale((num_periods/num_tbox)/min(f_vec), inst)
    err = set_g(min(g_vec)*0.8, inst, sf_vg, s_handle, g_err, iterations_test, k_p, checkAmplifier=True)
    if err == 0:
        print("***Checking amplifier level: Failed, too many iterations***")
        return 0
    print('Low test: OK')

def loop(g_vec, f_vec, R_vec, inst, arduino, sf_vg, s_handle, g_err, iterations, k_p, channel, num_periods, num_tbox):

    N_i = np.size(g_vec)
    N_j = np.size(R_vec)
    N_k = np.size(f_vec)

    Vrms_vec_in = np.ones([N_i, N_j, N_k])
    freq_in = np.ones([N_i, N_j, N_k])

    Vrms_vec_out = np.ones([N_i, N_j, N_k])
    freq_out = np.ones([N_i, N_j,  N_k])
    phase_out = np.ones([N_i, N_j, N_k])

    counter = 1
    i = 0
    for g in g_vec:
        set_g(g, inst, sf_vg, s_handle, g_err, iterations, k_p, checkAmplifier=False)
        inst.write(':TRIGger:EDGe:SOURce CHANnel2')
        inst.write(':TRIGger:EDGe:SLOPe POS')
        inst.write(':TRIGger:EDGe:LEVel ' + str(g/10))
        time.sleep(3)
        j = 0
        for R in R_vec:
            arduino.set_resistance(R)
            k = 0
            for f in f_vec:
                t1 = time.time()
                inst.write(channel + 'FREQuency ' + str(f))
                set_voltagescale(inst, 'CHANnel1')
                set_voltagescale(inst, 'CHANnel2')
                set_timescale((num_periods/num_tbox)/f, inst)
                time.sleep(1)
                print("---------DATA---------")
                print("Meassurment " + str(counter) + " out of " + str(N_i*N_j*N_k))
                Vrms_vec_in[i, j, k] = float(
                    inst.query(':MEASure:ITEM? VRMS,CHANnel2'))
                freq_in[i, j] = float(
                    inst.query(':MEASure:ITEM? FREQuency,CHANnel2'))

                Vrms_vec_out[i, j, k] = float(
                    inst.query(':MEASure:ITEM? VRMS,CHANnel1'))
                phase_out[i, j, k] = float(
                    inst.query(':MEASure:ITEM? RPHase,CHANnel2,CHANnel1'))
                freq_out[i, j, k] = float(
                    inst.query(':MEASure:ITEM? FREQuency,CHANnel1'))

                print(counter*100/(N_i*N_j*N_k), '%')
                print((N_i-i)*(N_j-j)*(N_k-k)*(time.time()-t1)/60, 'minutes left')
                counter = counter + 1
                k = k + 1
            j = j + 1
        i = i + 1
    return (Vrms_vec_in, freq_in, Vrms_vec_out, freq_out, phase_out, N_i, N_j, N_k)

def findOptFreq(fs, gs, Rs,  g_err):

    # STARTING VARIABLES
    # Resistance: Load Resistance
    # fmin: Minimum frequency in Hz
    # delta_f = 0.5  # Step size
    # fmax = 20  # Maximum frequency in Hz
    # set_g = 0.2  # Minimum acceleration in g
    # delta_g = 0.2  # Step size
    # g_max = 0.4  # Maximum acceleration in g
    # g_err = 0.01  # Acceptable error in g. g-gerr < g_real < g + g_err
    # END STARTING VARIABLES
    arduino = arduino_potentiometer_single()
    (f_vec, g_vec, R_vec) = createLoopArrays(arduino, fs, gs, Rs)
    N_k = np.size(f_vec)
    P = np.ones([N_k, 1])
    # "Minimum frequency in Hz, Maximum frequency in Hz, Step size; next interval"
    filename = 'data'
    k_p = 1.5  # Constant used to set g (P-regulator)
    iterations = 15

    sf_vg = 100*1e-3  # 100 mV per g
    s_handle = 10  # Förstärkning på M32 lådan
    num_tbox = 12  # Timescale is set for one box width and there are 12
    # boxes on screen
    num_periods = 5  # Number of periods displayed on oscilloscope screen

    channel = ''
    oscillResource = 'USB0::0x1AB1::0x04CE::DS1ZD171500380::INSTR'
# CODE
    # Useful commands
    # CHANnel1:
    #   FREQuency?
    #   VOLTage?
    #
    #

# IMPORT INSTRUMENT
    rm = visa.ResourceManager()
    print("List of possible resources:")
    print(rm.list_resources())
    inst = rm.open_resource(oscillResource)
    print("Using resource:")
    print(inst.query("*IDN?"))
# Initiate instrument
    inst.write(':CHANnel1:OFFSet 0')
    inst.write(':CHANnel2:OFFSet 0')

# Check amplifier levels
    g = g_vec[0]
    R = R_vec[0]
    checkAmplifier(inst, channel, f_vec, g_vec, sf_vg, g_err, k_p, s_handle, num_periods, num_tbox)
    set_g(g, inst, sf_vg, s_handle, g_err, iterations, k_p, checkAmplifier=False)
    inst.write(':TRIGger:EDGe:SOURce CHANnel2')
    inst.write(':TRIGger:EDGe:SLOPe POS')
    inst.write(':TRIGger:EDGe:LEVel ' + str(g/10))
    time.sleep(3)
    arduino.set_resistance(R)
    k = 0

    print(f_vec)
    for f in f_vec:
        inst.write(channel + 'FREQuency ' + str(f))
        set_voltagescale(inst, 'CHANnel1')
        set_voltagescale(inst, 'CHANnel2')
        set_timescale((num_periods/num_tbox)/f, inst)
        time.sleep(3)
        P_tmp = 0
        for i in range(3):
            P_tmp = P_tmp + 1000*float(inst.query(':MEASure:ITEM? VRMS,CHANnel1'))/R
        P[k] = P_tmp/5
        print(f)
        print(P[k])
    n = np.argmax(P)
    return f_vec[n]


def findOptRes(fs, gs, Rs,  g_err):

    # STARTING VARIABLES
    # Resistance: Load Resistance
    # fmin: Minimum frequency in Hz
    # delta_f = 0.5  # Step size
    # fmax = 20  # Maximum frequency in Hz
    # set_g = 0.2  # Minimum acceleration in g
    # delta_g = 0.2  # Step size
    # g_max = 0.4  # Maximum acceleration in g
    # g_err = 0.01  # Acceptable error in g. g-gerr < g_real < g + g_err
    # END STARTING VARIABLES
    arduino = arduino_potentiometer_single()
    (f_vec, g_vec, R_vec) = createLoopArrays(arduino, fs, gs, Rs)
    N_k = np.size(f_vec)
    P = np.ones([N_k, 1])
    # "Minimum frequency in Hz, Maximum frequency in Hz, Step size; next interval"
    filename = 'data'
    k_p = 1.5  # Constant used to set g (P-regulator)
    iterations = 15

    sf_vg = 100*1e-3  # 100 mV per g
    s_handle = 10  # Förstärkning på M32 lådan
    num_tbox = 12  # Timescale is set for one box width and there are 12
    # boxes on screen
    num_periods = 5  # Number of periods displayed on oscilloscope screen

    channel = ''
    oscillResource = 'USB0::0x1AB1::0x04CE::DS1ZD171500380::INSTR'
# CODE
    # Useful commands
    # CHANnel1:
    #   FREQuency?
    #   VOLTage?
    #
    #

# IMPORT INSTRUMENT
    rm = visa.ResourceManager()
    print("List of possible resources:")
    print(rm.list_resources())
    inst = rm.open_resource(oscillResource)
    print("Using resource:")
    print(inst.query("*IDN?"))
# Initiate instrument
    inst.write(':CHANnel1:OFFSet 0')
    inst.write(':CHANnel2:OFFSet 0')

# Check amplifier levels
    g = g_vec[0]
    f = f_vec[0]
    checkAmplifier(inst, channel, f_vec, g_vec, sf_vg, g_err, k_p, s_handle, num_periods, num_tbox)
    inst.write(channel + 'FREQuency ' + str(f))
    set_g(g, inst, sf_vg, s_handle, g_err, iterations, k_p, checkAmplifier=False)
    inst.write(':TRIGger:EDGe:SOURce CHANnel2')
    inst.write(':TRIGger:EDGe:SLOPe POS')
    inst.write(':TRIGger:EDGe:LEVel ' + str(g/10))
    time.sleep(3)

    k = 0
    for R in R_vec:
        arduino.set_resistance(R)
        k = 0
        set_voltagescale(inst, 'CHANnel1')
        set_voltagescale(inst, 'CHANnel2')
        set_timescale((num_periods/num_tbox)/f, inst)
        time.sleep(3)
        P_tmp = 0
        for i in range(10):
            P_tmp = P_tmp + 1000*float(inst.query(':MEASure:ITEM? VRMS,CHANnel1'))/R
        P[k] = P_tmp/10
        print(f)
        print(P[k])
    n = np.argmax(P)
    return R_vec[n]

def LOOPY(fs, gs, Rs,  g_err, folderLoc):

    # STARTING VARIABLES
    # Resistance: Load Resistance
    # fmin: Minimum frequency in Hz
    # delta_f = 0.5  # Step size
    # fmax = 20  # Maximum frequency in Hz
    # set_g = 0.2  # Minimum acceleration in g
    # delta_g = 0.2  # Step size
    # g_max = 0.4  # Maximum acceleration in g
    # g_err = 0.01  # Acceptable error in g. g-gerr < g_real < g + g_err
    # END STARTING VARIABLES
    arduino = arduino_potentiometer_single()
    (f_vec, g_vec, R_vec) = createLoopArrays(arduino, fs, gs, Rs)

    # "Minimum frequency in Hz, Maximum frequency in Hz, Step size; next interval"
    filename = 'data'
    k_p = 1.5  # Constant used to set g (P-regulator)
    iterations = 15

    sf_vg = 100*1e-3  # 100 mV per g
    s_handle = 10  # Förstärkning på M32 lådan
    num_tbox = 12  # Timescale is set for one box width and there are 12
    # boxes on screen
    num_periods = 5  # Number of periods displayed on oscilloscope screen

    channel = ''
    oscillResource = 'USB0::0x1AB1::0x04CE::DS1ZD171500380::INSTR'
# CODE
    # Useful commands
    # CHANnel1:
    #   FREQuency?
    #   VOLTage?
    #
    #

# IMPORT INSTRUMENT
    rm = visa.ResourceManager()
    print("List of possible resources:")
    print(rm.list_resources())
    inst = rm.open_resource(oscillResource)
    print("Using resource:")
    print(inst.query("*IDN?"))
# Initiate instrument
    inst.write(':CHANnel1:OFFSet 0')
    inst.write(':CHANnel2:OFFSet 0')

# Check amplifier levels
    checkAmplifier(inst, channel, f_vec, g_vec, sf_vg, g_err, k_p, s_handle, num_periods, num_tbox)
# Looping
    (Vrms_vec_in, freq_in, Vrms_vec_out, freq_out, phase_out, N_i, N_j, N_k) = loop(g_vec, f_vec, R_vec, inst, arduino, sf_vg, s_handle, g_err, iterations, k_p, channel, num_periods, num_tbox)

    output = [Vrms_vec_in, freq_in, Vrms_vec_out, freq_out, phase_out]
    filenames = ['Vrms_driving.txt',
                 'freq_driving.txt',
                 'Grms_out.txt',
                 'freq_out.txt',
                 'phase.txt']
    with open(folderLoc + "/data/dataformat.txt", 'w') as text_file:
        text_file.write('Storing method: Row major')
        text_file.write('Looping method: loop_acceleration(loop_resistance(loop_frequency(write number)))')
    with open(folderLoc + "/data/loopvectors.txt", "w") as text_file:
        for g in g_vec:
            for R in R_vec:
                for f in f_vec:
                    text_file.write(str(f))
                    text_file.write('\n')
                text_file.write(str(R))
                text_file.write('\n')
            text_file.write(str(g))
            text_file.write('\n')

    for o in enumerate(output):
        with open(folderLoc + "/data/" + filename + filenames[o[0]], "w") as text_file:
            i = 0
            for g in g_vec:
                j = 0
                for R in R_vec:
                    k = 0
                    for f in f_vec:
                        text_file.write(str(o[1][i, j, k]))
                        text_file.write('\n')
                        k = k + 1
                    j = j + 1
                i = i + 1
    P = 2*Vrms_vec_out
    for i in range(len(R_vec)):
        P[:, i, :] = (P[:, i, :]**2/R_vec[i])*1000 # power in mW

    (ng_0, nR_0, nf_0) = np.unravel_index(P.argmax(), P.shape)
    print('Maximum: ', ng_0, nR_0, nf_0)
    print(f_vec)
    print(g_vec)
    print(R_vec)
    print(np.size(g_vec))
    print(np.size(R_vec))
    print(np.size(f_vec))

    if(N_i > 1 and N_j > 1 and N_k > 1):
        print('Looped over acceleration, resistance and frequency')
        plot_frequencyResistance_3D(f_vec, R_vec, g_vec, ng_0, P, folderLoc)
        plot_frequencyAcceleration_3D(f_vec, R_vec, g_vec, nR_0, P, folderLoc)
        plot_accelerationResistance_3D(f_vec, R_vec, g_vec, nf_0, P, folderLoc)

        plot_frequencyResistance_2D(f_vec, R_vec, g_vec, ng_0, P, folderLoc)
        plot_frequencyAcceleration_2D(f_vec, R_vec, g_vec, nR_0, P, folderLoc)
        plot_accelerationResistance_2D(f_vec, R_vec, g_vec, nf_0, P, folderLoc)

        plot_resistance_2D(f_vec, R_vec, g_vec, nf_0, ng_0, P, folderLoc)
        plot_acceration_2D(f_vec, R_vec, g_vec, nf_0, nR_0, P, folderLoc)
        plot_frequency_2D(f_vec, R_vec, g_vec, nR_0, ng_0, P, folderLoc)
    if(N_i > 1 and N_j > 1 and N_k == 1):
        print('Looped over acceleration and resistance')
        plot_accelerationResistance_3D(f_vec, R_vec, g_vec, nf_0, P, folderLoc)
        plot_accelerationResistance_2D(f_vec, R_vec, g_vec, nf_0, P, folderLoc)

        plot_resistance_2D(f_vec, R_vec, g_vec, nf_0, ng_0, P, folderLoc)
        plot_acceration_2D(f_vec, R_vec, g_vec, nf_0, nR_0, P, folderLoc)
    if(N_i > 1 and N_j == 1 and N_k > 1):
        print('Looped over acceleration and frequency')
        plot_frequencyAcceleration_3D(f_vec, R_vec, g_vec, nR_0, P, folderLoc)
        plot_frequencyAcceleration_2D(f_vec, R_vec, g_vec, nR_0, P, folderLoc)

        plot_acceration_2D(f_vec, R_vec, g_vec, nf_0, nR_0, P, folderLoc)
        plot_frequency_2D(f_vec, R_vec, g_vec, nR_0, ng_0, P, folderLoc)
    if(N_i == 1 and N_j > 1 and N_k > 1):
        print('Looped over resistance and frequency')
        plot_frequencyResistance_3D(f_vec, R_vec, g_vec, ng_0, P, folderLoc)
        plot_frequencyResistance_2D(f_vec, R_vec, g_vec, nf_0, ng_0, P, folderLoc)

        plot_resistance_2D(f_vec, R_vec, g_vec, nf_0, ng_0, P, folderLoc)
        plot_frequency_2D(f_vec, R_vec, g_vec, nR_0, ng_0, P, folderLoc)
    if(N_i > 1 and N_j == 1 and N_k == 1):
        print('Looped over acceleration')
        plot_acceration_2D(f_vec, R_vec, g_vec, nf_0, nR_0, P, folderLoc)
    if(N_i == 1 and N_j > 1 and N_k == 1):
        print('Looped over resistance')
        plot_resistance_2D(f_vec, R_vec, g_vec, nf_0, ng_0, P, folderLoc)
    if(N_i == 1 and N_j == 1 and N_k > 1):
        print('Looped over frequency')
        plot_frequency_2D(f_vec, R_vec, g_vec, nR_0, ng_0, P, folderLoc)
    plt.show()


def plot_resistance_2D(frequency, resistance, acceleration, nf_0, ng_0,  P, folderLoc):
    titlefont = {'size': 16}
    labelfont = {'size': 14}

    fig = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(resistance, P[ng_0, :, nf_0])
    ax.set_title('Power as a function of Resistance at ' + str(frequency[nf_0]) + ' Hz and ' + str(acceleration[ng_0]) + ' g', **titlefont)
    ax.set_xlabel('Resistance (Ohm)', **labelfont)
    ax.set_ylabel('Power (mW)', **labelfont)
    ax.grid(True, which='both')
    ax.minorticks_on()
    fig.savefig(folderLoc + '/figures/resistance.png')
    fig.savefig(folderLoc + '/figures/resistance.eps')

def plot_acceration_2D(frequency, resistance, acceleration, nf_0, nR_0, P, folderLoc):
    titlefont = {'size': 16}
    labelfont = {'size': 14}
    fig = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(acceleration, P[:, nR_0, nf_0])
    ax.set_title('Power as a function of Acceleration at ' + str(frequency[nf_0]) + ' Hz and ' + str(np.round(resistance[nR_0])) + ' Ohm', **titlefont)
    ax.set_xlabel('Acceleration (g)', **labelfont)
    ax.set_ylabel('Power (mW)', **labelfont)
    ax.grid(True, which='both')
    ax.minorticks_on()
    fig.savefig(folderLoc + '/figures/acceration.png')
    fig.savefig(folderLoc + '/figures/acceration.eps')

def plot_frequency_2D(frequency, resistance, acceleration, nR_0, ng_0, P, folderLoc):
    titlefont = {'size': 16}
    labelfont = {'size': 14}
    fig = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(frequency, P[ng_0, nR_0, :])
    ax.set_title('Power as a function of Frequency at ' + str(acceleration[ng_0]) + ' g and ' + str(np.round(resistance[nR_0])) + ' Ohm', **titlefont)
    ax.set_xlabel('Frequency (Hz)', **labelfont)
    ax.set_ylabel('Power (mW)', **labelfont)
    ax.grid(True, which='both')
    ax.minorticks_on()
    fig.savefig(folderLoc + '/figures/frequency.png')
    fig.savefig(folderLoc + '/figures/frequency.eps')

def plot_accelerationResistance_2D(frequency, resistance, acceleration, nf_0, P, folderLoc):
    titlefont = {'size': 16}
    labelfont = {'size': 14}
    fig = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
    ax = fig.add_subplot(111)
    for i in range(len(acceleration)):
        ax.plot(resistance, P[i, :, nf_0], label='Acceleration: ' + str(acceleration[i]) + ' g')
    ax.set_title('Power as a function of Resistance and Acceleration at ' + str(frequency[nf_0]) + ' Hz', **titlefont)
    ax.set_xlabel('Resistance (Ohm)', **labelfont)
    ax.set_ylabel('Power (mW)', **labelfont)
    ax.legend(loc='upper right', prop={'size': 14})
    ax.grid(True, which='both')
    ax.minorticks_on()
    fig.savefig(folderLoc + '/figures/acceration_resistance.png')
    fig.savefig(folderLoc + '/figures/acceration_resistance.eps')

def plot_frequencyAcceleration_2D(frequency, resistance, acceleration, nR_0, P, folderLoc):
    titlefont = {'size': 16}
    labelfont = {'size': 14}
    fig = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
    ax = fig.add_subplot(111)
    for i in range(len(acceleration)):
        ax.plot(frequency, P[i, nR_0, :], label='Acceleration ' + str(acceleration[i]) + ' g')
    ax.set_title('Power as a function of Frequency and Acceleration at ' + str(np.round(resistance[nR_0])) + ' Ohm')
    ax.set_xlabel('Frequency (Hz)', **labelfont)
    ax.set_ylabel('Power (mW)', **labelfont)
    ax.legend(loc='upper right', prop={'size': 14})
    ax.grid(True, which='both')
    ax.minorticks_on()
    fig.savefig(folderLoc + '/figures/frequency_acceration.png')
    fig.savefig(folderLoc + '/figures/frequency_acceration.eps')

def plot_frequencyResistance_2D(frequency, resistance, acceleration, ng_0, P, folderLoc):
    titlefont = {'size': 16}
    labelfont = {'size': 14}
    fig = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
    ax = fig.add_subplot(111)
    for i in range(len(resistance)):
        ax.plot(frequency, P[ng_0, i, :], label='Resistance ' + str(np.round(resistance[i])) + ' Ohm')
    ax.set_title('Power as a function of Frequency and Resistance at ' + str(acceleration[ng_0]) + ' g', **titlefont)
    ax.set_xlabel('Frequency (Hz)', **labelfont)
    ax.set_ylabel('Power (mW)', **labelfont)
    ax.legend(loc='upper right', prop={'size': 14})
    ax.grid(True, which='both')
    ax.minorticks_on()
    fig.savefig(folderLoc + '/figures/frequency_resistance.png')
    fig.savefig(folderLoc + '/figures/frequency_resistance.eps')

def plot_accelerationResistance_3D(frequency, resistance, acceleration, nf_0, P, folderLoc):
    titlefont = {'size': 16}
    labelfont = {'size': 14}
    a, Res = np.meshgrid(acceleration, resistance, sparse=False, indexing='ij')
    fig = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(a, Res, P[:, :, nf_0])
    ax.set_title('Power as a function of Acceleration and Resistance at ' + str(frequency[nf_0]) + ' Hz', **titlefont)
    ax.set_xlabel('Acceleration (Hz)', **labelfont)
    ax.set_ylabel('Resistance (Ohm)', **labelfont)
    ax.set_zlabel('Power (mW)', **labelfont)
    fig.savefig(folderLoc + '/figures/acceration_resistance_surface.png')
    fig.savefig(folderLoc + '/figures/acceration_resistance_surface.eps')

def plot_frequencyAcceleration_3D(frequency, resistance, acceleration, nR_0, P, folderLoc):
    titlefont = {'size': 16}
    labelfont = {'size': 14}
    freq, g = np.meshgrid(frequency, acceleration, sparse=False, indexing='ij')
    fig = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(freq, g, np.transpose(P[:, nR_0, :]))
    ax.set_title('Power as a function of Frequency and Acceleration at ' + str(np.round(resistance[nR_0])) +' Ohm', **titlefont)
    ax.set_xlabel('Frequency (Hz)', **labelfont)
    ax.set_ylabel('Acceleration (Ohm)', **labelfont)
    ax.set_zlabel('Power (mW)', **labelfont)
    fig.savefig(folderLoc + '/figures/frequency_acceration_surface.png')
    fig.savefig(folderLoc + '/figures/frequency_acceration_surface.eps')

def plot_frequencyResistance_3D(frequency, resistance, acceleration, ng_0, P, folderLoc):
    titlefont = {'size': 16}
    labelfont = {'size': 14}
    freq, Res = np.meshgrid(frequency, resistance, sparse=False, indexing='ij')
    fig = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(freq, Res, np.transpose(P[ng_0, :, :]))
    ax.set_title('Power as a function of Frequency and Resistance at ' + str(acceleration[ng_0]) +' g', **titlefont)
    ax.set_xlabel('Frequency (Hz)', **labelfont)
    ax.set_ylabel('Resistance (Ohm)', **labelfont)
    ax.set_zlabel('Power (mW)', **labelfont)
    fig.savefig(folderLoc + '/figures/frequency_resistance_surface.png')
    fig.savefig(folderLoc + '/figures/frequency_resistance_surface.eps')
    # Plotting and saving data
    #titlefont = {'size': 16}
    #labelfont = {'size': 14}
    #plt.figure(None, figsize=(11.69, 8.27), dpi=100)  # A4 size 100 dpi
    #k = 0
    #for g in g_vec:
    #    lab = str(g) + ' (g)'xv, yv = np.meshgrid(x, y, sparse=False, indexing='ij')
    #    plt.plot(f_vec[1:], np.square(Vrms_vec_out[1:, k])*1000/Resistance,
    #             label=lab)
    #    plt.grid(True)
    #    plt.legend(loc='upper right', prop={'size': 14})
    #    k = k + 1
    #plt.title('Power as a function of frequency, load resistance R = '
    #          + str(np.round(Resistance)) + ' (${\Omega}$)', **titlefont)
    #plt.xlabel('Frequency (Hz)', **labelfont)
    #plt.ylabel('Power (mW)', **labelfont)
    #plt.savefig(folderLoc + '/figures/Transferfunction.png')
    #plt.savefig(folderLoc + '/figures/Transferfunction.eps')
    #inst.write(channel + 'OUTput 0')
    #print("########### FINISHED ###########")

    #plt.show()
