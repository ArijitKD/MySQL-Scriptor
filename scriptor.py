import tkinter as tk
from tkinter import messagebox as mbox
from tkinter import filedialog as fldg
import traceback as tb
import os

# CONSTANTS
APP_NAME = "MySQL Scriptor"
APP_VERSION = "1.0.0"
CONFIG_FILE = "settings.ini"
DEFAULT_CONFIG = ["WindowWidth=800\n",
                  "WindowHeight=450\n",
                  "XPosition=80\n",
                  "YPosition=120\n",
                  "IsMaximized=false"]
WINDOW_MIN_WIDTH = "640"
WINDOW_MIN_HEIGHT = "480"

class Scriptor:
    def run(self):
        self.window = tk.Tk()
        self.window.title("{} ({})".format(APP_NAME, APP_VERSION))
        self.window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.loadDefaultSettings()        
        try:
            self.loadCustomSettings()
        except FileNotFoundError:
            config_file = open(CONFIG_FILE, "w")
            config_file.writelines(DEFAULT_CONFIG)
            config_file.close()
        self.window.geometry("{}x{}+{}+{}".format(self.window.width, self.window.height, self.window.xposition, self.window.yposition))
        if (self.window.ismaximized == "true"):
            self.window.state("zoomed")
        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.window.mainloop()

    def winfo_isMaximized(self, win_obj):
        return (win_obj.winfo_width() == win_obj.winfo_screenwidth() or win_obj.winfo_height() == win_obj.winfo_screenheight())
    
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
                if (setting.startswith ("windowwidth")):
                    self.window.width = setting[setting.index("=")+1:] 
                if (setting.startswith ("windowheight")):
                    self.window.height = setting[setting.index("=")+1:]
                if (setting.startswith ("xposition")):
                    self.window.xposition = setting[setting.index("=")+1:]
                if (setting.startswith ("yposition")):
                    self.window.yposition = setting[setting.index("=")+1:]
                if (setting.startswith ("ismaximized")):
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