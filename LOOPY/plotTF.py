import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 100)
y = np.sin(t)

R = 1000
ax = plt.figure(None, figsize=(11.69, 8.27), dpi=100)
plt.plot(t, y)
titlefont = {'family' : 'normal',
            'size'   : 16}
labelfont = {'family' : 'normal',
            'size'   : 14}

plt.title('Power as a function of frequency, load resistance R = '+ str(R) +' (${\Omega_{rms}}$)', **titlefont)
plt.xlabel('Frequency (Hz)', **labelfont)
plt.ylabel('Power (mW)', **labelfont)
plt.show()
