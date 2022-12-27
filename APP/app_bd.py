from tkinter import *
from tkinter import ttk
from functools import partial
from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
import  os, csv, correo, pdf_app

COUNT = 0
DIR = os.path.realpath(__file__)
DIR = DIR.split("\\")
DIR.pop(len(DIR)-1)
DIR = "\\".join(DIR)

def envia_excel():
    
    messagebox.showinfo(title = "en desarrollo", message = "opcion en desarrollo")

def capturadora(captura : str, dir):
    
    if captura == "Correo invalido, ingrese nuevamente.":
        
        messagebox.showinfo(title = "Error_Enviar_Correo", message = "Correo invalido, ingrese nuevamente.")
        
    elif captura == "Error correo invalido" or captura == "correos o contraseñas equivocados.":
        
        messagebox.e(title = "Error_Enviar_Correo", message = "programa desconfigurado, contacte con el desrollador.")
        
    elif captura == "directorio no encontrado, revise el directorio.":
        
        messagebox.e(title = "Error_Enviar_Correo", message = f"directorio no encontrado, revise el directorio. '{dir}'")
    elif captura == "directorio corrupto.":
        
        messagebox.e(title = "Error_Enviar_Correo", message = f"directorio corrupto. '{dir}'")
    else:
        os.remove(dir)

def enviar_pdf_command(dir, dir_, entrada : 'CTkEntry', html_archivo):
    
    salida = entrada.get()
    
    if salida == "":
        messagebox.showinfo(title = "Error", message = "No se ingrese ningun correo.")
    
    pdf_app.crear_pdf(dir, dir_)
    
    captura = correo.enviar("pdf", dir, salida, html_archivo)
    
    capturadora(captura, dir)

def envia_pdf(tabla, dir_, event):
    
    
    dir = DIR + f"\\{tabla}.pdf"
    html_archivo = DIR + f"\\correo_pdf.html"

    app_2 = CTk()
    app_2.geometry("400x150")
    app_2.resizable(False, False)
    app_2.title("Base de Datos")
    
    entrada_ = CTkEntry(app_2, width = 250, font = ("arial", 15), justify = CENTER, text_color = "gray", border_width = 1)
    entrada_.insert(0, "Ingrese su correo:")
    entrada_.bind("<FocusIn>", partial(marca_agua, entrada_))
    entrada_.bind("<FocusOut>", partial(marca_agua, entrada_))
    entrada_.bind("<Enter>", partial(border_1, entrada_))
    entrada_.bind("<Leave>", partial(border_2, entrada_))
    entrada_.pack(pady = 10, ipady = 7)

        
    boton_1_ = CTkButton(app_2, text = "Enviar", width = 200, height = 65, command = partial(enviar_pdf_command, dir, dir_, entrada_, html_archivo))
    boton_1_.pack(pady = 10)
    
    app_2.mainloop()


