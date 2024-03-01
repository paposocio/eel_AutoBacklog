import eel
import tkinter
from tkinter import filedialog as fd

eel.init('web')

@eel.expose
def choose_file():
    tkinter.Tk().withdraw()
    filename = fd.askopenfilename()
    return filename
    
eel.start('fijo.html', size=(1000, 700))