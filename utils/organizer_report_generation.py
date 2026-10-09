from config import report_dir_path

from datetime import datetime 
import json

def organizer_json_generator(necessary_data,preview_records,message):

    if not report_dir_path.exists():
        report_dir_path.mkdir()

    data = {
        "Targeted Folder" : necessary_data["targeted_folder"],
        "No. of Files Detected" : len(necessary_data["dir_files"]),
        "No. of Duplicate Files Detected" : len(necessary_data["duplicate_file_list"]),
        "No. of Folders Detected" : len(necessary_data["dir_folders"]),
    }

    if len(necessary_data["dir_files"]) !=0:
        data["Files"] = necessary_data["dir_files"]

    if len(necessary_data["duplicate_file_list"]) !=0:
        data["Duplicate Files"] = necessary_data["duplicate_file_list"]

    if len(necessary_data["dir_folders"]) !=0:
        data["Folders"] = necessary_data["dir_folders"]

    if len(necessary_data["dir_files"]) != 0:
        data["Preview records"] = preview_records
        data["Message"] = message
    else:
        data["Message"] = "No files are detected to organize."

    data["Time"] = datetime.now().strftime("%H-%M-%S")

    file_name = f"{datetime.now().strftime('%d-%h-%Y')}_organizer_reports.json"
    file_path = report_dir_path/file_name

    if file_path.exists():
        existing_data = []

        with open(file_path,"r",encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
        if isinstance(existing_data,dict):
            existing_data = [existing_data]

        if isinstance (data,dict):                                 # To append the dictionary note with the existing one
            existing_data.append(data)

        else:
            existing_data.extend(data)

        with open(file_path,"w",encoding="utf-8") as f:
            json.dump(existing_data,f,indent= 5)
        
    else:
        with open(file_path,"w",encoding="utf-8") as f:
            json.dump(data,f,indent= 5)
