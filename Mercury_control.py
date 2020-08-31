import gui
import com
import tkinter as tk
import log
import logging
logger = logging.getLogger('log')     # Set the logger

if __name__ == "__main__":
    '''Executes when this is the main aplication'''
    logger.info('Starting main application Mercury_control')

    # Initiate the comport communication
    comports = com.ports.Ports()

    # Initiate gui interface
    root = tk.Tk()
    gui.main.Main_application(root, comports)
    root.mainloop()


