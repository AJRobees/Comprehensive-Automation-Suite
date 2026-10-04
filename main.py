import time
import tkinter as tk
from modules import *

if __name__ == "__main__":

    organizer = File_Organizer()
    scraper = Web_Scraper()

    print("\nGreetings, \n")

    tried = 1

    def show_automation_menu():
        print("Automation tools: \n"
        "\n      1. File Organizer",
        "\n      2. Web Scraper",
        "\n      0. Exit")

    def get_choice():
            choice = (input("\nEnter your choice : ")).lower()
            return choice   

    def retry_attempt(tried):
        """
        Manage repeated invalid confirmation attempts.

        Allows the user to retry the confirmation process and asks whether to
        continue after the maximum number of attempts is reached.

        Returns:
            str or None: The user's decision when the retry limit is reached.
        """
        if tried >=3:
            decide = (input("\nWant to continue? (yes/no): ")).lower()
            tried = 0
            if decide == "no":
                return decide
            else:
                 retry_attempt(tried)
        tried+=1
        return tried

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

    def get_file_organizer():
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

    def get_web_scraper():

        url = "https://www.lifestylestores.com/in/en/SHOP-Casio-CASIO-Enticer-Stainless-Steel-Chronograph-Watch--A2318-For-Men/p/1000014190004"
        #url = "https://www.myntra.com/headphones/boat/boat-rockerz-371-wireless-over-ear-headphones/38208480/buy"
        validity,responce = scraper.run_scraper(url)
        if validity:
            element = input("\nWhat you want to search? : ")
            result_element = scraper.search_element(element)
            print("\n",responce,"\nSearch result: \n")

            try:
                print(f"      {len(result_element)} matches are found.\n")
                save_as_json(url=url,search=element,result=result_element)

                if len(result_element) !=0:
                    for item in result_element: print(item)
                
            except TypeError:
                print("Error: The HTML was failed to parse!!")

        else:
             print("\n",responce)

    def launch_interface(option):

        option_1 = ["1","cli"]
        option_2 = ["2","gui"]
        option_0 = ["0","exit","back"]

        automation_1 = ["1","organizer","file organizer"]
        automation_2 = ["2","scraper", "web scraper"]

        if option in option_1:
            print("\nLoading the Interface... \n")
            time.sleep(3)

            show_automation_menu()
            chosen = get_choice()

            if chosen in automation_1:
                get_file_organizer()
                return "continue"
            
            elif chosen in automation_2:
                get_web_scraper()
                return "continue"

            elif chosen in option_0:
                 return "exit"

        elif option in option_2:
            print("\n Loading the Interface... \n")
            time.sleep(3)
            print('Under development !\n')
            #title_name = File_Organizer_GUI
            #creation_window(title_name)
            time.sleep(1)
            return "continue"

        elif option in option_0:
             print("\nExiting automation....\n")
             time.sleep(2)
             return "exit"

        else:
            print("Invalid choice, try again!")
            return "retry"

    def show_interface_menu():
            print("Interface: \n"
            "\n      1. CLI",
            "\n      2. GUI",
            "\n      0. Exit")

    def show_title():
        print("-"*80)
        print("                    Comprehensive Automation Suite                  ")
        print("-"*80,"\n")

    def run_main():
        show_title()
        show_interface_menu()
        chosen = get_choice()
        result = launch_interface(chosen)
        return result

    while True:
        result = run_main()
        if result == "exit":
            break
        elif result == "retry":
            print("\nPlease select between 1/yes or 2/no. \nOR \nWait for 3 tries, Try ",tried)
            
            attempt = retry_attempt(tried)
            # Retry the confirmation until the user provides a valid choice or exits.
            if attempt == "no":
                tried = 1
                reply = "3 attempts are over, try again with valid choice."
            tried +=1

            if attempt != "no":
                run_main()

