from functools import partial
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from tkinter import Tk
from tkinter import *
from customtkinter import *
from tkinter import *

def login():
    gauth = GoogleAuth()
        
    return GoogleDrive(gauth)

def crear_archivo_texto(nombre_archivo, contenido, id_folder):
    
    credenciales = login()
    archivo = credenciales.CreateFile({"title" : nombre_archivo,
                                       "parents" : [{"kind" : "drive#filelink", "id" : id_folder}]})
    archivo.SetContentString(contenido)
    archivo.Upload()
    
    
def subir_archivo(ruta_archivo, id_folder):
    
    credenciales = login()
    archivo = credenciales.CreateFile({"parents" : [{"kind" : "drive#filelink", "id" : id_folder}]})
    archivo["title"] = ruta_archivo.split("/")[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()    
    
def bajar_archivo_por_id(id_drive,ruta_descarga):
    
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_drive}) 
    nombre_archivo = archivo['title']
    archivo.GetContentFile(ruta_descarga + nombre_archivo)
    
def busca(query):
    resultado = []
    credenciales = login()
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    for f in lista_archivos:
       resultado.append({"id" : f["id"], "embebido" : f['embedLink'], "title" : f['title'], "type" : f['mimeType']})
    return resultado

# DESCARGAR UN ARCHIVO DE DRIVE POR NOMBRE
def bajar_acrchivo_por_nombre(nombre_archivo,ruta_descarga):
    credenciales = login()
    lista_archivos = credenciales.ListFile({'q': "title = '" + nombre_archivo + "'"}).GetList()
    if not lista_archivos:
        print('No se encontro el archivo: ' + nombre_archivo)
    archivo = credenciales.CreateFile({'id': lista_archivos[0]['id']}) 
    archivo.GetContentFile(ruta_descarga + nombre_archivo)

# BORRAR/RECUPERAR ARCHIVOS
def borrar_recuperar(id_archivo):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    # MOVER A BASURERO
    archivo.Trash()
    # SACAR DE BASURERO
    archivo.UnTrash()
    # ELIMINAR PERMANENTEMENTE
    archivo.Delete()

# CREAR CARPETA
def crear_carpeta(nombre_carpeta,id_folder):
    credenciales = login()
    folder = credenciales.CreateFile({'title': nombre_carpeta, 
                               'mimeType': 'application/vnd.google-apps.folder',
                               'parents': [{"kind": "drive#fileLink",\
                                                    "id": id_folder}]})
    folder.Upload()

# MOVER ARCHIVO
def mover_archivo(id_archivo,id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    propiedades_ocultas = archivo['parents']
    archivo['parents'] = [{'isRoot': False, 
                           'kind': 'drive#parentReference', 
                           'id': id_folder, 
                           'selfLink': 'https://www.googleapis.com/drive/v2/files/' + id_archivo + '/parents/' + id_folder,
                           'parentLink': 'https://www.googleapis.com/drive/v2/files/' + id_folder}]
    archivo.Upload(param={'supportsTeamDrives': True})   
    
    
def descarga(lista):
    
    for i in range(len(lista)):
        
        if globals()[f"control_var_{i}"].get() == i + 1:
            
            print("si")
            
            bajar_archivo_por_id(lista[i]["id"], "import_")
    
    
def importar_drive(nombre_archivo, ruta_base_importacion):
    
    lista = busca(nombre_archivo) 
    
    app = CTk()

    for i in range(len(lista)):
        
        globals()[f"control_var_{i}"] = IntVar()
        
        globals()[f"radio_button_{i}"] = CTkCheckBox(master = app, text = f"{lista[i]['title']} - {lista[i]['type']}", variable = globals()[f"control_var_{i}"], onvalue = i + 1)
        globals()[f"radio_button_{i}"].pack(pady = 20)
        globals()[f"boton_ver_{i}"] = CTkButton(app, text = "ver", command = partial(os.system, f"start {lista[i]['embebido']}"))
        globals()[f"boton_ver_{i}"].pack(pady = 20)

    button_dowload = CTkButton(app, text = "Descargar", command = partial(descarga, lista))
    button_dowload.pack()
        
    app.mainloop()
        
importar_drive("title = 'correo.csv'", "")