'''
MySQL Scriptor: Simple script editor that can execute MySQL scripts.

This file is a part of MySQL Scriptor.

Copyright (C) 2021 Arijit Kumar Das (Github: @ArijitKD)

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

from tkinter import messagebox as mbox
from tkinter import filedialog as fldg
from app_constants import *


class Scriptor:
    def run(self):
        self.window = tk.Tk()
        self.window.title("{} ({})".format(APP_NAME, APP_VERSION))
        self.window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.loadDefaultSettings()        
        try:
            self.loadCustomSettings()
        except FileNotFoundError:
            pass
        self.window.geometry("{}x{}+{}+{}".format(self.window.width, self.window.height, self.window.xposition, self.window.yposition))
        if (self.window.ismaximized == "true"):
            self.window.state("zoomed")
        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.window.mainloop()

    def winfo_isMaximized(self, tk_obj):
        return (tk_obj.winfo_width() == tk_obj.winfo_screenwidth() or tk_obj.winfo_height() == tk_obj.winfo_screenheight())
    
    def loadDefaultSettings(self):
        self.window.width = "800"
        self.window.height = "450"
        self.window.xposition = "80"
        self.window.yposition = "120"
        self.window.ismaximized = "false"
        
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
                if (setting.startswith("windowheight") and setting[setting.index("=")-1]=="t"):
                    self.window.height = setting[setting.index("=")+1:]
                if (setting.startswith("xposition") and setting[setting.index("=")-1]=="n"):
                    self.window.xposition = setting[setting.index("=")+1:]
                if (setting.startswith("yposition") and setting[setting.index("=")-1]=="n"):
                    self.window.yposition = setting[setting.index("=")+1:]
                if (setting.startswith("ismaximized") and setting[setting.index("=")-1]=="d"):
                    self.window.ismaximized = setting[setting.index("=")+1:]

    def saveSettings(self, file=CONFIG_FILE):
        with open(file, "w") as config_file:
            config_file.writelines(["WindowWidth={}\n".format(self.window.winfo_width()),
                                    "WindowHeight={}\n".format(self.window.winfo_height()),
                                    "XPosition={}\n".format(self.window.winfo_x()),
                                    "YPosition={}\n".format(self.window.winfo_y()),
                                    "IsMaximized={}\n".format(str(self.winfo_isMaximized(self.window)).lower())])
            
    def saveFile(self):
        print ("File Saved.")

    def saveAsFile(self):
        pass

    def closeWindow(self):
        save_prompt = mbox.askyesnocancel(title = APP_NAME, message = "The current script is unsaved. If you do not save, changes made may be lost. Save current script?")
        if (save_prompt != None):
            if (save_prompt == True):
                self.saveFile()
            self.saveSettings()
            self.window.destroy()
        
        
if (__name__ == "__main__"):
    scriptor = Scriptor()
    scriptor.run()
