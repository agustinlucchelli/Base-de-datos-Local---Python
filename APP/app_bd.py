#!/usr/bin/env python

from tkinter import *
from tkinter import ttk
from functools import partial
from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
import  os, csv, correo, pdf_app, excel_app, base_local, eliminar_fila, cripto
import modificar_linea as mod
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def validacion_correos(correo_entrante) -> bool:
    
    parm = False
    correo.leer_correo()
    try:
        with open(f"{BASE_DIR}\\APP\\Envio_csv\\tabla_correo.csv", newline = "") as csv_info:
                
            informacion = csv.reader(csv_info, dialect = "excel", delimiter = ",")
            informacion = list(informacion)

    except FileNotFoundError:
            print(f"Archivo no encontrado, revise el directorio. 'Envio_csv\\tabla_correo.csv'")
        
    except IOError:
            print(f"Archivo corrupto. 'Envio_csv\\tabla_correo.csv'")

    info = list(informacion)
    
    for i in range(1, len(info)):
        
        if cripto.desencriptar(info[i][0]) == correo_entrante:
            parm = True
    return parm
    
COUNT = 0
DIR = os.path.realpath(__file__)
DIR = DIR.split("\\")
DIR.pop(len(DIR)-1)
DIR = "\\".join(DIR)

globals()["ESTADO"] = "CORREO"
globals()["lista_bases"] = []
globals()["lista_filas"] = []

def acortador_2(boton : 'Label', barra_nav, boton_enviar_pdf : 'Label', boton_enviar_excel : 'Label', boton_opcion : 'Label', boton_1 : 'CTkButton', boton_2 : 'CTkButton', boton_3 : 'CTkButton', boton_4 : 'CTkButton', boton_5 : 'CTkButton', boton_6 : 'CTkButton', parm, parm_2, parm_3, modo, imagen):
    
    boton.config(image = imagen)
    boton.config(background = parm_2)
    barra_nav.config(background = parm_2)
    set_appearance_mode(modo)
    
    imagen_pdf = Image.open(DIR + "\\imagenes_00!1\\pdf" + parm + ".png")
    imagen_pdf = imagen_pdf.resize((52,52))
    imagen_pdf = ImageTk.PhotoImage(imagen_pdf) 
    
    imagen_pdf_2 = Image.open(DIR + "\\imagenes_00!1\\pdf_2" + parm + ".png")
    imagen_pdf_2 = imagen_pdf_2.resize((50,50))
    imagen_pdf_2 = ImageTk.PhotoImage(imagen_pdf_2) 
    
    imagen_excel = Image.open(DIR + "\\imagenes_00!1\\excel" + parm + ".png")
    imagen_excel = imagen_excel.resize((55,36))
    imagen_excel = ImageTk.PhotoImage(imagen_excel) 
    
    imagen_excel_2 = Image.open(DIR + "\\imagenes_00!1\\excel_2" + parm + ".png")
    imagen_excel_2 = imagen_excel_2.resize((53,34))
    imagen_excel_2 = ImageTk.PhotoImage(imagen_excel_2)
    
    imagen_correo = Image.open(DIR + "\\imagenes_00!1\\boton_correo" + parm + ".png")
    imagen_correo = imagen_correo.resize((53,30))
    imagen_correo = ImageTk.PhotoImage(imagen_correo)
    
    imagen_correo_1 = Image.open(DIR + "\\imagenes_00!1\\boton_local" + parm + ".png")
    imagen_correo_1 = imagen_correo_1.resize((53,30))
    imagen_correo_1 = ImageTk.PhotoImage(imagen_correo_1)
        
    boton_1.configure(text_color = parm_3)
    boton_2.configure(text_color = parm_3)
    boton_4.configure(text_color = parm_3)
    boton_5.configure(text_color = parm_3)
    boton_6.configure(text_color = parm_3)
    try:
        boton_3.configure(text_color = parm_3)
    except:
        pass
    
    boton_enviar_pdf.config(image = imagen_pdf)
    boton_enviar_excel.config(image = imagen_excel)
    boton_opcion.config(image = imagen_correo)
        
    boton_enviar_pdf.bind("<Enter>", partial(cambio_boton, boton_enviar_pdf, imagen_pdf, imagen_pdf_2))
    boton_enviar_pdf.bind("<Leave>", partial(cambio_boton, boton_enviar_pdf, imagen_pdf, imagen_pdf_2))
        
    boton_enviar_excel.bind("<Enter>", partial(cambio_boton, boton_enviar_excel, imagen_excel, imagen_excel_2))
    boton_enviar_excel.bind("<Leave>", partial(cambio_boton, boton_enviar_excel, imagen_excel, imagen_excel_2))
        
    boton_opcion.bind("<Button-1>", partial(cambio_boton, boton_opcion, imagen_correo, imagen_correo_1))

def capturadora(captura : str, dir):
    
    if captura == "Correo invalido, ingrese nuevamente.":
        
        messagebox.showinfo(title = "Error_Enviar_Correo", message = "Correo invalido, ingrese nuevamente.")
        
    elif captura == "Error correo invalido" or captura == "correos o contraseñas equivocados.":
        
        messagebox.showinfo(title = "Error_Enviar_Correo", message = "programa desconfigurado, contacte con el desrollador.")
        
    elif captura == "directorio no encontrado, revise el directorio.":
        
        messagebox.showinfo(title = "Error_Enviar_Correo", message = f"directorio no encontrado, revise el directorio. '{dir}'")
    elif captura == "directorio corrupto.":
        
        messagebox.showinfo(title = "Error_Enviar_Correo", message = f"directorio corrupto. '{dir}'")
    else:
        os.remove(dir)


def enviar_excel_command( directorio_excel, directorio_csv, entrada_1 : 'CTkEntry', html_archivo):
    
    salida = entrada_1.get()
    
    validacion = validacion_correos(salida)
    if validacion:

        if salida == "":
            messagebox.showinfo(title = "Error", message = "No se ingrese ningun correo.")
            
        excel_app.converti_excel(directorio_csv, directorio_excel)
            
        captura = correo.enviar("excel", directorio_excel, salida, html_archivo)
            
        capturadora(captura, directorio_excel)
    else:
        
       parm = messagebox.askokcancel("Redirect","Mail no valiado, desea validarlo?")
       if parm:
           os.system("start https://devcop.pythonanywhere.com")
           

