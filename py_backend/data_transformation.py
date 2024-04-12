import pandas as pd
from configparser import ConfigParser


def data_transformation(rutas, meses):

    ruta_excel_base1, ruta_excel_base2, ruta_excel_base3, ruta_excel_estadoPrio = rutas
    mes_medicion, mes_anterior, mes_antepasado = meses
    
    dataframe1 = pd.read_excel(
        ruta_excel_base1, sheet_name="Priorizacion " + mes_medicion
    )
    dataframe1[mes_medicion] = 1

    dataframe2 = pd.read_excel(
        ruta_excel_base2, sheet_name="Priorizacion " + mes_anterior
    )
    dataframe2[mes_anterior] = 1

    dataframe3 = pd.read_excel(
        ruta_excel_base3, sheet_name="Priorizacion " + mes_antepasado
    )
    dataframe3[mes_antepasado] = 1

    dataframe4 = pd.read_excel(
        ruta_excel_estadoPrio, sheet_name="Priorizacion Baclok FJ"
    )
    dataframe4["Estado Prio"] = 1

    dataframe_fusionado = pd.merge(dataframe1, dataframe2, on=["NODO","REGIONAL","CIUDAD","ALIADO","DISTRITO","OPERA"], how="outer")
    dataframe_fusionado = pd.merge(
        dataframe_fusionado, dataframe3, on=["NODO","REGIONAL","CIUDAD","ALIADO","DISTRITO","OPERA"], how="outer"
    )

    dataframe_fusionado = pd.merge(
        dataframe_fusionado, dataframe4, on="NODO", how="outer"
    )

    dataframe_fusionado[mes_antepasado] = dataframe_fusionado[mes_antepasado].fillna(0)
    dataframe_fusionado[mes_anterior] = dataframe_fusionado[mes_anterior].fillna(0)
    dataframe_fusionado[mes_medicion] = dataframe_fusionado[mes_medicion].fillna(0)
    dataframe_fusionado["Estado Prio"] = dataframe_fusionado["Estado Prio"].fillna(0)
    
    # Define la función para evaluar cada fila y asignar un texto y un valor numérico
    def evaluar_fila(fila):
        config = ConfigParser()
        config.read("settings.ini", encoding="utf-8")

        if fila["FASE REAL MESA"] == "Monitoreo" and fila["Estado Prio"] == 1:
            return ("Monitoreo", int(config["ConfigFijo"]["monitoreo"]))
        elif (
            fila["FASE REAL MESA"] != "Monitoreo"
            and fila["FASE REAL MESA"] != "No diagnostico"
        ):
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
            return ("Mes de medicion no + 2", int(config["ConfigFijo"]["medNoMasDos"]))
        elif (
            fila[mes_medicion] == 1
            and fila[mes_anterior] == 0
            and fila[mes_antepasado] == 0
        ):
            return ("Mes de medicion si + 0", int(config["ConfigFijo"]["medMasCero"]))
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
    columnas = [
        "NODO",
        "REGIONAL",
        "CIUDAD",
        "ALIADO",
        "OPERA",
        mes_antepasado,
        mes_anterior,
        mes_medicion,
        "Caso",
        "Priorizacion"
    ]

    dataframe_fusionado = dataframe_fusionado[columnas]
    
    dataframe_fusionado = dataframe_fusionado.drop_duplicates(subset=['NODO'])
    
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



ruta1 = r"C:\Users\38510611\Desktop\files\240404-Priorizacion ICR-Disponibilidad Cierre Mar 1.xlsx"
ruta2 = r"C:\Users\38510611\Desktop\files\240308-Priorizacion ICR-Disponibilidad Cierre Feb.xlsx"
ruta3 = r"C:\Users\38510611\Desktop\files\240207-Priorizacion ICR-Disponibilidad Cierre ENE S 1.xlsx"
ruta4 = r"C:\Users\38510611\Desktop\files\estado_nodos.xlsx"

mes1 = "2024-03"
mes2 = "2024-02"
mes3 = "2024-01"

rutas = [ruta1, ruta2, ruta3, ruta4]
meses = [mes1, mes2, mes3]

data_transformation(rutas, meses)
