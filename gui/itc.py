'''Itc controlling frame'''

# Imports
import tkinter as tk    # Gui package
from tkinter import ttk # Fancier widgets
from tkinter import messagebox

from gui.funct import Strip_T, List_sensors



class ITC_frame(tk.Frame):
    '''The controll frame for ITC'''
    def __init__(self, parent, ports):
        tk.Frame.__init__(self, parent, width=300, height=900, padx=5, pady=5)
        self.parent = parent
        self.ports = ports
        self.Widgets()


    def Widgets(self):
        '''Shapes the frame's widgets'''
        # Label
        self.label_title = ttk.Label(self, text='Mercury iTC')
        self.label_title.config(font=('Courier', 16))
        self.label_title.pack(side='top', fill='x', padx=10)

        # Status frame
        self.frame_status = Status(self, self.ports)
        self.frame_status.pack(side='top', fill='x', padx=5, pady=5)

        # Set frame
        self.frame_set = SetT(self, self.ports)
        self.frame_set.pack(side='top', fill='x', padx=5, pady=5)

        # Loop frame
        self.frame_loop = Loop(self, self.ports)
        self.frame_loop.pack(side='top', fill='x', padx=5, pady=5)

        # Heater limits frame
        self.frame_limits = Limits(self, self.ports)
        self.frame_limits.pack(side='top', fill='x', padx=5, pady=5)

        # Select sensor frame
        self.frame_sensor = tk.Frame(self)
        self.frame_sensor.pack(side='top', fill='x', padx=5, pady=5)
        ttk.Label(self.frame_sensor, text='Sensor select').grid(row=0,
            column=0)
        ttk.Label(self.frame_sensor, text='  ').grid(row=0, column=1)
        self.grid_columnconfigure(1, weight=1) # Alows stretch and centering
        self.list_sens = List_sensors('TEMP', self.ports.itc)
        self.var_sens = tk.StringVar(self)
        self.var_sens.set('MB1.T1') # Default board
        self.combo_sens = ttk.Combobox(self.frame_sensor, width=7, state='readonly',
            values=self.list_sens, textvar=self.var_sens)
        self.combo_sens.grid(row=0, column=2)

        # Load parameters
        self.button_load = ttk.Button(self, text='Load from iTC',
            command=self.Load_parameters, width=20)
        self.button_load.pack(side='top',pady=5)


    def Load_parameters(self):
        '''Talks to ITC and refreshes all values in entry boxes'''
        print('Loading ITC parameters from', self.var_sens.get())
        tlog = self.ports.Get_Tstatus(self.var_sens.get())
        tset = self.ports.Get_Tset(self.var_sens.get())
        tloop = self.ports.Get_Tloop(self.var_sens.get())
        tlimits = self.ports.Get_Tlimits(self.var_sens.get(), tloop[3])

        self.frame_status.Update(tlog)
        self.frame_set.Update(tset)
        self.frame_loop.Update(tloop)
        self.frame_limits.Update(tlimits)

        print('Finished updating')



class Status(tk.LabelFrame):
    '''Status frame and inner objects'''
    def __init__(self, parent, ports):
        '''Calls init method of LabelFrame and fills up frame'''
        tk.LabelFrame.__init__(self, parent, text='Status', padx=10, pady=5)
        self.parent = parent
        self.ports = ports
        self.Widgets()


    def Widgets(self):
        '''Shapes the frame's widgets'''
        # Labels
        ttk.Label(self, text='Temperature').grid(row=0, column=0)
        ttk.Label(self, text='Setpoint').grid(row=0, column=2)

        ttk.Label(self, text='Heater %').grid(row=2, column=0)
        ttk.Label(self, text='Flow %').grid(row=2, column=2)

        # Spacer
        ttk.Label(self, text='  ').grid(row=0,column=1)
        self.grid_columnconfigure(1, weight=1) # Alows stretch and centering

        # Entries
        self.var_temp = tk.StringVar(self)
        self.entry_temp = ttk.Entry(self, textvariable=self.var_temp,
            justify='center', width=12, state='readonly')
        self.entry_temp.grid(row=1, column=0)

        self.var_tset = tk.StringVar(self)
        self.entry_tset = ttk.Entry(self, textvariable=self.var_tset,
            justify='center', width=12, state='readonly')
        self.entry_tset.grid(row=1, column=2)

        # Status bars
        self.var_heater = tk.IntVar(self)
        self.bar_heater = ttk.Progressbar(self, variable=self.var_heater,
            length=68)
        self.bar_heater.grid(row=3, column=0)

        self.var_flow = tk.IntVar(self)
        self.bar_flow = ttk.Progressbar(self, variable=self.var_flow,
            length=68)
        self.bar_flow.grid(row=3, column=2)

    
    def Update(self, tlog):
        '''Updates values from iTC'''
        print('Updating iTC status', tlog)
        self.var_temp.set(tlog[1])
        self.var_tset.set(tlog[2])
        self.var_heater.set(int(tlog[3]))
        try:
            self.var_flow.set(int(tlog[4]))
        except:
            self.var_flow.set(0)



