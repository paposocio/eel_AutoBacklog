import eel
import tkinter
from tkinter import filedialog as fd

eel.init("web")


@eel.expose
def choose_file():
    file_options = {
        "defaultextension": ".xlsx",
        "filetypes": [
            ("Archivos de Excel", "*.xlsx;*.xls")
        ],
    }
    tkinter.Tk().withdraw()
    filename = fd.askopenfilename(**file_options)
    return filename


eel.start("index.html")
