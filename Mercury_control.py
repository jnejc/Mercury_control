import gui
import com
import tkinter as tk

if __name__ == "__main__":
    '''Executes when this is the main aplication'''
    print('I am main, I think')

    comports = com.ports.Ports()

    root = tk.Tk()
    gui.main.Main_application(root, comports)
    root.mainloop()
