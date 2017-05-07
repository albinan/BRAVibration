
import tkinter as tk
from Loop import LOOPY
import ctypes
import numpy as np


class Win:
    def startbutton_callback(self):
        finterval = self.e_finterval.get()
        ginterval = self.e_ginterval.get()
        gerr = float(self.e_gerr.get())
        resistance = float(self.e_resistance.get())
        ######################################
        ######################################
        if self.folderLoc == "NoDir":
            ctypes.windll.user32.MessageBoxW(0, "Välj mapp där mätdatan kommer sparas", "Error", 1)
        else:
            LOOPY(finterval, ginterval, gerr, resistance, self.folderLoc)
        ######################################
        ######################################

    def savebutton_callback(self):
        self.folderLoc = tk.filedialog.askdirectory()
        print('Saving files to:', self.folderLoc)

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
        self.label_resistance = tk.Label(master, text="Resistans [Ohm]: ", font=textfont)
        self.e_finterval = tk.Entry(master, font=textfont, width = boxwidth)
        self.e_finterval.delete(0, tk.END)
        self.e_finterval.insert(0, "20.0,30.0,0.5")
        self.e_ginterval = tk.Entry(master, font=textfont, width = boxwidth)
        self.e_ginterval.delete(0, tk.END)
        self.e_ginterval.insert(0, "0.2,0.2,0.2")
        self.e_gerr = tk.Entry(master, font=textfont, width = boxwidth)
        self.e_gerr.delete(0, tk.END)
        self.e_gerr.insert(0, "0.01")
        self.e_resistance = tk.Entry(master, font=textfont, width = boxwidth)
        self.e_resistance.delete(0, tk.END)
        self.e_resistance.insert(0, "1000")

        self.label_finterval.grid(row=0, column=0)
        self.label_ginterval.grid(row=1, column=0)
        self.label_gerr.grid(row=2, column=0)
        self.label_resistance.grid(row=3, column=0)

        self.e_finterval.grid(row=0, column=1)
        self.e_ginterval.grid(row=1, column=1)
        self.e_gerr.grid(row=2, column=1)
        self.e_resistance.grid(row=3, column=1)
        self.startbutton = tk.Button(master, text="Starta mätning",font=buttonfont, command=self.startbutton_callback)
        self.startbutton.grid(row=4, column=1)
        self.savebutton = tk.Button(master, text="Välj mapp för att spara filer", font=buttonfont, command=self.savebutton_callback)
        self.savebutton.grid(row=4, column=0)
        self.formatbutton = tk.Button(master, text="Format", font=buttonfont, command=self.formatbutton_callback)
        self.formatbutton.grid(row=0, column=3)

        self.folderLoc = "NoDir"
root = tk.Tk()
w = Win(root)


root.mainloop()
