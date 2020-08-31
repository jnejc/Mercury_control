'''Log frame'''

# Imports
import tkinter as tk    # Gui package
from tkinter import ttk # Fancier widgets
from tkinter import messagebox
# Plotting
import matplotlib
matplotlib.use('TkAgg') # Selects tkinter backend
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
    NavigationToolbar2Tk)
from matplotlib.figure import Figure
# Logging
import datetime # A format for dates and time
import csv # For importing and exporting CSV files
import os # For compiling directory paths

import logging
logger = logging.getLogger('log')     # Set the logger

class Log_frame(tk.Frame):
    '''The plotting and logging frame'''
    def __init__(self, parent, ports):
        tk.Frame.__init__(self, parent, width=1000, height=900)
        self.parent = parent
        self.ports = ports
        self.Widgets()


    def Widgets(self):
        '''Shapes the frame's widgets'''
        self.plot1 = Temperature_plot(self, self.ports)
        self.plot1.pack(side='top', fill='both', expand=True)

        self.plot2 = Field_plot(self, self.ports)
        self.plot2.pack(side='top', fill='both', expand=True)



class Log_plot(tk.Frame):
    '''The base for single plot frame'''
    def __init__(self, parent, ports):
        tk.Frame.__init__(self, parent, padx=5, pady=5)
        self.parent = parent
        self.ports = ports

        # Set parameters
        self.y_len = len(self.y_list)

        # Build widgets
        self.Widgets()

    
    def Widgets(self):
        '''Places the widgets and plot'''
        # Label
        self.label_title = tk.Label(self, text=self.title)
        self.label_title.config(font=('Courier', 16))
        self.label_title.pack(side='top')

        # Control buttons frame
        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.pack(side='top', fill='x')
        self.Buttons()

        self.Plot_setup()


    def Plot_setup(self):
        ''' Creates the plot and main settings'''
        # Plot canvas
        self.fig = Figure(figsize=(5,3), dpi=100)
        self.axes = self.fig.add_subplot(111)
        #self.fig.subplots_adjust(bottom=0.16, left= 0.10, right=0.96, top=0.94)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
        self.canvas._tkcanvas.pack(side='top', fill='both', expand=True)

        # Settings
        self.axes.grid()
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel(self.y_axis)

        # Prepare data lists
        self.x = [datetime.datetime.now()]
        self.y = [[0] for i in self.y_list]

        self.lines = list()

        date_format = matplotlib.dates.DateFormatter('%H:%M:%S')
        self.axes.xaxis.set_major_formatter(date_format)
        for i,trace in enumerate(self.y):
            logger.debug(self.x, trace)
            line, = self.axes.plot(self.x, trace, 'o-', label=self.y_list[i])
            self.lines.append(line)
        self.fig.autofmt_xdate(rotation=30)

        # Add legends
        self.axes.legend()


    def Buttons(self):
        '''The logging control buttons'''
        # Calling functions
        def Start_log(event=None):
            '''Starts the logging'''
            self.button_log['text'] = 'Stop log'
            self.button_log['command'] = Stop_log
            self.logging = self.button_log.after(10, Log)


        def Stop_log(event=None):
            '''Interrupts the logging'''
            self.button_log['text'] = 'Start log'
            self.button_log['command'] = Start_log
            self.button_log.after_cancel(self.logging)
            self.logging = None # Removes reference to logging event


        def Log():
            '''Actions to do for every log, and call next repetition'''
            log = self.Update()

            # Add to log file
            self.Write_log(log)

            # Add to plot lists
            self.x.append(log[0])
            for i in range(self.y_len):
                self.y[i].append(float(log[i+1][:-1]))
                self.lines[i].set_ydata(self.y[i])
                self.lines[i].set_xdata(self.x)
            self.axes.relim()
            self.axes.autoscale_view() 
            self.canvas.draw() # Redraw canvas

            # Continue logging
            self.logging = self.button_log.after(self.time, Log)


        def Change_time(event=None):
            '''Change of logging interval, as option is selected from box'''
            logger.info('Logging interval changed to: '+self.var_time.get())
            self.time = self.dict_times[self.var_time.get()]
            # Logs now and continues with new interval
            if self.button_log['text'] == 'Stop log':
                self.button_log.after_cancel(self.logging)
                self.logging = self.button_log.after(10, Log)


        def Clear_plot(event=None):
            '''Clears all but the last point in the plot and replots'''
            self.x = [self.x[-1]]
            for i in range(self.y_len):
                self.y[i] = [self.y[i][-1]]
                self.lines[i].set_ydata(self.y[i])
                self.lines[i].set_xdata(self.x)
            self.axes.relim()
            self.axes.autoscale_view() 
            self.canvas.draw() # Redraw canvas


        # Buttons
        self.button_log = ttk.Button(self.frame_buttons, text='Start log',
            command=Start_log)
        self.button_log.pack(side='left')

        # Select frequency
        ttk.Label(self.frame_buttons, text='  Interval: ').pack(side='left')
        self.dict_times = {'5s':5000, '20s':20000, '1m':60000,
            '5m':5*60*1000, '20m':20*60*1000, '1h':60*60*1000}
        self.var_time = tk.StringVar(self)
        self.var_time.set('20s') # Default interval
        self.time = self.dict_times[self.var_time.get()]
        self.combo_time = ttk.Combobox(self.frame_buttons, width=7,
            state='readonly', values=list(self.dict_times.keys()),
            textvar=self.var_time)
        self.combo_time.pack(side='left')
        self.combo_time.bind("<<ComboboxSelected>>", Change_time)

        # Button Clear plot
        self.button_clear = ttk.Button(self.frame_buttons, text='Clear plot',
            command=Clear_plot)
        self.button_clear.pack(side='right')


    def Write_log(self, log):
        '''Writes the log data into a log file'''
        file_name = log[0].strftime('%Y%m%d')+ self.file_end
        file_path = os.path.join(self.file_directory, file_name)

        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            # Add line
            line = []
            line.append(log[0].strftime('%H:%M:%S'))
            for i in log[1:]: # Also writes heater value
                line.append(i)
            writer.writerow(line)



