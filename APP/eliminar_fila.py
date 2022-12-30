import pandas as pd 
import csv

def borrar_linea_pd(csv_ruta : str, rango):
    
    info = pd.read_csv(csv_ruta)
    info.drop(rango, axis = 0, inplace = True)
    info.to_csv(csv_ruta, index = False)
    
    
