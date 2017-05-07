import numpy as np
from readcsv import readcsvDir
import os
import matplotlib.pyplot as plt
from transferFunctions import G_harmonic, G_electric_gen_noL, H_noL
from optimize import errFun, errFunAmp
from linnearmodels import mod0001
import csv

def ifprint(s, ts):
    if ts:
        print(s)
if __name__ == '__main__':
    path = os.getcwd()
    data_train = readcsvDir(path + '/data/train', delim=',')
    nkt = np.shape(data_train)[0]  # Number of files in train data
    nits = 15 # Data point to start from.
    nite = np.shape(data_train)[1] - 15  # Data point to end at
    nit = nite - nits # Number of data points
    # data_train format:
    # 0  <  i  <=  nkt
    # data_train[i][:,0] : Frequency set on oscilloscope
    # data_train[i][:,1] : Frequency meassured from accelerometer
    # data_train[i][:,2] : Root mean square voltage meassured from accelerometer
    # data_train[i][:,3] : Frequency meassured from harvester output
    # data_train[i][:,4] : Root mean square meassured from harvester output
    # data_train[i][:,5] : Phase meassured between signal from accelerometer and
    #                      output from harvester

    data_validate = readcsvDir(path + '/data/validate', delim=',')
    # data_validate format:
    # 0  <  i  <=  n_data_validate
    # data_validate[:,0] : Time domain data of voltage from accelerometer
    # data_validate[:,1] : Time domain data of output voltage from harvester

    ### Calculate bode from train data
    freq =  np.zeros([nit, nkt])
    print(np.shape(freq))
    for i in range(0, nkt):
        freq[:, i] = data_train[i][nits:nite, 0]

    #f = freq[:, 0]
    ## Amplitude spectrum
    H_k = np.zeros([nit, nkt])
    for i in range(0, nkt):
        H_k[:, i] = np.divide(np.sqrt(2)*data_train[i][nits:nite, 4], data_train[i][nits:nite, 2])
    # Average of amplitude spectrum
    H_k_av = np.zeros(nit)
    for i in range(0, nkt):
        H_k_av = H_k_av + H_k[:, i]
    H_k_av = H_k_av/nkt

    ## Phase spectrum
    phi_k = np.zeros([nit, nkt])
    for i in range(0, nkt):
        phi_k[:, i] = -data_train[i][nits:nite, 5]
    # Average of phase specrtum
    phi_k_av = np.zeros(nit)
    for i in range(0, nkt):
        phi_k_av = phi_k_av + phi_k[:, i]
    phi_k_av = phi_k_av/nkt

    ##Plot Bode
    fig_bode = plt.figure(figsize=(11.69,8.27), dpi = 100)
    fig_bode.suptitle('Input: Driving acceleration = 0.2, 0.4, 0.6, 0.8 (g) \n Output: Voltage from harvester (V)\n ', size=16, fontweight='bold', style='italic')
    # Gain
    ax_gain = fig_bode.add_subplot(211)
    ax_gain.set_title('Amplitude response', size=18, fontweight='bold')
    ax_gain.set_ylabel('Magnitude |H| (dB)', size = 16)
    ax_gain.grid(True)
    ax_gain.plot(freq, 20*np.log(H_k), '.')
    # ax_gain.plot(freq, 20*np.log(H_k_av))
    # Phase
    ax_phase = fig_bode.add_subplot(212)
    ax_phase.set_title('Phase response', size=18, fontweight='bold')
    ax_phase.set_xlabel('Frequency (Hz)', size = 16)
    ax_phase.set_ylabel('Phase H$_{\phi}$ (deg)', size = 16)
    ax_phase.plot(freq, phi_k, '.')
    # plt.plot(freq, phi_k_av)
    ax_phase.grid(True)
    ## Fitting model



    f_n = 46
    xi = 0.139504643669
    K = 319.278485721

    with open('param.csv', newline='') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',')
     next(spamreader)
     for row in spamreader:
        K = float(row[0])
        xi = float(row[1])
        f_n = float(row[2])
    ### Train data
    # Bode plot meassurments as complex number
    S_k_train = H_k_av*np.exp(1j*phi_k_av*np.pi/180)

    #Calculate gradient and take one step
    delta_K = K/1000
    delta_xi = xi/1000
    delta_fn = f_n/1000

    S_mech = G_harmonic(freq[:, 0], f_n, xi)
    S_elec_gen = G_electric_gen_noL(freq[:, 0], K)
    S_model = H_noL(freq[:, 0], K, f_n, xi)
    # Error function with real and imaginary parts seperated
    err = (np.sum(np.abs(np.abs(S_k_train) - np.abs(S_model))) +
             np.sum(np.abs(np.angle(S_k_train) - np.angle(S_model))))/nit

    print('shape', np.shape(S_model), np.shape(S_k_train), np.shape(S_model-S_k_train))
    print('K: ', K, 'xi: ', xi,'Error: ', errFun(S_model, S_k_train))
    plt.figure()
    plt.subplot(211)
    plt.plot(freq[:, 0], np.abs(S_k_train), color='black')
    plt.plot(freq[:, 0], np.abs(S_model),'.', label='before')
    plt.subplot(212)
    plt.plot(freq[:, 0], np.angle(S_k_train), color='black')
    plt.plot(freq[:, 0], np.angle(S_model),'.')
    c = 1
    iterations = 100
    K_vec = np.zeros(iterations)
    xi_vec = np.zeros(iterations)
    f_n_vec = np.zeros(iterations)
    residual = np.zeros(iterations)
    df_ndres_vec = np.zeros(iterations)
    dKdres_vec = np.zeros(iterations)
    dxidres_vec = np.zeros(iterations)
    for i in range(0, iterations):
        # print('K: ', K, 'xi: ', xi, 'Error: ', errFun)
        K_vec[i] = K
        xi_vec[i] = xi
        f_n_vec[i] = f_n
        residual[i] = errFun(S_model, S_k_train)

        dKdres_vec[i] = (errFun(S_k_train, H_noL(freq[:, 0], K + delta_K, f_n, xi))
                - errFun(S_k_train, H_noL(freq[:, 0], K, f_n, xi)))/delta_K
        K = K - 100*dKdres_vec[i]

        dxidres_vec[i] = (errFun(S_k_train, H_noL(freq[:, 0], K, f_n, xi + delta_xi))
                - errFun(S_k_train, H_noL(freq[:, 0], K, f_n, xi)))/delta_xi
        xi = xi - 0.0001*dxidres_vec[i]

        df_ndres_vec[i] = (errFun(S_k_train, H_noL(freq[:, 0], K, f_n + delta_fn, xi))
                - errFun(S_k_train, H_noL(freq[:, 0], K, f_n, xi)))/delta_fn
        f_n = f_n - 0.001*df_ndres_vec[i]

        S_model = H_noL(freq[:, 0], K, f_n, xi)

    print('K: ', K, 'xi: ', xi, 'f_n', f_n, 'Error: ', errFun(S_model, S_k_train))
    with open('param.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['K', 'xi', 'f_n'])
        spamwriter.writerow([str(K), str(xi), str(f_n)])
    plt.subplot(211)
    plt.plot(freq[:,0], np.abs(S_model),'.',color='red', label='after')
    plt.grid(True)
    plt.legend()
    plt.subplot(212)
    plt.plot(freq[:,0],np.angle(S_model),'.', color='red')
    plt.grid(True)
    # Insert optimization algortihm here

    ax_gain.text(96, 4, 'Model: Black line' ' \n' r'$H(j \omega) = \frac{Kj \omega}{(\omega_n^2 - \omega^2) + 2j\omega \xi \omega}$' '\n' r'$K = '+ str(np.round(K, 2)) + '$' '\n' r'$\omega_n = 2\pi \cdot'+ str(np.round(f_n, 2)) + '$' '\n' r'$\xi = '+ str(np.round(xi, 3)) + '$', size = 14,
            bbox={'facecolor':'white', 'alpha':0.8, 'pad':5})
    ax_gain.plot(freq[:, 0], 20*np.log(np.abs(S_model)), color='black')

    ax_phase.plot(freq[:, 0], np.angle(S_model, deg=True), color='black')

    n_start = 10
    fig_graddesc_eval = plt.figure(figsize=(11.69,8.27), dpi = 100)
    ax_graddesc_eval = fig_graddesc_eval.add_subplot(211)
    ax_graddesc_eval.plot(K_vec[n_start:]/np.abs(np.max(K_vec)),'.', label = 'K')
    ax_graddesc_eval.plot(xi_vec[n_start:]/np.abs(np.max(xi_vec)),'.', label = 'xi')
    ax_graddesc_eval.plot(f_n_vec[n_start:]/np.abs(np.max(f_n_vec)),'.', label = 'f_n')
    ax_graddesc_eval.plot(residual[n_start:]/np.abs(np.max(residual)),'.', label = 'residual')
    plt.legend()
    ax_graddesc_eval = fig_graddesc_eval.add_subplot(212)
    ax_graddesc_eval.plot(df_ndres_vec[n_start:]/np.abs(np.max(df_ndres_vec[n_start:])), '.', label = 'f_n derivative')
    ax_graddesc_eval.plot(dxidres_vec[n_start:]/np.abs(np.max(dxidres_vec[n_start:])), '.', label = 'xi derivative')
    ax_graddesc_eval.plot(dKdres_vec[n_start:]/np.abs(np.max(dKdres_vec[n_start:])), '.', label = 'K derivative')
    plt.legend()


    #fig_model = plt.figure(figsize=(11.69,8.27), dpi = 100)
    #ax_mgain = fig_model.add_subplot(211)
    #ax_mgain.plot(freq[:,0], 20*np.log(np.abs(S_mech)))
    #ax_mgain.plot(freq[:,0], 20*np.log(np.abs(S_elec_gen)))
    #ax_mgain.plot(freq[:,0], 20*np.log(np.abs(S_elec_gen*S_mech)))
    #ax_mgain.grid(True)
    # ax_mgain.plot(freq, 20*np.log(H_k_av))

    #ax_mphase = fig_model.add_subplot(212)
    #ax_mphase.plot(freq[:,0], np.angle(S_mech, deg=True), label='Mechanical subsystem')
    #ax_mphase.plot(freq[:,0], np.angle(S_elec_gen, deg=True), label='Electrical subsystem')
    #ax_mphase.plot(freq[:,0], np.angle(S_elec_gen*S_mech, deg=True),label='Total system')
    #ax_mphase.grid(True)
    #plt.legend()
    plt.show()
    #fs = 2.0*1e-1
    #Vin = data_validate[:, 0]
    #n = np.size(Vin)
    #t = np.linspace(0, 2.1*0.025, n)
    #Vout = data_train[:, 1]

    #Vin_hat = np.fft.fft(Vin)/n
    #Vout_hat = np.fft.fft(Vout)/n
    #freq = np.fft.fftfreq(n, fs)
    #plt.figure()
    #plt.subplot(221)
    #plt.plot(Vin)
    #plt.grid(True)
    #plt.title('Signal (in)')
    #plt.subplot(222)
    #plt.plot(Vout)
    #plt.grid(True)
    #plt.title('Signal (out)')
    #plt.subplot(223)
    #plt.grid(True)
    #plt.plot(freq[0:n/2], np.abs(Vin_hat)[0:n/2])
    #plt.title('DFT Signal (in)')
    #plt.subplot(224)
    #plt.plot(freq[0:n/2], np.abs(Vout_hat)[0:n/2])
    #plt.title('DFT Signal (out)')
    #plt.grid(True)

    #V_pred_hat = np.zeros(np.size(freq), dtype=np.complex)
    #for f in enumerate(freq):
    #    V_pred_hat[f[0]] = G_harmonic(f[1]*2*np.pi, w_n, xi)*G_electric_gen_noL(2*np.pi*f[1], K)*Vin_hat[f[0]]




    #plt.figure()
    #plt.subplot(211)
    #plt.semilogy(freq[0:n/2], np.abs(Vout_hat)[0:n/2])
    #plt.subplot(212)
    #plt.semilogy(freq[0:n/2], np.abs(V_pred_hat)[0:n/2])
    #plt.show()

    print('finished')
