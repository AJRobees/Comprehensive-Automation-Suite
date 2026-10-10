"""
JSON report generation utilities for the File Organizer.

This module collects file organization summary data and saves it
to a dated JSON report. Existing reports for the same day are
loaded and updated with additional operation records.
"""
from config import report_dir_path

from datetime import datetime 
import json

def organizer_json_generator(necessary_data,preview_records,message):
    """
    Generate and save a JSON report for a file organization operation.

    Creates the report directory if it does not exist, builds a summary
    from the supplied scan data, and includes detected filenames,
    duplicate filenames, and existing folder names when available.
    Preview records are included when files were detected. If a report
    for the current date already exists, appends the new record to it.

    Args:
        necessary_data: A dictionary containing the target folder name,
            detected filenames, duplicate filenames, and folder names.
        preview_records: The planned file organization records, each
            containing a filename, category, and destination.
        message: A message describing the operation's outcome.

    Returns:
        None
    """
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