def envia_excel(tabla, dir_, event):
    
    dir = DIR + f"\\{tabla}.csv"
    html_archivo = DIR + f"\\correo_excel.html"
    
    if globals()["ESTADO"] == "CORREO":
        
        app_3 = CTk()
        app_3.geometry("400x150")
        app_3.resizable(False, False)
        app_3.title("Base de Datos")
        
        entrada_1 = CTkEntry(app_3, width = 250, font = ("arial", 15), justify = CENTER, text_color = "gray", border_width = 1)
        entrada_1.insert(0, "Ingrese su correo:")
        entrada_1.bind("<FocusIn>", partial(marca_agua, entrada_1, 2))
        entrada_1.bind("<FocusOut>", partial(marca_agua, entrada_1, 2))
        entrada_1.bind("<Enter>", partial(border_1, entrada_1))
        entrada_1.bind("<Leave>", partial(border_2, entrada_1))
        entrada_1.pack(pady = 10, ipady = 7)

        boton_2_ = CTkButton(app_3, text = "Enviar", width = 200, height = 65, command = partial(enviar_excel_command, dir, dir_, entrada_1, html_archivo))
        boton_2_.pack(pady = 10)
        app_3.mainloop()
        
    else:
    
        directorio = filedialog.asksaveasfilename()
        directorio = directorio + f"_{tabla}.xlsx"
        
        excel_app.converti_excel(dir_, directorio)


def enviar_pdf_command(dir, dir_, entrada : 'CTkEntry', html_archivo):
    
    salida = entrada.get()
    
    validacion = validacion_correos(salida)
    if validacion:
        if salida == "":
            messagebox.showinfo(title = "Error", message = "No se ingrese ningun correo.")
        
        pdf_app.crear_pdf(dir, dir_)
            
        captura = correo.enviar("pdf", dir, salida, html_archivo)
            
        capturadora(captura, dir)
    else:
        
       parm = messagebox.askokcancel("Redirect","Mail no valiado, desea validarlo?")
       if parm:
           os.system("start https://devcop.pythonanywhere.com")
           
    

def envia_pdf(tabla, dir_, event):
    
    
    dir = DIR + f"\\{tabla}.csv"
    html_archivo = DIR + f"\\correo_pdf.html"

    if globals()["ESTADO"] == "CORREO":

        app_2 = CTk()
        app_2.geometry("400x150")
        app_2.resizable(False, False)
        app_2.title("Base de Datos")
        
        entrada_ = CTkEntry(app_2, width = 250, font = ("arial", 15), justify = CENTER, text_color = "gray", border_width = 1)
        entrada_.insert(0, "Ingrese su correo:")
        entrada_.bind("<FocusIn>", partial(marca_agua, entrada_, 2))
        entrada_.bind("<FocusOut>", partial(marca_agua, entrada_, 2))
        entrada_.bind("<Enter>", partial(border_1, entrada_))
        entrada_.bind("<Leave>", partial(border_2, entrada_))
        entrada_.pack(pady = 10, ipady = 7)

            
        boton_1_ = CTkButton(app_2, text = "Enviar", width = 200, height = 65, command = partial(enviar_pdf_command, dir, dir_, entrada_, html_archivo))
        boton_1_.pack(pady = 10)
        
        app_2.mainloop()
        
    else:
        
        directorio = filedialog.asksaveasfilename()
        directorio = directorio + f"_{tabla}.pdf"
        
        pdf_app.crear_pdf(directorio, dir_)
        
        
def borrar_base(tabla : 'ttk.Treeview', directorio, lista):
    
    try:
        id = tabla.selection()[0]
    except IndexError:
        messagebox.showinfo(title = "Errro", message = "seleccione una base.")
    
    db = tabla.item(id, option = "text")
    
    db = str(db).split("_")
    
    base = base_local.Data_Base(nombre = "mod", validacion = "gestion")
    base.borrar_db(directorio = directorio, nombre = db[0], validacion = db[1])
    
    for i in lista:
        tabla.delete(globals()[f"fila_{i}"])
        
    lista = []
            
    for i in os.listdir(directorio):
                
        if os.path.isdir(f"{directorio}/{i}") and i != "imagenes_00!1" and i != "APP":
            lista.append(i)
            
    for i in lista:
                    
        globals()[f"fila_{i}"] = tabla.insert("", END, text = i)


def agregar_base(tabla : 'ttk.Treeview', lista, entrada_1 : 'CTkEntry', directorio):
    
    data = str(entrada_1.get())
    
    if "_" not in str(entrada_1.get()) or len(data.split("-")) > 2:
        messagebox.showinfo(title = "Error", message = "Debe ingresar entre '_', el nombre y validacion de la base.")
    else:
        
        base_local.Data_Base(nombre = data.split("_")[0], validacion = data.split("_")[1], directorio = directorio)
        
        globals()[f"fila_{data.split('_')[0]}"] = tabla.insert("", END, text = data)
        globals()["lista_bases"].append(globals()[f"fila_{data.split('_')[0]}"])
        


