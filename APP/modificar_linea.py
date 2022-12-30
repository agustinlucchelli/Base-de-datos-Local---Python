import eliminar_fila ,os
import pandas as pd

def modificar_linea(csv_ruta : str, row, head, range):
    
    eliminar_fila.borrar_linea_pd(csv_ruta, range)
    
    diccionario = dict(zip(head, row))
    
    dt = pd.DataFrame([diccionario])
    csv_ = pd.read_csv(csv_ruta)
    dt.to_csv("medio.csv", index = False)
    csv_cabeza = csv_[:range]
    csv_cabeza.to_csv("cabeza.csv", index = False)
    csv_pie = csv_[range:]
    csv_pie.to_csv("pie.csv", index = False)
    
    dt_final = pd.concat(map(pd.read_csv, ["cabeza.csv", "medio.csv", "pie.csv"]), ignore_index = True, axis = 0)
    os.remove(csv_ruta)
    dt_final.to_csv(csv_ruta, index = False)
    os.remove("cabeza.csv")
    os.remove("pie.csv")
    os.remove("medio.csv")