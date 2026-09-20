from pathlib import Path

# Vallidate the existence of the directory.
def validate_dir(folder_dir):
    if folder_dir.exists() and folder_dir.is_dir():
        return True
    else:
        return False

# To Find the matching extension to categories the files. 
def get_category(extension):

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
    Returns a unique Path by appending a counter in parentheses (e.g., report (1).pdf)
    if the file already exists. Continues incrementing if duplicates exist.
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

        project_dir = Path(__file__).parents[1]        # Assigning project directory.
        self.files_dir = project_dir/"tests"/"file_organizer_test"       # Assign the directory where needs to be organized.

        self.targetted_folder = self.files_dir.name
        self.files_name = []
        self.duplicate_files_name = []
        self.folders_name = []
    
        '''     It validates the existence of the assigned directory. It find the no. of files and folders available
        in that location and organize the files into it's respective categoized folder if the category folder is does 
        not exist, it creates them before moving the files.'''

    def scan_directory(self):
        self.dir_files = list([file for file in self.files_dir.iterdir() if file.is_file()])
        self.dir_folders = list([folder for folder in self.files_dir.iterdir() if folder.is_dir()])
        
    def categorization(self):

        self.folders_name.extend([folder.name for folder in self.dir_folders])

        for file in self.dir_files:
            self.files_name.append(file.name)
            file_category = get_category(file.suffix)

            category_path = self.files_dir/file_category
            file_path = category_path/file.name

            if validate_dir(category_path):
                if file_path.exists():
                    new_file_path = duplicate_handling(file_path)
                    self.duplicate_files_name.append(new_file_path.name)
                    file.rename(new_file_path)

                else:
                    file.rename(file_path)
                
            else:
                category_path.mkdir()
                file.rename(file_path)

    def manage_file_organizer(self):

        if validate_dir(self.files_dir):
            self.scan_directory()
            self.categorization()
            return self.targetted_folder,self.files_name,self.folders_name,self.duplicate_files_name


