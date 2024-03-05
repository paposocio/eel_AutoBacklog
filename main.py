import eel
import tkinter
from tkinter import filedialog as fd
from data_transformation import data_transformation

eel.init("web")


@eel.expose
def choose_file():
    # Crear una ventana modal
    window = tkinter.Tk()
    window.withdraw()
    window.attributes("-topmost", True)
    # Agregar el widget para seleccionar el archivo
    file_options = {
        "defaultextension": ".xlsx",
        "filetypes": [("Archivos de Excel", "*.xlsx;*.xls")],
    }

    filename = fd.askopenfilename(parent=window, **file_options)

    # Cerrar la ventana modal
    window.destroy()

    return filename


@eel.expose
def data(rutas, meses):
    data_transformation(rutas, meses)


eel.start("index.html")