class SetT(tk.LabelFrame):
    '''Set temperature frame and inner objects'''
    def __init__(self, parent, ports):
        '''Calls init method of LabelFrame and fills up frame'''
        tk.LabelFrame.__init__(self, parent, text='Set Temperature', padx=10,
            pady=5)
        self.parent = parent
        self.ports = ports
        self.Widgets()


    def Widgets(self):
        '''Shapes the frame's widgets'''
        # Labels
        ttk.Label(self, text='Set T:').grid(row=0, column=0, sticky='E')
        ttk.Label(self, text='Ramp rate:').grid(row=1, column=0, sticky='E')
        ttk.Label(self, text='Enable ramp').grid(row=2, column=0, sticky='E')
        ttk.Label(self, text='Flow control').grid(row=3, column=0, sticky='E')
        ttk.Label(self, text='Confirm').grid(row=4, column=0, sticky='E')

        ttk.Label(self, text='K').grid(row=0, column=3, sticky='W')
        ttk.Label(self, text='K/min').grid(row=1, column=3, sticky='W')

        # Spacer
        ttk.Label(self, text='  ').grid(row=0, column=1)
        self.grid_columnconfigure(1, weight=1) # Alows stretch and centering

        # Checkbuttons
        self.var_ramp = tk.BooleanVar(self)
        self.check_ramp = ttk.Checkbutton(self, variable=self.var_ramp)
        self.check_ramp.grid(row=2, column=2, columnspan=2)

        self.var_flow = tk.BooleanVar(self)
        self.check_flow = ttk.Checkbutton(self, variable=self.var_flow)
        self.check_flow.grid(row=3, column=2, columnspan=2)

        # Entries
        self.var_set = tk.StringVar(self)
        self.entry_set = ttk.Entry(self, width=7, textvariable=self.var_set,
            justify='right')
        self.entry_set.grid(row=0, column=2)

        self.var_rate = tk.StringVar(self)
        self.entry_rate = ttk.Entry(self, width=7, textvariable=self.var_rate,
            justify='right')
        self.entry_rate.grid(row=1, column=2)

        # Button
        self.button_set = ttk.Button(self, text='Set T',
            command=self.Set, width=10)
        self.button_set.grid(row=4, column=2, columnspan=2)


    def Set(self):
        '''Confirms written values and sends to iTC'''
        print('Setting Temperature')

    
    def Update(self, tset):
        '''Updates previously set values from iTC'''
        print('Updating previous set temperature values', tset)
        self.var_set.set(Strip_T(tset[0]))
        self.var_rate.set(Strip_T(tset[1]))
        self.var_ramp.set(True if tset[2] == 'ON' else False)
        self.var_ramp.set(True if tset[3] == 'ON' else False)



