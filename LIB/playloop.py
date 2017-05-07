import os
import wave
import threading
import sys
import time

# PyAudio Library
import pyaudio


class WavePlayerLoop(threading.Thread):
    """
    A simple class based on PyAudio to play wave loop.
    It's a threading class. You can play audio while your application
    continues to do its stuff. :)
    """
    CHUNK = 1024

    def __init__(self, filepath, loop=True):
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

    def run(self):
        time.sleep(1)
        # Open Wave File and start play!
        wf = wave.open(self.filepath, 'rb')
        player = pyaudio.PyAudio()
        # Open Output Stream (basen on PyAudio tutorial)
        devinfo = player.get_device_info_by_index(1)
        rate = wf.getframerate()
        if player.is_format_supported(float(rate)
                                     , input_device=devinfo['index']
                                     , input_channels=devinfo['maxInputChannels']
                                     , input_format=pyaudio.paInt16):
            print('Sample rate: ', rate, ' is supported')
        else:
            print('Sample rate ', rate, ' is not supported')
        print('Hellooooooooo')
        print('Sample rate: ', rate)
        stream = player.open(format=player.get_format_from_width(wf.getsampwidth())
                             , channels=wf.getnchannels()
                             , rate=rate
                             , output=True)

        # PLAYBACK LOOP
        self.timeStamp = time.time()
        data = wf.readframes(self.CHUNK)
        while self.loop:
            stream.write(data)
            data = wf.readframes(self.CHUNK)
            if data == '':  # If file is over then rewind.
                wf.rewind()
                data = wf.readframes(self.CHUNK)
        stream.close()
        player.terminate()

    def play(self):
        """
        Just another name for self.start()
        """
        self.start()

    def stop(self):
        """
        Stop playback.
        """
        self.loop = False
        return self.timeStamp

    def whatsTheTime(self):
        return self.time
