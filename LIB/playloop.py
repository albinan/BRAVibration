import os
import wave
import threading
import sys
import time
import numpy as np
# PyAudio Library
import pyaudio


class WavePlayerLoop(threading.Thread):
    """
    A simple class based on PyAudio to play wave loop.
    It's a threading class. You can play audio while your application
    continues to do its stuff. :)
    """
    CHUNK = 1024

    def __init__(self, filepath, loop=True, t_start=0, length=1000000):
        """
        Initialize `WavePlayerLoop` class.
        PARAM:
            -- filepath (String) : File Path to wave file.
            -- loop (boolean)    : True if you want loop playback.
            False otherwise.
            """
        super(WavePlayerLoop, self).__init__()
        self.filepath = os.path.abspath(filepath)
        self.loop = loop
        self.timeStamp = 0
        self.t_start = t_start
        self.length = length

        # Open Wave File and start play!
        self.wf = wave.open(self.filepath, 'rb')
        self.player = pyaudio.PyAudio()
        # Open Output Stream (basen on PyAudio tutorial)
        devinfo = self.player.get_device_info_by_index(1)
        self.rate = self.wf.getframerate()
        if self.player.is_format_supported(float(self.rate)
                                     , input_device=devinfo['index']
                                     , input_channels=devinfo['maxInputChannels']
                                     , input_format=pyaudio.paInt16):
            print('Sample rate: ', self.rate, ' is supported')
        else:
            print('Sample rate ', self.rate, ' is not supported')
        print('Sample rate wav file: ', self.rate)
        self.stream = self.player.open(format=self.player.get_format_from_width(self.wf.getsampwidth())
                             , channels=self.wf.getnchannels()
                             , rate=self.rate
                             , output=True)

    def run(self):
        time.sleep(2) # Waiting for  oscilloscoe to clear
        # PLAYBACK LOOP
        startpos = int(np.round(self.rate*self.t_start))
        self.wf.setpos(startpos)
        n_frames = int(self.length*self.rate)
        if n_frames+startpos > self.wf.getnframes():
            n_frames = self.wf.getnframes()-startpos
        frames = self.wf.readframes(n_frames)
        self.timeStamp_start = time.time()
        self.stream.write(frames)
        self.timeStamp_stop = time.time()
        self.wf.close()
        self.stream.close()
        self.player.terminate()

    def play(self):
        """
        Just another name for self.start()
        """
        self.start()

    def stop(self):
         self.loop = False
