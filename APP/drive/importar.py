import pandas as pd 

def importar_excel(directorio_excel : str, directorio_base_csv):
    try:
        Data_Frame = pd.read_excel(directorio_excel)
        
        if "/" in directorio_excel:
            nombre = directorio_excel.split("/")[-1]
            Data_Frame.to_csv(directorio_base_csv + "/" + nombre, index = False)
        elif "\\" in directorio_excel:
            nombre = directorio_excel.split("\\")[-1]
            Data_Frame.to_csv(directorio_base_csv + "\\" + nombre, index = False)
        else:
            nombre = directorio_excel
            Data_Frame.to_csv(nombre, index = False)
        
    except FileNotFoundError:
        return f"el archivo Excel es inexistente en el directorio: {directorio_excel}"
    except IOError:
        
        return f"archivo {nombre} corrupto."
    except:
        return "ocurrio un error con la importacion del archivo Excel."