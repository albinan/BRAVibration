from PyQt5 import QtWidgets
import sys
from importdata import guiimport
import numpy as np
from meas import snapsnot
import matplotlib.pyplot as plt
from win32api import GetSystemMetrics
from scipy.fftpack import fft, fftfreq
from scipy.integrate import cumtrapz
from scipy.signal import spectrogram
from linnearmodels import mod0001

class window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Data analysis
        self.data = []
        self.curdatanumber = 0
        self.header = []

        self.t = []
        self.a = []
        self.freq = []
        self.dft = []
        self.psd = []
        self.fs = []
        self.rms = []

        self.psdintegral = []

        self.inputFileLoc = []
        self.outputFolderLoc = ''

        vbox1 = QtWidgets.QVBoxLayout()
        vbox2 = QtWidgets.QVBoxLayout()
        titlehbox1 = QtWidgets.QHBoxLayout()
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        titlehbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()
        hbox32 = QtWidgets.QHBoxLayout()
        hbox35 = QtWidgets.QHBoxLayout()
        hbox4 = QtWidgets.QHBoxLayout()
        hbox5 = QtWidgets.QHBoxLayout()
        hbox6 = QtWidgets.QHBoxLayout()
        hbox7 = QtWidgets.QHBoxLayout()
        hbox9 = QtWidgets.QHBoxLayout()

        hbox10 = QtWidgets.QHBoxLayout()
        hbox = QtWidgets.QHBoxLayout(self)
        # Style settings
        titletext = 'font-size: 16pt; font-family: Sans;'
        buttontext = 'font-size: 14pt; font-family: Sans;'
        labeltext = 'font-size: 12pt; font-family: Sans;'
        edittext = 'font-size: 12pt; font-family: Sans;'
        dropdowntext = 'font-size: 10pt; font-family: Sans;'
        self.figsize  = (8.27,11.69)
        self.dpi = 100
        # ----- Title horizontal box 1-----
        # Enclosing import section
        importLabel = QtWidgets.QLabel( 'Import data from file or oscilloscope and choose output destination')
        importLabel.setStyleSheet(titletext)
        titlehbox1.addStretch()
        titlehbox1.addWidget(importLabel)
        titlehbox1.addStretch()

        # -----Horizontal box 1-----
        ## Contents: Import button and settings
        # Import button
        self.browse_inputFile_button = QtWidgets.QPushButton()
        self.browse_inputFile_button.setText(' Browse csvfile ')
        self.browse_inputFile_button.setStyleSheet(buttontext)
        self.browse_inputFile_button.clicked.connect(
            self.browse_inputFile_button_press)
        # Headerlines edit
        headerlines_Label = QtWidgets.QLabel('Headerlines: ')
        headerlines_Label.setStyleSheet(labeltext)
        self.headerlines_Edit = QtWidgets.QLineEdit('1')
        self.headerlines_Edit.setStyleSheet(edittext)
        self.headerlines_Edit.setFixedWidth(50)
        # Regular expression edit
        regExp_Label = QtWidgets.QLabel('Regular Expression: ')
        regExp_Label.setStyleSheet(labeltext)
        self.regExp_Edit = QtWidgets.QLineEdit('[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?')
        self.regExp_Edit.setStyleSheet(edittext)
        # Add content to Layout
        hbox1.addWidget(self.browse_inputFile_button)
        hbox1.addWidget(headerlines_Label)
        hbox1.addWidget(self.headerlines_Edit)
        hbox1.addWidget(regExp_Label)
        hbox1.addWidget(self.regExp_Edit)
        hbox1.addStretch()

        # -----Horizontal box 2-----
        ## Contents: Choose output folder button output folder label
        # Output folder button
        self.browse_outputFolder_button = QtWidgets.QPushButton()
        self.browse_outputFolder_button.setText(' Browse output folder ')
        self.browse_outputFolder_button.clicked.connect(
            self.browse_outputFolder_button_press)
        self.browse_outputFolder_button.setStyleSheet(buttontext)
        # Output location label
        self.browse_outputFolder_text = QtWidgets.QLabel()
        self.browse_outputFolder_text.setStyleSheet(labeltext)
        # Add content to Layout
        hbox2.addWidget(self.browse_outputFolder_button)
        hbox2.addStretch()
        hbox2.addWidget(self.browse_outputFolder_text)

        # ----- Title horizontal box 2-----
        # Enclosing choose data and analyze section
        datasetLabel = QtWidgets.QLabel('Choose dataset and analyze data')
        datasetLabel.setStyleSheet(titletext)
        titlehbox2.addStretch()
        titlehbox2.addWidget(datasetLabel)
        titlehbox2.addStretch()

        # -----Horizontal box 3 -----
        ## Contents: Choose current data set dropdown menu and label
        dropdownmenu_Label = QtWidgets.QLabel('Choose data set : ')
        dropdownmenu_Label.setStyleSheet(labeltext)
        self.dropdownmenu = QtWidgets.QComboBox()
        self.dropdownmenu.currentIndexChanged.connect(self.dataindex)
        self.dropdownmenu.setFixedWidth(int(GetSystemMetrics(0)/3))
        self.dropdownmenu.setStyleSheet(dropdowntext)

        self.cleardata_button = QtWidgets.QPushButton(' Clear data ')
        self.cleardata_button.clicked.connect(self.cleardata)
        self.cleardata_button.setStyleSheet(buttontext)
        # Add contents to layout
        hbox3.addStretch()
        hbox3.addWidget(dropdownmenu_Label)
        hbox3.addWidget(self.dropdownmenu)
        hbox3.addWidget(self.cleardata_button)
        hbox3.addStretch()
        # -----Horizontal box 3.5-----
        ## Contents: Scrollarea containing headerlines
        headerLabel = QtWidgets.QLabel('Header: ')
        headerLabel.setStyleSheet(labeltext)
        self.header_Edit = QtWidgets.QTextEdit()
        scrollArea1 = QtWidgets.QScrollArea()
        scrollArea1.setWidget(self.header_Edit)
        scrollArea1.setMaximumSize(GetSystemMetrics(0),
                    int(GetSystemMetrics(1)/8))
        self.header_Edit.setFixedSize(GetSystemMetrics(0),
                    int(GetSystemMetrics(1)/6))

        hbox35.addWidget(headerLabel)
        hbox35.addWidget(scrollArea1)
        # -----Horizontal box 4-----
        ## Contents: Table containing sample of data
        dataLabel = QtWidgets.QLabel('Data:    ')
        dataLabel.setStyleSheet(labeltext)
        self.table = QtWidgets.QTableWidget()
        hbox4.addWidget(dataLabel)
        hbox4.addWidget(self.table)
        # -----Horizontal box 5-----
        timecolumn_Label = QtWidgets.QLabel('Column with time data: ')
        timecolumn_Label.setStyleSheet(labeltext)
        self.timecolumn_Edit = QtWidgets.QLineEdit('1')
        self.timecolumn_Edit.setFixedWidth(50)
        self.timecolumn_Edit.setStyleSheet(edittext)
        scaleTime_Label = QtWidgets.QLabel('Factor to scale time to seconds: ')
        scaleTime_Label.setStyleSheet(labeltext)
        self.scaleTime_Edit = QtWidgets.QLineEdit('0.000001')
        self.scaleTime_Edit.setFixedWidth(150)
        self.scaleTime_Edit.setStyleSheet(edittext)

        acccolumn_Label = QtWidgets.QLabel('Columns with acceleration data: ')
        acccolumn_Label.setStyleSheet(labeltext)
        self.acccolumn_Edit = QtWidgets.QLineEdit('2,3,4')
        self.acccolumn_Edit.setFixedWidth(60)
        self.acccolumn_Edit.setStyleSheet(edittext)

        scaleAcc_Label = QtWidgets.QLabel('Factor to scale acceleration to g: ')
        scaleAcc_Label.setStyleSheet(labeltext)

        self.scaleAcc_Edit = QtWidgets.QLineEdit('1')
        self.scaleAcc_Edit.setFixedWidth(30)
        self.scaleAcc_Edit.setStyleSheet(edittext)
        hbox5.addWidget(timecolumn_Label)
        hbox5.addWidget(self.timecolumn_Edit)
        hbox5.addWidget(scaleTime_Label)
        hbox5.addWidget(self.scaleTime_Edit)
        hbox5.addStretch()
        hbox5.addWidget(acccolumn_Label)
        hbox5.addWidget(self.acccolumn_Edit)
        hbox5.addWidget(scaleAcc_Label)
        hbox5.addWidget(self.scaleAcc_Edit)
        hbox5.addStretch()
        #-----Horizontal box 6-----
        self.snapshot_button = QtWidgets.QPushButton()
        self.snapshot_button.clicked.connect(self.take_snapshot)
        self.snapshot_button.setText(' Take snapshot from oscilloscope ')
        self.snapshot_button.setStyleSheet(buttontext)

        snapshotchannels_Label = QtWidgets.QLabel('Channels used: ')
        snapshotchannels_Label.setStyleSheet(labeltext)
        self.snapshotchannels_Edit = QtWidgets.QLineEdit('1,2')
        self.snapshotchannels_Edit.setMaximumWidth(60)
        self.snapshotchannels_Edit.setStyleSheet(edittext)

        hbox6.addWidget(self.snapshot_button)
        hbox6.addWidget(snapshotchannels_Label)
        hbox6.addWidget(self.snapshotchannels_Edit)
        hbox6.addStretch()
        #-----Horizontal box 7-----
        self.analyze_button = QtWidgets.QPushButton(' Analyze data ')
        self.analyze_button.clicked.connect(self.analyze)
        self.analyze_button.setStyleSheet(buttontext)

        self.bandwidth_label = QtWidgets.QLabel('Bandwidth in Hz: ')
        self.bandwidth_label.setStyleSheet(labeltext)

        self.bandwidth_edit = QtWidgets.QLineEdit('1')
        self.bandwidth_edit.setStyleSheet(edittext)

        self.interval_label = QtWidgets.QLabel('Frequency interval in Hz: ')
        self.interval_label.setStyleSheet(labeltext)

        self.interval_edit = QtWidgets.QLineEdit('10,100')
        self.interval_edit.setStyleSheet(edittext)

        self.usealldata_checkbox = QtWidgets.QCheckBox('Use entire signal')
        self.usealldata_checkbox.setChecked(True)
        self.usealldata_checkbox.setStyleSheet(labeltext)

        self.clearallanalyzed_button = QtWidgets.QPushButton(' Clear all analyzed data ')
        self.clearallanalyzed_button.clicked.connect(self.clearanalyzeddata)
        self.clearallanalyzed_button.setStyleSheet(buttontext)

        hbox7.addStretch()
        hbox7.addWidget(self.bandwidth_label)
        hbox7.addWidget(self.bandwidth_edit)
        hbox7.addWidget(self.interval_label)
        hbox7.addWidget(self.interval_edit)
        hbox7.addWidget(self.analyze_button)
        hbox7.addWidget(self.usealldata_checkbox)

        hbox7.addStretch()
        hbox7.addWidget(self.clearallanalyzed_button)
        hbox7.addStretch()
        #-----Horizontal box 9-----
        self.plotdata_Edit = QtWidgets.QLineEdit()
        scrollArea2 = QtWidgets.QScrollArea()
        scrollArea2.setWidget(self.plotdata_Edit)
        scrollArea2.setMaximumSize(GetSystemMetrics(0),
                    int(GetSystemMetrics(1)/8))
        self.plotdata_Edit.setFixedSize(GetSystemMetrics(0),
                    int(GetSystemMetrics(1)/6))

        hbox9.addWidget(scrollArea2)
        #-----Horizontal box 10-----
        self.plotall_button = QtWidgets.QPushButton('Plot all analyzed data')
        self.plotall_button.clicked.connect(self.plotall)
        self.plotall_button.setEnabled(False)
        hbox10.addWidget(self.plotall_button)
        # ----- Add layouts to vertical box -----
        vbox1.addLayout(titlehbox1)
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox6)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(titlehbox2)
        vbox1.addLayout(hbox3)
        vbox1.addLayout(hbox32)
        vbox1.addLayout(hbox35)
        vbox1.addLayout(hbox4)
        vbox1.addLayout(hbox5)
        vbox1.addLayout(hbox7)
        vbox1.addLayout(hbox9)
        vbox1.addStretch()
        vbox1.addLayout(hbox10)
        vbox2.addStretch()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

    def cleardata(self):
        try:
            #self.data = []
            #self.curdatanumber = 0
            #self.header = []
            #self.inputFileLoc = []
            print('not finished')
        except Exception as e:
            print(e)
    def clearanalyzeddata(self):
        self.t = []
        self.a = []
        self.freq = []
        self.dft = []
        self.psd = []
        self.fs = []
        self.rms = []
        self.psdintegral = []
        self.plotdata_Edit.setText('')
        self.plotall_button.setEnabled(False)

    def plotall(self):
        try:
            print('Initializing plot')
            titlesize = 16
            labelsize = 14
            fig_signal = plt.figure(figsize=(8.27,11.69*2/3), dpi=self.dpi)
            ax_signal = fig_signal.add_subplot(111)
            axis = ['x', 'y', 'z', 'w']
            lineStyle = ['solid', 'dashed', 'dashdot', 'dotted']
            t_min = 10000
            t_max = 0
            print('Plotting time signal')
            for i in range(0, np.shape(self.t)[0]):
                for j in range(0, np.shape(self.a[i])[0]):
                    ax_signal.plot(self.t[i], self.a[i][j], label = str(axis[j]) + '-axis\n'
                                    + 'Sample frequency: ' + str(round(self.fs[i])) + ' Hz\n'
                                    + 'RMS: ' + "{0:0.2f}".format(self.rms[i][j]) + ' g\n'
                                    + 'Time of measurement: ' + "{:.2e}".format(self.t[i][-1] - self.t[i][0]) + ' s', linewidth=0.5)
                if self.t[i][-1] > t_max:
                    t_max = self.t[i][-1]
                if self.t[i][0] < t_min:
                    t_min = self.t[i][0]

            ax_signal.grid(b=True, which='major', linestyle='solid')
            ax_signal.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_signal.set_xlim(t_min, t_max)
            ax_signal.minorticks_on()
            ax_signal.set_title('Acceleration in time domain', fontsize=titlesize)
            ax_signal.set_xlabel('Time (s)', fontsize=labelsize)
            ax_signal.set_ylabel('Acceleration (g)', fontsize=labelsize)
            ymin, ymax = ax_signal.get_ylim()
            ax_signal.set_ylim(ymin, ymax*1.5)
            plt.legend(loc=2, ncol=2)

            fig_psd = plt.figure(figsize=self.figsize, dpi=self.dpi)
            ax_psd = fig_psd.add_subplot(311)
            ax_cumint = fig_psd.add_subplot(312)
            ax_psdbw = fig_psd.add_subplot(313)

            fig_model = plt.figure(figsize=self.figsize, dpi=self.dpi)
            ax_inputspectrum = fig_model.add_subplot(311)
            ax_model = fig_model.add_subplot(312)
            ax_outputspectrum = fig_model.add_subplot(313)
            cumint_max = 0
            bw = 1
            mod = mod0001()
            fmaxpsdbw = []
            maxpsdbw = []
            for i in range(0, np.shape(self.freq)[0]):
                n = np.size(self.t[i])
                n_bw = int(np.ceil(bw/(self.freq[i][1]-self.freq[i][0])))
                freq_pos = self.freq[i][1:int(n/2)]
                if np.mod(n_bw, 2) !=0:
                    n_bw = n_bw + 1
                for j in range(0, np.shape(self.dft[i])[0]):
                    print('Plotting PSD')
                    ax_psd.semilogy(freq_pos, self.psd[i][j], linewidth=0.5)
                    print('Plotting cummulative integral')
                    line = ax_cumint.plot(freq_pos, self.psdintegral[i][j], linewidth=1)
                    ax_cumint.plot([0, np.max(freq_pos)], [self.rms[i][j], self.rms[i][j]], color=line[0].get_color(), linestyle='dashed', linewidth=1)
                    print('Plotting PSDBW')
                    psdbw = self.psdintegral[i][j][int(n_bw):]-self.psdintegral[i][j][:-int(n_bw)]
                    fmin_interest = float(self.interval_edit.text().split(',')[0])
                    fmax_interest = float(self.interval_edit.text().split(',')[1])
                    print(fmin_interest, fmax_interest)
                    nmin_interest = np.argmin(np.abs(freq_pos-fmin_interest))
                    nmax_interest = np.argmin(np.abs(freq_pos-fmax_interest))
                    print(nmin_interest, nmax_interest)
                    if nmin_interest != nmax_interest:
                        maxpsdbw.append(np.max(psdbw[nmin_interest:nmax_interest]))
                    else:
                        print('hello')
                        maxpsdbw.append(np.max(psdbw))

                    print(j*i+j)
                    nmaxpsdbw = np.argmin(np.abs(psdbw-maxpsdbw[j*i+j]))
                    print(nmaxpsdbw)
                    fmaxpsdbw.append(freq_pos[nmaxpsdbw+int(n_bw/2)])

                    print('n_bw', n_bw)
                    ax_psdbw.semilogy(freq_pos[int(n_bw/2):-int(n_bw/2)], psdbw, linewidth=0.5,label=str(axis[j]) + '-axis, fmax = ' + str("{0:0.1f}".format(fmaxpsdbw[j*i+j])) + ' (Hz), gmax=' + "{0:0.3f}".format(maxpsdbw[j*i+j])+' (g)')
                    wmax = 2*np.pi*freq_pos[nmaxpsdbw]
                    kmax = wmax**2*mod.mass
                    H = mod.H(self.freq[i], k=kmax)
                    print('Calculating and plotting model')
                    Vfft_pred = np.abs(H)*np.exp(1j*np.angle(H)*np.pi/180)*np.abs(self.dft[i][j])*np.exp(1j*np.angle(self.dft[i][j])*np.pi/180)
                    print('1')
                    Vpsd_pred = np.abs(Vfft_pred)**2/(n*self.fs[i])
                    print('2')
                    Vrms_pred = np.sqrt(np.trapz(Vpsd_pred, dx=freq_pos[2]-freq_pos[1]))
                    print('3')
                    Prms_pred = Vrms_pred**2/mod.testRload
                    print('4')
                    ax_inputspectrum.semilogy(freq_pos, 2*np.abs(self.dft[i][j][1:int(n/2)]), label=str(axis[j]) +'-axis', linewidth=0.5)
                    print('5')
                    ax_outputspectrum.semilogy(freq_pos, 2*np.abs(Vpsd_pred[1:int(n/2)]), label=str(axis[j]) +'-axis, P_avg = ' +"{0:0.2f}".format(Prms_pred*1000)+' mW' , linewidth=0.5)
                    print('6')
                    ax_model.plot(freq_pos, 2*np.abs(H[1:int(n/2)]), label='Model V(jw)/g(jw), data ' + str(i) + ' ' + str(axis[j]) +'-axis', linewidth=1)

                    if np.max(self.psdintegral[i][j]) > cumint_max:
                        cumint_max = np.max(self.psdintegral[i][j])

            fmin_interest = float(self.interval_edit.text().split(',')[0])
            fmax_interest = float(self.interval_edit.text().split(',')[1])
            print('hurrdurr')
            print(fmin_interest)
            print(fmax_interest)
            ax_psd.set_title('Acceleration Spectral Density', fontsize=titlesize)
            ax_psd.set_ylabel('ASD (g^2/Hz)', fontsize=labelsize)

            ax_psd.set_xlim(fmin_interest, fmax_interest)
            ax_psd.set_xticklabels([])
            ax_psd.grid(b=True, which='major', linestyle='solid')
            ax_psd.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_psd.minorticks_on()
            print('6')
            ax_cumint.set_title('Integral of Acceleration Spectral Density', fontsize=titlesize)
            ax_cumint.set_ylabel('Acceleration (g)', fontsize=labelsize)
            ax_cumint.set_xlim(fmin_interest, fmax_interest)
            ax_cumint.set_ylim(0, cumint_max*1.2)
            ax_cumint.set_xticklabels([])
            ax_cumint.grid(b=True, which='major', linestyle='solid')
            ax_cumint.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_cumint.minorticks_on()
            print('7')
            ax_psdbw.set_title('Integral of ASD with ' + str(bw) +' Hz Bandwidth', fontsize=titlesize)
            ax_psdbw.set_ylabel('Acceleration (g)', fontsize=labelsize)
            ax_psdbw.set_xlabel('Frequency (Hz)', fontsize=labelsize)
            ax_psdbw.grid(b=True, which='major', linestyle='solid')
            ax_psdbw.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_psdbw.set_xlim(fmin_interest, fmax_interest)
            ylim = ax_psdbw.get_ylim()
            ax_psdbw.minorticks_on()
            ax_psdbw.legend(loc=2)
            #for f in fmaxpsdbw:
            #    ax_psdbw.plot([f, f], [ylim[0], ylim[1]], color='k', linestyle='dashed', linewidth=1)


            print('8')
            ax_inputspectrum.set_title('Input spectrum (DFT)', fontsize=titlesize)
            ax_inputspectrum.set_ylabel('Acceleration (g)', fontsize=labelsize)
            ax_inputspectrum.grid(b=True, which='major', linestyle='solid')
            ax_inputspectrum.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_inputspectrum.set_xlim(fmin_interest, fmax_interest)
            ax_inputspectrum.minorticks_on()
            ax_inputspectrum.set_xticklabels([])

            ax_model.set_title('Model of harvester', fontsize=titlesize)
            ax_model.set_ylabel('H(jw)=G(jw)/V(jw) (g/V)', fontsize=labelsize)
            ax_model.grid(b=True, which='major', linestyle='solid')
            ax_model.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_model.set_xlim(fmin_interest, fmax_interest)
            ax_model.minorticks_on()
            ax_model.set_xticklabels([])

            ax_outputspectrum.set_title('Estimated output voltage over ' + str(mod.testRload) +' Ohm load', fontsize=titlesize)
            ax_outputspectrum.set_ylabel('Estimated voltage (V)', fontsize=labelsize)
            ax_outputspectrum.set_xlabel('Frequency (Hz)', fontsize=labelsize)
            ax_outputspectrum.grid(b=True, which='major', linestyle='solid')
            ax_outputspectrum.grid(b=True, which='minor', linestyle='dashed', linewidth=0.2)
            ax_outputspectrum.set_xlim(fmin_interest, fmax_interest)
            ymin, ymax = ax_outputspectrum.get_ylim()
            ax_outputspectrum.set_ylim(ymin, ymax*100)
            ax_outputspectrum.legend(loc=2, ncol=2)
            ax_outputspectrum.minorticks_on()
            print('what')
            #f, t2, Sxx = signal.spectrogram(x, Fs, nperseg = Fs/4)
            #fig_spectrogram = plt.figure(figsize=(8.27,11.69*2/3), dpi=self.dpi)
            #ax_spectrogram = fig_spectrogram.add_subplot(111)
            #ax_spectrogram.pcolormesh(t2, f, np.log(Sxx))
            #ax_spectrogram.set_ylabel('Frequency (Hz)')
            #ax_spectrogram.xlabel('Time (sec)')
            plt.show()
        except Exception as e:
            print(e)
    def take_snapshot(self):
        outputFolderLoc = self.outputFolderLoc
        if self.outputFolderLoc != '':
            print('what')
            data, header, fileLoc = snapsnot(outputFolderLoc, self.snapshotchannels_Edit.text())
            self.data.append(data)
            self.header.append(header)
            self.inputFileLoc.append(fileLoc)
            self.dropdownmenu.addItem(fileLoc)
        else:
            print('Choose ouput folder')

    def dataindex(self, k):
        print(k)
        self.curdatanumber = k
        self.header_Edit.setText(self.header[k])
        ni, nj = np.shape(self.data[k])
        if ni > 10:
            ni = 10

        self.table.setRowCount(ni)
        self.table.setColumnCount(nj)
        for i in range(0, ni):
            for j in range(0, nj):
                itemij = QtWidgets.QTableWidgetItem(
                    str(self.data[k][i, j]))
                self.table.setItem(i, j, itemij)

    def browse_inputFile_button_press(self):
        try:
            a = guiimport()
            a.headerlines = 1
            a.filetype = '*.csv *.txt'
            a.headerlines = int(self.headerlines_Edit.text())
            a.regExp = self.regExp_Edit.text()
            self.data.append(a.importdata())
            self.header.append(a.header)
            self.inputFileLoc.append(a.fileLoc)
            self.dropdownmenu.addItem(self.inputFileLoc[-1][0])
        except Exception as e:
            print(e)

    def browse_outputFolder_button_press(self):
        folderLoc = QtWidgets.QFileDialog.getExistingDirectory()
        try:
            self.browse_outputFolder_text.setText(folderLoc)
            self.outputFolderLoc = folderLoc
        except Exception as e:
            print(e)

    def analyze(self):
        try:
            print('Initializing analysis')
            # Create local time variable and convert to seconds
            print('Creating time vector')
            t = self.data[self.curdatanumber][:, int(self.timecolumn_Edit.text())-1]
            scaletoseconds=float(self.scaleTime_Edit.text())
            print('Scaling to seconds ' + str(scaletoseconds) )
            t = t*scaletoseconds
            n = np.size(t) # Number of samples

            # Create proper time vector with same sample frequency
            if t[100] > t[0]: # If t vector does not reset in interval
                timestep = (t[9999]-t[0])/10000 # Average of 10 samples in case of unequal samplewidth
            else:
                timestep = (t[19999]-t[10000])/10000
            t = np.asarray(range(0, n))*timestep # Easier to deal with np array

            acccolumns = self.acccolumn_Edit.text().split(',') # Acceleration
                # column numbers from ui

            if not self.usealldata_checkbox.isChecked():
                # Get subinterval from time data
                fig_getinval = plt.figure(figsize=self.figsize, dpi=150)
                ax_getinval = fig_getinval.add_subplot(111)
                a_max = 0
                a_min = 0

                for col in acccolumns:
                    i = int(col)-1 # Columns start with index 1 in gui
                    a = self.data[self.curdatanumber][:, i]

                    if np.max(a) > a_max:
                        a_max = np.max(a)
                    if np.min(a) < a_min:
                        a_min = np.min(a)
                    ax_getinval.plot(t/60, a)

                ax_getinval.set_xlabel('Time (min)')
                ax_getinval.set_ylabel('Acceleration (g)')
                ax_getinval.set_xlim(t[0]/60, t[-1]/60)
                ax_getinval.set_ylim(a_min, a_max)

                t1, t2 = plt.ginput(2)
                n1 = np.argmin(np.abs(t-t1[0]*60))
                n2 = np.argmin(np.abs(t-t2[0]*60))
                if n1 > n2:
                    n1, n2 = n2, n1
                t = t[n1:n2]

            if np.mod(np.size(t), 2) != 0: # Vector has to have even number of elements for fft indexing
                t = t[:-1]
            t = t # Start time vector from 0
            n = np.size(t) # Redefining number of elements from new interval
            fs = 1/timestep # Sampling frequency
            dft = []    # List with each element containing dft from analyzed column
            psd = []    # List with each element containing asd from analyzed column
            psdintegral = [] # List with each element containing integral of psd from analyzed column

            signal = [] # List with each element containing acceleration from analyzed column
            rms = [] # List with each element containing rms of signal from analyzed column
            freq = fftfreq(n, timestep) # Frequency spectrum
            counter = 1
            for col in acccolumns: # Loop through all columns specified from gui
                i = int(col)-1 # Gui index starts from 1
                print('Creating acceleration vector ' + str(counter) + ' out of ' + str(np.size(acccolumns)))
                counter += 1
                a = self.data[self.curdatanumber][:, i]
                if not self.usealldata_checkbox.isChecked():
                    a = a[n1:n2]
                print('Removing mean')
                a = a - np.mean(a)
                print('Making vector even')
                if np.mod(np.size(a), 2) != 0:
                    a = a[:-1]
                print('Calculating rms')
                rms.append(rootMeanSquare(a))
                print('Calculating discrete fourier transform')
                afft = fft(a)
                print('Calculating acceleration spectral density')
                apsd = np.abs(afft)**2/(fs*n)
                apsd = 2*apsd[1:int(n/2)]
                #afft = 2*afft[1:int(n/2)]
                print('Integrating psd')
                apsdintegral = np.sqrt(cumtrapz(apsd, freq[1:int(n/2)], initial=0))

                signal.append(a)
                dft.append(afft)
                psd.append(apsd)
                psdintegral.append(apsdintegral)

            print('Saving data to work session')
            self.t.append(t)
            self.a.append(signal)
            self.freq.append(freq)
            self.dft.append(dft)
            self.psd.append(psd)
            self.psdintegral.append(psdintegral)
            self.fs.append(fs)
            self.rms.append(rms)
            print(self.rms)

            self.plotdata_Edit.setText(self.plotdata_Edit.text() + '\n' +
                self.inputFileLoc[self.curdatanumber][0] + 'SIGNAL/PSD/CUMINT')




            self.plotall_button.setEnabled(True)



        except Exception as e:
            print(e)

def rootMeanSquare(a):
    rms = 0
    N = np.size(a)
    for i in range(0, N):
        rms = rms + a[i]**2
    rms = rms/N
    rms = np.sqrt(rms)
    return rms
app = QtWidgets.QApplication(sys.argv)
a = window()
a.showMaximized()

#fileLoc = QFileDialog.getOpenFileName(filter='*.csv')
sys.exit(app.exec_()) # Magic after return statement? Pls explain
