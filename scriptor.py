'''
MySQL Scriptor: Simple script editor that can execute MySQL scripts.

This file is a part of MySQL Scriptor.

Copyright (C) 2022 Arijit Kumar Das (Github: @ArijitKD)

MySQL Scriptor is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MySQL Scriptor is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with MySQL Scriptor.  If not, see <https://www.gnu.org/licenses/>.
'''


import os
import traceback as tb
import tkinter as tk

import tkinter.ttk as ttk
from tkinter import messagebox as mbox
from tkinter import filedialog as fldg
from app_constants import *
    
class Scriptor:

    def __init__(self):
        self.window = tk.Tk()
        self.filename = "Unnamed script"
        
    def run(self):
        print (APP_NAME+"\nVersion: "+APP_VERSION+"\n")
        print ("============================================    APP LOGS    ============================================")
        self.update_title(self.filename)
        self.window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        self.loadDefaultSettings()
        try:
            self.loadCustomSettings()
        except FileNotFoundError:
            print ("WARNING: File settings.ini not found, no custom settings applied.")
        self.window.geometry("{}x{}+{}+{}".format(self.window.width, self.window.height, self.window.xposition, self.window.yposition))
        if (self.window.laststate == "maximized"):
            self.window.state("zoomed")

        self.addMenuBar()
        self.addEditArea()
        self.addStatusArea()
        
        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.window.mainloop()

    def winfo_isMaximized(self, tk_obj):
        return (tk_obj.winfo_width() == tk_obj.winfo_screenwidth() or tk_obj.winfo_height() == tk_obj.winfo_screenheight())

    def write_status(self, string, write_mode="append"):
        if (write_mode=="overwrite"):
            self.statusarea.delete("1.0", "end")
            self.statusarea.insert(index="1.0", chars=string)
        elif (write_mode=="append"):
            self.statusarea.insert(index="end", chars="\n"+string)
        else:
            raise tk.TclError("bad write mode \"{}\": must be \"append\" or \"overwrite\"".format(write_mode))

    def update_title(self, filename):
        self.window.title("{} - {} ({})".format(filename, APP_NAME, APP_VERSION))

    def format_filename(self, filename):
        return filename.replace("/", "\\") if os.name == "nt" else filename

    def addMenuBar(self):
        # Creating Menubar
        self.menubar = tk.Menu(self.window,font=("segoe ui",9))
        # Configuring menubar on window window
        self.window.config(menu=self.menubar)
        # Creating File Menu
        self.filemenu = tk.Menu(self.menubar,font=("segoe ui", 9),tearoff=0)
        # Adding New file Command
        self.filemenu.add_command(label="New",accelerator="Ctrl+N",command=self.createNewFile)
        # Adding Open file Command
        self.filemenu.add_command(label="Open",accelerator="Ctrl+O",command=self.openFile)
        # Adding Save File Command
        self.filemenu.add_command(label="Save",accelerator="Ctrl+S",command=self.saveFile)
        # Adding Save As file Command
        self.filemenu.add_command(label="Save As",accelerator="Ctrl+A",command=self.saveAsFile)
        # Adding Seprator
        self.filemenu.add_separator()
        # Adding Exit window Command
        self.filemenu.add_command(label="Exit",accelerator="Ctrl+E",command=self.closeWindow)
        # Cascading filemenu to menubar
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Creating Edit Menu
        self.editmenu = tk.Menu(self.menubar,font=("segoe ui", 9),tearoff=0)
        # Adding Cut text Command
        self.editmenu.add_command(label="Cut",accelerator="Ctrl+X",command=self.cutItem)
        # Adding Copy text Command
        self.editmenu.add_command(label="Copy",accelerator="Ctrl+C",command=self.copyItem)
        # Adding Paste text command
        self.editmenu.add_command(label="Paste",accelerator="Ctrl+V",command=self.pasteItem)
        # Adding Seprator
        self.editmenu.add_separator()
        # Adding Undo text Command
        self.editmenu.add_command(label="Undo",accelerator="Ctrl+U",command=self.undoAction)
        # Cascading editmenu to menubar
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        # Creating Help Menu
        self.helpmenu = tk.Menu(self.menubar,font=("segoe ui",9),tearoff=0)
        # Adding About Command
        self.helpmenu.add_command(label="About "+APP_NAME,command=self.appAbout)
        # Cascading helpmenu to menubar
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

    def addEditArea(self):
        # Creating Scrollbar_Y
        editor_scrol_y = ttk.Scrollbar(self.window,orient="vertical")
        # Creating Scrollbar_X
        editor_scrol_x = ttk.Scrollbar(self.window,orient="horizontal")
        # Creating Text Area
        self.editarea = tk.Text(self.window, xscrollcommand=editor_scrol_x.set, yscrollcommand=editor_scrol_y.set, wrap="none", font=("Consolas", 12), state="normal", relief="groove", background="#002240", foreground="#fff", insertbackground="#fff")
        # Adding Scrollbar_x to text area
        editor_scrol_x.config(command=self.editarea.xview)
        # Adding Scrollbar_y to text area
        editor_scrol_y.config(command=self.editarea.yview)
        # Packing scrollbar_y to root window
        editor_scrol_y.pack(side="right",fill="y")
        # Packing Text Area to root window
        self.editarea.pack(side="top", fill="both",expand=1)
        # Packing scrollbar_x to root window
        editor_scrol_x.pack(side="top",fill="x")
        # Edit area should be focused
        self.editarea.focus_set()

    def addStatusArea(self):
        # Creating Scrollbar_Y
        status_scrol_y = ttk.Scrollbar(self.window, orient="vertical")
        # Creating Statusbar
        self.statusarea = tk.Text(self.window, height=10, font=("segoe ui", 9), yscrollcommand=status_scrol_y.set, relief="groove", background="#1f1f1f", foreground="#fff", insertbackground="#fff", wrap="char")
        # Creating StatusTitlebar
        self.statusbar = ttk.Label(self.window,font=("segoe ui",10), text="Status Window", relief="groove")
        # Adding Scrollbar_y to status area
        status_scrol_y.config(command=self.statusarea.yview)
        # Packing scrollbar_y to root window
        status_scrol_y.pack(side="right", fill="both")
        # Packing StatusTitlebar to root window
        self.statusbar.pack(side="top",fill="both")
        # Packing status bar to root window
        self.statusarea.pack(side="top",fill="both")
        # Writing the status
        self.write_status("Ready", write_mode="overwrite")
        
    def loadDefaultSettings(self):
        self.window.width = "800"
        self.window.height = "450"
        self.window.xposition = "80"
        self.window.yposition = "120"
        self.window.laststate = "maximized"
        print ("INFO: Loaded default application settings.")
        
    def loadCustomSettings(self, file=CONFIG_FILE):        
        if (not os.path.isfile(file)):
            raise FileNotFoundError        
        else:
            config_file = open(file, "r")
            settings = config_file.readlines()
            config_file.close()
            for setting in settings:
                setting = setting.strip().replace(" ", "").lower()
                if (setting.startswith("windowwidth") and setting[setting.index("=")-1]=="h"):
                    self.window.width = setting[setting.index("=")+1:]
                elif (setting.startswith("windowheight") and setting[setting.index("=")-1]=="t"):
                    self.window.height = setting[setting.index("=")+1:]
                elif (setting.startswith("xposition") and setting[setting.index("=")-1]=="n"):
                    self.window.xposition = setting[setting.index("=")+1:]
                elif (setting.startswith("yposition") and setting[setting.index("=")-1]=="n"):
                    self.window.yposition = setting[setting.index("=")+1:]
                elif (setting.startswith("laststate") and setting[setting.index("=")-1]=="e"):
                    self.window.laststate = setting[setting.index("=")+1:]
        print ("INFO: Custom settings have been loaded and will override the respective default settings.")

    def saveSettings(self, file=CONFIG_FILE):
        with open(file, "w") as config_file:
            if (self.winfo_isMaximized(self.window)):
                config_file.writelines(["WindowWidth={}\n".format(self.window.width),
                                        "WindowHeight={}\n".format(self.window.height),
                                        "XPosition={}\n".format(self.window.xposition),
                                        "YPosition={}\n".format(self.window.yposition),
                                        "LastState={}\n".format("maximized")])
            else:
                config_file.writelines(["WindowWidth={}\n".format(self.window.winfo_width()),
                                        "WindowHeight={}\n".format(self.window.winfo_height()),
                                        "XPosition={}\n".format(self.window.winfo_x()),
                                        "YPosition={}\n".format(self.window.winfo_y()),
                                        "LastState={}\n".format("normal")])
        print ("INFO: Configuration settings were saved successfully.")

    def createNewFile(self):
        self.write_status("New script created")
        print ("INFO: New file created.")
        

    def openFile(self):
        # Exception handling
        try:
          # Asking for file to open
          self.filename = fldg.askopenfilename(title = "Open",filetypes = [("MySQL Scripts (*.mysql)","*.mysql"), ("SQL Scripts (*.sql)","*.sql"), ("All Files (*.)","*.*")])
          self.filename = self.format_filename(self.filename)
          # checking if filename not none
          if self.filename:
            # opening file in readmode
            infile = open(self.filename,"r")
            # Clearing text area
            self.editarea.delete("1.0", "end")
            # Inserting data Line by line into text area
            for line in infile:
              self.editarea.insert("end", line)
            # Closing the file  
            infile.close()
            # Calling Set title
            #self.settitle()
            self.update_title(self.filename)
            self.write_status("Opened {}.".format(self.filename))
        except Exception as e:
          mbox.showerror("Exception",e)
            
    def saveFile(self):
        print ("INFO: File saved.")
        self.write_status("Saved file: {}".format(self.filename))

    def saveAsFile(self):
        pass

    def closeWindow(self):
        save_prompt = mbox.askyesnocancel(title = APP_NAME, message = "The current script is unsaved. If you do not save, changes made may be lost. Save current script?")
        if (save_prompt != None):
            if (save_prompt == True):
                self.saveFile()
            self.saveSettings()
            self.window.destroy()
            print ("INFO: Successful exit [No errors].")
            raise SystemExit(0)

    def cutItem(self):
        pass

    def copyItem(self):
        pass

    def pasteItem(self):
        pass

    def undoAction(self):
        pass

    def redoAction(self):
        pass

    def appAbout(self):
        mbox.showinfo(title="About",
                      message=
'''
{}
Version: {}

{} is a simple script editor that can execute MySQL scripts.

{}

{} is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

{} is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with {}.  If not, see <https://www.gnu.org/licenses/>.
'''.format(APP_NAME, APP_VERSION, APP_NAME, COPYRIGHT_STRING, APP_NAME, APP_NAME, APP_NAME))
        
        
if (__name__ == "__main__"):
    scriptor = Scriptor()
    scriptor.run()