class Loop(tk.LabelFrame):
    '''Loop frame and inner objects'''
    def __init__(self, parent, ports):
        '''Calls init method of LabelFrame and fills up frame'''
        tk.LabelFrame.__init__(self, parent, text='Loop control', padx=10,
            pady=5)
        self.parent = parent
        self.ports = ports
        self.Widgets()


    def Widgets(self):
        '''Shapes the frame's widgets'''
        # Labels
        ttk.Label(self, text='P:').grid(row=0, column=0, sticky='E')
        ttk.Label(self, text='I:').grid(row=1, column=0, sticky='E')
        ttk.Label(self, text='D:').grid(row=2, column=0, sticky='E')
        ttk.Label(self, text='Heater').grid(row=3, column=0, sticky='E')
        ttk.Label(self, text='Aux').grid(row=4, column=0, sticky='E')

        ttk.Label(self, text='min').grid(row=1, column=3, sticky='W')
        ttk.Label(self, text='min').grid(row=2, column=3, sticky='W')

        # Spacer
        ttk.Label(self, text='  ').grid(row=0, column=1)
        self.grid_columnconfigure(1, weight=1) # Alows stretch and centering

        # Entries
        self.var_P = tk.StringVar(self)
        self.entry_P = ttk.Entry(self, width=7, textvariable=self.var_P,
            justify='right')
        self.entry_P.grid(row=0, column=2, sticky='E')

        self.var_I = tk.StringVar(self)
        self.entry_I = ttk.Entry(self, width=7, textvariable=self.var_I,
            justify='right')
        self.entry_I.grid(row=1, column=2, sticky='E')

        self.var_D = tk.StringVar(self)
        self.entry_D = ttk.Entry(self, width=7, textvariable=self.var_D,
            justify='right')
        self.entry_D.grid(row=2, column=2, sticky='E')

        # Combo box
        self.list_heat = List_sensors('HTR', self.ports.itc)
        self.var_heat = tk.StringVar(self)
        self.combo_heat = ttk.Combobox(self, width=8, state='readonly',
            values=self.list_heat, textvar=self.var_heat)
        self.combo_heat.grid(row=3, column=2, columnspan=2, sticky='W')

        self.list_aux = List_sensors('AUX', self.ports.itc)
        self.var_aux = tk.StringVar(self)
        self.combo_aux = ttk.Combobox(self, width=8, state='readonly',
            values=self.list_aux, textvar=self.var_aux)
        self.combo_aux.grid(row=4, column=2, columnspan=2, sticky='W')

        # Button
        self.button_set = ttk.Button(self, text='Set',
            command=self.Set, width=10)
        self.button_set.grid(row=5, column=0, columnspan=4)

    

    def Set(self):
        '''Confirms written values and sends to iTC'''
        print('Updating loop parameters')


    def Update(self, tloop):
        '''Updates values from iTC'''
        print('Updating loop control values', tloop)
        self.var_P.set(tloop[0])
        self.var_I.set(tloop[1])
        self.var_D.set(tloop[2])
        self.var_heat.set(tloop[3])
        self.var_aux.set(tloop[4])



class Limits(tk.LabelFrame):
    '''Limits frame and inner objects'''
    def __init__(self, parent, ports):
        '''Calls init method of LabelFrame and fills up frame'''
        tk.LabelFrame.__init__(self, parent, text='Heating limits', padx=10, pady=5)
        self.parent = parent
        self.ports = ports
        self.Widgets()


    def Widgets(self):
        '''Shapes the frame's widgets'''
        # Labels
        ttk.Label(self, text='Heater limit:').grid(row=0, column=0, sticky='E')
        ttk.Label(self, text='Max temp limit:').grid(row=1, column=0,
            sticky='E')
        ttk.Label(self, text='Min temp limit:').grid(row=2, column=0,
            sticky='E')

        ttk.Label(self, text='V').grid(row=0, column=3, sticky='W')
        ttk.Label(self, text='K').grid(row=1, column=3, sticky='W')
        ttk.Label(self, text='K').grid(row=2, column=3, sticky='W')

        # Spacer
        ttk.Label(self, text='  ').grid(row=0, column=1)
        self.grid_columnconfigure(1, weight=1) # Alows stretch and centering

        # Entries
        self.var_heat = tk.StringVar(self)
        self.entry_heat = ttk.Entry(self, width=7, textvariable=self.var_heat,
            justify='right')
        self.entry_heat.grid(row=0, column=2)

        self.var_tmax = tk.StringVar(self)
        self.entry_tmax = ttk.Entry(self, width=7, textvariable=self.var_tmax,
            justify='right')
        self.entry_tmax.grid(row=1, column=2)

        self.var_tmin = tk.StringVar(self)
        self.entry_tmin = ttk.Entry(self, width=7, textvariable=self.var_tmin,
            justify='right')
        self.entry_tmin.grid(row=2, column=2)

        # Button
        self.button_set = ttk.Button(self, text='Set',
            command=self.Set, width=10)
        self.button_set.grid(row=4, column=0, columnspan=4)


    def Set(self):
        '''Confirms written values and sends to iTC'''
        print('Setting heater limits')


    def Update(self, tlimits):
        '''Updates heating limits values from iTC'''
        print('Updating heating limits values', tlimits)
        self.var_heat.set(tlimits[0])
        self.var_tmax.set(Strip_T(tlimits[1]))
        self.var_tmin.set(Strip_T(tlimits[2]))