def acortador_1(directorio, main_label : 'LabelFrame', entrada : 'ttk.Treeview', boton_3 : 'CTkButton', boton_2 : 'CTkButton', boton_1 : 'CTkButton', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label'):
    
    try:
        if "base_local.py" in os.listdir(directorio):
            
            main_label.config(text = "")
    
            lista = []
            
            for i in os.listdir(directorio):
                
                if os.path.isdir(f"{directorio}/{i}") and i != "imagenes_00!1" and i != "APP":
                    lista.append(i)
            
            entrada.destroy()
            boton_3.destroy()
            
            tabla = ttk.Treeview(main_label)
            tabla.heading("#0", text = "bases de datos")
            
            yscrollbar = ttk.Scrollbar(main_label, orient = "vertical", command = tabla.yview)
            yscrollbar.pack(side = RIGHT, fill = "y")
            
            xscrollbar = ttk.Scrollbar(main_label, orient = "horizontal", command= tabla.xview)
            xscrollbar.pack(side = BOTTOM, fill = "x")
            
            for i in lista:
                    
                globals()[f"fila_{i}"] = tabla.insert("", END, text = i)               
            
            tabla.place(x = 0, y = 0, width = 585, height = 374)
            
            boton_1.configure(command = partial(listar_tablas, tabla, directorio, lista, boton_1, boton_2, yscrollbar, xscrollbar, main_label, app, boton_pdf, boton_excel))
            boton_2.configure(text = "Atras", command = partial(
                                                                atras_1,
                                                                tabla,
                                                                yscrollbar,
                                                                xscrollbar,
                                                                boton_1,
                                                                boton_2,
                                                                main_label,
                                                                app,
                                                                boton_pdf
                                                                ))
                
        else:
            
            messagebox.showinfo(title = "Error", message = "Este no es el directorio de la base de datos.")
    
    except FileNotFoundError:
        
        messagebox.showinfo(title = "Directorio Invalido", message = f"Directorio no existente '{directorio}'")
        
    except OSError:
        
        messagebox.showinfo(title = "campo vacio", message = "Ingrese un directorio.")


def fun_1():
    
    archivos = os.listdir()
    
    text = "ARCHIVOS DIRECTORIO ACTUAL: \n\n"
    
    for i in archivos:
        
        text += f"{i}\n"
        
    return text


def comandos(boton_1 : 'CTkButton', boton_3 : 'CTkButton', entrada : 'CTkEntry', main_label : 'LabelFrame', boton_2 : 'CTkButton', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label'):
    
    boton_1.configure(command = partial(listar_db, entrada, main_label, boton_1, boton_3, boton_2, app, boton_pdf, boton_excel))
    boton_3.configure(command = partial(listar_db_buscador, entrada, main_label, boton_1, boton_3, boton_2, app, boton_pdf, boton_excel))
    
def atras_3(boton_2 : 'CTkButton', tabla : 'ttk.Treeview', lista_, lista, boton_1 : 'CTkButton', directorio, yscrollbar : 'ttk.Scrollbar', xscrollbar : 'ttk.Scrollbar', main_label : 'LabelFrame', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label'):
            
    boton_pdf.place_forget()
    boton_excel.place_forget()
            
    for i in range(len(lista)):
        
        tabla.delete(globals()[f"#{i}"])   
    for i in range(1, len(lista) + 1):  
        tabla.column(f"#{i}", width = 0)
    
    tabla.column("#0", width = 585)
    tabla.heading("#0", text = "tablas") 
            
    for i in lista_:
                        
        globals()[f"fila_{i}"] = tabla.insert("", END, text = i)
        
    boton_2.configure(command = partial(
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
            boton_pdf
            ))


def abrir_tabla(tabla : 'ttk.Treeview', directorio, base, lista_, app : 'Tk', boton_pdf : 'Button', boton_2 : 'CTkButton', boton_1 : 'CTkButton',  yscrollbar : 'ttk.Scrollbar', xscrollbar : 'ttk.Scrollbar', main_label : 'LabelFrame', boton_excel : Label):
    
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
                    tabla.column(f"#{i}", minwidth = 0, width = 50 + len(lista[0][i-1]), stretch = NO)
                else:
                    tabla.column(f"#{i}", minwidth = 0, width = 50, stretch = NO)

            tabla.heading("#0", text = tabla_)  
            
            for i in range(len(lista[0])):
                
                tabla.heading(f"#{i+1}", text = lista[0][i])
            
            for i in lista_:
                        
                tabla.delete(globals()[f"fila_{i}"])
                
            lista.pop(0)
            
            for i in range(len(lista)):
                
                globals()[f"#{i}"] = tabla.insert("", END, text = "", values = lista[i])
                
        boton_2.configure(command = partial(atras_3, boton_2, tabla, lista_, lista, boton_1, directorio, yscrollbar, xscrollbar, main_label , app, boton_pdf, boton_excel))
                
        boton_pdf.place(x = 430, y = 400)
        boton_pdf.bind("<Button-1>", partial(envia_pdf, tabla_, dir))
        
        boton_excel.place(x = 490, y = 408)
        boton_excel.bind("<Button-1>", partial(envia_excel, tabla_, dir))
                
        
    except IndexError:
        try:
            
            messagebox.showinfo(title = "Delimiter Error", message = f"El archivo no esta delimitado por comas, reviselo. '{directorio}/{base}/{tabla_}.csv'")
            
        except UnboundLocalError:
            
            messagebox.showinfo(title = "Archivo Error", message = f"No selecciono ninguna tabla. '{directorio}/{base}/{tabla_}.csv'")

    except FileNotFoundError:
        
        messagebox.showinfo(title = "Archivo no encontrado", message = f"Revise el directorio. '{directorio}/{base}/{tabla_}.csv'")
        
    except IOError:
        
        messagebox.showinfo(title = "Archivo corrupto.", message = f"Archivo corrupto. '{directorio}/{base}/{tabla_}.csv'")


def atras_2(boton_1 : 'CTkButton', boton_2 : 'CTkButton', tabla : 'ttk.Treeview',directorio, lista, yscrollbar : 'ttk.Scrollbar', xscrollbar : 'ttk.Scrollbar', main_label : LabelFrame, app : 'Tk', boton_pdf : 'Button'):
    
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
            
    tabla.place(x = 0, y = 0, width = 585, height = 374)
    
    boton_1.configure(command = partial(listar_tablas, tabla, directorio, lista, boton_1, boton_2, yscrollbar, xscrollbar, main_label, app, boton_pdf))
    boton_2.configure(text = "Atras", command = partial(
                                                                atras_1,
                                                                tabla,
                                                                yscrollbar,
                                                                xscrollbar,
                                                                boton_1,
                                                                boton_2,
                                                                main_label,
                                                                app,
                                                                boton_pdf
                                                                ))

def listar_tablas(tabla : 'ttk.Treeview', directorio, lista_, boton_1 : 'Button', boton_2 : 'CTkButton', yscrollbar : 'ttk.Scrollbar', xscrollbar : 'ttk.Scrollbar', main_label : 'LabelFrame', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label'):
    
    try:
        
        lista = []
        
        id = tabla.selection()[0]
        
        base = tabla.item(id, option = "text")
        
        for i in os.listdir(f"{directorio}/{base}"):
            extension = i.split(".")

            if extension[1] == "csv":
                lista.append(extension[0])
                
        tabla.heading("#0", text = "tablas")
        
        for i in lista_:
                        
            tabla.delete(globals()[f"fila_{i}"])
            
        for i in lista:
                        
            globals()[f"fila_{i}"] = tabla.insert("", END, text = i)
            
        boton_1.configure(command = partial(abrir_tabla,tabla, directorio, base, lista, app, boton_pdf, boton_2, boton_1,  yscrollbar, xscrollbar, main_label, boton_excel))
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
            boton_pdf
            ))

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
            boton_pdf : 'Button'
                    ):
    
    tabla.destroy()
    xscrollbar.destroy()
    yscrollbar.destroy()
    boton_1.destroy()
    boton_2.destroy()
    
    main_label.config(text = fun_1())
    
    entrada = CTkEntry(app, width = 250, font = ("arial", 15), justify = CENTER, text_color = "grey", border_width = 1)
    entrada.insert(0, "Ingrese el directorio:")
    entrada.bind("<FocusIn>", partial(marca_agua, entrada))
    entrada.bind("<FocusOut>", partial(marca_agua, entrada))
    entrada.bind("<Enter>", partial(border_1, entrada))
    entrada.bind("<Leave>", partial(border_2, entrada))
    entrada.pack(pady = 10, ipady = 7)
    
    boton_3 = CTkButton(app, text = "Buscar Directorio", width = 20, height = 6)
    boton_3.place(x = 10, y = 339)
    
    boton_1 = CTkButton(app, text = "Abrir", width = 200, height = 65)
    boton_1.pack(pady = 10)
    
    boton_2 = CTkButton(app, text = "Salir", width = 200, height = 65, command = app.destroy)
    boton_2.pack(pady = 10)
    
    comandos(boton_1, boton_3, entrada, main_label, boton_2, app, boton_pdf)
            
def listar_db(entrada : 'Entry', main_label : 'LabelFrame', boton_1 : 'Button', boton_3 : 'CTkButton', boton_2 : 'CTkButton', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label'):
    
    directorio = entrada.get()
    
    acortador_1(directorio, main_label, entrada, boton_3, boton_2, boton_1, app, boton_pdf, boton_excel)
        
    
def listar_db_buscador(entrada : 'CTkEntry', main_label : 'LabelFrame', boton_1 : 'CTkButton', boton_3 : 'CTkButton', boton_2 : 'CTkButton', app : 'Tk', boton_pdf : 'Button', boton_excel : 'Label'):
    
    info = filedialog.askdirectory()
    directorio = info.capitalize()
    
    if directorio == "":
        return "vacio"
    
    acortador_1(directorio, main_label, entrada, boton_3, boton_2, boton_1, app, boton_pdf, boton_excel)
        
        
def marca_agua(entrada : 'CTkEntry', event):
    
    global COUNT
    
    COUNT += 1
    
    texto = entrada.get()
    
    if texto == "Ingrese el directorio:" or texto == "Ingrese su correo:":
        
        entrada.delete(0, END)
        entrada.configure(text_color = "black")
        
    elif texto == "":
        
        entrada.configure(text_color = "gray")
        entrada.insert(0, "Ingrese el directorio:")
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
    
    entrada.configure(border_color = "#5499c7", border_width = 2)
    
    string = str(entrada.focus_get())
    
    if len(string) > len(".!ctkentry.!entry") and string != "":
        
        
        
        for i in range(len(string) - len(".!ctkentry.!entry")):
            
            string = list(string)
            string.pop(len(string) - i - 8)

    string = "".join(string)       

    if string != ".!ctkentry.!entry":
        
        entrada.configure(text_color = "#5499c7")


def border_2(entrada : 'CTkEntry', event):
    
    entrada.configure(border_color = "gray", border_width = 1)
    
    string = str(entrada.focus_get())
    
    if len(string) > len(".!ctkentry.!entry") and string != "":
        
        
        
        for i in range(len(string) - len(".!ctkentry.!entry")):
            
            string = list(string)
            string.pop(len(string) - i - 8)

    string = "".join(string)
    
    if string != ".!ctkentry.!entry":
        
        entrada.configure(text_color = "gray")
        
    elif string == ".!ctkentry.!entry":
        
        entrada.configure(text_color = "black")
    
    
def cambio_boton(boton : 'Button', imagen_1, imagen_2, event):
    
    
    if "Leave" in str(event):
        boton.config(image = imagen_1)   
    elif "Enter" in str(event):
        boton.config(image = imagen_2)
    
def main():
    
    app = CTk()
    app.geometry("600x560")
    app.resizable(False, False)
    app.title("Base de Datos")
    
    icono = Image.open(DIR + "\\imagenes_00!1\\icon.png")
    icono = icono.resize((120, 60))
    icono = ImageTk.PhotoImage(icono)
    app.call("wm", "iconphoto", app._w, icono)
    
    main_label = LabelFrame(app, background = "black", width = 500, height = 300, text = fun_1(), foreground = "white", border = 0, labelanchor = "n", font = ("verdana", 12))
    main_label.pack(expand = True, fill= BOTH)

    entrada = CTkEntry(app, width = 250, font = ("arial", 15), justify = CENTER, text_color = "gray", border_width = 1)
    entrada.insert(0, "Ingrese el directorio:")
    entrada.bind("<FocusIn>", partial(marca_agua, entrada))
    entrada.bind("<FocusOut>", partial(marca_agua, entrada))
    entrada.bind("<Enter>", partial(border_1, entrada))
    entrada.bind("<Leave>", partial(border_2, entrada))
    entrada.pack(pady = 10, ipady = 7)
    
    boton_3 = CTkButton(app, text = "Buscar Directorio", width = 20, height = 6)
    boton_3.place(x = 35, y = 350)
    
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
                
    boton_enviar_pdf = Label(app, image = imagen_pdf, background = "#242424", border = 0)
    boton_enviar_pdf.bind("<Enter>", partial(cambio_boton, boton_enviar_pdf, imagen_pdf, imagen_pdf_2))
    boton_enviar_pdf.bind("<Leave>", partial(cambio_boton, boton_enviar_pdf, imagen_pdf, imagen_pdf_2))
    
    boton_enviar_excel = Label(app, image = imagen_excel, background = "#242424", border = 0)
    boton_enviar_excel.bind("<Enter>", partial(cambio_boton, boton_enviar_excel, imagen_excel, imagen_excel_2))
    boton_enviar_excel.bind("<Leave>", partial(cambio_boton, boton_enviar_excel, imagen_excel, imagen_excel_2))
    
    comandos(boton_1, boton_3, entrada, main_label, boton_2, app, boton_enviar_pdf, boton_enviar_excel)

    app.mainloop()
    
if __name__ == "__main__":
    main()