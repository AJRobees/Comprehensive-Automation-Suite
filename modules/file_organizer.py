"""
File Organizer module for the Comprehensive Automation Suite.

This module provides functionality to scan a target directory, categorize
files based on their extensions, detect duplicate file names, create an
organization preview, and move files into their respective category folders.

It also provides CLI functions for displaying the organization preview and
terminal report. Application events are recorded using the shared logging
system provided by the general_logger module.
"""

from pathlib import Path
from .general_logger import get_logger

logger = get_logger("file_organizer")

# Validate the existence of the directory.
def validate_dir(folder_dir):
    """
        Validate whether the given path exists and refers to a directory.

        Returns:
            bool: True if the path exists and is a directory, otherwise False.
    """
    if folder_dir.exists() and folder_dir.is_dir():
        return True
    else:
        return False

# To Find the matching extension to categories the files. 
def get_category(extension):
    """
    Determine the category of a file based on its extension.

    Known extensions are grouped into categories such as Image, Audio,
    Video, Documents, PDF, Spreadsheets, and Archives. Extensions that
    do not match a defined category are classified as Other.

    Returns:
        str: The category assigned to the given file extension.
    """

    # File extensions grouped by their corresponding file categories.
    image_category = [".jpg",".jpeg",".png",".gif",]
    audio_category = [".mp3",".wav",]
    video_category = [".mp4",".mkv",".avi",]
    document_category = [".doc",".docx",".txt",]
    pdf_category = [".pdf",]
    spreadsheet_category = [".xls",".xlsx",".csv",]
    archive_category = [".zip",".rar",".7z",]

    if extension in image_category:
        return "Image"

    elif extension in audio_category:
        return "Audio"
    
    elif extension in video_category:
        return "Video"
   
    elif extension in document_category:
        return "Documents"
    
    elif extension in pdf_category:
        return "PDF"
    
    elif extension in spreadsheet_category:
        return "Spreadsheets"
    
    elif extension in archive_category:
        return "Archives"

    else:
        return "Other"

def duplicate_handling(given_path):
    """
    Generate a unique file path when a duplicate file already exists.

    Appends an incrementing number in parentheses to the original filename
    until an unused path is found.

    Returns:
        Path: A unique path for the duplicate file.
    """
    if given_path.exists() and given_path.is_file():
        original_stem = given_path.stem
        increment = 1

        while given_path.exists():
            new_name = f"{original_stem} ({increment})"
            given_path = given_path.with_stem(new_name)
            increment +=1

        return given_path

