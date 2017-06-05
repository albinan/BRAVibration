import pyaudio
import wave
import numpy as np
import scipy.io.wavfile

t = np.linspace(0, 10, 10000000)
signalmeas = np.cos(50*2*np.pi*t)
signalmeas = np.uint8(signalmeas)

print(type(signalmeas[1]))
scipy.io.wavfile.write('testtest.wav', int(1/(t[1]-t[0])), signalmeas)


CHUNK = 1024

wf = wave.open('testtest.wav', 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)
for i in range(1, 10):
    stream.write(data)
    data = wf.readframes(CHUNK)
    if data == b'':
        print('rewind')
        wf.rewind()

stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
