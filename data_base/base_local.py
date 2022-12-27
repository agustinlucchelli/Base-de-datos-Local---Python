import csv
import os
from shutil import rmtree



def leer(nombre, directorio):
    
        try:
            with open(f"{directorio}/{nombre}.csv", newline = "") as csv_info:
                
                informacion = csv.reader(csv_info, dialect = "excel", delimiter = ",")
                informacion = list(informacion)

                for linea in informacion:
                    if len(linea) == 1:
                        raise IndexError
                    elif len(linea) != len(informacion[0]): 
                        print("Archivo invalido, revise las cantidad de columnas en las lineas.")
                    else:
                        yield linea
                    

        except IndexError:
            print("El archivo no esta delimitado por comas, reviselo. 'data_base/{nombre}.csv'")

        except FileNotFoundError:
            print(f"Archivo no encontrado, revise el directorio. 'data_base/{nombre}.csv'")
        
        except IOError:
            print(f"Archivo corrupto. 'data_base/{nombre}.csv'")
        

def escribir(nombre, lista, directorio):
    
    obtencion = list(leer(nombre, directorio))
    if len(lista) != len(obtencion[0]):
        return print("Lista de datos no coincidente con el numero de columnas de la tabla.")
    
    try: 
        with open(f"{directorio}/{nombre}.csv", "a",newline = "\n") as csv_file:
                
            escrito = csv.writer(csv_file, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
            escrito.writerow(lista)
    except IndexError:
        print("El archivo no esta delimitado por comas, reviselo. '{directorio}/{nombre}.csv'")

    except FileNotFoundError:
        print(f"Archivo no encontrado, revise el directorio. '{directorio}/{nombre}.csv'")
        
    except IOError:
        print(f"Archivo corrupto. '{directorio}/{nombre}.csv'")
        
def crear(nombre, var,lista, directorio):
    
    if var == 0:
        if f"{nombre}.csv" in os.listdir(directorio):
            return "existe"
        else:
            with open(f"{directorio}/{nombre}.csv", "w",newline = "\n") as csv_file:
                escrito = csv.writer(csv_file, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
                escrito.writerow(lista)
    elif var == 1:
        
        if nombre in os.listdir(directorio) and os.path.isdir(f"{directorio}/{nombre}"):
            return "existe"
        else:
            os.mkdir(f"{directorio}/{nombre}")
    elif var == 2:
        
        if f"{nombre}.txt" in os.listdir(directorio) and os.path.isfile(f"{directorio}/{nombre}"):
            return "existe"
        else:
            var = open(f"{directorio}/{nombre}.txt", "w")
            var.close()

class Data_Base():
    
    def __init__(self, directorio, **kwargs):
        
        self.directorio = directorio
        
        self.conteo = {}
        
        for i in kwargs:
            exec(f'self.{i} = kwargs[i]')
                 
        if self.nombre in os.listdir(self.directorio) and f"{self.nombre}.txt" not in os.listdir(self.directorio):
            
            rmtree(f"{self.directorio}/{self.nombre}")
            
        elif f"{self.nombre}_{self.validacion}" not in os.listdir(self.directorio) and f"{self.nombre}_{self.validacion}.txt" in os.listdir(self.directorio):
                 
            os.remove(f"{self.directorio}/{self.nombre}_{self.validacion}.txt")
                 
        crear(f"{self.nombre}_{self.validacion}",1,[], self.directorio)
        crear(f"{self.nombre}_{self.validacion}",2,[], self.directorio)
        
    def crear_tabla(self,**kwargs):
        
        nombre_csv = kwargs["nombre"]
        
        self.conteo[nombre_csv] = 0
        
        if f"{nombre_csv}.txt" in os.listdir(f"{self.directorio}/{self.nombre}_{self.validacion}"):
            
            pass
        
        else:
        
            if len(kwargs["lista_head"]) == 0:
                print("lista de cabecera vacia, revise el parametro.")

            else:

                if f"{self.nombre}_{self.validacion}/{nombre_csv}.txt" not in os.listdir(f"{self.directorio}/{self.nombre}_{self.validacion}") and f"{self.nombre}_{self.validacion}/{nombre_csv}.csv" in os.listdir(f"{self.directorio}/{self.nombre}_{self.validacion}"):
                    os.remove(f"{self.nombre}_{self.validacion}/{nombre_csv}.csv")
                crear(f"{self.nombre}_{self.validacion}/{nombre_csv}",0,kwargs["lista_head"], self.directorio)
                crear(f"{self.nombre}_{self.validacion}/{nombre_csv}",2,[], self.directorio)
        
    def borrar_tabla(self, **kwargs):

        if kwargs["nombre"] + ".csv" not in os.listdir(f"{self.directorio}/{self.nombre}_{self.validacion}"):
            print("tabla a borrar inexistente.")
        else:
            nombre = kwargs["nombre"]
            os.remove(f"{self.directorio}/{self.nombre}_{self.validacion}/{nombre}.csv")
            os.remove(f"{self.directorio}/{self.nombre}_{self.validacion}/{nombre}.txt")
            
    def borrar_fila(self, **kwargs):
        
        nombre = kwargs["nombre"]
        
        if kwargs["nombre"] + ".csv" not in os.listdir(f"{self.directorio}/{self.nombre}_{self.validacion}"):
            
            print(f"tabla inexistente.  '{self.directorio}/{self.nombre}_{self.validacion}/{nombre}.csv'")
            
        else:
            lineas = list(leer(f"{self.nombre}_{self.validacion}/{nombre}", self.directorio))
            
            if "-" not in kwargs["fila"]:
                
                filas = kwargs["fila"]
                
                if int(filas) > len(lineas) - 1:
                
                    print(f"parametro 'numero de fila', excede el rango del csv, el maximo de filas es: {len(lineas)}")
                
                else:
                
                    for i in range(len(lineas)):
                    
                        if i == int(filas):
                            lineas.pop(i)
                            
                    self.borrar_tabla(nombre = nombre)
                    self.crear_tabla(nombre = nombre, lista_head = lineas[0])
                    for i in range(len(lineas)-1):
                        self.agregar_datos(nombre = nombre, lista = lineas[i+1])
                
            else:
                
                filas = kwargs["fila"].split("-")
                
                if filas[0] > filas[1]:
                    
                    print("El orden de filas debe ir de menor a mayor.")
            
                if int(filas[1]) > len(lineas) - 1 and int(filas[0]) < 0:
                    
                    print(f"parametro 'numero de fila', excede el rango del csv, el maximo de filas es: {len(lineas)}")

                else: 
                    
                    count = -1
                    
                    for i in range(len(lineas)):
                        
                        if i >= int(filas[0]) and 1 < int(filas[1]):
                            
                            count += 1
                            lineas.pop(i-count)
                        
                    self.borrar_tabla(nombre = nombre)
                    self.crear_tabla(nombre = nombre, lista_head = lineas[0])
                    for i in range(len(lineas)-1):
                        self.agregar_datos(nombre = nombre, lista = lineas[i+1])
                
    
    def borrar_db(self, **kwargs):
        
        if kwargs["nombre"] not in os.listdir(f"{self.directorio}"):
            print("base de datos a borrar inexistente.")
        else:
            rmtree(f"{self.directorio}/{self.nombre}")
            os.remove(f"{self.directorio}/{self.nombre}_{self.validacion}.txt")
            
    def agregar_datos_estatico(self, **kwargs):
        
        nombre = kwargs["nombre"]
        
        if kwargs["nombre"] + ".csv" not in os.listdir(f"{self.directorio}/{self.nombre}_{self.validacion}"):
            
            print("tabla inexistente.")

        else:
            
            self.conteo[nombre] += 1
            lineas = list(leer(f"{self.nombre}_{self.validacion}/{nombre}", self.directorio))
             
            if len(lineas) == self.conteo[nombre]:
                escribir(f"{self.nombre}_{self.validacion}/{nombre}", kwargs["lista"], self.directorio)
            
    
    def agregar_datos(self, **kwargs):
        
        nombre = kwargs["nombre"]
        
        if kwargs["nombre"] + ".csv" not in os.listdir(f"{self.directorio}/{self.nombre}_{self.validacion}"):
            
            print(f"tabla inexistente. '{self.directorio}/{self.nombre}_{self.validacion}/{nombre}.csv'")
            
        else:
            
            self.conteo[nombre] += 1
            lineas = list(leer(f"{self.nombre}_{self.validacion}/{nombre}", self.directorio))
            escribir(f"{self.nombre}_{self.validacion}/{nombre}", kwargs["lista"], self.directorio)
    
    def actualizar(self, **kwargs):
        
        nombre = kwargs["nombre"]
        
        if kwargs["nombre"] + ".csv" not in os.listdir(f"{self.directorio}/{self.nombre}_{self.validacion}"):
            
            print(f"tabla inexistente.  '{self.directorio}/{self.nombre}_{self.validacion}/{nombre}.csv'")
            
        else:
            
            lineas = list(leer(f"{self.nombre}_{self.validacion}/{nombre}", self.directorio))
            
            if int(kwargs["actualizacion"][0]) > len(lineas) - 1:
                print(f"parametro 'numero de fila', excede el rango del csv, el maximo de filas es: {len(lineas)}")
            elif int(kwargs["actualizacion"][1]) > len(lineas[0]) - 1:
                print(f"parametro 'numero de columna', excede el rango del csv, el maximo de columnas es: {len(lineas[0])}")
            elif int(kwargs["actualizacion"][0]) > len(lineas) - 1 and int(kwargs["actualizacion"][1]) > len(lineas[0]) - 1:
                print(f"parametro 'numero de columna', excede el rango del csv, el maximo de columnas es: {len(lineas[0])}")
                print(f"parametro 'numero de fila', excede el rango del csv, el maximo de filas es: {len(lineas)}")
            else:
                
                for i in range(len(lineas)):
                    if i == int(kwargs["actualizacion"][0]):
                        for j in range(len(lineas[i])):
                            if j == int(kwargs["actualizacion"][1]) - 1:
                                lineas[i][j] = kwargs["actualizacion"][2]
                
                self.borrar_tabla(nombre = nombre)
                self.crear_tabla(nombre = nombre, lista_head = lineas[0])
                for i in range(len(lineas)-1):
                    self.agregar_datos(nombre = nombre, lista = lineas[i+1])
                    
    
    def consultar_datos(self, **kwargs):
        
        nombre = kwargs["nombre"]
        
        if kwargs["nombre"] + ".csv" not in os.listdir(f"{self.directorio}/{self.nombre}_{self.validacion}"):
            
            print(f"tabla inexistente.  '{self.directorio}/{self.nombre}_{self.validacion}/{nombre}.csv'") 
            
        else:
            
            if kwargs["modo"][0] == "casilla" and int(len(kwargs["modo"])) < 3:
                print("falta especificar la posicion de la casilla.")
            else:
                if kwargs["modo"][0] == "casilla":
                    
                    lineas = list(leer(f"{self.nombre}_{self.validacion}/{nombre}", self.directorio))
                    
                    if int(kwargs["modo"][1]) > len(lineas):
                        print(f"parametro 'numero de fila', excede el rango del csv, el maximo de filas es: {len(lineas)}")
                    elif int(kwargs["modo"][2]) > len(lineas[0]) - 1:
                        print(f"parametro 'numero de columna', excede el rango del csv, el maximo de columnas es: {len(lineas[0])}")
                    elif int(kwargs["modo"][1]) > len(lineas) - 1 and int(kwargs["modo"][2]) > len(lineas[0]) - 1:
                        print(f"parametro 'numero de columna', excede el rango del csv, el maximo de columnas es: {len(lineas[0])}")
                        print(f"parametro 'numero de fila', excede el rango del csv, el maximo de filas es: {len(lineas)}")
                        
                    else:
                        
                        return lineas[int(kwargs["modo"][1])][int(kwargs["modo"][1])]
                
                elif kwargs["modo"][0] == "completo":
                    
                    return list(leer(f"{self.nombre}_{self.validacion}/{nombre}", self.directorio))