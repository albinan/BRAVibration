import numpy as np
import visa
import time
import os
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
import threading
import sys
from aquire import aquire_type_constants
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB')
from playloop import WavePlayerLoop

class Oscilloscope():
    '''
    A class containing low and high level function for RIGOL DS1074Z.
    '''

    WRITE = 'w'
    READ = 'r'

    # AQUIRE TYPES
    NORMAL ='NORMal'
    AVERAGES = 'AVERages'
    PEAK ='PEAK'
    HIGH_RESOLUTION = 'HRESolution'


    AQUIRE_TYPE.normal
    def __init__(self, activeChannels=[2], oscillResource='USB0::0x1AB1::0x04CE::DS1ZD171500380::INSTR', wavlength=6, memdepth=12000, offset=0):
        print('__init__ oscill')
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(oscillResource)
        self.run()
        self.set_activeChannels(activeChannels)
        self.set_wavmode('RAW')
        self.set_wavform('ASCii')
        self.set_wavlength(wavlength)
        self.set_memdepth(memdepth)
        for channel in activeChannels:
            self.set_verticalOffset(channel, offset)

    # ----------SYSTEM COMMANDS----------

    def sys_auto_scale(self):
        '''
        Enable the waveform auto setting function.
        The oscilloscope will automatically adjust the vertical scale,
        horizontal timebase, and trigger mode according to the input signal to
        realize optimum waveform display.
        '''
        self.inst.write(':AUToscale')

    def sys_clear_screen(self):
        '''
        Clear all the waveforms on the screen.
        If the oscilloscope is in the RUN state, waveform will still be
        displayed.
        '''
        self.inst.write(':CLEar')

    def sys_run(self, willRun=True):
        '''
        The :RUN command starts the oscilloscope and the :STOP command stops
        the oscilloscope.
        '''
        # NOTE: When the waveform record function is enabled or during the
        # playback of the recorded waveform, these commands are invalid.
        # FIX BOOLEAN

        if willRun:
            self.inst.write(':RUN')
        elif not willRun:
            self.inst.write(':STOP')

    def sys_force_trigger(self):
        '''
        Generate a trigger signal forcefully
        '''
        # NOTE: This command is only applicable to the normal and
        # single trigger modes (see the :TRIGger:SWEep command)
        # FIX BOOLEAN
        self.inst.write(':TFORce')

    '''
    AQUIRE COMMANDS
    The :ACQuire commands are used to set and query the memory depth,
    acquisition mode and the number of averages as well as query the current
    sample rate of the oscilloscope.
    '''

    def aquire_averages(self, mode, count=2):
        '''
        Set or query the number of averages under the average acquisition mode.
        Averages 2^count times.
        '''
        #NOTE: count has to be an integer between 1 and 10

        if mode == self.WRITE:
            if isinstance(count, int) and (1 <= count <= 10):
                self.inst.write(':ACQuire:AVERages ' + str(count))
                return 1
            else:
                print('Cannot set averages to ' + str(2**count))
                return 0
        elif mode == self.READ:
            return int(self.inst.query(':ACQuire:AVERages?'))

    def aquire_set_memdepth_analog(self, memdepth):
        '''
        - When a single channel is enabled, the range of <mdep> is {AUTO|12000|
        120000|1200000|12000000|24000000}. Wherein, 24000000 (pts) is an
        optional memory depth.
        - When dual channels are enabled, the range of <mdep> is {AUTO|6000|
        60000|600000|6000000|12000000}. Wherein, 12000000 (pts) is an optional
        memory depth.
        - When three/four channels are enabled, the range of <mdep> is {AUTO|
        3000|30000|300000|3000000|6000000}. Wherein, 6000000 (pts) is an
        optional memory depth.
        '''
        # NOTE: Memory Depth = Sample Rate x Waveform Length
        # Wherein, the Waveform Length is the product of the horizontal
        # timebase (set by the :TIMebase[:MAIN]:SCALe command) times the number
        # of grids in the horizontal direction on the screen (12)
        activeChannels = self.get_activeChannels()
        print('Active channels: ', activeChannels)
        n_activeChannels = np.size(activeChannels)

        memdepth_set = 0
        if memdepth == 0:
            self.inst.write(':ACQuire:MDEPth AUTO')
        elif n_activeChannels == 1:
            allowed_mdepth = np.array([12000, 120000, 1200000, 12000000])
            memdepth_set = allowed_mdepth[np.argmin(
                           np.abs(allowed_mdepth-memdepth))]
            self.inst.write(':ACQuire:MDEPth ' + str(memdepth_set))
        elif n_activeChannels == 2:
            allowed_mdepth = np.array([6000, 60000, 600000, 6000000])
            memdepth_set = allowed_mdepth[np.argmin(
                            np.abs(allowed_mdepth-memdepth))]
            self.inst.write(':ACQuire:MDEPth ' + str(memdepth_set))
        elif n_activeChannels == 3 or n_activeChannels == 4:
            allowed_mdepth = np.array([3000, 30000, 300000, 3000000])
            memdepth_set = allowed_mdepth[np.argmin(
                           np.abs(allowed_mdepth-memdepth))]
            self.inst.write(':ACQuire:MDEPth ' + str(memdepth_set))

        if memdepth_set != self.aquire_get_memdepth_analog():
            print('Failed to set memory depth to ' + str(memdepth_set))
            return 0
        print('Successfully set memory depth to ' + str(memdepth_set))
        return 1

    def aquire_get_memdepth_analog(self):
        memdepth = self.inst.query(':ACQuire:MDEPth?')
        if memdepth == 'AUTO':
            return 0
        else:
            memdepth = int(memdepth)
            return memdepth

    def aquire_set_type(self, aq_type):
        '''
        NORMal: in this mode, the oscilloscope samples the signal at equal time
                interval to rebuild the waveform. For most of the waveforms,
                the best display effect can be obtained using this mode.
        AVERages: in this mode, the oscilloscope averages the waveforms from
                multiple samples to reduce the random noise of the input signal
                and improve the vertical resolution.
                The number of averages can be set by the:ACQuire:AVERages
                command.
                Greater number of averages can lower the noise and increase the
                vertical resolution, but will also slow the response of the
                displayed waveform to the waveform changes.
        PEAK (Peak Detect): in this mode, the oscilloscope acquires the maximum
                and minimum values of the signal within the sample interval to
                get the envelope of the signal or the narrow pulse of the
                signal that might be lost. In this mode, signal confusion can
                be prevented but the noise displayed would be larger.
        HRESolution (High Resolution): this mode uses a kind of ultra-sample
                technique to average the neighboring points of the sample
                waveform to reduce the random noise on the input signal and
                generate much smoother waveforms on the screen. This is
                generally used when the sample rate of the digital converter
                is higher than the storage rate of the acquisition memory.
        '''

        if aq_type in ['NORMal', 'AVERages', 'PEAK', 'HRESolution']:
            self.inst.write(':ACQuire:TYPE ' + aq_type)
            if aq_type in self.aquire_get_type():
                print('Successfully set aquire type to ' + str(aq_type))
                return 1
            else:
                print('Failed to set aquire type to' + str(aq_type))
        else:
            print('Invalid aquire_type')
            return 0

    def aquire_get_type(self):
        return self.inst.qurey(':ACQuire:TYPE?')

    def set_wavmode(self, wavmode):
        self.inst.write(':WAV:MODE ' + wavmode)
        self.wavmode = wavmode

    def set_verticalOffset(self, channel, offset):
        self.inst.write(':CHANnel:' + str(channel) + ':OFFSet ' + str(offset))

    def get_wavmode(self):
        return self.inst.query(':WAV:MODE?')

    def set_wavform(self, wavform):
        self.inst.write(':WAV:FORM ' + wavform)
        self.wavform = wavform

    def get_wavform(self):
        return self.inst.query(':WAV:FORM?')

    def get_output_frequency(self, channel):
        inst.write(':CHANnel:' + channel + 'FREQuency?')

    def run(self):
        self.inst.write(':RUN')
        time.sleep(1)

    def set_wavlength(self, t):
        '''
        Sets the oscilloscope window size to the closest possible value to t
        '''

        t_inc = np.array([0.000000005, 0.00000002, 0.00000005, 0.0000001,
                         0.0000005, 0.000001, 0.000005, 0.00002,
                         0.00005, 0.0001, 0.0005, 0.001,
                         0.005, 0.02, 0.05, 0.1,
                         0.5, 1, 2, 5, 20, 50])
        t_win = 12*t_inc
        t_set = t_inc[np.argmin(np.abs(t_win-t))]
        t_current = float(self.inst.query(':TIMebase:MAIN:SCALe?'))
        if t_set != t_current:
            self.inst.write(':TIMebase:MAIN:SCALe ' + str(t_set))
            time.sleep(2)
        self.wavelength = t_set*12

    def get_wavlength(self):
        return 12*float(self.inst.query(':TIMebase:MAIN:SCALe?'))

    def set_activeChannels(self, activeChannels):
        if np.max(activeChannels) < 1 or np.max(activeChannels) > 4:
            print('Invalid channel number')
        else:
            resid = list(set([1, 2, 3, 4]) ^ set(activeChannels))
            for i in activeChannels:
                self.inst.write(':CHANnel' + str(i) + ':DISPlay ON')
            for i in resid:
                self.inst.write(':CHANnel' + str(i) + ':DISPlay OFF')
                self.activeChannels = activeChannels

    def get_activeChannels(self):
        activeChannels = []
        for i in range(1, 5):
            if int(self.inst.query(':CHANnel' + str(i) + ':DISPlay?')):
                activeChannels.append(i)
        return activeChannels




    def set_sampleRate(self, fs):
        self.set_memdepth(fs*self.get_wavlength())
        self.sampleRate = self.get_sampleRate()

    def get_sampleRate(self):
        return float(self.inst.query(':ACQuire:SRATe?'))

    def amplifierCheck(self):
        """
        Checks if amplifier is set high and low enough to fit achieve g level
        """
        y = float(self.inst.query(':VOLTage?'))
        if y > 4.9:
            print('Increase level on amplifier')
            print('Waiting 7 seconds...')
            time.sleep(7)
        elif y < 21*1e-3:
            print('Decrease level on amplifier')
            print('Waiting 7 seconds...')
            time.sleep(7)

    def G2V(self, g, sf, s_handle):
        # Vpp: Voltage peak to peak
        # sf: scaling factor from voltage to g
        Vpp = g/(sf*s_handle)
        return Vpp

    def set_g(
          self, g_f, sf_vg, s_handle, g_err, iterations, k_p, checkAmplifier):

        # Initiation variables
        # The value of V that we want
        y_f = self.G2V(g_f, sf_vg, s_handle)
        # The value of V that we have
        y_0 = float(self.inst.query(':MEASure:ITEM? VRMS,CHANnel2'))
        # Variable we want to mimimize
        r = y_f-y_0

        y_err = self.G2V(g_err, sf_vg, s_handle)  # Tranlated error to V
        counter = 0

        while np.abs(r) > y_err:
            self.autotune_voltagescale('CHANnel1')
            self.autotune_voltagescale('CHANnel2')
            x = float(self.inst.query('VOLTage?')) + k_p*r

            if np.abs(x) < 1000:  # Can not set voltage to unreasonable value
                self.inst.write('VOLTage ' + str(x))

                if checkAmplifier:
                    # Checks if meassured voltage is greater or less
                    # than actual voltage
                    self.amplifierCheck(self.inst)

            time.sleep(1)

            self.autotune_voltagescale(self.inst, 'CHANnel1')
            self.autotune_voltagescale(self.inst, 'CHANnel2')
            # The value of V that we have
            y_0 = float(self.inst.query(':MEASure:ITEM? VRMS,CHANnel2'))
            r = y_f-y_0  # Variable we want to mimimize
            counter = counter + 1
            if counter > iterations:
                print('Too many iterations')
                return 0

        return 1

    def set_voltagescale(self, V, channel, margin=False):
        try:
            V_win = np.array(
                             [0.001, 0.002, 0.005, 0.01,
                              0.02, 0.05, 0.1, 0.2, 0.5,
                              1, 2, 5, 10])
            if margin:
                n_set = np.argmin(np.abs(V_win-V/8))
                if V > V_win[n_set]:
                    V_set = V_win[n_set + 1]
                else:
                    V_set = V_win[n_set]
            else:
                V_set = V_win[np.argmin(np.abs(V_win-V/8))]

            self.inst.write(':CHANnel' + str(channel) + ':SCALe ' + str(V_set))
        except Exception as e:
            print(e)

    def get_voltagescale(self, channel):
        V_win = 8*float(self.inst.query(':CHANnel' + str(channel) + ':SCALe?'))
        return V_win

    def autotune_voltagescale(self, channel):
        V_win = np.array(
         [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10])
        # p2p voltage divided by the number of divisions on screen
        V = float(self.inst.query(':MEASure:ITEM? VPP,'+channel))/8
        while V > 9999:
            V_current = float(self.inst.query(':' + channel + ':SCALe?'))
            if V_current > 6:
                print('Unexpected error')
                exit(0)
            V_set = V_win[np.argmin(np.abs(V_win-V_current)) + 1]
            print('Setting scale to ' + str(V_set) + ' V')
            self.inst.write(':' + channel + ':SCALe ' + str(V_set))
            time.sleep(3)
            print('Waiting in 3 seconds: Finding window size')
            V = float(self.inst.query(':MEASure:ITEM? VPP,'+channel))/8
        # We want the closest value above V for the window
        # so that the signal will fit.
        # We are thefore looking for the closest value above 0 in V_win - V.
        for i in range(np.size(V_win)):
            if (V_win[i] - V) < 0:
                V_win[i] = 9999

        V_set = V_win[np.argmin(V_win-V) + 1]

        V_current = float(self.inst.query(':' + channel + ':SCALe?'))
        # print('Voltage:' + str(V/8))
        # print('Voltage_set:' + str(V_set))
        # print('Voltage_current:' + str(V_current))
        if V_set != V_current:
            self.inst.write(':' + channel + ':SCALe ' + str(V_set))
            time.sleep(1)
            print('Waiting 1 second: Setting voltage scale')

    def snapshot(self):
        """
        Takes a snapshot of the screen while the instrument is running
        """
        print('snapshot oscill')
        self.t_inc = float(self.inst.query(':WAVeform:XINCrement?'))
        self.fs = 1/self.t_inc
        V_chan = []
        for channel in self.activeChannels:
            V_chan_tmp = []
            self.inst.write(':WAV:SOUR CHAN' + str(channel))
            V_chan_str = self.inst.query(':WAV:DATA?')
            V_chan_str = V_chan_str[11:].split(',')
            V_chan_tmp.extend([float(i) for i in V_chan_str])
            V_chan.append(V_chan_tmp)
            print(self.get_wavform())
            print(self.get_wavmode())
        n = np.size(V_chan[0])
        t = []
        t.append(np.asarray(range(0, n))*self.t_inc)
        data = np.transpose(np.vstack((t, V_chan)))
        return data

    def get_batch(self):
        """
        Returns a touple with batchsize and number of batches for reading data
        """
        wavform = self.get_wavform()
        print('waveform: ', wavform)
        if 'ASC' in wavform:
            memdepth = self.get_memdepth()
            if memdepth > 15625:
                return 15000, int(memdepth/15000)
            else:
                return memdepth, 1
        else:
            print('Set waveform to ASCii')

    def meas_RMS(self, channel):
        print(':MEASure:ITEM VRMS,CHANnel' + str(channel))
        Vrms = float(self.inst.query(
            ':MEASure:ITEM? VRMS,CHANnel' + str(channel)))
        if Vrms > 10000000000:
            return -1
        else:
            print('Vrms :', Vrms)
            return Vrms

    def meas_VPP(self, channel):
        print(':MEASure:ITEM VPP,CHANnel' + str(channel))
        Vpp = float(self.inst.query(
            ':MEASure:ITEM? VPP,CHANnel' + str(channel)))
        return Vpp

    def meas_frequency(self, channel):
        print(':MEASure:ITEM FREQuency,CHANnel' + str(channel))
        freq = float(self.inst.query(
            ':MEASure:ITEM? FREQuency,CHANnel' + str(channel)))
        if freq > 10000000000:
            return -1
        else:
            print('Vrms :', freq)
            return freq

    def record_init(self, rec_time, sampleRate):
        self.set_wavlength(rec_time, inc=0)
        self.set_sampleRate(sampleRate)

    def record(self, wavFileLoc, t_start, length):
        self.WPL = WavePlayerLoop(wavFileLoc, t_start=t_start, length=length)
        self.run()
        data = []
        self.inst.write('CLEAR')

        self.WPL.play()  # Playing signal
        timeStamp = time.time()
        time.sleep(self.wavelength*3/4)
        self.inst.write('STOP')
        time.sleep(self.wavelength/2)
        self.WPL.stop()
        batchsize, batches = self.get_batch()
        print('Active Channels', self.activeChannels)
        for channel in self.activeChannels:
            self.inst.write(':WAV:SOUR CHAN' + str(channel))
            time.sleep(1)
            dataTmp = []
            print('Wav source', self.inst.query(':WAVeform:SOURce?'))
            for i in range(0, batches):
                try:
                    print(i/batches)
                    self.inst.write(':WAV:STAR ' + str(i*batchsize + 1))
                    self.inst.write(':WAV:STOP ' + str((i+1)*batchsize))
                    V_chan1_str = self.inst.query(':WAV:DATA?')
                    V_chan1_str = V_chan1_str[11:].split(',')
                    dataTmp.extend([float(i) for i in V_chan1_str])
                except Exception as e:
                    print(e)
                    i = i - 1
            n_data = np.size(dataTmp)
            t = np.arange(0, n_data)*1/self.get_sampleRate()
            dataTmp = np.asarray(dataTmp)
            dataTmp = np.vstack((t, dataTmp))
            dataTmp = np.transpose(dataTmp)

            data.append(dataTmp)

        return data, timeStamp


        #S8. :WAV:STAR 125001 Set the start point of the second reading operation to the 125001th waveform point
        #S9. :WAV:STOP 250000 Set the stop point of the second reading operation to the 250000th waveform point
        #S10. :WAV:DATA? Read the data from the 125001th waveform point to the 250000th waveform point Perform the third reading operation
        #S11. :WAV:STAR 250001 Set the start point of the third reading operation to the 250001th waveform point
        #S12. :WAV:STOP 300000 Set the stop point of the third reading operation to the 300000th waveform point (the last point)
    def terminate(self):
        self.inst.close()