class File_Organizer():
    def __init__(self):

        self.project_dir = Path(__file__).parents[1]      
        self.files_dir = self.project_dir/"tests"/"file_organizer_test" 

        self.targeted_folder = self.files_dir.name
        self.files_name = []
        self.duplicate_files_name = []
        self.folders_name = []
        self.preview_records = []
        self.tried = 1

    def scan_directory(self):
        """
        Scan the target directory and separate its files and folders.

        Stores the detected files and subdirectories in instance attributes for
        use during the file categorization and preview process.
        """
        logger.info("Initializing file scanning.... ")

        self.dir_files = list([file for file in self.files_dir.iterdir() if file.is_file()])
        self.dir_folders = list([folder for folder in self.files_dir.iterdir() if folder.is_dir()])
        
        logger.info("File scanning is completed.")

    def preview_creator(self,file_name,file_category,file_destination):
        """
        Create and store a preview record for a file.

        The preview record contains the file name, assigned category, and
        destination path that will be used during organization.
        """
        preview = {
            "Name": file_name,
            "Category": file_category,
            "Destination": file_destination,
        }
        self.preview_records.append(preview)
        
    def categorization(self):
        """
        Categorize detected files and construct their organization preview.

        Determines each file's category from its extension, checks for duplicate
        destination names, and stores the resulting organization details in the
        preview records.
        """
        self.folders_name.extend([folder.name for folder in self.dir_folders])
        logger.info("Constructing preview records.")

        for file in self.dir_files:
            self.files_name.append(file.name)
            file_category = get_category(file.suffix)

            category_path = self.files_dir/file_category
            file_path = category_path/file.name

            # Generate a new destination name when a duplicate file is detected.
            if file_path.exists():
                logger.warning("Duplicate file is detected!")
                new_file_path = duplicate_handling(file_path)
                self.duplicate_files_name.append(new_file_path.name)
                
                self.preview_creator(file.name,file_category,new_file_path.relative_to(self.files_dir))

            else:
                self.preview_creator(file.name,file_category,file_path.relative_to(self.files_dir))
        logger.info("Preview construction is completed.")
        
    def manage_file_organizer(self):
        """
        Start the file organizer workflow after validating the target directory.

        Scans the directory, categorizes the detected files, and prepares the
        information required by the CLI for displaying the organization preview.

        Returns:
            tuple: Necessary directory information and the generated preview
            records when the target directory is valid.
        """
        logger.info("File organizer was started.")
        
        if validate_dir(self.files_dir):
            self.scan_directory()
            self.categorization()
            necessary_data = {"targeted_folder":self.targeted_folder,
                            "dir_files":self.files_name,
                            "dir_folders":self.folders_name,
                            "duplicate_file_list":self.duplicate_files_name,}
            return necessary_data,self.preview_records
        
        else:
            logger.error("Invalid target path!")

    def retry_attempt(self):
        """
        Manage repeated invalid confirmation attempts.

        Allows the user to retry the confirmation process and asks whether to
        continue after the maximum number of attempts is reached.

        Returns:
            str or None: The user's decision when the retry limit is reached.
        """
        if self.tried ==3:
            decide = (input("\nWant to continue? (yes/no): ")).lower()
            self.tried = 0
            if decide == "no":
                logger.warning("File organization is terminated by user.")
                return decide
        self.tried+=1

    def move_confirmation(self,preview_records):
        """
        Confirm and perform the planned file organization.

        Requests user confirmation, creates missing category folders, and moves
        files to their planned destinations. Invalid choices are handled through
        the retry mechanism.

        Returns:
            str: A message describing the result of the organization operation.
        """
        decide = (input("\nWant to organize these files? \n 1. Yes \n 2. No : ")).lower()

        if decide == "1" or decide == "yes":
            for row in preview_records:
                # Resolve the category folder and final destination from the preview record.
                file = self.files_dir/row["Name"]
                category_folder = self.files_dir/row["Destination"].parent
                destination = self.files_dir/row["Destination"]

                if category_folder.exists():
                    file.rename(destination)
                else:
                    category_folder.mkdir()
                    file.rename(destination)

            reply = "File organization completed successfully."
            logger.info("File organization completed successfully.")
            return reply

        elif decide == "2" or decide == "no":
            reply = "File organization is stopped."
            logger.info("File organization is stopped by user.")
            return reply

        else:
            print("\nPlease select between 1/yes or 2/no. \nOR \nWait for 3 tries, Try ",self.tried)

            attempt = self.retry_attempt()
            # Retry the confirmation until the user provides a valid choice or exits.
            if attempt == "no":
                self.tried = 1
                reply = "3 attempts are over, try again with valid choice."
                return reply
            else:
                reply = self.move_confirmation(preview_records)
                return reply


# CLI-only display functions called by the main program.
def show_organizer_preview(preview_records):
    """
    Display the file organization preview in the CLI.
    """
    headers = preview_records[0].keys()
    [print(end=f"{header}                    ") for header in headers]
    print("\n","-"*80)
    for row in preview_records:

        print(f"{row["Name"]}                   {row["Category"]}                   {row["Destination"]}")

    print("-"*80)

def organizer_terminal_report(necessary_data):
    """
    Display the file organizer results and summary in the CLI.
    """
    category_folders = ["Image","Audio","Video","Documents","PDF","Spreadsheets","Archives","Other"]
    print(f"targeted Folder : {necessary_data["targeted_folder"]}\n")

    print(f"No. of Files Detected : {len(necessary_data["dir_files"])}\n")
    for file in necessary_data["dir_files"]:
        print(file)

    print(f"\nNo. of Duplicate Files Detected : {len(necessary_data["duplicate_file_list"])}\n")
    if len(necessary_data["duplicate_file_list"]) != 0:
        print("  New file name:")
        for file in necessary_data["duplicate_file_list"]:
            print(file)

    print(f"\nNo. of Folders Detected : {len(necessary_data["dir_folders"])}\n")
    for folder in necessary_data["dir_folders"]:
        print(folder)

    if any(category not in necessary_data["dir_folders"] for category in category_folders):
        print("\n New folders are created to organize.\n")
        logger.info("New folders are created to organize.")

    if len(necessary_data["dir_files"]) != 0:
        print(f"\n {len(necessary_data["dir_files"])} files are planned for organization.\n")
    else:
        print("\n No files are detected to organize.\n")
        logger.info("No files are detected to organize.")

    