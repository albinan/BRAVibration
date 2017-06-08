import numpy as np

def ifprint(s, ts):
    if ts:
        print(s)
class mod0001():
    dm = 0
    def __init__(self):
        def mech_damping_dm(m, w_n, xi, a, Rcoil, Rload):
            dm = 2*m*w_n*xi - (a**2)/(Rload*(Rload + Rcoil))
            return dm
        def spring_const_k(w_n, m):
            k = (w_n**2)*m
            return k
        def emag_const_NBl(K, m, Rload, Rcoil):
            NBl = -K*(Rload + Rcoil)/Rload
            return NBl
        self.K = 314.411978426
        self.xi = 0.136453458646
        self.w_n = 2*np.pi*45.4006993251

        self.mass = 0.034
        self.Rcoil = 334
        self.k = spring_const_k(self.w_n, self.mass)
        self.kmeas = 2030
        self.testRload = 997
        self.NBl = emag_const_NBl(self.K, self.mass, self.testRload, self.Rcoil)
        self.dm = mech_damping_dm(self.mass, self.w_n, self.xi, self.NBl, self.Rcoil, self.testRload)

        self.Name = 'Testing harvester'
        self.TransferFunction = 'V/A = m*NBl*Rload*s/((ms**2 + (dm - (NBl)^2/Rload)*s + k)(Rload + Rcoil))'
        self.Color = 'Black'
        self.Spring = 'Instert name'
        self.SpringEquation = 'F = k*x, k = ' + str(self.k)
        self.islinnear = True
        self.Date = '08/02/2017'

    def H_generic(self, freq):
        w = 2*np.pi*freq
        return -self.K*1j*w/(self.w_n**2 - w**2 + 2*1j*self.w_n*self.xi*w)

    def H(self, freq, testRload=0,  m=0, k=0, dm=0, Rcoil=0, NBl=0, L=0, ts = False):
        if testRload  == 0:
            testRload = self.testRload
        if m == 0:
            m = self.mass
            ifprint('mass: '+ str(m), ts)
        if k == 0:
            k = self.k
            ifprint('spring constant: '+ str(k), ts)
        if dm == 0:
            dm = self.dm
            ifprint('mechanical damping: '+ str(dm), ts)
        if Rcoil == 0:
            Rcoil = self.Rcoil
            ifprint('resistance coil: '+ str(Rcoil), ts)
        if NBl == 0:
            NBl = self.NBl
            ifprint('NBl: '+ str(NBl), ts)
        s = 1j*2*np.pi*freq
        return m*NBl*testRload*s/((m*s**2 + dm*s + k)*(L*s + testRload + Rcoil) + (NBl)**2*s/testRload)

    def info(self):
        s = '--------------------------------------------------------------\n'
        s = s + 'Model name : ' + self.Name + '\n'
        s = s + 'Transfer Function : ' + self.TransferFunction + '\n'
        s = s + 'Spring : ' + self.Spring + '\n'
        s = s + '   Linnear spring : ' + str(self.islinnear) + '\n'
        s = s + '   Spring equation : ' + self.SpringEquation + '\n'
        s = s + '--------------------------------------------------------------'
        return s