def acortador_1(directorio, main_label : 'LabelFrame', entrada : 'ttk.Treeview', boton_3 : 'CTkButton', boton_2 : 'CTkButton', boton_1 : 'CTkButton', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label', texto_1 : 'CTkLabel', boton_opcion : 'CTkLabel', entrada_1 : 'CTkEntry', boton_4 : 'CTkButton', boton_5 : 'CTkButton',boton_6 : 'CTkButton', v : 'ttk.Scrollbar'):
    
    try:
        if "base_local.py" in os.listdir(directorio):
            
            v.pack_forget()
            
            lista = []
            
            for i in os.listdir(directorio):
                
                if os.path.isdir(f"{directorio}/{i}") and i != "imagenes_00!1" and i != "APP":
                    lista.append(i)
            
            entrada.pack_forget()
            boton_3.destroy()
            
            tabla = ttk.Treeview(main_label)
            tabla.heading("#0", text = "bases de datos")
            
            yscrollbar = ttk.Scrollbar(main_label, orient = "vertical", command = tabla.yview)
            yscrollbar.pack(side = RIGHT, fill = "y")
            
            xscrollbar = ttk.Scrollbar(main_label, orient = "horizontal", command= tabla.xview)
            xscrollbar.pack(side = BOTTOM, fill = "x")
            
            for i in lista:
                    
                globals()[f"fila_{i}"] = tabla.insert("", END, text = i)       
            
            tabla.place(x = 0, y = 0, width = 585, height = 432)
            
            boton_4.configure(state = NORMAL, command = partial(borrar_base, tabla, directorio, lista))
            
            boton_1.configure(command = partial(listar_tablas, tabla, directorio, lista, boton_1, boton_2, yscrollbar, xscrollbar, main_label, app, boton_pdf, boton_excel, texto_1, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v))
            boton_2.configure(text = "Atras", command = partial(
                                                                atras_1,
                                                                tabla,
                                                                yscrollbar,
                                                                xscrollbar,
                                                                boton_1,
                                                                boton_2,
                                                                main_label,
                                                                app,
                                                                boton_pdf,
                                                                boton_excel,
                                                                texto_1,
                                                                boton_opcion,
                                                                entrada_1,
                                                                boton_4,
                                                                boton_5,
                                                                boton_6,
                                                                v
                                                                ))
            
            entrada_1.configure(state = NORMAL, text_color = "gray")
            entrada_1.insert(0, "Ingrese nombre:")
            
            boton_6.configure(state = NORMAL, command = partial(agregar_base, tabla, lista, entrada_1, directorio))            
        else:
            
            messagebox.showinfo(title = "Error", message = "Este no es el directorio de la base de datos.")
    
    except FileNotFoundError:
        
        messagebox.showinfo(title = "Directorio Invalido", message = f"Directorio no existente '{directorio}'")
        
    except OSError:
        
        messagebox.showinfo(title = "campo vacio", message = "Ingrese un directorio.")


def fun_1():
    
    archivos = os.listdir()
    
    text = "\n                      ARCHIVOS DIRECTORIO ACTUAL: \n\n"   
    
    for i in archivos:
        
        text += f"  {i}\n"
        
    return text


def comandos(boton_1 : 'CTkButton', boton_3 : 'CTkButton', entrada : 'CTkEntry', main_label : 'LabelFrame', boton_2 : 'CTkButton', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label', texto_1 : 'CTkLabel', boton_opcion : 'CTkLabel', entrada_1 : 'CTkEntry', boton_4 : 'CTkButton', boton_5 : 'CTkButton', boton_6 : 'CTkButton', v : 'ttk.Scrollbar'):
    
    boton_1.configure(command = partial(listar_db, entrada, main_label, boton_1, boton_3, boton_2, app, boton_pdf, boton_excel, texto_1, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v))
    boton_3.configure(command = partial(listar_db_buscador, entrada, main_label, boton_1, boton_3, boton_2, app, boton_pdf, boton_excel, texto_1, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v))
    
def atras_3(boton_2 : 'CTkButton', tabla : 'ttk.Treeview', lista_, lista, boton_1 : 'CTkButton', directorio, yscrollbar : 'ttk.Scrollbar', xscrollbar : 'ttk.Scrollbar', main_label : 'LabelFrame', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label', texto_1 : 'CTkLabel', base, lista__, boton_opcion : 'CTkLabel', entrada_1 : 'CTkEntry', boton_4 : 'CTkButton', boton_5 : 'CTkButton', boton_6 : 'CTkButton', v : 'ttk.Scrollbar'):
            
    boton_pdf.place_forget()
    boton_excel.place_forget()
    texto_1.place_forget()
    boton_opcion.place_forget()
    boton_1.configure(state = NORMAL)
            
    for i in range(len(lista)):
        
        tabla.delete(globals()[f"#{i}"])   
        
    for i in range(1, len(lista[0]) + 1):  
        tabla.column(f"#{i}", width = 0)

    tabla.column("#0", width = 585)
    tabla.heading("#0", text = "tablas") 
            
    for i in lista_:
                        
        globals()[f"fila_{i}"] = tabla.insert("", END, text = i)
        
    for i in globals()["lista_filas"]:
        
        tabla.delete(i)
        
    boton_2.configure(command = partial(
            atras_2,
            boton_1,
            boton_2,
            tabla,
            directorio, 
            lista__,
            yscrollbar, 
            xscrollbar,
            main_label,
            app, 
            boton_pdf,
            boton_excel,
            texto_1,
            base,
            boton_opcion,
            entrada_1,
            boton_4,
            boton_5,
            boton_6,
            v
            ))
    
    entrada_1.delete(0, END)


def borrar_linea(dir, tabla : 'ttk.Treeview' , lista):
    
    try:
        index = 0
        try:
            id = tabla.selection()[0]
        except IndexError:
            messagebox.showinfo(title = "Error", message = "seleccione una fila.")
        for i in range(len(lista)):
            if str(id) == globals()[f"#{i}"]:
                tabla.delete(globals()[f"#{i}"])
                index = i 
            
        eliminar_fila.borrar_linea_pd(dir, index)
        

    except IndexError:
        try:
            
            messagebox.showinfo(title = "Delimiter Error", message = f"El archivo no esta delimitado por comas, reviselo. '{dir}'")
            
        except UnboundLocalError:
            
            messagebox.showinfo(title = "Archivo Error", message = f"No selecciono ninguna tabla.")

    except FileNotFoundError:
        
        messagebox.showinfo(title = "Archivo no encontrado", message = f"Revise el directorio. '{dir}.csv'")
        
    except IOError:
        
        messagebox.showinfo(title = "Archivo corrupto.", message = f"Archivo corrupto. '{dir}.csv'")


def pedir_cambio(entrada_4 : 'CTkEntry', lista, lectura, boton_3_ : 'CTkButton', index, dir, tex_show : 'CTkLabel', count):  
    
    if " " in entrada_4.get():
        messagebox.showerror(title = "Error", message = "no ingrese espacios, sustituyalo por guiones medios")
        tex_show.configure(text = "Error")
        boton_3_.configure(state = DISABLED)
        
        return
    
    lista = lista.split("-")
    lista.pop(len(lista)-1)

    if len(lista) < len(lectura):
        
        count += 1
        
        lista.append("")
        lista = "-".join(lista)
        lista += str(entrada_4.get()) + "-"
        entrada_4.delete(0, END)
        if count < len(lectura):
            tex_show.configure(text = f"columna: {lectura[count]}")
        elif count == len(lectura):
            tex_show.configure(text = f"Listo!")
            lista = lista.split("-")
            lista.pop(len(lista)-1)
                
        boton_3_.configure(command = partial(pedir_cambio, entrada_4, lista, lectura, boton_3_, index, dir, tex_show, count))
        
    if type(lista) == list:
        if len(lista) == len(lectura):
            mod.modificar_linea(dir, lista, lectura, index)
            boton_3_.configure(state = DISABLED)
        

def modificar_linea(lectura, tabla : 'ttk.Treeview', lista, dir):
    
    index = 0
        
    id = tabla.selection()[0]
    
    for i in range(len(lista)):
        
        if str(globals()[f"#{i}"]) == str(id):
            index = i
            
    app_4 = CTk()
    app_4.geometry("400x150")
    app_4.resizable(False, False)
    app_4.title("Base de Datos")
    
    tex_show = CTkLabel(app_4, text = f"columna: {lectura[0][0]}")
    tex_show.pack()    
    
    entrada_4 = CTkEntry(app_4, width = 250, font = ("arial", 15), justify = CENTER, text_color = "gray", border_width = 1)
    entrada_4.insert(0, f"Ingrese modificacion:")
    entrada_4.bind("<FocusIn>", partial(marca_agua, entrada_4, 4))
    entrada_4.bind("<FocusOut>", partial(marca_agua, entrada_4, 4))
    entrada_4.bind("<Enter>", partial(border_1, entrada_4))
    entrada_4.bind("<Leave>", partial(border_2, entrada_4))
    entrada_4.pack(pady = 10, ipady = 7)

    texto = ""
    count = 0
    boton_3_ = CTkButton(app_4, text = "Enviar", width = 200, height = 65)
    boton_3_.configure(command = partial(pedir_cambio, entrada_4, texto,lectura[0], boton_3_, index, dir, tex_show, count))
    boton_3_.pack(pady = 10)
    app_4.mainloop()
        
        
def pedir_cambio_2(entrada_5 : 'CTkEntry', lista, lectura, boton_4_ : 'CTkButton', dir, tex_show : 'CTkLabel', count, tabla : 'ttk.Treeview'):
    
    if " " in entrada_5.get():
        messagebox.showerror(title = "Error", message = "no ingrese espacios, sustituyalo por guiones medios")
        tex_show.configure(text = "Error")
        boton_4_.configure(state = DISABLED)
        
        return
    
    lista = lista.split("-")
    lista.pop(len(lista)-1)

    if len(lista) < len(lectura):
        
        count += 1
        
        lista.append("")
        lista = "-".join(lista)
        lista += str(entrada_5.get()) + "-"
        entrada_5.delete(0, END)
        if count < len(lectura):
            tex_show.configure(text = f"columna: {lectura[count]}")
        elif count == len(lectura):
            tex_show.configure(text = f"Listo!")
            lista = lista.split("-")
            lista.pop(len(lista)-1)
                
        boton_4_.configure(command = partial(pedir_cambio_2, entrada_5, lista,lectura, boton_4_, dir, tex_show, count, tabla))
    if type(lista) == list:
        if len(lista) == len(lectura):
 
            with open(f"{dir}", "a", newline = "\n") as csv_file:
                
                escrito = csv.writer(csv_file, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
                escrito.writerow(lista)
            
            boton_4_.configure(state = DISABLED)

                    
            globals()["lista_filas"].append(tabla.insert("", END, text = "", values = lista))
        
        
def agregar_fila(lectura, tabla : 'ttk.Treeview', dir):
    
    app_5 = CTk()
    app_5.geometry("400x150")
    app_5.resizable(False, False)
    app_5.title("Base de Datos")
    
    tex_show = CTkLabel(app_5, text = f"columna: {lectura[0][0]}")
    tex_show.pack()    
    
    entrada_5 = CTkEntry(app_5, width = 250, font = ("arial", 15), justify = CENTER, text_color = "gray", border_width = 1)
    entrada_5.insert(0, f"Ingrese nombre:")
    entrada_5.bind("<FocusIn>", partial(marca_agua, entrada_5, 3))
    entrada_5.bind("<FocusOut>", partial(marca_agua, entrada_5, 3))
    entrada_5.bind("<Enter>", partial(border_1, entrada_5))
    entrada_5.bind("<Leave>", partial(border_2, entrada_5))
    entrada_5.pack(pady = 10, ipady = 7)

    texto = ""
    count = 0
    boton_4_ = CTkButton(app_5, text = "Enviar", width = 200, height = 65)
    boton_4_.configure(command = partial(pedir_cambio_2, entrada_5, texto, lectura[0], boton_4_, dir, tex_show, count, tabla))
    boton_4_.pack(pady = 10)
    app_5.mainloop()
        

def abrir_tabla(tabla : 'ttk.Treeview', directorio, base, lista_, app : 'Tk', boton_pdf : 'Label', boton_2 : 'CTkButton', boton_1 : 'CTkButton',  yscrollbar : 'ttk.Scrollbar', xscrollbar : 'ttk.Scrollbar', main_label : 'LabelFrame', boton_excel : Label, texto_1 : 'CTkLabel', lista__, boton_opcion : 'CTkLabel', entrada_1 : 'CTkEntry', boton_4 : 'CTkButton', boton_5 : 'CTkButton', boton_6 : 'CTkButton', v : 'ttk.Scrollbar'):
    
    try:
            lista = []
            id = tabla.selection()[0]
            tabla_ = tabla.item(id, option = "text")

            dir = f"{directorio}/{base}/{tabla_}.csv"
            
            with open(f"{directorio}/{base}/{tabla_}.csv") as archivo_csv:
                
                parm = False
                
                lectura = csv.reader(archivo_csv)
                lectura = list(lectura)
                
                for i in lectura:
                    
                    if len(i) != len(lectura[0]): 
                        
                        parm = True
                    
                    
                if len(lectura[0]) == 1:
                        
                    raise IndexError
                    
                elif parm: 
                        
                    messagebox.showinfo(title = "Archivo invalido.", message = f"Revise las cantidad de columnas en las lineas.. '{directorio}/{base}/{tabla_}.csv'")

                else:
                    for i in lectura:
                    
                        lista.append(i)

                tabla.config(columns = lista[0])    
                
                for i in range(len(lista[0])+1):
                    if i != 0:
                        tabla.column(f"#{i}", minwidth = 0, width = 50 + len(lista[0][i-1])*8, stretch = NO)
                    else:
                        tabla.column(f"#{i}", minwidth = 0, width = 50 + len(lista[0][i-1])*8, stretch = NO)

                tabla.heading("#0", text = tabla_)  
                
                for i in range(len(lista[0])):
                    
                    tabla.heading(f"#{i+1}", text = lista[0][i])
                
                for i in lista_:
                            
                    tabla.delete(globals()[f"fila_{i}"])
                    
                lista.pop(0)
                
                for i in range(len(lista)):
                    
                    globals()[f"#{i}"] = tabla.insert("", END, text = "", values = lista[i])
                
            boton_1.configure(state = DISABLED)        
                    
            boton_2.configure(command = partial(atras_3, boton_2, tabla, lista_, lista, boton_1, directorio, yscrollbar, xscrollbar, main_label , app, boton_pdf, boton_excel, texto_1, base, lista__, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v))
                    
            boton_pdf.place(x = 435, y = 507)
            boton_pdf.bind("<Button-1>", partial(envia_pdf, tabla_, dir))
            
            boton_excel.place(x = 495, y = 515)
            boton_excel.bind("<Button-1>", partial(envia_excel, tabla_, dir))
            
            boton_opcion.place(x = 465, y = 567)
            
            texto_1.place(x = 455, y = 475)
            
            boton_4.configure(command = partial(borrar_linea, dir, tabla, lista))
            boton_5.configure(state = NORMAL, command = partial(modificar_linea, list(lectura), tabla, lista, dir))
            boton_6.configure(command = partial(agregar_fila, list(lectura), tabla, dir))
            entrada_1.delete(0, END)
            entrada_1.configure(state = DISABLED , fg_color = "#343638")
        
        
    except IndexError:
        try:
            messagebox.showinfo(title = "Delimiter Error", message = f"El archivo no esta delimitado por comas o esta corrupto, reviselo. '{directorio}/{base}/{tabla_}.csv'")
        except UnboundLocalError:
            
            messagebox.showinfo(title = "Archivo Error", message = f"No selecciono ninguna tabla.")

    except FileNotFoundError:
        
        messagebox.showinfo(title = "Archivo no encontrado", message = f"Revise el directorio. '{directorio}/{base}/{tabla_}.csv'")
        
    except IOError:
        
        messagebox.showinfo(title = "Archivo corrupto.", message = f"Archivo corrupto. '{directorio}/{base}/{tabla_}.csv'")


def atras_2(boton_1 : 'CTkButton', boton_2 : 'CTkButton', tabla : 'ttk.Treeview',directorio, lista, yscrollbar : 'ttk.Scrollbar', xscrollbar : 'ttk.Scrollbar', main_label : LabelFrame, app : 'Tk', boton_pdf : 'Label', boton_excel : 'Label', texto_1 : 'CTkLabel', base, boton_opcion : 'CTkLabel', entrada_1 : 'CTkEntry', boton_4 : 'CTkButton', boton_5 : 'CTkButton', boton_6 : 'CTkButton', v : 'ttk.Scrollbar'):
    
    tabla.destroy()
    yscrollbar.destroy()
    xscrollbar.destroy()
        
    tabla = ttk.Treeview(main_label)
    tabla.heading("#0", text = "bases de datos")
            
    yscrollbar = ttk.Scrollbar(main_label, orient = "vertical", command = tabla.yview)
    yscrollbar.pack(side = RIGHT, fill = "y")
            
    xscrollbar = ttk.Scrollbar(main_label, orient = "horizontal", command= tabla.xview)
    xscrollbar.pack(side = BOTTOM, fill = "x")
            
    for i in lista:
                    
        globals()[f"fila_{i}"] = tabla.insert("", END, text = i)               
            
    tabla.place(x = 0, y = 0, width = 585, height = 432)
    
    boton_1.configure(command = partial(listar_tablas, tabla, directorio, lista, boton_1, boton_2, yscrollbar, xscrollbar, main_label, app, boton_pdf, boton_excel, texto_1, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v))
    boton_2.configure(text = "Atras", command = partial(
                                                                atras_1,
                                                                tabla,
                                                                yscrollbar,
                                                                xscrollbar,
                                                                boton_1,
                                                                boton_2,
                                                                main_label,
                                                                app,
                                                                boton_pdf,
                                                                boton_excel,
                                                                texto_1,
                                                                boton_opcion,
                                                                entrada_1, 
                                                                boton_4, 
                                                                boton_5,
                                                                boton_6,
                                                                v
                                                                ))
    
    entrada_1.delete(0, END)

def borrar_tablas(tabla : 'ttk.Treeview', directorio, base, lista):
    
    base_ = base.split("_")
    
    try:
        id = tabla.selection()[0]
    except IndexError:
        messagebox.showinfo(title = "Error", message = "seleccione una tabla.")
        
    base_1 = tabla.item(id, option = "text")
    
    base_datos = base_local.Data_Base(nombre = "mod", validacion = "gestion")
    base_datos.borrar_tabla( directorio = directorio, nombre_base = base_[0], validacion = base_[1], nombre = base_1)
    
    for i in lista:
                        
        tabla.delete(globals()[f"fila_{i}"])
        
    lista = []
    
    for i in os.listdir(f"{directorio}/{base}"):    
            extension = i.split(".")

            if len(extension) > 1:
                if extension[1] == "csv":
                    lista.append(extension[0])
                    
    for i in lista:
                        
            globals()[f"fila_{i}"] = tabla.insert("", END, text = i)


def agregar_tabla(tabla : 'ttk.Treeview', directorio, base, lista, entrada_1 : 'CTkEntry'):
    
    if "_" not in directorio:
        
        messagebox.showerror(title = "Error", message = "Directorio corrupto.")
    else:  
        data = str(entrada_1.get())
        
        try:
            with open(f"{directorio}/{base}/{data}_{directorio.split('_')[1]}.csv", "w") as csv_file:
                
                pass
            
            with open(f"{directorio}/{base}/{data}_{directorio.split('_')[1]}.txt", "w") as txt_file:
                
                pass
            
            globals()[f"fila_{data}"] = tabla.insert("", END, text = data + "_" + directorio.split('_')[1])
        except:
            
            messagebox.showerror(title = "Error", message = "Error de lectura del sistema." )

def listar_tablas(tabla : 'ttk.Treeview', directorio, lista_, boton_1 : 'Button', boton_2 : 'CTkButton', yscrollbar : 'ttk.Scrollbar', xscrollbar : 'ttk.Scrollbar', main_label : 'LabelFrame', app : 'Tk', boton_pdf : 'Label', boton_excel : 'Label', texto_1 : 'CTkLabel', boton_opcion : 'CTkLabel', entrada_1 : 'CTkEntry', boton_4 : 'CTkButton', boton_5 : 'CTkButton', boton_6 : 'CTkButton', v : 'ttk.Scrollbar'):
    
    try:

        lista = []
            
        id = tabla.selection()[0]
            
        base = tabla.item(id, option = "text")
            
        for i in os.listdir(f"{directorio}/{base}"):    
            extension = i.split(".")

            if len(extension) > 1:
                if extension[1] == "csv":
                    lista.append(extension[0])
                    
        tabla.heading("#0", text = "tablas")
            
        for i in lista_:
                            
            tabla.delete(globals()[f"fila_{i}"])
            
        if len(globals()["lista_bases"]) != 0:
            for i in globals()["lista_bases"]:        
                    
                tabla.delete(i)
                
                
        for i in lista:
                            
            globals()[f"fila_{i}"] = tabla.insert("", END, text = i)
            
        boton_1.configure(command = partial(abrir_tabla,tabla, directorio, base, lista, app, boton_pdf, boton_2, boton_1,  yscrollbar, xscrollbar, main_label, boton_excel, texto_1, lista_, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v))
        boton_2.configure(text = "Atras", command = partial(
                atras_2,
                boton_1,
                boton_2,
                tabla,
                directorio, 
                lista_,
                yscrollbar, 
                xscrollbar,
                main_label,
                app, 
                boton_pdf,
                boton_excel,
                texto_1,
                base,
                boton_opcion,
                entrada_1,
                boton_4,
                boton_5,
                boton_6,
                v
                ))
            
        boton_4.configure(command = partial(borrar_tablas, tabla, directorio, base, lista))
        boton_6.configure(command = partial(agregar_tabla, tabla, directorio, base, lista, entrada_1))

    except FileNotFoundError:
        
        messagebox.showinfo(title = "Directorio Invalido", message = f"Directorio no existente '{directorio}/{base}'")
    except IndexError:
        
        messagebox.showinfo(title = "Directorio Invalido", message = f"No se seleciono ninguna base.") 
    
def atras_1(
            tabla : 'ttk.Treeview',
            yscrollbar : 'ttk.Scrollbar',
            xscrollbar : 'ttk.Scrollbar',
            boton_1 : 'CTkButton',
            boton_2 : 'CTkButton',
            main_label : 'LabelFrame',
            app : 'Tk',
            boton_pdf : 'Label',
            boton_excel : 'Label',
            texto_1 : 'CTkLabel',
            boton_opcion : 'CTkLabel',
            entrada_1 : 'CTkEntry',
            boton_4 : 'CTkButton',
            boton_5 : 'CTkButton',
            boton_6 : 'CTkButton',
            v : 'ttk.Scrollbar'
                    ):
    
    tabla.destroy()
    xscrollbar.destroy()
    yscrollbar.destroy()
    boton_1.destroy()
    boton_2.destroy()
    entrada_1.delete(0, END)
    
    v.pack(fill = "y", side = RIGHT)
    
    entrada = CTkEntry(app, width = 250, font = ("arial", 15), justify = CENTER, text_color = "grey", border_width = 1)
    entrada.insert(0, "Ingrese el directorio:")
    entrada.bind("<FocusIn>", partial(marca_agua, entrada, 1))
    entrada.bind("<FocusOut>", partial(marca_agua, entrada, 1))
    entrada.bind("<Enter>", partial(border_1, entrada))
    entrada.bind("<Leave>", partial(border_2, entrada))
    entrada.pack(pady = 10, ipady = 7)

    boton_3 = CTkButton(app, text = "Buscar Directorio", width = 20, height = 6)
    boton_3.place(x = 450, y = 419)
    
    boton_1 = CTkButton(app, text = "Abrir", width = 200, height = 65)
    boton_1.pack(pady = 10)
    
    boton_2 = CTkButton(app, text = "Salir", width = 200, height = 65, command = app.destroy)
    boton_2.pack(pady = 10)
    
    entrada_1.configure(state = DISABLED, fg_color = "#343638")
    
    comandos(boton_1, boton_3, entrada, main_label, boton_2, app, boton_pdf, boton_excel, texto_1, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v)
            
def listar_db(entrada : 'Entry', main_label : 'LabelFrame', boton_1 : 'Button', boton_3 : 'CTkButton', boton_2 : 'CTkButton', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label', texto_1 : 'CTkLabel', boton_opcion : 'CTkLabel', entrada_1 : 'CTkEntry', boton_4 : 'CTkButton', boton_5 : 'CTkButton', boton_6 : 'CTkButton', v : 'ttk.Scrollbar'):
    
    directorio = entrada.get()
    
    acortador_1(directorio, main_label, entrada, boton_3, boton_2, boton_1, app, boton_pdf, boton_excel, texto_1, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v)
        
    
def listar_db_buscador(entrada : 'CTkEntry', main_label : 'LabelFrame', boton_1 : 'CTkButton', boton_3 : 'CTkButton', boton_2 : 'CTkButton', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label', texto_1 : 'CTkLabel', boton_opcion : 'CTkLabel', entrada_1 : 'CTkEntry', boton_4 : 'CTkButton', boton_5 : 'CTkButton', boton_6 : 'CTkButton', v : 'ttk.Scrollbar'):
    
    info = filedialog.askdirectory()
    directorio = info.capitalize()
    
    if directorio == "":
        return "vacio"
    
    acortador_1(directorio, main_label, entrada, boton_3, boton_2, boton_1, app, boton_pdf, boton_excel, texto_1, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v)
        
        
def marca_agua(entrada : 'CTkEntry', id, event):
    
    global COUNT
    
    COUNT += 1
    
    texto = entrada.get()
    
    if texto == "Ingrese el directorio:" or texto == "Ingrese su correo:" or texto == "Ingrese modificacion:" or texto == "Ingrese nombre:":
        
        entrada.delete(0, END)
        entrada.configure(text_color = "black")
        
    elif texto == "":
        
        entrada.configure(text_color = "gray")
        if id == 1:
            entrada.insert(0, "Ingrese el directorio:")
        elif id == 2:
            entrada.insert(0, "Ingrese su correo:")
        elif id == 3:
            entrada.insert(0, "Ingrese nombre:")
        elif id == 4:
            entrada.insert(0, "Ingrese modificacion:")
    else: 
        
        if str(event) == "<FocusIn event>":
            entrada.configure(text_color = "black")  
        elif str(event) == "<FocusOut event>":
            entrada.configure(text_color = "gray")
             
    if COUNT % 2 == 0:
        
        entrada.configure(fg_color = "#333333")
    
    else:
        
        entrada.configure(fg_color = "#666666")

        
def border_1(entrada : 'CTkEntry', event):
    
    if entrada._state == "normal":
    
        entrada.configure(border_color = "#5499c7", border_width = 2)
        
        string = str(entrada.focus_get())
        
        if len(string) > len(".!ctkentry.!entry") and string != "":
            
            for i in range(len(string) - len(".!ctkentry.!entry")):
                
                string = list(string)
                string.pop(len(string) - i - 8)

        string = "".join(string)       
        
        if string != ".!ctkentry.!entry" or str(entrada._is_focused) == "False" or str(entrada.winfo_name()) not in str(entrada.focus_displayof()):
            
            entrada.configure(text_color = "#5499c7")
    else:
        return


def border_2(entrada : 'CTkEntry', event):
    
    if entrada._state == "normal":
        entrada.configure(border_color = "gray", border_width = 1)
        
        string = str(entrada.focus_get())
        
        if len(string) > len(".!ctkentry.!entry") and string != "":
            
            for i in range(len(string) - len(".!ctkentry.!entry")):
                
                string = list(string)
                string.pop(len(string) - i - 8)

        string = "".join(string)
        
        if string != ".!ctkentry.!entry" or str(entrada._is_focused) == "False" or str(entrada.winfo_name()) not in str(entrada.focus_displayof()):
            
            entrada.configure(text_color = "gray")
            
        elif string == ".!ctkentry.!entry":
            
            entrada.configure(text_color = "black")
    else:
        return
    
    
def cambio_boton(boton : 'Button', imagen_1, imagen_2, event):
    
    if "Leave" in str(event):
        boton.config(image = imagen_1)   
    elif "Enter" in str(event):
        boton.config(image = imagen_2)
    elif "ButtonPress" in str(event):  
        
        if str(boton["image"]) == str(imagen_1):
            boton.config(image = imagen_2)
            
        elif str(boton["image"]) == str(imagen_2):
            boton.config(image = imagen_1)         
            
        if str(boton) == ".!label3":
            
            if globals()["ESTADO"] == "CORREO":
                globals()["ESTADO"] = "LOCAL"
            elif globals()["ESTADO"] == "LOCAL":
                globals()["ESTADO"] = "CORREO"
                

def cambio_tema(boton : 'Label', imagen_1, imagen_2, barra_nav, boton_enviar_pdf : 'Label', boton_enviar_excel : 'Label', boton_opcion : 'Label', boton_1 : 'CTkButton', boton_2 : 'CTkButton', boton_3 : 'CTkButton', boton_4 : 'CTkButton', boton_5 : 'CTkButton', boton_6 : 'CTkButton', event):
    
    if str(boton["image"]) == str(imagen_1):
    
        acortador_2(boton, barra_nav, boton_enviar_pdf, boton_enviar_excel, boton_opcion, boton_1, boton_2, boton_3, boton_4, boton_5, boton_6, "_", "#ebebeb", "#2020dd", "Light", imagen_2)  
        
    elif str(boton["image"]) == str(imagen_2):
        
        acortador_2(boton, barra_nav, boton_enviar_pdf, boton_enviar_excel, boton_opcion, boton_1, boton_2, boton_3, boton_4, boton_5, boton_6, "", "#242424", "white", "Dark", imagen_1)
        
        
def border_enter_button(boton : 'Label', event):
    
    if str(boton["image"]) == "pyimage1":
        if "Enter" in str(event):
            boton.config(border = 1, background = "gray")
        elif "Leave" in str(event):
            boton.config(border = 0, background = "#ebebeb")
    elif str(boton["image"]) == "pyimage2":
        if "Enter" in str(event):
            boton.config(border = 1, background = "black")
        elif "Leave" in str(event):
            boton.config(border = 0, background = "#242424")
        
        
def main():
    
    app = CTk()
    app.geometry("600x645")
    app.resizable(False, False)
    app.title("Base de Datos")
    
    barra_nav = LabelFrame(width = 300, height = 27, background = "#242424", border = 0)
    barra_nav.pack(side = TOP)
    
    imagen_dia = Image.open(DIR + "\\imagenes_00!1\\dia.png")
    imagen_dia = imagen_dia.resize((25,24))
    imagen_dia = ImageTk.PhotoImage(imagen_dia)
    
    imagen_noche= Image.open(DIR + "\\imagenes_00!1\\nocturn.png")
    imagen_noche = imagen_noche.resize((25,24))
    imagen_noche = ImageTk.PhotoImage(imagen_noche)
    
    icono = Image.open(DIR + "\\imagenes_00!1\\icon.png")
    icono = icono.resize((120, 60))
    icono = ImageTk.PhotoImage(icono)
    app.call("wm", "iconphoto", app._w, icono)
    
    main_label= Text(app, height=400, width=300, background = "black", fg = "white")
    main_label.pack(fill = BOTH, expand = True) 
    main_label.insert(INSERT, fun_1())
    main_label.config(state = DISABLED)
    
    v = ttk.Scrollbar(main_label, orient='vertical', command = main_label.yview)
    v.pack(side=RIGHT, fill='y')
    
    main_label.configure(yscrollcommand=v.set)
    
    texto_1 = CTkLabel(app, text = "exportar tabla")

    entrada = CTkEntry(app, width = 250, font = ("arial", 15), justify = CENTER, text_color = "gray", border_width = 1)
    entrada.insert(0, "Ingrese el directorio:")
    entrada.bind("<FocusIn>", partial(marca_agua, entrada, 1))
    entrada.bind("<FocusOut>", partial(marca_agua, entrada, 1))
    entrada.bind("<Enter>", partial(border_1, entrada))
    entrada.bind("<Leave>", partial(border_2, entrada))
    entrada.pack(pady = 10, ipady = 7)
    
    boton_3 = CTkButton(app, text = "Buscar Directorio", width = 20, height = 6)
    boton_3.place(x = 450, y = 433)
    
    boton_1 = CTkButton(app, text = "Abrir", width = 200, height = 65)
    boton_1.pack(pady = 10)
    
    boton_2 = CTkButton(app, text = "Salir", width = 200, height = 65, command = app.destroy)
    boton_2.pack(pady = 10)
    
    imagen_pdf = Image.open(DIR + "\\imagenes_00!1\\pdf.png")
    imagen_pdf = imagen_pdf.resize((52,52))
    imagen_pdf = ImageTk.PhotoImage(imagen_pdf) 
    
    imagen_pdf_2 = Image.open(DIR + "\\imagenes_00!1\\pdf_2.png")
    imagen_pdf_2 = imagen_pdf_2.resize((50,50))
    imagen_pdf_2 = ImageTk.PhotoImage(imagen_pdf_2) 
    
    imagen_excel = Image.open(DIR + "\\imagenes_00!1\\excel.png")
    imagen_excel = imagen_excel.resize((55,36))
    imagen_excel = ImageTk.PhotoImage(imagen_excel) 
    
    imagen_excel_2 = Image.open(DIR + "\\imagenes_00!1\\excel_2.png")
    imagen_excel_2 = imagen_excel_2.resize((53,34))
    imagen_excel_2 = ImageTk.PhotoImage(imagen_excel_2)
    
    imagen_correo = Image.open(DIR + "\\imagenes_00!1\\boton_correo.png")
    imagen_correo = imagen_correo.resize((53,30))
    imagen_correo = ImageTk.PhotoImage(imagen_correo)
    
    imagen_correo_1 = Image.open(DIR + "\\imagenes_00!1\\boton_local.png")
    imagen_correo_1 = imagen_correo_1.resize((53,30))
    imagen_correo_1 = ImageTk.PhotoImage(imagen_correo_1)
                
    boton_enviar_pdf = Label(app, image = imagen_pdf, background = "#242424", border = 0)
    boton_enviar_pdf.bind("<Enter>", partial(cambio_boton, boton_enviar_pdf, imagen_pdf, imagen_pdf_2))
    boton_enviar_pdf.bind("<Leave>", partial(cambio_boton, boton_enviar_pdf, imagen_pdf, imagen_pdf_2))
    
    boton_enviar_excel = Label(app, image = imagen_excel, background = "#242424", border = 0)
    boton_enviar_excel.bind("<Enter>", partial(cambio_boton, boton_enviar_excel, imagen_excel, imagen_excel_2))
    boton_enviar_excel.bind("<Leave>", partial(cambio_boton, boton_enviar_excel, imagen_excel, imagen_excel_2))
    
    boton_opcion = Label(app, image = imagen_correo, background = "#242424", border = 0)
    boton_opcion.bind("<Button-1>", partial(cambio_boton, boton_opcion, imagen_correo, imagen_correo_1))
    
    cambio_color = Label(image = imagen_noche, border = 0, background = "#242424", width = 25, height = 25)
    cambio_color.place(x = 0, y = 0)
    
    cambio_color.bind("<Enter>", partial(border_enter_button, cambio_color))
    cambio_color.bind("<Leave>", partial(border_enter_button, cambio_color))
    
    texto_2 = CTkLabel(app, text = "modificaciones")
    texto_2.place(x = 55, y = 475)
    
    entrada_1 = CTkEntry(app, width = 160, font = ("arial", 12), justify = CENTER, text_color = "gray", border_width = 1, state = DISABLED) 
    entrada_1.insert(0, "Ingrese nombre:")
    entrada_1.bind("<FocusIn>", partial(marca_agua, entrada_1, 3))
    entrada_1.bind("<FocusOut>", partial(marca_agua, entrada_1, 3))
    entrada_1.bind("<Enter>", partial(border_1, entrada_1))
    entrada_1.bind("<Leave>", partial(border_2, entrada_1))
    entrada_1.place(x = 20, y = 516) 
    
    boton_4 = CTkButton(app, text = "borrar", width = 67, height = 35, state = DISABLED)
    boton_4.place(x = 27, y = 559)
    
    boton_5 = CTkButton(app, text = "modificar", width = 50, height = 35, state = DISABLED)
    boton_5.place(x = 101, y = 559)
    
    boton_6 = CTkButton(app, text = "agregar", width = 63, height = 35, state = DISABLED)
    boton_6.place(x = 64, y = 602)
    
    cambio_color.bind("<Button-1>", partial(cambio_tema, cambio_color, imagen_noche, imagen_dia, barra_nav, boton_enviar_pdf, boton_enviar_excel, boton_opcion, boton_1, boton_2, boton_3, boton_4, boton_5, boton_6))
    comandos(boton_1, boton_3, entrada, main_label, boton_2, app, boton_enviar_pdf, boton_enviar_excel, texto_1, boton_opcion, entrada_1, boton_4, boton_5, boton_6, v)

    app.mainloop()
    
if __name__ == "__main__":
    main()