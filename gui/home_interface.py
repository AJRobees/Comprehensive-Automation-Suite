import tkinter as tk
import messagebox

from .gui_file_organizer import File_Organizer_GUI


class Home_Interface():
    def __init__(self):

        self.is_autoation_working = False
            
        # color schemes
        self.mid_blue = "#0A62A1"
        self.white = "white"
        self.milky_blue = "#B0D5EF"
        self.black = "black"

        self.root = tk.Tk()
        self.root.wm_title("Home panel")

        self.root.update() #update the window to display in centre.
        self.window_width = 450
        self.window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int(screen_width - self.window_width) // 2
        y = int(screen_height - self.window_height) // 2

        #formula = "(w) x (h) + (x) + (y)"
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}") #center the window on the screen

        self.main_frame = tk.Frame(self.root,bg=self.mid_blue,height=50,highlightcolor=self.white,
                    highlightthickness=1)

        self.toggle_btn = tk.Button(self.main_frame,text="≡",font=("Bold",20),
                            bg= self.mid_blue, fg=self.white,relief="flat",
                            activebackground=self.mid_blue,activeforeground=self.white, command=self.toggle_menu)
        self.toggle_btn.pack(side="left")

        title_label = tk.Label(self.main_frame, text="COMPREHENSIVE AUTOMATION SUITE", font=("Times New Roman Bold",14),
                            bg= self.mid_blue, fg=self.white, padx=10, pady=10)
        title_label.pack(side="left")

        self.main_frame.pack(side="top",fill="x")
        self.main_frame.pack_propagate(False)

        '''        
        self.content_frame = tk.Frame(self.root,height=600,width=500)
        self.content_frame.place_configure(x=0,y=50)
        self.content_frame.pack(side="left")
        self.content_frame.pack_propagate(False)
        '''
        self.root.mainloop()


    def toggle_menu(self):
        self.wn_width = self.root.winfo_width()
        self.wn_height = self.root.winfo_height()

        self.toggle_menu_fm = tk.Frame(self.root,bg=self.milky_blue,highlightcolor=self.black,
                        highlightthickness=2)
        self.toggle_menu_fm.place(x=0,y=50,width=200,height=self.wn_height)

        self.toggle_btn.config(text="X",command=self.collapse_toggle_menu)

        self.f_organizer_btn = tk.Button(self.toggle_menu_fm, text="File Organizer", relief="flat", font=("Times New Roman Bold",14),
                        bg= self.milky_blue, fg=self.black, activebackground=self.milky_blue, activeforeground=self.black,
                        command= lambda value ="file_organizer": self.launch_automation(value))
        self.f_organizer_btn.pack(pady=10,fill="x")

        self.w_scraper_btn = tk.Button(self.toggle_menu_fm, text="Web scraper", relief="flat", font=("Times New Roman Bold",14),
                        bg= self.milky_blue, fg=self.black, activebackground=self.milky_blue, activeforeground=self.black,
                        command= lambda value ="web_scraper": self.launch_automation(value))
        self.w_scraper_btn.pack(pady=10,fill="x")

        self.msg_label = tk.Label(self.toggle_menu_fm,text="Available in the future",font=("Times New Roman Bold",14),
                            bg= self.milky_blue, fg=self.black)
        self.msg_label.pack(pady=10)

        self.back_btn = tk.Button(self.toggle_menu_fm,text=" <── ", font=("Times New Roman Bold",14),
                                  bg= self.milky_blue, fg=self.black,relief="flat")
        self.back_btn.pack(padx=10,pady=10)

    def collapse_toggle_menu(self):
        self.toggle_menu_fm.destroy()
        self.toggle_btn.config(text="≡",command=self.toggle_menu)

    def home_page(self):

        self.collapse_toggle_menu()
        home_frame = tk.Frame(self.root)
        home_frame.pack()

        home_title = tk.Label(home_frame,text="Welcome",font=("Times New Roman Bold",16),)
        home_title.pack(anchor="center")
        self.content_frame.config(height=self.wn_height,width=self.wn_width)
        

    def launch_automation(self,automation_name):

        self.collapse_toggle_menu()

        if not self.is_autoation_working:
            self.is_autoation_working = True

            if automation_name == "file_organizer":
                self.automation = File_Organizer_GUI

            elif automation_name == "web_scraper":
                messagebox.showinfo("Maintainance","Web Scraper is under Development!")

            if automation_name != "web_scraper":
                self.mod = self.automation(self.root)

                self.mod.pack()

                # When closing the window(x) asks the confirmation and the confirmation function stays on it's module.
                self.root.protocol("WM_DELETE_WINDOW",self.mod.on_close) 

        elif self.is_autoation_working:
            messagebox.askyesno("warning !!",f"{automation_name} is already working, Want to stop? ")

            if True:
                self.mod.destroy()
                messagebox.showinfo("info",f"{automation_name} has been stopped.")
                self.is_autoation_working = False

