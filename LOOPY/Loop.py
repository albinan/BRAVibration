# NOTE  CHANNEL1 HAS TO MEASSURE VOLTAGE OVER HARVESTER
#       CHANNEL2 HAS TO MEASSURE VOLTAGE OVER G

import numpy as np
import visa
from V2G import V2G
# from G2V import G2V
from set_timescale import set_timescale
from set_voltagescale import set_voltagescale
from set_g import set_g
import time
import matplotlib.pyplot as plt
import os
from createArray import createArray
def LOOPY(fs, gs, g_err, Resistance, folderLoc):
    # Make directories for saving data
    if not os.path.exists(folderLoc+'/figures'):
        os.makedirs(folderLoc+'/figures')
        print('Creating folder: '+folderLoc+'/figures')
    if not os.path.exists(folderLoc+'/data'):
        os.makedirs(folderLoc+'/data')
        print('Creating folder: '+folderLoc+'/data')
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
    f_vec = createArray(fs, isFreqency=True)
    g_vec = createArray(gs, isFreqency=False)
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
# Check if amplifier spans the needed g levels
    iterations_test = 25  # More iterations needed when going from max(g_vec) to gmin
    print('Checking if amplifier is set high enough...')
    inst.write(channel + 'OUTput 1')
    inst.write(channel + 'FREQuency ' + str(max(f_vec)))
    set_timescale((num_periods/num_tbox)/max(f_vec), inst)
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
# Looping
    N_i = np.size(f_vec)
    N_j = np.size(g_vec)
    Vrms_vec_in = np.ones([N_i, N_j])
    freq_in = np.ones([N_i, N_j])

    Vrms_vec_out = np.ones([N_i, N_j])
    freq_out = np.ones([N_i, N_j])
    phase_out = np.ones([N_i, N_j])

    HEADER = 'Frequency, Frequency_g, g, Frequency_V, RMS_V, Phase_V'
    j = 0
    counter = 1
    for g in g_vec:
        i = 0
        inst.write(':TRIGger:EDGe:SOURce CHANnel2')
        inst.write(':TRIGger:EDGe:SLOPe POS')
        inst.write(':TRIGger:EDGe:LEVel ' + str(g/10))
        time.sleep(3)
        for f in f_vec:
            set_voltagescale(inst, 'CHANnel1')
            set_voltagescale(inst, 'CHANnel2')
            set_timescale((num_periods/num_tbox)/f, inst)
            set_g(g, inst, sf_vg, s_handle, g_err, iterations, k_p, checkAmplifier=False)
            time.sleep(1)
            print("---------DATA---------")
            print("Meassurment " + str(counter) + " out of " + str(N_i*N_j))
            Vrms_vec_in[i, j] = float(
                inst.query(':MEASure:ITEM? VRMS,CHANnel2'))
            freq_in[i, j] = float(
                inst.query(':MEASure:ITEM? FREQuency,CHANnel2'))

            Vrms_vec_out[i, j] = float(
                inst.query(':MEASure:ITEM? VRMS,CHANnel1'))
            phase_out[i, j] = float(
                inst.query(':MEASure:ITEM? RPHase,CHANnel2,CHANnel1'))
            freq_out[i, j] = float(
                inst.query(':MEASure:ITEM? FREQuency,CHANnel1'))

            print("Vrms_out: " + str(Vrms_vec_in[i, j]) +
            ", G-level: " + str(V2G(Vrms_vec_in[i, j], sf_vg, s_handle)) +
            ", Power: " + str(np.square(Vrms_vec_out[i, j])*1000/Resistance) +
            ", Frequency: " + str(f))

            inst.write(channel + 'FREQuency ' + str(f))
            i = i + 1
            counter = counter + 1
        filename_g = filename + "g" + str(g*100) + '.csv'

        output = np.hstack((f_vec.reshape(N_i, 1), freq_in[0:, j].reshape(N_i, 1),
                                Vrms_vec_in[0:, j].reshape(N_i, 1), freq_out[0:, j].reshape(N_i, 1),
                                Vrms_vec_out[0:, j].reshape(N_i, 1), phase_out[0:, j].reshape(N_i, 1)))
        np.savetxt(
            folderLoc + "/data/" + filename_g, output, delimiter=',', newline='\n', header=HEADER)
        j = j + 1

    # Plotting and saving data
    titlefont = {'size': 16}
    labelfont = {'size': 14}
    plt.figure(None, figsize=(11.69, 8.27), dpi=100)  # A4 size 100 dpi
    k = 0
    for g in g_vec:
        lab = str(g) + ' (g)'
        plt.plot(f_vec[1:], np.square(Vrms_vec_out[1:, k])*1000/Resistance,
                 label=lab)
        plt.grid(True)
        plt.legend(loc='upper right', prop={'size': 14})
        k = k + 1
    plt.title('Power as a function of frequency, load resistance R = '
              + str(np.round(Resistance)) + ' (${\Omega}$)', **titlefont)
    plt.xlabel('Frequency (Hz)', **labelfont)
    plt.ylabel('Power (mW)', **labelfont)
    plt.savefig(folderLoc + '/figures/Transferfunction.png')
    plt.savefig(folderLoc + '/figures/Transferfunction.eps')
    inst.write(channel + 'OUTput 0')
    k = 0
    print("########### FINISHED ###########")

    plt.show()
