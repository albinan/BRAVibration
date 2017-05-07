import numpy as np
from linnearmodels import mod0001
t = np.linspace(0, 1)
signal = 3*np.sin(3*2*np.pi*t)
timestep = t[2]-t[1]
n=signal.size
m = mod0001
print(m.H(m,-1), '|', m.H(m,1))
#f = [0, 1, ...,   n/2-1,     -n/2, ..., -1] / (d*n)   if n is even
#f = [0, 1, ..., (n-1)/2, -(n-1)/2, ..., -1] / (d*n)   if n is odd

import matplotlib.pyplot as plt
fftsignal_pos = np.fft.fft(signal)/n
freq = np.fft.fftfreq(n, timestep)

plt.figure()
plt.subplot(211)
plt.plot(freq, np.abs(fftsignal_pos),'.')
plt.subplot(212)
B = np.fft.ifft(fftsignal_pos)
plt.plot(t, signal)
plt.plot(t,B*n)
plt.show()
