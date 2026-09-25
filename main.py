import time
import tkinter as tk
from modules import *
from gui import * 

if __name__ == "__main__":

    organizer = File_Organizer()

    print("\nGreetings, \n")
    chosen_interface = (input("Select the Process Interface, \n 1. CLI \n 2. GUI \n 3. Exit : ")).lower()
    print("\n Loading the Interface... \n")
    time.sleep(1)

    def creation_window(title_name):         # Function that common for the GUI module like calculator, timer and stopwatch
            
            window = tk.Tk()
        
            window.title(title_name) #set the title of the window
            window.resizable(0,0) #Not allow the window to resize
    
            mod = title_name(window)
    
            window.update() #update the window to display the buttons
            window_width = window.winfo_reqwidth()
            window_height = window.winfo_reqheight()
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = int(screen_width - window_width) // 2
            y = int(screen_height - window_height) // 2
    
            #formula = "(w) x (h) + (x) + (y)"
            window.geometry(f"{window_width}x{window_height}+{x}+{y}") #center the window on the screen
    
            window.wm_geometry(f"{550}x{650}+{x}+{y}")
    
            mod.pack()
            # When closing the window(x) asks the confirmation and the confirmation function stays on it's module.
            #window.protocol("WM_DELETE_WINDOW",mod.on_close)       
            window.mainloop()
           

    if chosen_interface == "1":
        try:
            print('Initialzing File organizer...\n')
            time.sleep(1)
            necessary_data,preview_records = organizer.manage_file_organizer()

            organizer_terminal_report(necessary_data)

            if len(necessary_data["dir_files"]) != 0:
                show_organizer_preview(preview_records)
                decision = organizer.move_confirmation(preview_records)
                print("\n",decision,"\n")

            print("                 ","*"*40,"\n")

        except TypeError:
            print("Invalid target path !!")

    elif chosen_interface == "2":
        print('Initialzing File organizer...\n')
        title_name = File_Organizer_GUI
        creation_window(title_name)
        time.sleep(1)

    else:
        print("Exit")

    
