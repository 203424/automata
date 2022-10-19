from tkinter import filedialog
from tkinter.ttk import Treeview
from logic.functions import leer_linea
from tkinter import Tk,Frame, END, Label, CENTER, Button, Text, messagebox
import os

def show_frame(frame):
    frame.tkraise()

window = Tk()
window.minsize(width=600, height=600)
window.title("Extractor de fuentes con Autómatas!")
window.iconbitmap('./icon.ico')

window.rowconfigure(0,weight=1)
window.columnconfigure(0,weight=1)

w_entrada = Frame(window) #Pantalla de inicio
w_salida = Frame(window) #Pantalla para mostrar el .txt

for frame in (w_entrada, w_salida):
    frame.config(bg="#91afc6")
    frame.grid(row=0, column=0, sticky="nsew")

show_frame(w_entrada)
ruta_str = "Ruta: "

def abrir_archivo():
    lineas_validadas.delete("0.0",END)
    archivo = filedialog.askopenfilename(title="Abrir", initialdir="./", filetypes=(("Archivos .css", "*.css"), ("Archivos .txt", "*.txt")))
    file_dir["text"] = ruta_str+ archivo
    print("archivo: ",archivo)
    if archivo == "":
        messagebox.showwarning(title="Alerta",message="No se ha seleccionado un archivo")
    else:
        lineas_validas = leer_linea(archivo)
        conta = 0
        for i in lineas_validas:
            conta += 1
            lineas_validadas.insert(END,conta)
            lineas_validadas.insert(END," ")
            lineas_validadas.insert(END,i)
            lineas_validadas.insert(END,"\n\n")
        
        guardar_btn['command']=lambda:guardar_archivo(lineas_validas)
        guardar_btn.pack()
        
def limpiar_tabla():
    for dato in tv.get_children(): #limpia la tabla en caso de tener información
        tv.delete(dato)

def quitar_repetidos(lista):
    lista_final = list()
    nombres_genericos = ["inherit","serif","sans-serif","cursive","fantasy","monospace"] #fuentes válidas pero que no son utiles
    for l in lista: 
        fonts = l[l.index(":")+1:len(l)+1].split(",")
        for font in fonts:
            font = font.replace(";","")
            if '"' in font or "'" in font:
                font = font.replace('"',"")
                font = font.replace("'","")
            if font[0] == " ":
                font = font.replace(" ","",1)
            if font not in lista_final and font not in nombres_genericos:
                lista_final.append(font) #guarda las fuentes en una lista aparte
    return lista_final

def escribir_archivo(archivo,texto):
    contenido = texto + "\n"
    archivo.write(contenido)

def guardar_fuentes(archivo_fuentes,lista_final):
    if os.path.exists(archivo_fuentes):
        os.remove(archivo_fuentes)
    archivo = open (archivo_fuentes, 'w')
    for l in lista_final:
        escribir_archivo(archivo,l)
    archivo.close()

def guardar_archivo(lineas_validas):
    guardar_btn.pack_forget()
    lineas_validadas.delete("0.0",END) #limpia el textarea
    file_dir["text"] = ruta_str #limpia la etiqueta que mostraba la ruta del archivo

    archivo_fuentes = './fonts.txt' #ruta del archivo de salida
    
    limpiar_tabla()
    show_frame(w_salida)
    lista_final = quitar_repetidos(lineas_validas)
    guardar_fuentes(archivo_fuentes, lista_final)

    tv.heading(1,text="Fonts")    
    conta = 0
    for i in lista_final:
        i = '"'+i+'"' #agrega comillas dobles a las fuentes por los espacios entre palabras
        conta += 1
        tv.insert("",END,values=i) #muestra las fuentes del txt en una tabla
    num_fuentes['text'] = "Fuentes encontradas: " + str(conta) 

font_text = "Helvetica 12 bold"

label_title = Label(w_entrada,text="Extractor de fuentes",justify=CENTER,font="Helvetica 24 bold",bg="#91afc6",foreground="white").pack()
label_title = Label(w_salida,text="Extractor de fuentes",justify=CENTER,font="Helvetica 24 bold",bg="#91afc6",foreground="white").pack()
#Entrada
file_dir = Label(w_entrada,text="Ruta: ",font="Helvetica 12",bg="#91afc6",foreground="white")
file_dir.pack()

abrir_btn = Button(w_entrada,text="Abrir",command=abrir_archivo,borderwidth=0,width=10,font=font_text)
abrir_btn.pack()

lineas_validadas = Text(w_entrada)
lineas_validadas.pack(padx=30,pady=20)

guardar_btn = Button(w_entrada,text="Guardar",borderwidth=0,width=10,font=font_text)

num_fuentes = Label(w_salida,text="Fuentes encontradas: ",font=font_text)
num_fuentes.pack(pady=10)

tv = Treeview(w_salida, columns=1, show="headings", height="10")
tv.pack(pady=20)

back_btn = Button(w_salida,text="Volver",command=lambda:show_frame(w_entrada),borderwidth=0,width=10,font="Helvetica 12 bold")
back_btn.pack()

window.mainloop()