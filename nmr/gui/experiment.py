'''Experiment select frame'''

# Imports
import tkinter as tk    # Gui package
from tkinter import ttk # Fancier widgets
from tkinter import messagebox

import logging
logger = logging.getLogger('log')     # Set the logger



class Experiment_frame(tk.Frame):
    '''The Frame for selecting experiments or creating new'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=300, height=900, padx=5, pady=5)
        self.parent = parent

        self.Widgets()


    def Widgets(self):
        '''Shapes the frame's widgets'''
        # Label
        self.label_title = ttk.Label(self, text='Experiments')
        #self.label_title.config(font=('Courier', 16))
        self.label_title.pack(side='top', fill='x', padx=10)

        # Status frame
        self.frame_status = Status(self, self.ports)
        self.frame_status.pack(side='top', fill='x', padx=5, pady=5)

        # Set frame
        self.frame_set = SetF(self, self.ports)
        self.frame_set.pack(side='top', fill='x', padx=5, pady=5)

        # Switch frame
        self.frame_switch = Switch(self, self.ports)
        self.frame_switch.pack(side='top', fill='x', padx=5, pady=5)

        # Ramp frame
        self.frame_ramp = Ramp(self, self.ports)
        self.frame_ramp.pack(side='top', fill='x', padx=5, pady=5)

        # Sensor frame
        self.frame_sensors = Sensors(self, self.ports)
        self.frame_sensors.pack(side='top', fill='x', padx=5, pady=5)

        # Select frame
        self.frame_select = Select(self, self.ports)
        self.frame_select.pack(side='top', fill='x', padx=5 , pady=5)

        # Load parameters
        self.button_load = ttk.Button(self, text='Load from iPS',
            command=self.Load_parameters, width=20)
        self.button_load.pack(side='top',pady=10)


    def Load_parameters(self):
        '''Talks to IPS and refreshes all values in entry boxes'''
        logger.info('Loading IPS parameters from:'+ self.frame_select.var_sens.get())

        flog = self.ports.Get_Fstatus(self.frame_select.var_sens.get())
        fset = self.ports.Get_Fset(self.frame_select.var_sens.get())
        fmode = self.ports.Get_Fmode(self.frame_select.var_sens.get())
        fsensors = self.ports.Get_Fsensors(self.frame_select.var_sens.get(),
            self.frame_select.var_lvl.get(),self.frame_select.var_temp.get())

        self.frame_status.Update(flog)
        self.frame_set.Update(fset)
        self.frame_switch.Update(fmode[0])
        self.frame_ramp.Update(fmode[1])
        self.frame_sensors.Update(fsensors)
