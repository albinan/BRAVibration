
import tkinter as tk
from tkinter import filedialog
from Loop import LOOPY, findOptFreq, findOptRes
import ctypes
import numpy as np
import sys
sys.path.append('C:/Users/ReVibe/Documents/Albin/BRAVibration/LIB')
from arduino import arduino_potentiometer_single

class Win:
    def startbutton_callback(self):
        finterval = self.e_finterval.get()
        ginterval = self.e_ginterval.get()
        gerr = float(self.e_gerr.get())
        R_vec = self.e_resistance.get()
        R_vec = R_vec.split(',')
        R_vec = list(map(float, R_vec))

        ######################################
        ######################################
        if self.folderLoc == "NoDir":
            ctypes.windll.user32.MessageBoxW(0, "Välj mapp där mätdatan kommer sparas", "Error", 1)
        else:
            LOOPY(finterval, ginterval, R_vec, gerr, self.folderLoc)
        ######################################
        ######################################

    def savebutton_callback(self):
        self.folderLoc = filedialog.askdirectory()
        print('Saving files to:', self.folderLoc)

    def zeroResbutton_callback(self):
        arduino = arduino_potentiometer_single(Rcirc=0)
        arduino.set_resistance(0)
        arduino.terminate

    def findOptFreqbutton_callback(self):
        finterval = self.e_finterval.get()
        finterval = finterval.split(',')
        finterval = list(map(float, finterval))

        ginterval = self.e_ginterval.get()
        ginterval = ginterval.split(',')
        ginterval = list(map(float, ginterval))

        g_err = float(self.e_gerr.get())

        Rinterval = self.e_resistance.get()
        Rinterval = Rinterval.split(',')
        Rinterval = list(map(float, Rinterval))
        print(ginterval, Rinterval)
        if ginterval[0] == ginterval[1] and Rinterval[0] == Rinterval[1]:
            ginterval = self.e_ginterval.get()
            finterval = self.e_finterval.get()
            f_opt = findOptFreq(finterval, ginterval, Rinterval,  g_err)
            self.e_resistance.delete(0, tk.END)
            self.e_resistance.insert(0, str(f_opt))
        else:
            print('**********************************************')
            print('Frequency, Acceleration and Resistance has to be constant')
            print('**********************************************')

    def findOptResbutton_callback(self):
        finterval = self.e_finterval.get()
        finterval = finterval.split(',')
        finterval = list(map(float, finterval))

        ginterval = self.e_ginterval.get()
        ginterval = ginterval.split(',')
        ginterval = list(map(float, ginterval))

        g_err = float(self.e_gerr.get())

        Rinterval = self.e_resistance.get()
        Rinterval = Rinterval.split(',')
        Rinterval = list(map(float, Rinterval))
        print(ginterval, Rinterval)
        if ginterval[0] == ginterval[1] and finterval[0] == finterval[1]:
            ginterval = self.e_ginterval.get()
            finterval = self.e_finterval.get()
            f_opt = findOptRes(finterval, ginterval, Rinterval,  g_err)
            self.e_finterval.delete(0, tk.END)
            self.e_finterval.insert(0, str(f_opt))
        else:
            print('**********************************************')
            print('Frequency, Acceleration and Resistance has to be constant')
            print('**********************************************')
    def formatbutton_callback(self):
        print("---------FORMAT AV FREKVENSINTERVALL-------------------")
        print("*********Ett intervall*********************************")
        print("Varje intervall skrivs som minfreqvens,maxfrekvens,steglängd.")
        print("----- Ex: 18.0,19.0,0.2 ger frekvenserna 18.0 18.2 18.4 18.6 18.8 och 19.0")
        print("*********Flera intervall*******************************")
        print("Olika intervall separeras med ;")
        print("----- Ex: 18.0,19.0,0.5;19.2,20,0.2;20.5,21,0.5 ger:")
        print("----- 18.0 18.5 19.0 19.2 19.4 19.6 19.8 20 20.5 21")
        print("*********Kommentarer***********************************")
        print("Punkt används som avgränsare. Ex: 18.3")
        print("Vill man loopa baklänges är steglängden negativ")
        print("----- Ex: 19.0,18.0,-0.2 ger 19.0 18.8 18.6 18.4 18.2 18.0")
    def __init__(self, master):
        textfont = ("Courier", 13)
        buttonfont = ("Courier", 13)
        boxwidth = 50
        self.master = master
        self.master.resizable(width=False, height=False)
        self.label_finterval = tk.Label(master, text="Frekvensintervall [Hz]: ", font=textfont)
        self.label_ginterval = tk.Label(master, text="Accelerationsintervall [g]: ", font=textfont)
        self.label_gerr = tk.Label(master, text="Maximalt mätfel [g]: ", font=textfont)
        self.label_resistance = tk.Label(master, text="Resistansintervall [Ohm]: ", font=textfont)
        self.label_tot_res = tk.Label(master, text="Total resistans utan potentiometer [Ohm]: ", font=textfont)
        self.e_finterval = tk.Entry(master, font=textfont, width = boxwidth)
        self.e_finterval.delete(0, tk.END)
        self.e_finterval.insert(0, "40,40,0.1")
        self.e_ginterval = tk.Entry(master, font=textfont, width = boxwidth)
        self.e_ginterval.delete(0, tk.END)
        self.e_ginterval.insert(0, "0.2,0.2,0.2")
        self.e_gerr = tk.Entry(master, font=textfont, width = boxwidth)
        self.e_gerr.delete(0, tk.END)
        self.e_gerr.insert(0, "0.01")
        self.e_resistance = tk.Entry(master, font=textfont, width = boxwidth)
        self.e_resistance.delete(0, tk.END)
        self.e_resistance.insert(0, "1300,1300,40")

        self.e_tot_res = tk.Entry(master, font=textfont, width = boxwidth)
        self.e_tot_res.delete(0, tk.END)
        self.e_tot_res.insert(0, "67")

        self.label_finterval.grid(row=0, column=0)
        self.label_ginterval.grid(row=1, column=0)
        self.label_gerr.grid(row=2, column=0)
        self.label_resistance.grid(row=3, column=0)
        self.label_tot_res.grid(row=4, column=0)

        self.e_finterval.grid(row=0, column=1)
        self.e_ginterval.grid(row=1, column=1)
        self.e_gerr.grid(row=2, column=1)
        self.e_resistance.grid(row=3, column=1)
        self.e_tot_res.grid(row=4, column=1)



        self.zeroResbutton = tk.Button(master, text="Nollställ potentiometer", font=buttonfont, command=self.zeroResbutton_callback)
        self.zeroResbutton.grid(row=4, column=2)

        self.findOptFreq_button = tk.Button(master, text="Hitta egenfrekvens", font=buttonfont, command=self.findOptFreqbutton_callback)
        self.findOptFreq_button.grid(row=0, column=2)

        self.findOptRes_button = tk.Button(master, text="Hitta optimal resistans", font=buttonfont, command=self.findOptResbutton_callback)
        self.findOptRes_button.grid(row=3, column=2)

        self.startbutton = tk.Button(master, text="Starta mätning", font=buttonfont, command=self.startbutton_callback)
        self.startbutton.grid(row=5, column=1)
        self.savebutton = tk.Button(master, text="Välj mapp för att spara filer", font=buttonfont, command=self.savebutton_callback)
        self.savebutton.grid(row=5, column=0)
        self.formatbutton = tk.Button(master, text="Format", font=buttonfont, command=self.formatbutton_callback)
        self.formatbutton.grid(row=0, column=3)

        self.folderLoc = "NoDir"
root = tk.Tk()
w = Win(root)


root.mainloop()
