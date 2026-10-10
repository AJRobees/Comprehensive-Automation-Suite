"""
Graphical user interface for the File Organizer module.

This module provides a Tkinter interface for selecting a target folder,
displaying detected files and folders, reviewing the organization preview,
and confirming or cancelling the file organization operation.

The actual scanning, categorization, and file-moving logic is handled
by the File_Organizer class.
"""

from modules import File_Organizer

from config import tests_dir_path
from tkinter import messagebox,ttk
import tkinter as tk

class File_Organizer_GUI(tk.Frame):
    """
    Provide the graphical interface for the File Organizer.

    The interface allows users to specify a folder, start scanning,
    review the scan report and planned file destinations, and confirm
    or cancel the organization operation.
    """
    def __init__(self,master):
        """
        Initialize the File Organizer interface and its main controls.

        Args:
            master: The parent Tkinter window or container.

        Configures the window dimensions, initializes the folder location
        variable, and creates the folder input field and scan button.
        """
        super().__init__(master)
        self.master = master
        self.master.title("File Organizer")
        self.master.geometry("620x180")
        self.master.minsize(480, 180)        
        self.master.maxsize(960, 480)        

        self.milky_blue = "#98CEF4"
        self.black = "black"

        self.location_var = tk.StringVar(value=str(tests_dir_path/"file_organizer_test" ))

        tk.Label(self,text="File Organizer",font=("Times New Roman Bold", 16)).pack(anchor="center",pady=(0,12))

        path_frame = tk.Frame(self)
        path_frame.pack(fill="x")

        tk.Label(path_frame,text="Folder Location : ",font=("Times New Roman",14)).pack(side="left",padx=(0,8))

        self.location_entry = tk.Entry(path_frame, font=("Times New Roman",14),textvariable=self.location_var,
                                       width=60)
        self.location_entry.pack(fill="x",expand=True,side="left")

        self.start_btn = tk.Button(self,text=" Start/Scan ", font=("Times New Roman",10),relief="ridge",
                                   bg=self.milky_blue, command=self.start_organizer)
        self.start_btn.pack(anchor="e", pady=(12,0))

        self.pack(padx=20,expand=True)


    def start_organizer(self):
        """
        Start the file scanning and preview preparation process.

        Creates a File_Organizer instance and passes the stripped folder
        path to its preparation workflow. Displays an error dialog if the
        target path is invalid; otherwise, opens the report window.
        """
        self.organizer = File_Organizer()
        self.given_path = self.location_var.get()
        result = self.organizer.manage_file_organizer(self.given_path.strip())

        if result is None:
            messagebox.showerror("Invalid folder", "The selected path is not a valid folder.", parent=self)
            return

        self.show_report(result)
        
    def show_report(self,data):
        """
        Display the scan report and organization preview in a separate window.

        Args:
            data: A tuple containing the organizer's summary dictionary
                and the list of preview records.

        Displays detected files, duplicate filenames, existing folders,
        and planned category folders. When files are available for
        organization, displays their planned destinations in a table
        and provides a confirmation action.

        The confirmation action calls the File_Organizer instance to
        perform or cancel the operation and displays the resulting message.
        """
        self.necessary_data,self.preview_records = data

        category_folders = ["Image", "Audio", "Video", "Documents", "PDF",
                            "Spreadsheets", "Archives", "Other"]

        report_window = tk.Toplevel(self.master)
        report_window.title("File Organizer Report")
        report_window.geometry("860x720")
        report_window.minsize(480, 320)  
        
        tk.Label(report_window, text="File Organizer Report",
                 font=("Times New Roman", 18, "bold")).pack(anchor="w", padx=18, pady=(16, 8))

        report_frame = tk.Frame(report_window)
        report_frame.pack(fill="x", padx=18, pady=(0, 12))

        scrollbar = tk.Scrollbar(report_frame,cursor="")
        scrollbar.pack(side="right",fill="y")

        report_text = tk.Text(report_frame,wrap="word",yscrollcommand=scrollbar.set,
                              font=("Times New Roman", 12), padx=14, pady=10,height= 15)
        report_text.pack(side="left",expand=True)
        scrollbar.config(command=report_text.yview)
        report_text.tag_configure("heading",font=("Times New Roman",12,"bold"))

        def add_section(header,items):
            """
            Insert a labelled list of items into the report text widget.

            Args:
                header: The heading to display above the items.
                items: The collection of item names to display.

            Displays the heading and each item when the collection is non-empty,
            then inserts a blank line to separate report sections.
            """
            if items:
                report_text.insert("end",f"     {header}:\n","heading")
                for item in items:
                    report_text.insert("end",f"         {item}\n")  

            report_text.insert("end","\n")
                

        report_text.insert("end",f"Targeted Folder : {self.necessary_data['targeted_folder']}\n\n")
        report_text.insert("end",f"No. of Files Detected : {len(self.necessary_data['dir_files'])}\n")
        add_section("Files",self.necessary_data['dir_files'])
        
        report_text.insert("end",f"No. of Duplicate Files Detected : {len(self.necessary_data['duplicate_file_list'])}\n")
        add_section("Duplicate Files with new name",self.necessary_data['duplicate_file_list'])

        report_text.insert("end",f"No. of Folders Detected : {len(self.necessary_data['dir_folders'])}\n")
        add_section("Folders",self.necessary_data['dir_folders'])

        if any( category not in self.necessary_data["dir_folders"] for category in category_folders):
            report_text.insert("end","New folders are planned for organization.\n\n")

        if self.necessary_data["dir_files"]:
            report_text.insert("end",f" {len(self.necessary_data['dir_files'])} are planned for organization.\n")
        else:
            report_text.insert("end","No files are detected to organize.\n")

        report_text.config(state="disabled")

        if len(self.necessary_data['dir_files']):

            tk.Label(report_window, text="Organization Preview",
                    font=("Times New Roman", 16, "bold")).pack(anchor="w", padx=18, pady=(0, 6))

            table_frame = tk.Frame(report_window,height=len(self.necessary_data['dir_files'])*5)
            table_frame.pack(expand=True,padx=20,pady=(0,8))
            table_frame.grid_rowconfigure(0,weight=1)
            table_frame.grid_columnconfigure(0,weight=1)

            columns = ("Name","Category","Destination")
            preview_table = ttk.Treeview(table_frame,columns=columns,show="headings")
            preview_table.heading(column="Name",text="Name")
            preview_table.heading(column="Category",text="Category")
            preview_table.heading(column="Destination",text="Destination")
            preview_table.column("Name", width=220, minwidth=120)
            preview_table.column("Category", width=140, minwidth=100)
            preview_table.column("Destination", width=320, minwidth=160)

            vertical_scrollbar = ttk.Scrollbar(table_frame,orient="vertical",command=preview_table.yview)
            horizontal_scrollbar = ttk.Scrollbar(table_frame,orient="horizontal",command=preview_table.xview)
            preview_table.configure(xscrollcommand=horizontal_scrollbar.set,yscrollcommand=vertical_scrollbar.set)

            preview_table.grid(row=0,column=0,sticky="nsew")
            vertical_scrollbar.grid(row=0,column=1,sticky="ns")
            horizontal_scrollbar.grid(row=1,column=0,sticky="we")

            for record in self.preview_records:
                preview_table.insert("", "end", values=(
                    record["Name"], record["Category"], record["Destination"]))


            def confirm_organize():
                """
                Ask the user to confirm or cancel the organization operation.

                Converts the confirmation dialog's Boolean response into the
                "yes" or "no" value expected by File_Organizer, invokes the
                organization workflow, displays its result, and closes the report
                window.
                """
                decision = messagebox.askyesno("Confirm","Confirm your decision.")
                if decision:
                    valid = "yes"
                else:
                    valid = "no"

                result = self.organizer.move_confirmation(self.preview_records,valid)
                messagebox.showinfo("",result)
                report_window.destroy()

            tk.Button(report_window,text=" Organize ",relief="raised",
                    command=confirm_organize).pack(side="right",pady=10,padx=(20,50),anchor="e")
        tk.Button(report_window,text=" Close ",relief="raised",
                  command=report_window.destroy).pack(side="right",padx=20,pady=10,anchor="e")


    def on_close(self):
        """
        Ask the user to confirm before closing the application window.

        Destroys the parent window only when the user confirms the
        close action.
        """
        decision = messagebox.askokcancel("Quit","Are you sure?")
        if decision is True:
            self.master.destroy()