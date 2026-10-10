"""
File Organizer module for the Comprehensive Automation Suite.

This module scans a target directory, categorizes files by extension,
detects duplicate destination filenames, creates an organization preview,
and moves files into their designated category folders after confirmation.

It also provides CLI functions for displaying the preview and a summary
of the detected files and folders. Application events are recorded
through the shared logging system.
"""

from config import tests_dir_path
from configs import get_logger
from utils import organizer_json_generator
from pathlib import Path

logger = get_logger("file_organizer")

# Validate the existence of the directory.
def validate_dir(folder_dir):
    """
    Check whether the supplied path exists and refers to a directory.

    Args:
        folder_dir: The path to validate.

    Returns:
        bool: True if the path exists and is a directory; otherwise, False.
    """
    if folder_dir.exists() and folder_dir.is_dir():
        return True
    else:
        return False

# To Find the matching extension to categories the files. 
def get_category(extension):
    """
    Determine a file category from its extension.

    Args:
        extension: The file extension, including the leading period.

    Returns:
        str: The matching category: Image, Audio, Video, Documents,
        PDF, Spreadsheets, Archives, or Other for unrecognized extensions.
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
    Generate an unused path for an existing file with a duplicate name.

    Appends an incrementing number in parentheses to the filename stem
    until a path that does not exist is found.

    Args:
        given_path: The existing file path to rename.

    Returns:
        Path: The first unused candidate path, or None if the supplied
        path does not exist or is not a file.
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
    """
    Manage the file organization workflow.

    The class scans the selected directory, categorizes files, records
    duplicate destination names, builds preview records, handles user
    confirmation, moves files, and generates an organization report.
    """
    def __init__(self):
        """
        Initialize the lists and counter used by the organizer.

        The attributes store detected filenames, duplicate filenames,
        folder names, preview records, and the current retry count.
        """
   
        self.files_name = []
        self.duplicate_files_name = []
        self.folders_name = []
        self.preview_records = []
        self.tried = 1

    def scan_directory(self):
        """
        Scan the selected directory and separate files from subdirectories.

        Stores the detected file paths in 'self.dir_files' and directory
        paths in 'self.dir_folders' for use by the categorization workflow.
        """
        logger.info("Initializing file scanning.... ")

        self.dir_files = list([file for file in self.files_dir.iterdir() if file.is_file()])
        self.dir_folders = list([folder for folder in self.files_dir.iterdir() if folder.is_dir()])
        
        logger.info("File scanning is completed.")

    def preview_creator(self,file_name,file_category,file_destination):
        """
        Create and store a preview record for a file.

        Args:
            file_name: The original filename.
            file_category: The category assigned to the file.
            file_destination: The planned destination path relative to the
                selected directory.

        Appends a dictionary containing the file name, category, and
        destination to 'self.preview_records'.
        """
        preview = {
            "Name": file_name,
            "Category": file_category,
            "Destination": str(file_destination),
        }
        self.preview_records.append(preview)
        
    def categorization(self):
        """
        Categorize detected files and build their organization preview.

        Determines each file's category from its extension, records detected
        filenames and existing folder names, and checks whether the planned
        destination already exists. If a duplicate destination is found,
        generates an alternative filename and records it.

        Stores each planned operation in 'self.preview_records'.
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
        
    def manage_file_organizer(self,folder_path):
        """
        Initialize and run the file organization preparation workflow.

        Uses the default test directory when 'folder_path' is empty;
        otherwise, uses the supplied path as the target directory.
        Validates the target, scans its contents, categorizes files,
        and prepares the summary data and preview records.

        Args:
            folder_path: The target directory path, or an empty string
                to use the default test directory.

        Returns:
            tuple: A pair containing the summary dictionary and preview
            records when the directory is valid. Returns None if validation
            fails.
        """
        logger.info("File organizer was started.")

        if folder_path == "":
            self.tests_dir = tests_dir_path
            self.files_dir = self.tests_dir/"file_organizer_test" 
            self.targeted_folder = self.files_dir.name
        else:
            self.tests_dir = Path(folder_path) 
            self.files_dir = self.tests_dir
            self.targeted_folder = self.files_dir.name
        

        if validate_dir(self.files_dir):
            self.scan_directory()
            self.categorization()
            self.necessary_data = {"targeted_folder":self.targeted_folder,
                            "dir_files":self.files_name,
                            "dir_folders":self.folders_name,
                            "duplicate_file_list":self.duplicate_files_name,}
            return self.necessary_data,self.preview_records
        
        else:
            logger.error("Invalid target path!")

    def retry_attempt(self):
        """
        Track invalid confirmation attempts and periodically ask whether
        the user wants to continue.

        When the retry counter reaches three, prompts the user to continue
        or stop, resets the counter, and returns the user's response if
        they choose to stop.

        Returns:
            str or None: Returns "no" if the user chooses to stop at the
            prompt; otherwise, returns None.
        """
        if self.tried ==3:
            decide = (input("\nWant to continue? (yes/no): ")).lower().strip()
            self.tried = 0
            if decide == "no":
                logger.warning("File organization is terminated by user.")
                return decide
        self.tried+=1

    def retry_responce(self):
        """
        Display a retry prompt and process the retry attempt.

        Calls 'retry_attempt()' to check whether the user has exhausted
        the allowed attempts. If the user chooses to stop, resets the
        counter and returns a message indicating that the retry limit
        has been reached.

        Returns:
            str or None: A retry-limit message if the user chooses to stop;
            otherwise, None.
        """
        print("\nPlease select between 1/yes or 2/no. \nOR \nWait for 3 tries, Try ",self.tried)

        attempt = self.retry_attempt()
        # Retry the confirmation until the user provides a valid choice or exits.
        if attempt == "no":
            self.tried = 1
            reply = "3 attempts are over, try again with valid choice."
            return reply

    def reset_data(self):
        """
        Reset the organizer's stored data for a new operation.

        Clears the filename, duplicate filename, folder name, and preview
        lists, and resets the retry counter to its initial value.
        """
        self.files_name = []
        self.duplicate_files_name = []
        self.folders_name = []
        self.preview_records = []
        self.tried = 1

    def move_confirmation(self,preview_records,decision):
        """
        Process the user's decision and perform the planned file organization.

        If the decision is "1" or "yes", creates missing category folders
        and moves files to their planned destinations. Otherwise, records
        that the operation was stopped. Generates a JSON report and resets
        the stored organizer data after either normal outcome.

        Args:
            preview_records: The list of planned file operations.
            decision: The user's confirmation or cancellation response.

        Returns:
            str or None: A completion or cancellation message when the
            corresponding operation finishes. Returns None if a
            FileNotFoundError is caught.
        """
        try:
            if decision == "1" or decision == "yes":
                for row in preview_records:
                    # Resolve the category folder and final destination from the preview record.
                    file = self.files_dir/row["Name"]
                    category_folder = (self.files_dir/row["Destination"]).parent
                    destination = self.files_dir/row["Destination"]

                    if category_folder.exists():
                        file.rename(destination)
                    else:
                        category_folder.mkdir()
                        file.rename(destination)

                reply = "File organization completed successfully."
                logger.info("File organization completed successfully.")
                organizer_json_generator(self.necessary_data,self.preview_records,reply)
                self.reset_data()
                return reply

            else:
                reply = "File organization is stopped by user."
                logger.info("File organization is stopped by user.")
                organizer_json_generator(self.necessary_data,self.preview_records,reply)
                logger.info("Organized records saved as json.")
                self.reset_data()
                return reply

        except FileNotFoundError:
            logger.error("Invalid file name or path!")



# CLI-only display functions called by the main program.
def show_organizer_preview(preview_records):
    """
    Display the file organization preview in the command-line interface.

    Args:
        preview_records: A list of dictionaries containing each file's
            name, category, and planned destination.

    Displays the preview as rows in the terminal.
    """
    headers = preview_records[0].keys()
    [print(end=f"{header}                    ") for header in headers]
    print("\n","-"*80)
    for row in preview_records:

        print(f"{row["Name"]}                   {row["Category"]}                   {row["Destination"]}")

    print("-"*80)

def organizer_terminal_report(necessary_data):
    """
    Display a summary of the file organizer's scan in the terminal.

    Args:
        necessary_data: A dictionary containing the target folder name,
            detected filenames, existing folder names, and duplicate
            destination filenames.

    Displays the detected files, duplicate filenames, folders, and
    whether new category folders are expected to be created.
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

    