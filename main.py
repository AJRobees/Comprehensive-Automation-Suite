import time
from modules import *

if __name__ == "__main__":

    organizer = File_Organizer()

    print("\nGreetings, \n")
    chosen_interface = input("Select the Process Interface, \n 1. CLI \n 2. GUI \n 3. Exit : ")
    print("\n Loading the Interface... \n")
    time.sleep(1)

    if chosen_interface == "1":
        #try:
            print('Initialzing File organizer...\n')
            time.sleep(1)
            targetted_folder,dir_files,dir_folders,duplicate_file_list = organizer.manage_file_organizer()

            print(f"Targetted Folder : {targetted_folder}\n")

            print(f"No. of Files Detected : {len(dir_files)}\n")
            for file in dir_files:
                print(file)

            print(f"\nNo. of Duplicate Files Detected : {len(duplicate_file_list)}\n","  New file name:")
            for file in duplicate_file_list:
                print(file)

            print(f"\nNo. of Folders Detected : {len(dir_folders)}\n")
            for folder in dir_folders:
                print(folder)

            if len(dir_folders) == 0:
                print("\n New folders are created to organize.\n")

            if len(dir_files) != 0:
                print(f"\n {len(dir_files)} Files are organized.\n")
            else:
                print("\n No files are detected to organize.\n")

        #except TypeError:
        #    print("Invalid target path !!")

    elif chosen_interface == "2":
        print('Initialzing File organizer...\n')
        time.sleep(1)
        File_Organizer()

    else:
        print("Exit")
