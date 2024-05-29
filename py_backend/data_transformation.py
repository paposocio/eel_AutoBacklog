import pandas as pd
from configparser import ConfigParser


def data_transformation(rutas, meses):
    # Se hace primero un borrado de el preview para evitar 
    # conflictos con previews que se hayan hecho antriormente
    
    # Leer el archivo Excel
    df = pd.read_excel("file_preview.xlsx")

    # Crear un DataFrame vacío con las mismas columnas
    df_empty = pd.DataFrame(columns=df.columns)

    # Escribir el DataFrame vacío en la misma hoja
    with pd.ExcelWriter(df, engine="openpyxl", mode="a") as writer:
        # Borrar la hoja existente
        writer.book.remove(writer.book.active)
        # Escribir el DataFrame vacío en una nueva hoja con el mismo nombre
        df_empty.to_excel(writer, index=False, sheet_name="Sheet1")

    ruta_excel_base1, ruta_excel_base2, ruta_excel_base3, ruta_excel_estadoPrio = rutas
    mes_medicion, mes_anterior, mes_antepasado = meses

    config = ConfigParser()
    config.read("settings.ini", encoding="utf-8")

    # Leer los DataFrames originales
    dataframe1 = pd.read_excel(
        ruta_excel_base1, sheet_name="Priorizacion " + mes_medicion
    )
    dataframe2 = pd.read_excel(
        ruta_excel_base2, sheet_name="Priorizacion " + mes_anterior
    )
    dataframe3 = pd.read_excel(
        ruta_excel_base3, sheet_name="Priorizacion " + mes_antepasado
    )
    dataframe4 = pd.read_excel(
        ruta_excel_estadoPrio, sheet_name=config["ConfigFijo"]["nombreLibro"]
    )

    # Concatenar los DataFrames originales
    nodos_fusionados = pd.concat(
        [dataframe1, dataframe2, dataframe3], ignore_index=True
    )

    # Eliminar duplicados de nodos
    nodos_fusionados.drop_duplicates(inplace=True)

    # Crear DataFrame fusionado con nodos únicos
    dataframe_fusionado = nodos_fusionados.copy()

    # Verificar si el nodo aparece en cada DataFrame original y marcarlo con 1 o 0
    dataframe_fusionado[mes_medicion] = (
        dataframe_fusionado["NODO"].isin(dataframe1["NODO"]).astype(int)
    )
    dataframe_fusionado[mes_anterior] = (
        dataframe_fusionado["NODO"].isin(dataframe2["NODO"]).astype(int)
    )
    dataframe_fusionado[mes_antepasado] = (
        dataframe_fusionado["NODO"].isin(dataframe3["NODO"]).astype(int)
    )
    dataframe_fusionado["Estado Prio"] = (
        dataframe_fusionado["NODO"].isin(dataframe4["NODO"]).astype(int)
    )
    dataframe_fusionado["ESTADO"] = dataframe_fusionado["NODO"].map(
        dataframe4.set_index("NODO")["ESTADO-PRIO"]
    )

    # Define la función para evaluar cada fila y asignar un texto y un valor numérico
    def evaluar_fila(fila):
        config = ConfigParser()
        config.read("settings.ini", encoding="utf-8")

        if fila["ESTADO"] == "Monitoreo" and fila["Estado Prio"] == 1:
            return ("Monitoreo", int(config["ConfigFijo"]["monitoreo"]))
        elif fila["ESTADO"] != "Monitoreo" and fila["ESTADO"] != "No diagnostico":
            return ("Hold", int(config["ConfigFijo"]["hold"]))
        elif (
            fila[mes_medicion] == 1
            and fila[mes_anterior] == 1
            and fila[mes_antepasado] == 1
        ):
            return ("Recurrente 3 meses", int(config["ConfigFijo"]["rec3Mes"]))
        elif fila[mes_medicion] == 1 and (
            fila[mes_anterior] == 1 or fila[mes_antepasado] == 1
        ):
            return (
                "Mes de medicion si + 1 (cualquiera)",
                int(config["ConfigFijo"]["medMasUno"]),
            )
        elif (
            fila[mes_medicion] == 0
            and fila[mes_anterior] == 1
            and fila[mes_antepasado] == 1
        ):
            return (
                "Mes de medicion no + 2",
                int(config["ConfigFijo"]["medNoMasDos"]),
            )
        elif (
            fila[mes_medicion] == 1
            and fila[mes_anterior] == 0
            and fila[mes_antepasado] == 0
        ):
            return (
                "Mes de medicion si + 0",
                int(config["ConfigFijo"]["medMasCero"]),
            )
        elif fila[mes_medicion] == 0 and (
            fila[mes_anterior] == 1 or fila[mes_antepasado] == 1
        ):
            return (
                "Mes de medicion no + 1 (cualquiera)",
                int(config["ConfigFijo"]["medNoMasUno"]),
            )

    # Aplica la función a cada fila del DataFrame utilizando apply()
    dataframe_fusionado[["Caso", "Priorizacion"]] = dataframe_fusionado.apply(
        lambda fila: pd.Series(evaluar_fila(fila), index=["Caso", "Priorizacion"]),
        axis=1,
    )

    dataframe_fusionado_ordenado = dataframe_fusionado.sort_values(by="Priorizacion")

    # Resetear el índice sin agregar una nueva columna
    dataframe_fusionado_ordenado_reset = dataframe_fusionado_ordenado.reset_index(
        drop=True
    )

    dataframe_fusionado_ordenado_reset.index = pd.RangeIndex(
        start=1, stop=len(dataframe_fusionado_ordenado_reset) + 1, name="#"
    )

    # Guardar el DataFrame con el nuevo índice en un archivo Excel
    dataframe_fusionado_ordenado_reset.to_excel("file_preview.xlsx", index=True)
