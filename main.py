"""
Entry point for the Comprehensive Automation Suite.

This module initializes the automation tools and provides the main
application flow for selecting an interface and an automation tool.
It supports command-line and graphical interfaces, with options to
run the File Organizer, use the CLI Web Scraper, or exit the application.
"""
import time
from modules import *
from gui.home_interface import Home_Interface

if __name__ == "__main__":

    organizer = File_Organizer()
    scraper = Web_Scraper()


    print("\nGreetings, \n")

    tried = 1

    def show_automation_menu():
        """
        Display the available automation tools in the command line.

        Lists the File Organizer, Web Scraper, and exit options.
        """

        print("Automation tools: \n"
        "\n      1. File Organizer",
        "\n      2. Web Scraper",
        "\n      0. Exit")

    def get_choice():
        """
        Get and normalize the user's menu selection.

        Returns:
            str: The user's choice in lowercase, with surrounding
            whitespace removed.
        """
        choice = (input("\nEnter your choice : ")).lower().strip()
        return choice   
    
    def confirm_decision(records):
        """
        Ask the user to confirm or cancel the file organization operation.

        Args:
            records: The file organization preview records to process.

        Passes a valid response to the organizer. If the response is
        invalid, handles the retry process and asks again when appropriate.
        """
        decisions = ("1","yes","2","no")
        decide = (input("\nWant to organize these files? \n 1. Yes \n 2. No : ")).lower()

        if decide in decisions:
            responce = organizer.move_confirmation(records,decide)
            print("\n",responce,"\n")
        else:
            responce = organizer.retry_responce()
            if responce:
                print("\n",responce,"\n")

            else:
                confirm_decision(records)
    
    def get_file_organizer():
        """
        Run the File Organizer workflow through the command-line interface.

        Requests a target folder, prepares the organization summary and
        preview, displays the results, and asks for confirmation when files
        are available to organize. Displays an error message for an invalid
        target path.
        """
        try:
            print('Initialzing File organizer...\n')
            time.sleep(1)
            file_path = (input("Give the folder path to organize : \n")).strip()
            necessary_data,preview_records = organizer.manage_file_organizer(file_path)

            organizer_terminal_report(necessary_data)

            if len(necessary_data["dir_files"]) != 0:
                show_organizer_preview(preview_records)
                confirm_decision(preview_records)

            print("                 ","*"*40,"\n")

        except TypeError:
            print("Invalid target path !!")

    def get_web_scraper():
        """
        Run the Web Scraper workflow through the command-line interface.

        Requests a URL and an HTML element to search for, retrieves matching
        text, displays the results, and saves the extracted data as a JSON
        report when the scraping request succeeds.
        """
        url = input("\nGive url for web scraping : ")
        validity,responce = scraper.run_scraper(url.strip())
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

    def show_interface():
        """
        Display the interface selection menu and process the user's choice.

        Returns:
            str or None: The result returned by select_interface().
        """
        show_interface_menu()
        chosen = get_choice()
        result = select_interface(chosen)
        return result

    def select_interface(option):
        """
        Process the selected interface and automation tool.

        Args:
            option: The user's interface selection.

        Routes the user to the CLI automation menu, launches the GUI home
        interface, or handles an exit or invalid selection.

        Returns:
            str or None: The result indicating whether the application
            should continue or exit, when returned by the selected flow.
        """
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

            Home_Interface()
            
            time.sleep(1)

            return "continue"

        elif option in option_0:
             print("\nExiting automation....\n")
             time.sleep(2)
             return "exit"

        else:
            reply = organizer.retry_responce()
            if reply:
                print("\n",reply,"\n")
                return "exit"
            else:
                result = show_interface()
                return result

    def show_interface_menu():
        """
        Display the available interface options.

        Lists the CLI, GUI, and exit options.
        """
        print("\nInterface: \n"
        "\n      1. CLI",
        "\n      2. GUI",
        "\n      0. Exit")

    def show_title():
        """
        Display the application title in the command line.

        Prints the suite name between separator lines.
        """
        print("-"*80)
        print("                    Comprehensive Automation Suite                  ")
        print("-"*80,"\n")

    def run_main():
        """
        Run one cycle of the application's main menu flow.

        Displays the application title, shows the interface menu, and
        returns the result of the user's selection.
        """
        show_title()
        result = show_interface()
        return result

    while True:
        result = run_main()
        if result == "exit":
            break
        