class Field_plot(Log_plot):
    '''Inherits the Log plot framwork and holds Field plot specifics'''
    def __init__(self, parent, ports):
        '''Adds the field frame specifics, then initializes the log plot'''
        self.device = 'ips'
        self.title = 'Field log'
        self.y_axis = 'Field (T)'
        self.y_list = ['Set F', 'Current F', 'Peristent F']
        self.file_end = '_Field.log'

        # Create log directory
        self.file_directory = os.path.join('log_files','field')
        try:
            os.mkdir('log_files')
            os.mkdir(self.file_directory)
        except: pass

        Log_plot.__init__(self, parent, ports)


    def Update(self):
        '''Requests data from ips and adds to plot'''
        sensor = self.parent.parent.ips_frame.frame_select.var_sens.get()
        flog = self.ports.Get_Flog(sensor)
        logger.debug(flog)
        return flog



class Temperature_plot(Log_plot):
    '''Inherits the Log plot framwork and holds Field plot specifics'''
    def __init__(self, parent, ports):
        '''Adds the field frame specifics, then initializes the log plot'''
        self.device = 'itc'
        self.title = 'Temperature log'
        self.y_axis = 'Temperature (K)'
        self.y_list = ['Set T', 'Current T']
        self.file_end = '_Temp.log'

        # Create log directory
        self.file_directory = os.path.join('log_files','temperature')
        try:
            os.mkdir(self.file_directory)
        except: pass

        Log_plot.__init__(self, parent, ports)
        
    
    def Update(self):
        '''Requests data from itc and adds to plot'''
        sensor = self.parent.parent.itc_frame.var_sens.get()
        tlog = self.ports.Get_Tlog(sensor)
        logger.debug(tlog)
        return tlog