import gui
import com
import tkinter as tk

if __name__ == "__main__":
    '''Executes when this is the main aplication'''
<<<<<<< HEAD
    print('Starting main application Mercury_control')
=======
    print('I am main, I think')
>>>>>>> ce3e1b675b2e74bf118a890a489552465d36eff4

    comports = com.ports.Ports()

    root = tk.Tk()
    gui.main.Main_application(root, comports)
    root.mainloop()
