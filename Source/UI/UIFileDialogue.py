# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import tkinter as tk
from tkinter import filedialog
from .UIButton import UIButton

def GetFilePath():
    Opener = tk.Tk()
    Opener.withdraw()
    return filedialog.askopenfile()

class UIFileDialogueButton(UIButton):
    def GetFilePath(self):
        if self.data == "":
            Temp = GetFilePath()
            if Temp:
                self.data = str(Temp).split("'")[1]
                self.text = self.data.split("/")[-1].split(".")[0]
                self.RenderText()
    def __init__(self, x, y, width, height, name):
        self.data = ""
        super().__init__(x, y, width, height, name, onClickEvent = self.GetFilePath)