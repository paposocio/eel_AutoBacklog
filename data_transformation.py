import pandas as pd
import openpyxl

ruta_excel_base1 = '231207-Priorizacion ICR-Disponibilidad NOV S.xlsx'
ruta_excel_base2 = '240103-Priorizacion ICR-Disponibilidad Cierre DIC s.xlsx'
ruta_excel_base3 = '240207-Priorizacion ICR-Disponibilidad Cierre ENE S.xlsx'

mes3='ENE'
mes2='DIC'
mes1='NOV'

dataframe1 = pd.read_excel(ruta_excel_base1,sheet_name='Priorizacion '+mes1)
dataframe1[mes1]=1

dataframe2 = pd.read_excel(ruta_excel_base2,sheet_name='Priorizacion '+mes2)
dataframe2[mes2]=1

dataframe3 = pd.read_excel(ruta_excel_base3,sheet_name='Priorizacion '+mes3)
dataframe3[mes3]=1

dataframe_fusionado = pd.merge(dataframe1, dataframe2,on='NODO',how='outer')
dataframe_fusionado = pd.merge(dataframe_fusionado,dataframe3, on='NODO', how='outer')

dataframe_fusionado[mes1].fillna(0, inplace=True)
dataframe_fusionado[mes2].fillna(0, inplace=True)
dataframe_fusionado[mes3].fillna(0, inplace=True)

columnas=['NODO',mes1,mes2,mes3]

dataframe_fusionado = dataframe_fusionado[columnas]

dataframe_fusionado.to_excel('file.xlsx',index=False)

libro_trabajo = openpyxl.load_workbook()
hoja = libro_trabajo.active


