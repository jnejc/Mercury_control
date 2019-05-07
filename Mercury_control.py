import gui
import com
import tkinter as tk
import log

if __name__ == "__main__":
    '''Executes when this is the main aplication'''
    print('Starting main application Mercury_control')

    ## Initiate logging settings
    #logging.basicConfig(filename='log_files\\app.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    #logging.info('Starting log file')

    # Initiate the comport communication
    comports = com.ports.Ports()

    # Initiate gui interface
    root = tk.Tk()
    gui.main.Main_application(root, comports)
    root.mainloop()
