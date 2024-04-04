import eel
import tkinter
import pandas
from tkinter import filedialog as fd
from py_backend.data_transformation import data_transformation
from py_backend.data_exporting import data_export
from py_backend.settings import extractConfig
from py_backend.settings import fijoTop, fijoOrden, extractAllConfig

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


@eel.expose
def obtener_datos_excel():
    dataframe_excel = pandas.read_excel("file_preview.xlsx")
    # Convertir el DataFrame a formato JSON
    json_data = dataframe_excel.to_json(orient="split", index=False)
    # Retornar el JSON
    return json_data


@eel.expose
def export(option):
    data_export(option)


@eel.expose
def extConfig(seccion, atrib):
    return extractConfig(seccion, atrib)


@eel.expose
def extAllConfig():
    return extractAllConfig()


@eel.expose
def fijoT(atrib, valor):
    fijoTop(atrib, valor)


@eel.expose
def fijoO(valores):
    fijoOrden(valores)


eel.start("index.html", cmdline_args=["--start-maximized"],port='3309')