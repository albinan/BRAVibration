import csv
import numpy as np
import matplotlib.pyplot as plt
from linnearmodels import mod0001
data = []
header = ''
with open('meas.csv') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    header = header + next(reader)
    for row in reader:
        a = [float(i) for i in row]
        data.append(a)
data = np.asarray(data)

mod = mod0001()

print(header)
fs = 1

signal_in = data[:, 1]
signal_out = data[:, 0]
n = np.size(signal_in)
timestep = 0.0002
fs = 1/timestep
time = np.asarray(range(0, n, 1))*timestep

plt.subplot(211)
plt.plot(time, signal_in)
plt.plot(time, signal_out)
plt.subplot(212)
fftsignal_out = np.fft.fft(signal_out)
freq = np.fft.fftfreq(n, timestep)
fftsignal_in = np.fft.fft(signal_in)
plt.plot(freq, np.abs(fftsignal_out))
plt.plot(freq, np.abs(fftsignal_in))
fftsignal_prediction = np.abs(mod.H(freq, testRload=997))*np.abs(fftsignal_in)
signal_prediction = np.real(np.fft.ifft(fftsignal_prediction))
plt.plot(freq, np.abs(fftsignal_prediction))

plt.figure()
plt.plot(time, signal_out)
plt.plot(time, signal_prediction)

plt.figure()
plt.subplot(211)
plt.plot(freq, np.abs(fftsignal_prediction), '.')
plt.subplot(212)
plt.plot(freq, np.angle(fftsignal_prediction), '.')
plt.plot(freq, np.angle(fftsignal_in))
psd_pred = np.abs(fftsignal_prediction)**2/(n*fs)
psd_out = np.abs(fftsignal_out)**2/(n*fs)

rms_pred = np.sqrt(np.trapz(psd_pred, dx=freq[2]-freq[1]))
rms_meas = np.sqrt(np.mean(np.square(signal_out)))

print('Predicted rms in mW: ' + str(rms_pred**2*1000/997) + ' Meassured rms in mW: ' + str(rms_meas**2*1000/997) + ' Kvot: ' + str(rms_pred**2/rms_meas**2))
plt.show()
#fftsignal_prediction = self.H(freq)*fftsignal_in
#signal_prediction = np.fft.ifft(fftsignal_prediction)
