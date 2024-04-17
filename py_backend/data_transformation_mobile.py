import pandas as pd
from configparser import ConfigParser


def data_transformation_mobile(rutas, meses):

    ruta_excel_base1, ruta_excel_estadoPrio = rutas
    mes_medicion, mes_anterior, mes_antepasado = meses

    # Leer los DataFrames originales
    dataframe1 = pd.read_excel(ruta_excel_base1, sheet_name=mes_medicion)
    dataframe2 = pd.read_excel(ruta_excel_base1, sheet_name=mes_anterior)
    dataframe3 = pd.read_excel(ruta_excel_base1, sheet_name=mes_antepasado)
    dataframe4 = pd.read_excel(
        ruta_excel_estadoPrio, sheet_name="Estado-prio-estaciones-base"
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
        dataframe_fusionado["EST-BASE"].isin(dataframe1["EST-BASE"]).astype(int)
    )
    dataframe_fusionado[mes_anterior] = (
        dataframe_fusionado["EST-BASE"].isin(dataframe2["EST-BASE"]).astype(int)
    )
    dataframe_fusionado[mes_antepasado] = (
        dataframe_fusionado["EST-BASE"].isin(dataframe3["EST-BASE"]).astype(int)
    )
    dataframe_fusionado["Estado Prio"] = (
        dataframe_fusionado["EST-BASE"].isin(dataframe4["EST-BASE"]).astype(int)
    )
    dataframe_fusionado["ESTADO"] = dataframe_fusionado["EST-BASE"].map(
        dataframe4.set_index("EST-BASE")["ESTADO-PRIO"]
    )

    # Define la función para evaluar cada fila y asignar un texto y un valor numérico
    def evaluar_fila(fila):
        config = ConfigParser()
        config.read("settings.ini", encoding="utf-8")

        if fila["ESTADO"] == "Monitoreo" and fila["Estado Prio"] == 1:
            return ("Monitoreo", int(config["ConfigMovil"]["monitoreo"]))
        elif fila["ESTADO"] != "Monitoreo" and fila["ESTADO"] != "No diagnostico":
            return ("Hold", int(config["ConfigMovil"]["hold"]))
        elif (
            fila[mes_medicion] == 1
            and fila[mes_anterior] == 1
            and fila[mes_antepasado] == 1
        ):
            return ("Recurrente 3 meses", int(config["ConfigMovil"]["rec3Mes"]))
        elif fila[mes_medicion] == 1 and (
            fila[mes_anterior] == 1 or fila[mes_antepasado] == 1
        ):
            return (
                "Mes de medicion si + 1 (cualquiera)",
                int(config["ConfigMovil"]["medMasUno"]),
            )
        elif (
            fila[mes_medicion] == 0
            and fila[mes_anterior] == 1
            and fila[mes_antepasado] == 1
        ):
            return (
                "Mes de medicion no + 2",
                int(config["ConfigMovil"]["medNoMasDos"]),
            )
        elif (
            fila[mes_medicion] == 1
            and fila[mes_anterior] == 0
            and fila[mes_antepasado] == 0
        ):
            return (
                "Mes de medicion si + 0",
                int(config["ConfigMovil"]["medMasCero"]),
            )
        elif fila[mes_medicion] == 0 and (
            fila[mes_anterior] == 1 or fila[mes_antepasado] == 1
        ):
            return (
                "Mes de medicion no + 1 (cualquiera)",
                int(config["ConfigMovil"]["medNoMasUno"]),
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
    dataframe_fusionado_ordenado_reset.to_excel("file_preview_mobile.xlsx", index=True)
