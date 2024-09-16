# Creado por Isaac Villalobos Bonilla y Kevin Vega Gutierrez
import Leearchivos
import Entrada
import datetime
import os
from time import strftime
import tkinter as tk
from tkinter import filedialog
import pygame
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from Entrada import validarint,validarfloat,validarstring
from Leearchivos import propietarios,canciones,playlist,album,artistas,administradores,genero
dicpropietarios = propietarios()
diccanciones = canciones()
dicplaylist = playlist()
dicalbum = album()
dicartista = artistas()
dicgenero = genero()
dicadmin = administradores()
facturas={}
facturasgeneradaadmin={}
sizedicfacturasadmin=0
facturaspagadas={}
cuentaenbeta=False
descuentoactividad=75
descuentocreacion=0
descuentoinsercion=25
global cola
cola=[]
global historial
historial=[]
reproductor = None
pausado = False
canciones = []
cancion_actual = ""
pygame.mixer.init()
busqueda_album2=[]
busqueda_artistas2=[]
def costoactividad():
    costoactividad = 39.99 - (39.99 * (descuentoactividad / 100))
    costoactividad = round(costoactividad, 2)
    
    if costoactividad.is_integer():
        return int(costoactividad)
    else:
        return costoactividad
def costocreacion():
    costocreacion = 39.99 - (39.99 * (descuentocreacion / 100))
    costocreacion = round(costocreacion, 2)
    
    if costocreacion.is_integer():
        return int(costocreacion)
    else:
        return costocreacion
def costoinsercion():
    costoinsercion = 39.99 - (39.99 * (descuentoinsercion / 100))
    costoinsercion = round(costoinsercion, 2)
    
    if costoinsercion.is_integer():
        return int(costoinsercion)
    else:
        return costoinsercion
########################################################AUXILIAR#####################################################
def cerrar(ventana):
    if ventana and isinstance(ventana, tk.Tk):
        ventana.destroy()
def tiempo(clock_text):
    string = strftime('%H:%M:%S') 
    clock_text.config(text=string)
    clock_text.after(1000, lambda: tiempo(clock_text))
color = None
color2= None
lacoladereprod={}
def verificacionusuario(usuario):
    codpropietario = str(usuario)
    encontrado = False
    if codpropietario in facturas:
        messagebox.showerror("Error", "No has pagado la factura.")
        return 6
    else:
        for clave in dicpropietarios:
            if codpropietario == clave:
                encontrado = True
                estado_cuenta = dicpropietarios[codpropietario]['activo']
                if estado_cuenta == "1":
                    return 1  # Usuario encontrado y activo
                elif estado_cuenta == "0":
                    return 2  # Usuario encontrado pero inactivo
        if not encontrado:
            return 3  # Usuario no existe
def verificacionadministrador(usuario):
    codadmin = str(usuario)
    encontrado = False
    if codadmin in dicadmin:
            encontrado = True
            return 4  # Usuario encontrado y activo
    if not encontrado:
        return 5  # Usuario no existe
def verificacionmembresia(usuario):
    codmembresia = str(usuario)
    encontrado = False
    for clave, valores in dicpropietarios.items():
        if dicpropietarios[clave]['codmembresia']==codmembresia:
            encontrado = True
            return 2
    if not encontrado:
        return 1
########################################################ACTIVACION##################################################
def elegircolor():
    colores3 = tk.Tk()
    colores3.configure(bg='white')
    colores3.title("Elegir modo de color")
    colores3.geometry("800x500")
    colores3.resizable(False, False)
    fuente = ("Console", 20)
    fuente2 = ("Console", 14)
    usuario_admin = tk.StringVar()
    usuario_admin.set("Color")
    input_usuario = tk.Label(colores3, text="Elige el modo del reproductor:", bg='white', fg='black', font=fuente)
    input_usuario.place(x=100, y=100)
    radio_usuario = tk.Radiobutton(colores3, text="Claro", variable=usuario_admin, value="Claro", bg='white', fg='black', activebackground='white', selectcolor='gray', font=fuente)
    radio_usuario.place(x=100, y=150)

    radio_admin = tk.Radiobutton(colores3, text="Oscuro", variable=usuario_admin, value="Oscuro", bg='white', fg="black", activebackground='white', selectcolor='gray', font=fuente)
    radio_admin.place(x=100, y=185)

    boton_login = tk.Button(colores3, text="Aceptar", command=lambda: colores(colores3,usuario_admin.get()), bg='white', fg='black', font=fuente2,relief=tk.RAISED,borderwidth=4) 
    boton_login.place(x=100, y=240)    
    colores3.mainloop()

def colores(ventana, modo_color):
    global color
    global color20
    ventana.destroy()
    if modo_color == "Claro":
        color = "white"
        color20 = "white"
        elegirletras()
    elif modo_color == "Oscuro":
        color = "black"
        color20 = "black"
        elegirletrasn()
    else:
        messagebox.showerror("Error", "No has un modo de color valido. Intenta de nuevo.")

def elegirletras():
    colores4 = tk.Tk()
    colores4.configure(bg=color)
    colores4.title("Elegir color de letras")
    colores4.geometry("800x500")
    colores4.resizable(False, False)
    fuente = ("Console", 20)
    fuente2 = ("Console", 14)
    usuario_admin = tk.StringVar()
    usuario_admin.set("Color")
    input_usuario = tk.Label(colores4, text="Elige color de letras del reproductor:", bg=color, fg='black', font=fuente)
    input_usuario.place(x=100, y=100)
    radio_usuario = tk.Radiobutton(colores4, text="Contrario", variable=usuario_admin, value="Contrario", bg=color, fg='black', activebackground='white', selectcolor='gray', font=fuente)
    radio_usuario.place(x=100, y=150)

    radio_admin = tk.Radiobutton(colores4, text="Azul", variable=usuario_admin, value="Azul", bg=color, fg="black", activebackground='white', selectcolor='gray', font=fuente)
    radio_admin.place(x=100, y=185)

    radio_admin2 = tk.Radiobutton(colores4, text="Rojo", variable=usuario_admin, value="Rojo", bg=color, fg="black", activebackground='white', selectcolor='gray', font=fuente)
    radio_admin2.place(x=100, y=220)

    radio_admin3 = tk.Radiobutton(colores4, text="Morado", variable=usuario_admin, value="Morado", bg=color, fg="black", activebackground='white', selectcolor='gray', font=fuente)
    radio_admin3.place(x=100, y=255)
    
    boton_login = tk.Button(colores4, text="Aceptar", command=lambda: colores2(colores4,usuario_admin.get()), bg=color, fg='black', font=fuente2,relief=tk.RAISED,borderwidth=4) 
    boton_login.place(x=100, y=305)    
    colores4.mainloop()

def elegirletrasn():
    colores4 = tk.Tk()
    colores4.configure(bg=color)
    colores4.title("Elegir color de letras")
    colores4.geometry("800x500")
    colores4.resizable(False, False)
    fuente = ("Console", 20)
    fuente2 = ("Console", 14)
    usuario_admin = tk.StringVar()
    usuario_admin.set("Color")
    input_usuario = tk.Label(colores4, text="Elige color de letras del reproductor:", bg=color, fg='white', font=fuente)
    input_usuario.place(x=100, y=100)
    radio_usuario = tk.Radiobutton(colores4, text="Contrario", variable=usuario_admin, value="Contrario", bg=color, fg='white', activebackground='white', selectcolor='gray', font=fuente)
    radio_usuario.place(x=100, y=150)

    radio_admin = tk.Radiobutton(colores4, text="Azul Claro", variable=usuario_admin, value="Azul Claro", bg=color, fg="white", activebackground='white', selectcolor='gray', font=fuente)
    radio_admin.place(x=100, y=185)

    radio_admin2 = tk.Radiobutton(colores4, text="Verde Neon", variable=usuario_admin, value="Verde Neon", bg=color, fg="white", activebackground='white', selectcolor='gray', font=fuente)
    radio_admin2.place(x=100, y=220)

    radio_admin3 = tk.Radiobutton(colores4, text="Morado Neon", variable=usuario_admin, value="Morado Neon", bg=color, fg="white", activebackground='white', selectcolor='gray', font=fuente)
    radio_admin3.place(x=100, y=255)
    
    boton_login = tk.Button(colores4, text="Aceptar", command=lambda: colores2(colores4,usuario_admin.get()), bg=color, fg='white', font=fuente2,relief=tk.RAISED,borderwidth=4) 
    boton_login.place(x=100, y=305)    
    colores4.mainloop()



def colores2(ventana, modo_color):
    global color2
    global imageninsercionpropietario
    global imageninsercionplaylist
    global imageninsercionartista
    global imageninserciongenero
    global imageninsercionalbum
    global imageninsercioncancion
    global imageninsercionadmin
    global imagenbusquedapropietario
    global imagenbusquedaplaylist
    global imagenbusquedaartista
    global imagenbusquedagenero
    global imagenbusquedaalbum
    global imagenbusquedacancion
    global imagenbusquedaadmin
    global imageneliminarpropietario
    global imageneliminarplaylist
    global imageneliminarartista
    global imageneliminargenero
    global imageneliminaralbum
    global imageneliminarcancion
    global imageneliminaradmin
    global imagenmodificarpropietario
    global imagenmodificarplaylist
    global imagenmodificarartista
    global imagenmodificargenero
    global imagenmodificaralbum
    global imagenmodificarcancion
    global imagenmodificaradmin    
    global menuprincipalusuarios
    global menuprincipalalbumes
    global menuprincipalpagos
    global menuprincipalmusica
    global menuprincipalpropietario
    global menuprincipalplaylist
    global menuprincipalgenero
    global menuprincipalcancion
    global menuprincipalalbum
    global menuprincipalartista
    global menuprincipaladmin
    global menuprincipaldescuentos
    global menuprincipalfacturas
    global menuprincipalgenerar
    global menuprincipalpagar
    global  play_btn_file
    global  pause_btn_file
    global  next_btn_file
    global  prev_btn_file
    global  cargar_file
    global  menuprincipalreproduccion
    ventana.destroy()
    if color=="black" and modo_color=="Contrario": #########BLANCO#########
        color2="white"
        imageninsercionpropietario = "carpeta_imagenes/blanco/Insertarproblanco.png"
        imageninsercionplaylist = "carpeta_imagenes/blanco/Insertarplayblanco.png"
        imageninsercionartista = "carpeta_imagenes/blanco/Insertarartistablanco.png"
        imageninserciongenero = "carpeta_imagenes/blanco/Insertargeneroblanco.png"
        imageninsercionalbum = "carpeta_imagenes/blanco/Insertaralbumblanco.png"
        imageninsercioncancion = "carpeta_imagenes/blanco/Insertarcancionblanco.png"
        imageninsercionadmin = "carpeta_imagenes/blanco/Insertaradminblanco.png"
        imagenbusquedapropietario = "carpeta_imagenes/blanco/buscarproblanco.png"
        imagenbusquedaplaylist = "carpeta_imagenes/blanco/buscarplaylistblanco.png"
        imagenbusquedaartista = "carpeta_imagenes/blanco/buscarartistablanco.png"
        imagenbusquedagenero = "carpeta_imagenes/blanco/buscargeneroblanco.png"
        imagenbusquedaalbum = "carpeta_imagenes/blanco/buscaralbumblanco.png"
        imagenbusquedacancion = "carpeta_imagenes/blanco/buscarcancionblanco.png"
        imagenbusquedaadmin = "carpeta_imagenes/blanco/buscaradminblanco.png"
        imageneliminarpropietario = "carpeta_imagenes/blanco/eliminarproblanco.png"
        imageneliminarplaylist = "carpeta_imagenes/blanco/eliminarplaylistblanco.png"
        imageneliminarartista = "carpeta_imagenes/blanco/eliminarartistablanco.png"
        imageneliminargenero = "carpeta_imagenes/blanco/eliminargeneroblanco.png"
        imageneliminaralbum = "carpeta_imagenes/blanco/eliminaralbumblanco.png"
        imageneliminarcancion = "carpeta_imagenes/blanco/eliminarcancionblanco.png"
        imageneliminaradmin = "carpeta_imagenes/blanco/eliminaradminblanco.png"
        imagenmodificarpropietario = "carpeta_imagenes/blanco/modificarproblanco.png"
        imagenmodificarplaylist = "carpeta_imagenes/blanco/modificarplaylistblanco.png"
        imagenmodificarartista = "carpeta_imagenes/blanco/modificarartistablanco.png"
        imagenmodificargenero = "carpeta_imagenes/blanco/modificargeneroblanco.png"
        imagenmodificaralbum = "carpeta_imagenes/blanco/modificaralbumblanco.png"
        imagenmodificarcancion = "carpeta_imagenes/blanco/modificarcancionblanco.png"
        imagenmodificaradmin = "carpeta_imagenes/blanco/modificaradminblanco.png"
        menuprincipalalbumes="carpeta_imagenes/blanco/albumesblanco.png"
        menuprincipalusuarios="carpeta_imagenes/blanco/usuariosblanco.png"
        menuprincipalpagos="carpeta_imagenes/blanco/pagosb.png"
        menuprincipalmusica="carpeta_imagenes/blanco/musicablanco.png"
        menuprincipalpropietario="carpeta_imagenes/blanco/menupropietario.png"
        menuprincipalplaylist="carpeta_imagenes/blanco/menuplaylist.png"
        menuprincipalgenero="carpeta_imagenes/blanco/menugenero.png"
        menuprincipalcancion="carpeta_imagenes/blanco/menucancion.png"
        menuprincipalartista="carpeta_imagenes/blanco/menuartista.png"
        menuprincipalalbum="carpeta_imagenes/blanco/menualbum.png"
        menuprincipaladmin="carpeta_imagenes/blanco/menuadmin.png"
        menuprincipaldescuentos="carpeta_imagenes/blanco/descuentos.png"
        menuprincipalfacturas="carpeta_imagenes/blanco/facturas.png"
        menuprincipalgenerar="carpeta_imagenes/blanco/generar.png"
        menuprincipalpagar="carpeta_imagenes/blanco/pagar.png"
        play_btn_file = "carpeta_imagenes/blanco/play.png"
        pause_btn_file ="carpeta_imagenes/blanco/pause.png"
        next_btn_file = "carpeta_imagenes/blanco/siguiente.png"
        prev_btn_file = "carpeta_imagenes/blanco/anterior.png"
        cargar_file = "carpeta_imagenes/blanco/CargarCancion.png"
        menuprincipalreproduccion = "carpeta_imagenes/blanco/Reproductor.png"
        inicio()
    elif color=="white" and modo_color=="Contrario": #########NEGRO#########
        color2="black"
        imageninsercionpropietario = "carpeta_imagenes/negro/Insertarpronegro.png"
        imageninsercionplaylist = "carpeta_imagenes/negro/Insertarplaynegro.png"
        imageninsercionartista = "carpeta_imagenes/negro/Insertarartistanegro.png"
        imageninserciongenero = "carpeta_imagenes/negro/Insertargeneronegro.png"
        imageninsercionalbum = "carpeta_imagenes/negro/Insertaralbumnegro.png"
        imageninsercioncancion = "carpeta_imagenes/negro/Insertarcancionnegro.png"
        imageninsercionadmin = "carpeta_imagenes/negro/Insertaradminnegro.png"
        imagenbusquedapropietario = "carpeta_imagenes/negro/buscarpronegro.png"
        imagenbusquedaplaylist = "carpeta_imagenes/negro/buscarplaylistnegro.png"
        imagenbusquedaartista = "carpeta_imagenes/negro/buscarartistanegro.png"
        imagenbusquedagenero = "carpeta_imagenes/negro/buscargeneronegro.png"
        imagenbusquedaalbum = "carpeta_imagenes/negro/buscaralbumnegro.png"
        imagenbusquedacancion = "carpeta_imagenes/negro/buscarcancionnegro.png"
        imagenbusquedaadmin = "carpeta_imagenes/negro/buscaradminnegro.png"
        imageneliminarpropietario = "carpeta_imagenes/negro/eliminarpronegro.png"
        imageneliminarplaylist = "carpeta_imagenes/negro/eliminarplaylistnegro.png"
        imageneliminarartista = "carpeta_imagenes/negro/eliminarartistanegro.png"
        imageneliminargenero = "carpeta_imagenes/negro/eliminargeneronegro.png"
        imageneliminaralbum = "carpeta_imagenes/negro/eliminaralbumnegro.png"
        imageneliminarcancion = "carpeta_imagenes/negro/eliminarcancionnegro.png"
        imageneliminaradmin = "carpeta_imagenes/negro/eliminaradminnegro.png"
        imagenmodificarpropietario = "carpeta_imagenes/negro/modificarpronegro.png"
        imagenmodificarplaylist = "carpeta_imagenes/negro/modificarplaylistnegro.png"
        imagenmodificarartista = "carpeta_imagenes/negro/modificarartistanegro.png"
        imagenmodificargenero = "carpeta_imagenes/negro/modificargeneronegro.png"
        imagenmodificaralbum = "carpeta_imagenes/negro/modificaralbumnegro.png"
        imagenmodificarcancion = "carpeta_imagenes/negro/modificarcancionnegro.png"
        imagenmodificaradmin = "carpeta_imagenes/negro/modificaradminnegro.png"
        menuprincipalalbumes="carpeta_imagenes/negro/albumesnegro.png"
        menuprincipalusuarios="carpeta_imagenes/negro/usuariosnegro.png"
        menuprincipalpagos="carpeta_imagenes/negro/pagosn.png"
        menuprincipalmusica="carpeta_imagenes/negro/musicanegro.png"
        menuprincipalpropietario="carpeta_imagenes/negro/menupropietario.png"
        menuprincipalplaylist="carpeta_imagenes/negro/menuplaylist.png"
        menuprincipalgenero="carpeta_imagenes/negro/menugenero.png"
        menuprincipalcancion="carpeta_imagenes/negro/menucancion.png"
        menuprincipalartista="carpeta_imagenes/negro/menuartista.png"
        menuprincipalalbum="carpeta_imagenes/negro/menualbum.png"
        menuprincipaladmin="carpeta_imagenes/negro/menuadmin.png"
        menuprincipaldescuentos="carpeta_imagenes/negro/descuentos.png"
        menuprincipalfacturas="carpeta_imagenes/negro/facturas.png"
        menuprincipalgenerar="carpeta_imagenes/negro/generar.png"
        menuprincipalpagar="carpeta_imagenes/negro/pagar.png"
        play_btn_file = "carpeta_imagenes/Negro/play.png"
        pause_btn_file ="carpeta_imagenes/Negro/pause.png"
        next_btn_file = "carpeta_imagenes/Negro/siguiente.png"
        prev_btn_file = "carpeta_imagenes/Negro/anterior.png"
        cargar_file = "carpeta_imagenes/Negro/CargarCancion.png"
        menuprincipalreproduccion = "carpeta_imagenes/Negro/Reproductor.png"
        inicio()
    elif modo_color=="Azul": #########AZUL#########
        color2= "#13599c"
        imageninsercionpropietario = "carpeta_imagenes/azul/Insertarproazul.png"
        imageninsercionplaylist = "carpeta_imagenes/azul/Insertarplayazul.png"
        imageninsercionartista = "carpeta_imagenes/azul/Insertarartistaazul.png"
        imageninserciongenero = "carpeta_imagenes/azul/Insertargeneroazul.png"
        imageninsercionalbum = "carpeta_imagenes/azul/Insertaralbumazul.png"
        imageninsercioncancion = "carpeta_imagenes/azul/Insertarcancionazul.png"
        imageninsercionadmin = "carpeta_imagenes/azul/Insertaradminazul.png"
        imagenbusquedapropietario = "carpeta_imagenes/azul/buscarproazul.png"
        imagenbusquedaplaylist = "carpeta_imagenes/azul/buscarplaylistazul.png"
        imagenbusquedaartista = "carpeta_imagenes/azul/buscarartistaazul.png"
        imagenbusquedagenero = "carpeta_imagenes/azul/buscargeneroazul.png"
        imagenbusquedaalbum = "carpeta_imagenes/azul/buscaralbumazul.png"
        imagenbusquedacancion = "carpeta_imagenes/azul/buscarcancionazul.png"
        imagenbusquedaadmin = "carpeta_imagenes/azul/buscaradminazul.png"
        imageneliminarpropietario = "carpeta_imagenes/azul/eliminarproazul.png"
        imageneliminarplaylist = "carpeta_imagenes/azul/eliminarplaylistazul.png"
        imageneliminarartista = "carpeta_imagenes/azul/eliminarartistaazul.png"
        imageneliminargenero = "carpeta_imagenes/azul/eliminargeneroazul.png"
        imageneliminaralbum = "carpeta_imagenes/azul/eliminaralbumazul.png"
        imageneliminarcancion = "carpeta_imagenes/azul/eliminarcancionazul.png"
        imageneliminaradmin = "carpeta_imagenes/azul/eliminaradminazul.png"
        imagenmodificarpropietario = "carpeta_imagenes/azul/modificarproazul.png"
        imagenmodificarplaylist = "carpeta_imagenes/azul/modificarplaylistazul.png"
        imagenmodificarartista = "carpeta_imagenes/azul/modificarartistaazul.png"
        imagenmodificargenero = "carpeta_imagenes/azul/modificargeneroazul.png"
        imagenmodificaralbum = "carpeta_imagenes/azul/modificaralbumazul.png"
        imagenmodificarcancion = "carpeta_imagenes/azul/modificarcancionazul.png"
        imagenmodificaradmin = "carpeta_imagenes/azul/modificaradminazul.png"
        menuprincipalalbumes="carpeta_imagenes/azul/albumesazul.png"
        menuprincipalusuarios="carpeta_imagenes/azul/usuariosazul.png"
        menuprincipalpagos="carpeta_imagenes/azul/pagosn.png"
        menuprincipalmusica="carpeta_imagenes/azul/musicaazul.png"
        menuprincipalpropietario="carpeta_imagenes/azul/menupropietarios.png"
        menuprincipalplaylist="carpeta_imagenes/azul/menuplaylist.png"
        menuprincipalgenero="carpeta_imagenes/azul/menugenero.png"
        menuprincipalcancion="carpeta_imagenes/azul/menucancion.png"
        menuprincipalartista="carpeta_imagenes/azul/menuartista.png"
        menuprincipalalbum="carpeta_imagenes/azul/menualbum.png"
        menuprincipaladmin="carpeta_imagenes/azul/menuadmin.png"
        menuprincipaldescuentos="carpeta_imagenes/azul/descuentos.png"
        menuprincipalfacturas="carpeta_imagenes/azul/facturas.png"
        menuprincipalgenerar="carpeta_imagenes/azul/generar.png"
        menuprincipalpagar="carpeta_imagenes/azul/pagar.png"
        play_btn_file = "carpeta_imagenes/azul/play.png"
        pause_btn_file ="carpeta_imagenes/azul/pause.png"
        next_btn_file = "carpeta_imagenes/azul/siguiente.png"
        prev_btn_file = "carpeta_imagenes/azul/anterior.png"
        cargar_file = "carpeta_imagenes/azul/CargarCancion.png"
        menuprincipalreproduccion = "carpeta_imagenes/azul/Reproductor.png"        
        inicio()
    elif modo_color=="Rojo": #########ROJO#########
        color2= "#5e0a1b"
        imageninsercionpropietario = "carpeta_imagenes/rojo/Insertarprorojo.png"
        imageninsercionplaylist = "carpeta_imagenes/rojo/Insertarplayrojo.png"
        imageninsercionartista = "carpeta_imagenes/rojo/Insertarartistarojo.png"
        imageninserciongenero = "carpeta_imagenes/rojo/Insertargenerorojo.png"
        imageninsercionalbum = "carpeta_imagenes/rojo/Insertaralbumrojo.png"
        imageninsercioncancion = "carpeta_imagenes/rojo/Insertarcancionrojo.png"
        imageninsercionadmin = "carpeta_imagenes/rojo/Insertaradminrojo.png"
        imagenbusquedapropietario = "carpeta_imagenes/rojo/buscarprorojo.png"
        imagenbusquedaplaylist = "carpeta_imagenes/rojo/buscarplaylistrojo.png"
        imagenbusquedaartista = "carpeta_imagenes/rojo/buscarartistarojo.png"
        imagenbusquedagenero = "carpeta_imagenes/rojo/buscargenerorojo.png"
        imagenbusquedaalbum = "carpeta_imagenes/rojo/buscaralbumrojo.png"
        imagenbusquedacancion = "carpeta_imagenes/rojo/buscarcancionrojo.png"
        imagenbusquedaadmin = "carpeta_imagenes/rojo/buscaradminrojo.png"
        imageneliminarpropietario = "carpeta_imagenes/rojo/eliminarprorojo.png"
        imageneliminarplaylist = "carpeta_imagenes/rojo/eliminarplaylistrojo.png"
        imageneliminarartista = "carpeta_imagenes/rojo/eliminarartistarojo.png"
        imageneliminargenero = "carpeta_imagenes/rojo/eliminargenerorojo.png"
        imageneliminaralbum = "carpeta_imagenes/rojo/eliminaralbumrojo.png"
        imageneliminarcancion = "carpeta_imagenes/rojo/eliminarcancionrojo.png"
        imageneliminaradmin = "carpeta_imagenes/rojo/eliminaradminrojo.png"
        imagenmodificarpropietario = "carpeta_imagenes/rojo/modificarprorojo.png"
        imagenmodificarplaylist = "carpeta_imagenes/rojo/modificarplaylistrojo.png"
        imagenmodificarartista = "carpeta_imagenes/rojo/modificarartistarojo.png"
        imagenmodificargenero = "carpeta_imagenes/rojo/modificargenerorojo.png"
        imagenmodificaralbum = "carpeta_imagenes/rojo/modificaralbumrojo.png"
        imagenmodificarcancion = "carpeta_imagenes/rojo/modificarcancionrojo.png"
        imagenmodificaradmin = "carpeta_imagenes/rojo/modificaradminrojo.png"
        menuprincipalalbumes="carpeta_imagenes/rojo/albumesrojo.png"
        menuprincipalusuarios="carpeta_imagenes/rojo/usuariosrojo.png"
        menuprincipalpagos="carpeta_imagenes/rojo/pagosn.png"
        menuprincipalmusica="carpeta_imagenes/rojo/musicarojo.png"
        menuprincipalpropietario="carpeta_imagenes/rojo/menupropietario.png"
        menuprincipalplaylist="carpeta_imagenes/rojo/menuplaylist.png"
        menuprincipalgenero="carpeta_imagenes/rojo/menugenero.png"
        menuprincipalcancion="carpeta_imagenes/rojo/menucancion.png"
        menuprincipalartista="carpeta_imagenes/rojo/menuartista.png"
        menuprincipalalbum="carpeta_imagenes/rojo/menualbum.png"
        menuprincipaladmin="carpeta_imagenes/rojo/menuadmin.png"
        menuprincipaldescuentos="carpeta_imagenes/rojo/descuentos.png"
        menuprincipalfacturas="carpeta_imagenes/rojo/facturas.png"
        menuprincipalgenerar="carpeta_imagenes/rojo/generar.png"
        menuprincipalpagar="carpeta_imagenes/rojo/pagar.png"
        play_btn_file = "carpeta_imagenes/rojo/play.png"
        pause_btn_file ="carpeta_imagenes/rojo/pause.png"
        next_btn_file = "carpeta_imagenes/rojo/siguiente.png"
        prev_btn_file = "carpeta_imagenes/rojo/anterior.png"
        cargar_file = "carpeta_imagenes/rojo/CargarCancion.png"
        menuprincipalreproduccion = "carpeta_imagenes/rojo/Reproductor.png"        
        inicio()
    elif modo_color=="Morado": #########MORADO#########
        color2= "#422eb3"
        imageninsercionpropietario = "carpeta_imagenes/morado/Insertarpromorado.png"
        imageninsercionplaylist = "carpeta_imagenes/morado/Insertarplaymorado.png"
        imageninsercionartista = "carpeta_imagenes/morado/Insertarartistamorado.png"
        imageninserciongenero = "carpeta_imagenes/morado/Insertargeneromorado.png"
        imageninsercionalbum = "carpeta_imagenes/morado/Insertaralbummorado.png"
        imageninsercioncancion = "carpeta_imagenes/morado/Insertarcancionmorado.png"
        imageninsercionadmin = "carpeta_imagenes/morado/Insertaradminmorado.png"
        imagenbusquedapropietario = "carpeta_imagenes/morado/buscarpromorado.png"
        imagenbusquedaplaylist = "carpeta_imagenes/morado/buscarplaylistmorado.png"
        imagenbusquedaartista = "carpeta_imagenes/morado/buscarartistamorado.png"
        imagenbusquedagenero = "carpeta_imagenes/morado/buscargeneromorado.png"
        imagenbusquedaalbum = "carpeta_imagenes/morado/buscaralbummorado.png"
        imagenbusquedacancion = "carpeta_imagenes/morado/buscarcancionmorado.png"
        imagenbusquedaadmin = "carpeta_imagenes/morado/buscaradminmorado.png"
        imageneliminarpropietario = "carpeta_imagenes/morado/eliminarpromorado.png"
        imageneliminarplaylist = "carpeta_imagenes/morado/eliminarplaylistmorado.png"
        imageneliminarartista = "carpeta_imagenes/morado/eliminarartistamorado.png"
        imageneliminargenero = "carpeta_imagenes/morado/eliminargeneromorado.png"
        imageneliminaralbum = "carpeta_imagenes/morado/eliminaralbummorado.png"
        imageneliminarcancion = "carpeta_imagenes/morado/eliminarcancionmorado.png"
        imageneliminaradmin = "carpeta_imagenes/morado/eliminaradminmorado.png"
        imagenmodificarpropietario = "carpeta_imagenes/morado/modificarpromorado.png"
        imagenmodificarplaylist = "carpeta_imagenes/morado/modificarplaylistmorado.png"
        imagenmodificarartista = "carpeta_imagenes/morado/modificarartistamorado.png"
        imagenmodificargenero = "carpeta_imagenes/morado/modificargeneromorado.png"
        imagenmodificaralbum = "carpeta_imagenes/morado/modificaralbummorado.png"
        imagenmodificarcancion = "carpeta_imagenes/morado/modificarcancionmorado.png"
        imagenmodificaradmin = "carpeta_imagenes/morado/modificaradminmorado.png"
        menuprincipalalbumes="carpeta_imagenes/morado/albumesmorado.png"
        menuprincipalusuarios="carpeta_imagenes/morado/usuariosmorado.png"
        menuprincipalpagos="carpeta_imagenes/morado/pagosn.png"
        menuprincipalmusica="carpeta_imagenes/morado/musicamorado.png"
        menuprincipalpropietario="carpeta_imagenes/morado/menupropietario.png"
        menuprincipalplaylist="carpeta_imagenes/morado/menuplaylist.png"
        menuprincipalgenero="carpeta_imagenes/morado/menugenero.png"
        menuprincipalcancion="carpeta_imagenes/morado/menucancion.png"
        menuprincipalartista="carpeta_imagenes/morado/menuartista.png"
        menuprincipalalbum="carpeta_imagenes/morado/menualbum.png"
        menuprincipaladmin="carpeta_imagenes/morado/menuadmin.png"
        menuprincipaldescuentos="carpeta_imagenes/morado/descuentos.png"
        menuprincipalfacturas="carpeta_imagenes/morado/facturas.png"
        menuprincipalgenerar="carpeta_imagenes/morado/generar.png"
        menuprincipalpagar="carpeta_imagenes/morado/pagar.png"
        play_btn_file = "carpeta_imagenes/morado/play.png"
        pause_btn_file ="carpeta_imagenes/morado/pause.png"
        next_btn_file = "carpeta_imagenes/morado/siguiente.png"
        prev_btn_file = "carpeta_imagenes/morado/anterior.png"
        cargar_file = "carpeta_imagenes/morado/CargarCancion.png"
        menuprincipalreproduccion = "carpeta_imagenes/morado/Reproductor.png"        
        inicio()
    elif modo_color == "Azul Claro": #########AZUL CLARO#########
        color2="#42a4ff"
        imageninsercionpropietario = "carpeta_imagenes/azulclaro/Insertarproazulclaro.png"
        imageninsercionplaylist = "carpeta_imagenes/azulclaro/Insertarplayazulclaro.png"
        imageninsercionartista = "carpeta_imagenes/azulclaro/Insertarartistaazulclaro.png"
        imageninserciongenero = "carpeta_imagenes/azulclaro/Insertargeneroazulclaro.png"
        imageninsercionalbum = "carpeta_imagenes/azulclaro/Insertaralbumazulclaro.png"
        imageninsercioncancion = "carpeta_imagenes/azulclaro/Insertarcancionazulclaro.png"
        imageninsercionadmin = "carpeta_imagenes/azulclaro/Insertaradminazulclaro.png"
        imagenbusquedapropietario = "carpeta_imagenes/azulclaro/buscarproazulclaro.png"
        imagenbusquedaplaylist = "carpeta_imagenes/azulclaro/buscarplaylistazulclaro.png"
        imagenbusquedaartista = "carpeta_imagenes/azulclaro/buscarartistaazulclaro.png"
        imagenbusquedagenero = "carpeta_imagenes/azulclaro/buscargeneroazulclaro.png"
        imagenbusquedaalbum = "carpeta_imagenes/azulclaro/buscaralbumazulclaro.png"
        imagenbusquedacancion = "carpeta_imagenes/azulclaro/buscarcancionazulclaro.png"
        imagenbusquedaadmin = "carpeta_imagenes/azulclaro/buscaradminazulclaro.png"
        imageneliminarpropietario = "carpeta_imagenes/azulclaro/eliminarproazulclaro.png"
        imageneliminarplaylist = "carpeta_imagenes/azulclaro/eliminarplaylistazulclaro.png"
        imageneliminarartista = "carpeta_imagenes/azulclaro/eliminarartistaazulclaro.png"
        imageneliminargenero = "carpeta_imagenes/azulclaro/eliminargeneroazulclaro.png"
        imageneliminaralbum = "carpeta_imagenes/azulclaro/eliminaralbumazulclaro.png"
        imageneliminarcancion = "carpeta_imagenes/azulclaro/eliminarcancionazulclaro.png"
        imageneliminaradmin = "carpeta_imagenes/azulclaro/eliminaradminazulclaro.png"
        imagenmodificarpropietario = "carpeta_imagenes/azulclaro/modificarproazulclaro.png"
        imagenmodificarplaylist = "carpeta_imagenes/azulclaro/modificarplaylistazulclaro.png"
        imagenmodificarartista = "carpeta_imagenes/azulclaro/modificarartistaazulclaro.png"
        imagenmodificargenero = "carpeta_imagenes/azulclaro/modificargeneroazulclaro.png"
        imagenmodificaralbum = "carpeta_imagenes/azulclaro/modificaralbumazulclaro.png"
        imagenmodificarcancion = "carpeta_imagenes/azulclaro/modificarcancionazulclaro.png"
        imagenmodificaradmin = "carpeta_imagenes/azulclaro/modificaradminazulclaro.png"
        menuprincipalalbumes="carpeta_imagenes/azulclaro/albumesazulclaro.png"
        menuprincipalusuarios="carpeta_imagenes/azulclaro/usuariosazulclaro.png"
        menuprincipalpagos="carpeta_imagenes/azulclaro/pagosb.png"
        menuprincipalmusica="carpeta_imagenes/azulclaro/musicaazulclaro.png"
        menuprincipalpropietario="carpeta_imagenes/azulclaro/menupropietarios.png"
        menuprincipalplaylist="carpeta_imagenes/azulclaro/menuplaylist.png"
        menuprincipalgenero="carpeta_imagenes/azulclaro/menugenero.png"
        menuprincipalcancion="carpeta_imagenes/azulclaro/menucancion.png"
        menuprincipalartista="carpeta_imagenes/azulclaro/menuartista.png"
        menuprincipalalbum="carpeta_imagenes/azulclaro/menualbum.png"
        menuprincipaladmin="carpeta_imagenes/azulclaro/menuadmin.png"
        menuprincipaldescuentos="carpeta_imagenes/azulclaro/descuentos.png"
        menuprincipalfacturas="carpeta_imagenes/azulclaro/facturas.png"
        menuprincipalgenerar="carpeta_imagenes/azulclaro/generar.png"
        menuprincipalpagar="carpeta_imagenes/azulclaro/pagar.png"
        play_btn_file = "carpeta_imagenes/azulclaro/play.png"
        pause_btn_file ="carpeta_imagenes/azulclaro/pause.png"
        next_btn_file = "carpeta_imagenes/azulclaro/siguiente.png"
        prev_btn_file = "carpeta_imagenes/azulclaro/anterior.png"
        cargar_file = "carpeta_imagenes/azulclaro/CargarCancion.png"
        menuprincipalreproduccion = "carpeta_imagenes/azulclaro/Reproductor.png"        
        inicio()
    elif modo_color == "Verde Neon": #########VERDE NEON#########
        color2 = "#39FF14"
        imageninsercionpropietario = "carpeta_imagenes/verdeneon/Insertarproverdeneon.png"
        imageninsercionplaylist = "carpeta_imagenes/verdeneon/Insertarplayverdeneon.png"
        imageninsercionartista = "carpeta_imagenes/verdeneon/Insertarartistaverdeneon.png"
        imageninserciongenero = "carpeta_imagenes/verdeneon/Insertargeneroverdeneon.png"
        imageninsercionalbum = "carpeta_imagenes/verdeneon/Insertaralbumverdeneon.png"
        imageninsercioncancion = "carpeta_imagenes/verdeneon/Insertarcancionverdeneon.png"
        imageninsercionadmin = "carpeta_imagenes/verdeneon/Insertaradminverdeneon.png"
        imagenbusquedapropietario = "carpeta_imagenes/verdeneon/buscarproverdeneon.png"
        imagenbusquedaplaylist = "carpeta_imagenes/verdeneon/buscarplaylistverdeneon.png"
        imagenbusquedaartista = "carpeta_imagenes/verdeneon/buscarartistaverdeneon.png"
        imagenbusquedagenero = "carpeta_imagenes/verdeneon/buscargeneroverdeneon.png"
        imagenbusquedaalbum = "carpeta_imagenes/verdeneon/buscaralbumverdeneon.png"
        imagenbusquedacancion = "carpeta_imagenes/verdeneon/buscarcancionverdeneon.png"
        imagenbusquedaadmin = "carpeta_imagenes/verdeneon/buscaradminverdeneon.png"
        imageneliminarpropietario = "carpeta_imagenes/verdeneon/eliminarproverdeneon.png"
        imageneliminarplaylist = "carpeta_imagenes/verdeneon/eliminarplaylistverdeneon.png"
        imageneliminarartista = "carpeta_imagenes/verdeneon/eliminarartistaverdeneon.png"
        imageneliminargenero = "carpeta_imagenes/verdeneon/eliminargeneroverdeneon.png"
        imageneliminaralbum = "carpeta_imagenes/verdeneon/eliminaralbumverdeneon.png"
        imageneliminarcancion = "carpeta_imagenes/verdeneon/eliminarcancionverdeneon.png"
        imageneliminaradmin = "carpeta_imagenes/verdeneon/eliminaradminverdeneon.png"
        imagenmodificarpropietario = "carpeta_imagenes/verdeneon/modificarproverdeneon.png"
        imagenmodificarplaylist = "carpeta_imagenes/verdeneon/modificarplaylistverdeneon.png"
        imagenmodificarartista = "carpeta_imagenes/verdeneon/modificarartistaverdeneon.png"
        imagenmodificargenero = "carpeta_imagenes/verdeneon/modificargeneroverdeneon.png"
        imagenmodificaralbum = "carpeta_imagenes/verdeneon/modificaralbumverdeneon.png"
        imagenmodificarcancion = "carpeta_imagenes/verdeneon/modificarcancionverdeneon.png"
        imagenmodificaradmin = "carpeta_imagenes/verdeneon/modificaradminverdeneon.png"
        menuprincipalalbumes="carpeta_imagenes/verdeneon/albumesverdeneon.png"
        menuprincipalusuarios="carpeta_imagenes/verdeneon/usuariosverdeneon.png"
        menuprincipalpagos="carpeta_imagenes/verdeneon/pagosb.png"
        menuprincipalmusica="carpeta_imagenes/verdeneon/musicaverdeneon.png"
        menuprincipalpropietario="carpeta_imagenes/verdeneon/menupropietario.png"
        menuprincipalplaylist="carpeta_imagenes/verdeneon/menuplaylist.png"
        menuprincipalgenero="carpeta_imagenes/verdeneon/menugenero.png"
        menuprincipalcancion="carpeta_imagenes/verdeneon/menucancion.png"
        menuprincipalartista="carpeta_imagenes/verdeneon/menuartista.png"
        menuprincipalalbum="carpeta_imagenes/verdeneon/menualbum.png"
        menuprincipaladmin="carpeta_imagenes/verdeneon/menuadmin.png"
        menuprincipaldescuentos="carpeta_imagenes/verdeneon/descuentos.png"
        menuprincipalfacturas="carpeta_imagenes/verdeneon/facturas.png"
        menuprincipalgenerar="carpeta_imagenes/verdeneon/generar.png"
        menuprincipalpagar="carpeta_imagenes/verdeneon/pagar.png"
        play_btn_file = "carpeta_imagenes/verdeneon/play.png"
        pause_btn_file ="carpeta_imagenes/verdeneon/pause.png"
        next_btn_file = "carpeta_imagenes/verdeneon/siguiente.png"
        prev_btn_file = "carpeta_imagenes/verdeneon/anterior.png"
        cargar_file = "carpeta_imagenes/verdeneon/CargarCancion.png"
        menuprincipalreproduccion = "carpeta_imagenes/verdeneon/Reproductor.png"        
        inicio()
    elif modo_color == "Morado Neon": #########MORADO NEON#########
        color2 = "#BD00FF"
        imageninsercionpropietario = "carpeta_imagenes/moradoneon/Insertarpromoradoneon.png"
        imageninsercionplaylist = "carpeta_imagenes/moradoneon/Insertarplaymoradoneon.png"
        imageninsercionartista = "carpeta_imagenes/moradoneon/Insertarartistamoradoneon.png"
        imageninserciongenero = "carpeta_imagenes/moradoneon/Insertargeneromoradoneon.png"
        imageninsercionalbum = "carpeta_imagenes/moradoneon/Insertaralbummoradoneon.png"
        imageninsercioncancion = "carpeta_imagenes/moradoneon/Insertarcancionmoradoneon.png"
        imageninsercionadmin = "carpeta_imagenes/moradoneon/Insertaradminmoradoneon.png"
        imagenbusquedapropietario = "carpeta_imagenes/moradoneon/buscarpromoradoneon.png"
        imagenbusquedaplaylist = "carpeta_imagenes/moradoneon/buscarplaylistmoradoneon.png"
        imagenbusquedaartista = "carpeta_imagenes/moradoneon/buscarartistamoradoneon.png"
        imagenbusquedagenero = "carpeta_imagenes/moradoneon/buscargeneromoradoneon.png"
        imagenbusquedaalbum = "carpeta_imagenes/moradoneon/buscaralbummoradoneon.png"
        imagenbusquedacancion = "carpeta_imagenes/moradoneon/buscarcancionmoradoneon.png"
        imagenbusquedaadmin = "carpeta_imagenes/moradoneon/buscaradminmoradoneon.png"
        imageneliminarpropietario = "carpeta_imagenes/moradoneon/eliminarpromoradoneon.png"
        imageneliminarplaylist = "carpeta_imagenes/moradoneon/eliminarplaylistmoradoneon.png"
        imageneliminarartista = "carpeta_imagenes/moradoneon/eliminarartistamoradoneon.png"
        imageneliminargenero = "carpeta_imagenes/moradoneon/eliminargeneromoradoneon.png"
        imageneliminaralbum = "carpeta_imagenes/moradoneon/eliminaralbummoradoneon.png"
        imageneliminarcancion = "carpeta_imagenes/moradoneon/eliminarcancionmoradoneon.png"
        imageneliminaradmin = "carpeta_imagenes/moradoneon/eliminaradminmoradoneon.png"
        imagenmodificarpropietario = "carpeta_imagenes/moradoneon/modificarpromoradoneon.png"
        imagenmodificarplaylist = "carpeta_imagenes/moradoneon/modificarplaylistmoradoneon.png"
        imagenmodificarartista = "carpeta_imagenes/moradoneon/modificarartistamoradoneon.png"
        imagenmodificargenero = "carpeta_imagenes/moradoneon/modificargeneromoradoneon.png"
        imagenmodificaralbum = "carpeta_imagenes/moradoneon/modificaralbummoradoneon.png"
        imagenmodificarcancion = "carpeta_imagenes/moradoneon/modificarcancionmoradoneon.png"
        imagenmodificaradmin = "carpeta_imagenes/moradoneon/modificaradminmoradoneon.png"
        menuprincipalalbumes="carpeta_imagenes/moradoneon/albumesmoradoneon.png"
        menuprincipalusuarios="carpeta_imagenes/moradoneon/usuariosmoradoneon.png"
        menuprincipalpagos="carpeta_imagenes/moradoneon/pagosb.png"
        menuprincipalmusica="carpeta_imagenes/moradoneon/musicamoradoneon.png"
        menuprincipalpropietario="carpeta_imagenes/moradoneon/menupropietario.png"
        menuprincipalplaylist="carpeta_imagenes/moradoneon/menuplaylist.png"
        menuprincipalgenero="carpeta_imagenes/moradoneon/menugenero.png"
        menuprincipalcancion="carpeta_imagenes/moradoneon/menucancion.png"
        menuprincipalartista="carpeta_imagenes/moradoneon/menuartista.png"
        menuprincipalalbum="carpeta_imagenes/moradoneon/menualbum.png"
        menuprincipaladmin="carpeta_imagenes/moradoneon/menuadmin.png"
        menuprincipaldescuentos="carpeta_imagenes/moradoneon/descuentos.png"
        menuprincipalfacturas="carpeta_imagenes/moradoneon/facturas.png"
        menuprincipalgenerar="carpeta_imagenes/moradoneon/generar.png"
        menuprincipalpagar="carpeta_imagenes/moradoneon/pagar.png"
        play_btn_file = "carpeta_imagenes/moradoneon/play.png"
        pause_btn_file ="carpeta_imagenes/moradoneon/pause.png"
        next_btn_file = "carpeta_imagenes/moradoneon/siguiente.png"
        prev_btn_file = "carpeta_imagenes/moradoneon/anterior.png"
        cargar_file = "carpeta_imagenes/moradoneon/CargarCancion.png"
        menuprincipalreproduccion = "carpeta_imagenes/moradoneon/Reproductor.png"        
        inicio()
    else: #########FALLO SI NO SE ELIGE#########
        messagebox.showerror("Error", "No has elegido un color. Intenta de nuevo.")
def inicio():
    global pantalla
    global usuario_entrada
    pantalla = tk.Tk()
    pantalla.configure(bg=color)
    pantalla.title("Inicio de sesión")
    pantalla.geometry("800x500")
    pantalla.resizable(False, False)
    fuente = ("Console", 13)

    clock_text = tk.Label(pantalla, bg=color, fg=color2, font=("Console", 12))
    clock_text.grid(row=0, column=1, sticky="E", padx=10)

    fuente_reloj = ("Courier", 14, "bold")
    
    pantalla.columnconfigure(0, weight=1)
    pantalla.columnconfigure(1, weight=1)
    
    clock_text = tk.Label(pantalla, bg=color, fg=color2, font=fuente_reloj)
    clock_text.grid(row=0, column=1, sticky="E")

    tiempo(clock_text)

    input_usuario = tk.Label(pantalla, text="Usuario:", bg=color, fg=color2, font=fuente)
    input_usuario.place(x=100, y=100)
    usuario_entrada = tk.Entry(pantalla, fg=color, bg=color2, font=fuente)
    usuario_entrada.place(x=200, y=100)
    usuario_admin = tk.StringVar()
    usuario_admin.set("Usuario")



    radio_usuario = tk.Radiobutton(pantalla, text="Usuario", variable=usuario_admin, value="Usuario", bg=color, fg=color2, activebackground='white', selectcolor=color, font=fuente)
    radio_usuario.place(x=100, y=150)

    radio_admin = tk.Radiobutton(pantalla, text="Administrador", variable=usuario_admin, value="Administrador", bg=color, fg=color2, activebackground='white', selectcolor=color, font=fuente)
    radio_admin.place(x=100, y=185)

    boton_login = tk.Button(pantalla, text="Aceptar", command=lambda: validarint2(usuario_entrada, usuario_admin), bg=color, fg=color2, font=fuente,relief=tk.RAISED,borderwidth=4) 
    boton_login.place(x=100, y=240)



    pantalla.mainloop()

def validarint2(usuario_entrada, usuario_admin): #Valida que al puro inicio el usuario que sea entregado sea entero
    try:
        global usuario
        global usuarioparaveri
        usuarioparaveri= str(usuario_entrada.get())
        usuario = int(usuario_entrada.get())
        iniciarsesion(usuario_admin.get(), usuario) #Si es entero lo manda a revisar si necesita activacion
    except ValueError:
        messagebox.showerror("Error", "El usuario debe ser un número entero. Intenta de nuevo.")

def iniciarsesion(seleccion, Usuario): #Si existe el usuario y esta activo los deja entrar si no lo activa o lo crea
    global eventousuario
    seleccionado = seleccion
    usuario = Usuario
    if seleccionado == "Usuario":
        resultado = verificacionusuario(usuario)
    elif seleccionado == "Administrador":
        resultado = verificacionadministrador(usuario)
    else:
        resultado = "Parametros Incorrectos"
    if resultado == 1: #Si es uno existe y esta activa.
        cerrar(pantalla)
        eventousuario = "propietario"
        ventanaprincipal(0) 
    elif resultado == 2: #Si es dos existe y no esta activa.
        usuarioinactivo(usuario)
    elif resultado == 3: #Si es tres no existe.
        crearusuario(usuario)
    elif resultado == 4:
        cerrar(pantalla)
        eventousuario = "administrador"
        ventanaprincipal(1) 
    elif resultado == 5:
        messagebox.showerror("Administrador No Encontrado", "No existe ese administrador.")
    elif resultado == 6:
        cerrar(pantalla)
        eventousuario = "no pagado"
        messagebox.showinfo("Debes pagar la factura", "Se realizó un cobro debes pagar en la zona de facturas.")         
        ventanaprincipal(10)  
    else:
        messagebox.showerror("Error Desconocido", "Parámetros Incorrectos.")         
def usuarioinactivo(usuario): #avisa que el usuario esta inactivo
    global activacion
    cerrar(pantalla)
    activacion = tk.Tk()
    activacion.title("Activación de cuenta")
    activacion.geometry("800x500")
    activacion.resizable(False, False)
    activacion.configure(bg=color)
    fuente = ("Console", 16)

    activar = StringVar(value="No Activar")

    sobretexto = Label(activacion,text="Usuario Inactivo",bg=color,fg=color2,font=fuente)
    sobretexto2 = Label(activacion,text="¿Deseas Activarla?",bg=color,fg=color2,font=fuente)
    sobretexto3 = Label(activacion,text=f"Se te cobrará ${costoactividad()}",bg=color,fg=color2,font=fuente)

    sobretexto.pack(pady=(50, 10))
    sobretexto2.pack(pady=10)
    sobretexto3.pack(pady=10)

    radio_usuario = Radiobutton(activacion,text="Activar",variable=activar,value="Activar",bg=color,fg=color2,font=fuente,selectcolor=color)
    radio_admin = Radiobutton(activacion,text="No Activar",variable=activar,value="No Activar",bg=color,fg=color2,font=fuente,selectcolor=color)

    radio_usuario.pack(pady=10)
    radio_admin.pack(pady=10)

    boton_login = Button(activacion,text="Aceptar",command=lambda: deseactivar(activar.get(), usuario),bg=color,fg=color2,font=fuente)

    boton_login.pack(pady=30)

    activacion.mainloop()

def deseactivar(string, usuario): #revisa si quieren activar la cuenta
    global cuentaenbeta
    if string=="No Activar":
        cerrar(activacion)
        messagebox.showerror("Cuenta No Activada", "Cuenta no activada, Nos Vemos.")
    elif string=="Activar":
        #Se realiza el cobro
        realizaractivacion(usuario)
        messagebox.showinfo("Cuenta Activada", f"Se realizó un cobro de ${costoactividad()} y se registró en Cobro.txt, Paga en la zona de facturas.")
        cuentaenbeta=True
        cerrar(activacion)          
        ventanaprincipal(10)

def realizaractivacion(usuario):
    cod_propietario = str(usuario)
    for clave, valores in dicpropietarios.items():
        if cod_propietario == clave:
            estado_cuenta = valores.get("activo")
            if estado_cuenta == "0":
                valores["activo"] = '1'
                nombre = valores["nombrepro"]
                cod_membresia = valores["codmembresia"]
                nombre_archivo = f"{cod_propietario}.txt"
                if not os.path.exists("Cobros"):
                    os.makedirs("Cobros")
                ruta_de_cobro = os.path.join("Cobros", nombre_archivo)
                facturas[cod_propietario] = {'nombre': nombre, 'codmembresia': cod_membresia, 'costo: $': costoactividad()}
                with open(ruta_de_cobro, "a") as file:
                    file.write("-------------------------------------------------------------------------------------------------------------\n")
                    file.write(f"| Usuario: {nombre} | Codpropietario: {cod_propietario} | Costo: ${costoactividad()} |\n")
                    file.write("-------------------------------------------------------------------------------------------------------------\n")
########################################################CREACION###################################################
def crearusuario(usuario): #Será llamado si el usuario no existe
    global creacion
    cerrar(pantalla)
    creacion = tk.Tk()
    creacion.title("Creación de cuenta")
    creacion.geometry("800x500")
    creacion.resizable(False, False)
    creacion.configure(bg=color)
    fuente = ("Console", 16)
    
    input_usuario = tk.Label(creacion, text="Nombre" , bg=color , fg=color2, font=fuente)
    nombre = tk.Entry(creacion, fg=color, bg=color2, font=fuente)
    input_codmembresia = tk.Label(creacion, text="Codmembresia" , bg=color , fg=color2, font=fuente)
    codmembresia = tk.Entry(creacion, fg=color, bg=color2, font=fuente)    
    activar = StringVar(value="No Activar")

    sobretexto = Label(creacion,text="Usuario Inexistente",bg=color,fg=color2,font=fuente)

    sobretexto.pack(pady=(50, 10))
    input_usuario.pack(pady=(10))
    nombre.pack(pady=(10))
    input_codmembresia.pack(pady=(10))
    codmembresia.pack(pady=(10))    

    radio_usuario = Radiobutton(creacion,text="Crearlo",variable=activar,value="Crear",bg=color,fg=color2,font=fuente,selectcolor=color)
    radio_admin = Radiobutton(creacion,text="No Crearlo",variable=activar,value="No Crear",bg=color,fg=color2,font=fuente,selectcolor=color)

    radio_usuario.pack(pady=10)
    radio_admin.pack(pady=10)

    boton_login = Button(creacion,text="Aceptar",command=lambda: validarint3(activar.get(), usuario, nombre.get(), codmembresia.get()),bg=color,fg=color2,font=fuente)

    boton_login.pack(pady=30)

    creacion.mainloop()

def validarint3(activar, usuario, nombre, codmembresia): #Valida que al crear un usuario codmembresia sea entero
    try:
        codmembresia = int(codmembresia)
        pruebadexistencia(activar, usuario, nombre, codmembresia) #Y la manda a revisar que no exista el codmembresia
    except ValueError:
        messagebox.showerror("Error", "El codigo de la membresia debe ser un número entero. Intenta de nuevo.")

def pruebadexistencia(activar, usuario, nombre, codmembresia): #Revisa que no exista el codmembresia
    membresia = codmembresia
    resultado = verificacionmembresia(membresia)
    if resultado == 1: #Si es uno no existe continua
        deseacrear(activar, usuario, nombre, codmembresia)
    elif resultado == 2: #es encontrado
        messagebox.showerror("Error", "Codmembresia en uso.")
    else:
        messagebox.showerror("Error Desconocido", "Parámetros Incorrectos.")

def deseacrear(opcion, usuario, nombre, codmembresia): #revisa si quiere crear la cuenta o no
    global activaciondecreado

    if opcion == "No Crear":
        cerrar(creacion)
        messagebox.showerror("Cuenta No Creada", "Cuenta no creada, Nos Vemos.")
    elif opcion == "Crear":
        cerrar(creacion)
        
        # Nueva ventana para la activación
        activaciondecreado = tk.Tk()
        activaciondecreado.title("Activación de cuenta")
        activaciondecreado.geometry("800x500")
        activaciondecreado.resizable(False, False)
        activaciondecreado.configure(bg=color)

        fuente = ("Console", 16)
        activar = StringVar(value="No Activar")

        sobretexto2 = Label(activaciondecreado, text="¿Deseas Activarla?", bg=color, fg=color2, font=fuente)
        sobretexto3 = Label(activaciondecreado, text=f"Se te cobrará ${costocreacion()}", bg=color, fg=color2, font=fuente)

        sobretexto2.pack(pady=(50, 10))
        sobretexto3.pack(pady=10)

        radio_usuario = Radiobutton(activaciondecreado, text="Activar", variable=activar, value="Activar", bg=color, fg=color2, font=fuente, selectcolor=color)
        radio_admin = Radiobutton(activaciondecreado, text="No Activar", variable=activar, value="No Activar", bg=color, fg=color2, font=fuente, selectcolor=color)

        radio_usuario.pack(pady=10)
        radio_admin.pack(pady=10)

        boton_login = Button(activaciondecreado, text="Aceptar", command=lambda: creacioncompleta(activar.get(), usuario, nombre, codmembresia), bg=color, fg=color2, font=fuente)

        boton_login.pack(pady=30)

        activaciondecreado.mainloop()

def creacioncompleta(string, usuario, nombre, codmembresia): #revisa si quiere activar o no
    if string=="No Activar":
        cerrar(activaciondecreado)
        creacionmax(usuario, nombre, codmembresia,0)
        messagebox.showerror("Cuenta No Activada", "Cuenta creada mas no activada, Nos Vemos.")
    elif string=="Activar":
        creacionmax(usuario, nombre, codmembresia,1)
        messagebox.showinfo("Cuenta Creada", f"Cuenta Creada con éxito, Se realizó un cobro de ${costocreacion()} y se registró en Cobro.txt, Paga en la zona de facturas.")
        cerrar(activaciondecreado)          
        ventanaprincipal(10)

def creacionmax(usuario, nombre, codmembresia, activar): #Añade usuarios a dicpropietarios
    global cuentaenbeta
    usuario=str(usuario)
    activar=str(activar)
    if activar==0:
        valores = {"nombrepro": nombre, "codmembresia": codmembresia, "activo": activar}
        dicpropietarios[usuario] = valores
    else:
        cuentaenbeta=True
        valores = {"nombrepro": nombre, "codmembresia": codmembresia, "activo": activar}
        dicpropietarios[usuario] = valores
        nombre_archivo = f"{usuario}.txt"
        if not os.path.exists("Cobros"):
            os.makedirs("Cobros")
        rutadecobro = os.path.join("Cobros", nombre_archivo)
        facturas[usuario]={'nombre': nombre, 'codmembresia': codmembresia, 'costo: $': costocreacion()}
        with open(rutadecobro, "a") as file:
                file.write("-------------------------------------------------------------------------------------------------------------\n")
                file.write(f"Usuario: {nombre} | Codpropietario: {usuario} |Costo: ${costocreacion()}|\n")
                file.write("-------------------------------------------------------------------------------------------------------------\n")
########################################################MAIN#######################################################
def cerrarsesion(ventana):
    ventana.destroy()
    inicio()
def abrir_ventana():
    ventana_secundaria = tk.Toplevel()
    ventana_secundaria.title("Ventana Secundaria")
    etiqueta = tk.Label(ventana_secundaria, text="Esta es una ventana secundaria")
    etiqueta.pack()
def clic(evento):
    if eventousuario=="administrador":
        if "insertarpro"==evento:
            insertar_propietario()
        elif "insertarplay"==evento:
            insertar_playlist()
        elif "insertargenero"==evento:
            insertar_genero()
        elif "insertarart"==evento:
            insertar_artista()
        elif "insertaralbum"==evento:
            insertar_elalbum()
        elif "insertarcancion"==evento:
            insertar_canciones()
        elif "insertaradmin"==evento:
            insertar_administradores()
        elif "buscarpro"==evento:
            buscar_propietario()
        elif "buscarplay"==evento:
            buscar_playlist()
        elif "buscargenero"==evento:
            buscar_genero()
        elif "buscarart"==evento:
            buscar_artista()
        elif "buscaralbum"==evento:
            buscar_album()
        elif "buscarcancion"==evento:
            buscar_cancion()
        elif "buscaradmin"==evento:
            buscar_admin()
        elif "eliminarpro"==evento: 
            eliminar_propietario()
        elif "eliminarplay"==evento:
            eliminar_playlist()
        elif "eliminargenero"==evento:
            eliminar_genero()
        elif "eliminarart"==evento:
            eliminar_artista()
        elif "eliminaralbum"==evento:
            eliminar_album()
        elif "eliminarcancion"==evento:
            eliminar_cancion()
        elif "eliminaradmin"==evento:
            eliminar_admin()
        elif "modificarpro"==evento: 
            modificar_propietario()
        elif "modificarplay"==evento:
            modificar_playlist()
        elif "modificargenero"==evento:
            modificar_genero()
        elif "modificarart"==evento:
            modificar_artista()
        elif "modificaralbum"==evento:
            modificar_album()
        elif "modificarcancion"==evento:
            modificar_cancion()
        elif "modificaradmin"==evento:
            modificar_admin()
        elif "pagodecuenta"==evento:
            pagodefacturasvencidas()
        elif "generarfactura"==evento:
            generarfacturasadmin()
        elif "descuentos"==evento:
            descuentos_comando()
        elif "cargarmusica"==evento: 
            cargar_musica20()
        elif "reproduccirmusica"==evento:
            reproducir_musica()
        elif "pausarmusica"==evento:
            pausar_musica()
        elif "siguientemusica"==evento:
            siguiente_musica20()
        elif "anteriormusica"==evento:
            anterior_musica20()
    elif eventousuario=="propietario":
        if "insertarpro"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertarplay"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertargenero"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertarart"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertaralbum"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertarcancion"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertaradmin"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "buscarpro"==evento:
            buscar_propietario()
        elif "buscarplay"==evento:
            buscar_playlist()
        elif "buscargenero"==evento:
            buscar_genero()
        elif "buscarart"==evento:
            buscar_artista()
        elif "buscaralbum"==evento:
            buscar_album()
        elif "buscarcancion"==evento:
            buscar_cancion()
        elif "buscaradmin"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminarpro"==evento: 
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminarplay"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminargenero"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminarart"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminaralbum"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminarcancion"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminaradmin"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificarpro"==evento: 
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificarplay"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificargenero"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificarart"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificaralbum"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificarcancion"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificaradmin"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "pagodecuenta"==evento:
            pagodefacturasvencidas()
        elif "generarfactura"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "descuentos"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "cargarmusica"==evento: 
            cargar_musica20()
        elif "reproduccirmusica"==evento:
            reproducir_musica()
        elif "pausarmusica"==evento:
            pausar_musica()
        elif "siguientemusica"==evento:
            siguiente_musica20()
        elif "anteriormusica"==evento:
            anterior_musica20()
    elif eventousuario=="no pagado":
        if "insertarpro"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertarplay"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertargenero"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertarart"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertaralbum"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertarcancion"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "insertaradmin"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "buscarpro"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "buscarplay"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "buscargenero"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "buscarart"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "buscaralbum"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "buscarcancion"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "buscaradmin"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminarpro"==evento: 
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminarplay"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminargenero"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminarart"==evento:
            messagebox.showerror("Error", "No tienes utorización para esta función.")
        elif "eliminaralbum"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminarcancion"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "eliminaradmin"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificarpro"==evento: 
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificarplay"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificargenero"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificarart"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificaralbum"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificarcancion"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "modificaradmin"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "pagodecuenta"==evento:
            pagodefacturasvencidas()
        elif "generarfactura"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "descuentos"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "cargarmusica"==evento: 
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "reproduccirmusica"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "pausarmusica"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "siguientemusica"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
        elif "anteriormusica"==evento:
            messagebox.showerror("Error", "No tienes autorización para esta función.")
def mostrar_menu(event, menu):
    menu.post(event.x_root, event.y_root)  
def ventanaprincipal(bandera):
    global imageninsercionpropietario
    global eventousuario
    global ventanaprincipal100
    global tamaño
    if bandera==1:
        eventousuario = "administrador"
    elif bandera==0:
        eventousuario = "propietario"   
    else:
        eventousuario = "no pagado"        
    ventana = tk.Tk()
    ventana .configure(bg=color)
    ventana.title("Menú del Reproductor")
    ventana.geometry("800x600")
    fuente = ("Console", 10)
    fuenteg = ("Courier", 13, "bold")
    #Barra de herramientas para los Pop Ups
    barra_herramientas = tk.Menu(ventana, bg=color, fg=color2, font=fuente) # Color de fondo, texto y fuente
    ventana.config(menu=barra_herramientas)

    boton_cerrar_sesion = tk.Button(ventana, text="Cerrar Sesión", command=lambda: cerrarsesion(ventana),bg=color, fg=color2,font=fuenteg)
    boton_cerrar_sesion.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
    
    fuente_reloj = ("Courier", 14, "bold")
    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)
    clock_text = tk.Label(ventana, bg=color, fg=color2, font=fuente_reloj)
    clock_text.place(x=700, y=10)
    clock_text.grid(row=0, column=1, sticky="E", padx=10, pady=10)  
    tamaño=5
    tiempo(clock_text)

    ventanaprincipal100=ventana


    #Imagen USUARIOS##################################################
    imagen_menupro = tk.PhotoImage(file=imageninsercionpropietario).subsample(tamaño)

    insertar_prop = tk.Label(ventana, text="Usuarios", bg=color, fg=color2, font=fuenteg)
    insertar_prop.place(x=69, y=75)

    imageninspro = tk.PhotoImage(file=imageninsercionpropietario).subsample(tamaño)
    imagenbuspro = tk.PhotoImage(file=imagenbusquedapropietario).subsample(tamaño)
    imagenelipro = tk.PhotoImage(file=imageneliminarpropietario).subsample(tamaño)
    imagenmodpro = tk.PhotoImage(file=imagenmodificarpropietario).subsample(tamaño)

    menu_propietario = tk.Menu(ventana, tearoff=0)
    menu_propietario.add_command(image=imageninspro, command=lambda: clic("insertarpro"))
    menu_propietario.add_command(image=imagenbuspro, command=lambda: clic("buscarpro"))
    menu_propietario.add_command(image=imagenelipro, command=lambda: clic("eliminarpro"))
    menu_propietario.add_command(image=imagenmodpro, command=lambda: clic("modificarpro"))

    imagen_menuadmin = tk.PhotoImage(file=imageninsercionadmin).subsample(tamaño)

    imageninsadmin = tk.PhotoImage(file=imageninsercionadmin).subsample(tamaño)
    imagenbusadmin = tk.PhotoImage(file=imagenbusquedaadmin).subsample(tamaño)
    imageneliadmin = tk.PhotoImage(file=imageneliminaradmin).subsample(tamaño)
    imagenmodadmin = tk.PhotoImage(file=imagenmodificaradmin).subsample(tamaño)

    menu_admin = tk.Menu(ventana, tearoff=0)
    menu_admin.add_command(image=imageninsadmin, command=lambda: clic("insertaradmin"))
    menu_admin.add_command(image=imagenbusadmin, command=lambda: clic("buscaradmin"))
    menu_admin.add_command(image=imageneliadmin, command=lambda: clic("eliminaradmin"))
    menu_admin.add_command(image=imagenmodadmin, command=lambda: clic("modificaradmin"))

    imagen_propietario = tk.PhotoImage(file=menuprincipalpropietario).subsample(tamaño)
    boton_propietario = tk.Menubutton(ventana, image=imagen_propietario, bg=color, bd=0)
    boton_propietario.image = imagen_propietario  # Para evitar que la imagen sea eliminada por el recolector de basura
    boton_propietario.menu = menu_propietario

    imagen_admin = tk.PhotoImage(file=menuprincipaladmin).subsample(tamaño)
    boton_admin = tk.Menubutton(ventana, image=imagen_admin, bg=color, bd=0)
    boton_admin.image = imagen_admin
    boton_admin.menu = menu_admin

    imagen_menuprincipal = menuprincipalusuarios
    imagen_menuprincipal = tk.PhotoImage(file=imagen_menuprincipal).subsample(tamaño)
    menu_principal = tk.Menu(ventana, tearoff=0)
    menu_principal.add_cascade(label="Propietario", menu=boton_propietario.menu, image=imagen_propietario, compound="left")
    menu_principal.add_cascade(label="Admin", menu=boton_admin.menu, image=imagen_admin, compound="left")

    boton_imagen_principal = tk.Label(ventana, image=imagen_menuprincipal, bg=color)
    boton_imagen_principal.bind("<Button-1>", lambda event: mostrar_menu(event, menu_principal))
    boton_imagen_principal.place(x=18, y=115)
    #Imagen Musica##################################################
    imagen_menugenero = tk.PhotoImage(file=menuprincipalgenero).subsample(tamaño)
    imagen_menuplay = tk.PhotoImage(file=menuprincipalplaylist).subsample(tamaño)

    insertar_genero = tk.Label(ventana, text="Musica", bg=color, fg=color2, font=fuenteg)
    insertar_genero.place(x=230, y=75)

    imageninsplay = tk.PhotoImage(file=imageninsercionplaylist).subsample(tamaño)
    imagenbusplay = tk.PhotoImage(file=imagenbusquedaplaylist).subsample(tamaño)
    imageneliplay = tk.PhotoImage(file=imageneliminarplaylist).subsample(tamaño)
    imagenmodplay = tk.PhotoImage(file=imagenmodificarplaylist).subsample(tamaño)

    menu_play = tk.Menu(ventana, tearoff=0)
    menu_play.add_command(image=imageninsplay, command=lambda: clic("insertarplay"))
    menu_play.add_command(image=imagenbusplay, command=lambda: clic("buscarplay"))
    menu_play.add_command(image=imageneliplay, command=lambda: clic("eliminarplay"))
    menu_play.add_command(image=imagenmodplay, command=lambda: clic("modificarplay"))    

    imageninsgenero = tk.PhotoImage(file=imageninserciongenero).subsample(tamaño)
    imagenbusgenero = tk.PhotoImage(file=imagenbusquedagenero).subsample(tamaño)
    imageneligenero = tk.PhotoImage(file=imageneliminargenero).subsample(tamaño)
    imagenmodgenero = tk.PhotoImage(file=imagenmodificargenero).subsample(tamaño)

    menu_genero = tk.Menu(ventana, tearoff=0)
    menu_genero.add_command(image=imageninsgenero, command=lambda: clic("insertargenero"))
    menu_genero.add_command(image=imagenbusgenero, command=lambda: clic("buscargenero"))
    menu_genero.add_command(image=imageneligenero, command=lambda: clic("eliminargenero"))
    menu_genero.add_command(image=imagenmodgenero, command=lambda: clic("modificargenero"))

    imagen_menuartista = tk.PhotoImage(file=menuprincipalartista).subsample(tamaño)

    insertar_artista = tk.Label(ventana, text="Artista", bg=color, fg=color2, font=fuenteg)

    imageninsart = tk.PhotoImage(file=imageninsercionartista).subsample(tamaño)
    imagenbusart = tk.PhotoImage(file=imagenbusquedaartista).subsample(tamaño)
    imageneliart = tk.PhotoImage(file=imageneliminarartista).subsample(tamaño)
    imagenmodart = tk.PhotoImage(file=imagenmodificarartista).subsample(tamaño)

    menu_artista2 = tk.Menu(ventana, tearoff=0)
    menu_artista2.add_command(image=imageninsart, command=lambda: clic("insertarart"))
    menu_artista2.add_command(image=imagenbusart, command=lambda: clic("buscarart"))
    menu_artista2.add_command(image=imageneliart, command=lambda: clic("eliminarart"))
    menu_artista2.add_command(image=imagenmodart, command=lambda: clic("modificarart"))

    imagen_menuprincipal2 = tk.PhotoImage(file=menuprincipalmusica).subsample(tamaño)
    menu_principal2 = tk.Menu(ventana, tearoff=0)
    menu_principal2.add_cascade(label="Playlist", menu=menu_play, image=imagen_menuplay, compound="left")
    menu_principal2.add_cascade(label="Género", menu=menu_genero, image=imagen_menugenero, compound="left")
    menu_principal2.add_cascade(label="Artista", menu=menu_artista2, image=imagen_menuartista, compound="left")

    boton_imagen_principal2 = tk.Label(ventana, image=imagen_menuprincipal2, bg=color)
    boton_imagen_principal2.bind("<Button-1>", lambda event: mostrar_menu(event, menu_principal2))
    boton_imagen_principal2.place(x=188, y=115)
    #Imagen albumes#################################################
    imagen_menualbum = tk.PhotoImage(file=menuprincipalalbum).subsample(tamaño)

    insertar_album = tk.Label(ventana, text="Albumes", bg=color, fg=color2, font=fuenteg)
    insertar_album.place(x=377, y=75)

    imageninsalbum = tk.PhotoImage(file=imageninsercionalbum).subsample(tamaño)
    imagenbusalbum = tk.PhotoImage(file=imagenbusquedaalbum).subsample(tamaño)
    imagenelialbum = tk.PhotoImage(file=imageneliminaralbum).subsample(tamaño)
    imagenmodalbum = tk.PhotoImage(file=imagenmodificaralbum).subsample(tamaño)

    menu_album = tk.Menu(ventana, tearoff=0)
    menu_album.add_command(image=imageninsalbum, command=lambda: clic("insertaralbum"))
    menu_album.add_command(image=imagenbusalbum, command=lambda: clic("buscaralbum"))
    menu_album.add_command(image=imagenelialbum, command=lambda: clic("eliminaralbum"))
    menu_album.add_command(image=imagenmodalbum, command=lambda: clic("modificaralbum"))

    imagen_menucancion = tk.PhotoImage(file=menuprincipalcancion).subsample(tamaño)

    insertar_cancion = tk.Label(ventana, text="Canción", bg=color, fg=color2, font=fuenteg)

    imageninscancion = tk.PhotoImage(file=imageninsercioncancion).subsample(tamaño)
    imagenbuscancion = tk.PhotoImage(file=imagenbusquedacancion).subsample(tamaño)
    imagenelicancion = tk.PhotoImage(file=imageneliminarcancion).subsample(tamaño)
    imagenmodcancion = tk.PhotoImage(file=imagenmodificarcancion).subsample(tamaño)

    menu_cancion = tk.Menu(ventana, tearoff=0)
    menu_cancion.add_command(image=imageninscancion, command=lambda: clic("insertarcancion"))
    menu_cancion.add_command(image=imagenbuscancion, command=lambda: clic("buscarcancion"))
    menu_cancion.add_command(image=imagenelicancion, command=lambda: clic("eliminarcancion"))
    menu_cancion.add_command(image=imagenmodcancion, command=lambda: clic("modificarcancion"))

    imagen_menuprincipal3 = tk.PhotoImage(file=menuprincipalalbumes).subsample(tamaño)
    menu_principal3 = tk.Menu(ventana, tearoff=0)
    menu_principal3.add_cascade(label="Álbum", menu=menu_album, image=imagen_menualbum, compound="left")
    menu_principal3.add_cascade(label="Canción", menu=menu_cancion, image=imagen_menucancion, compound="left")

    boton_imagen_principal3 = tk.Label(ventana, image=imagen_menuprincipal3, bg=color)
    boton_imagen_principal3.bind("<Button-1>", lambda event: mostrar_menu(event, menu_principal3))
    boton_imagen_principal3.place(x=336, y=115)

    #Imagen Facturacion#############################################
    imagen_menufacturacion = tk.PhotoImage(file=menuprincipalfacturas).subsample(tamaño) ####

    insertar_facturacion = tk.Label(ventana, text="Pagos", bg=color, fg=color2, font=fuenteg)
    insertar_facturacion.place(x=527, y=75)

    imageninsfacturacion = tk.PhotoImage(file=menuprincipalgenerar).subsample(tamaño) ###
    imagenbusfacturacion = tk.PhotoImage(file=menuprincipalpagar).subsample(tamaño) ###

    menu_facturacion = tk.Menu(ventana, tearoff=0)
    menu_facturacion.add_command(image=imageninsfacturacion, command=lambda: clic("generarfactura"))
    menu_facturacion.add_command(image=imagenbusfacturacion, command=lambda: clic("pagodecuenta"))

    imagen_menudescuentos = tk.PhotoImage(file=menuprincipaldescuentos).subsample(tamaño) #### 

    imagen_menuprincipal4 = tk.PhotoImage(file=menuprincipalfacturas).subsample(tamaño)
    menu_principal4 = tk.Menu(ventana, tearoff=0)
    menu_principal4.add_cascade(label="Facturación", menu=menu_facturacion, image=imagen_menufacturacion, compound="left")
    menu_principal4.add_cascade(label="Descuentos", image=imagen_menudescuentos, compound="left", command=lambda: clic("descuentos"))

    boton_imagen_principal4 = tk.Label(ventana, image=imagen_menuprincipal4, bg=color)
    boton_imagen_principal4.bind("<Button-1>", lambda event: mostrar_menu(event, menu_principal4))
    boton_imagen_principal4.place(x=476, y=115)

    ###############################################IMAGEN REPRODUCTOR###################################################
    global lista_canciones
    imagen_cargar = tk.PhotoImage(file=menuprincipalreproduccion).subsample(tamaño*2)
    imagen_play = tk.PhotoImage(file=play_btn_file).subsample(tamaño*2)
    imagen_pause = tk.PhotoImage(file=pause_btn_file).subsample(tamaño*2)
    imagen_next = tk.PhotoImage(file=next_btn_file).subsample(tamaño*2)
    imagen_previous = tk.PhotoImage(file=prev_btn_file).subsample(tamaño*2)
    imagen_menu_cargar_canciones = tk.PhotoImage(file=cargar_file).subsample(tamaño*2)

    # Crear menú para las funciones de música
    menu_musica = tk.Menu(ventana, tearoff=0)
    menu_musica.add_command(image=imagen_play, command=lambda: clic("reproduccirmusica"))
    menu_musica.add_command(image=imagen_pause, command=lambda: clic("pausarmusica"))
    menu_musica.add_command(image=imagen_next, command=lambda: clic("siguientemusica"))
    menu_musica.add_command(image=imagen_previous, command=lambda: clic("anteriormusica"))

    # Etiqueta y menú para cargar música
    imagen_menu_cargar = tk.PhotoImage(file=menuprincipalreproduccion).subsample(tamaño)
    menu_principal25 = tk.Menu(ventana, tearoff=0)
    menu_principal25.add_cascade(label="Reproducción", menu=menu_musica, image=imagen_menu_cargar, compound="left", command=lambda: clic("reproduccion"))
    menu_principal25.add_cascade(label="Cargar Canciones", image=imagen_menu_cargar_canciones, compound="left", command=lambda: clic("cargarmusica"))

    insertar_reproductorizo = tk.Label(ventana, text="Reproductor", bg=color, fg=color2, font=fuenteg)
    insertar_reproductorizo.place(x=640, y=75)
    
    # Etiqueta para el botón principal de carga de música
    boton_imagen_cargar = tk.Label(ventana, image=imagen_menu_cargar, bg=color)
    boton_imagen_cargar.bind("<Button-1>", lambda event: mostrar_menu(event, menu_principal25))
    boton_imagen_cargar.place(x=617, y=120)

    # Posicionar los botones en la ventana usando place con un pequeño espacio entre ellos
    button_y = 330  # Coordenada Y fija para todos los botones
    button_x = 200  # Coordenada X inicial

    # Espacio entre botones
    spacing = 100

    # Crear etiquetas para botones de control de música y asignar sus respectivas imágenes
    etiqueta_previous_btn = tk.Label(ventana, image=imagen_previous, bg=color)
    etiqueta_previous_btn.bind("<Button-1>", lambda event: clic("anteriormusica"))
    

    etiqueta_play_btn = tk.Label(ventana, image=imagen_play, bg=color)
    etiqueta_play_btn.bind("<Button-1>", lambda event: clic("reproduccirmusica"))
  

    etiqueta_pause_btn = tk.Label(ventana, image=imagen_pause, bg=color)
    etiqueta_pause_btn.bind("<Button-1>", lambda event: clic("pausarmusica"))
 

    etiqueta_next_btn = tk.Label(ventana, image=imagen_next, bg=color)
    etiqueta_next_btn.bind("<Button-1>", lambda event: clic("siguientemusica"))




    ##################################################################################################


    # Submenú de inserción
    menu_mantenimiento = tk.Menu(barra_herramientas, tearoff=0, bg=color, fg=color2, activebackground='grey', font=fuente)
    barra_herramientas.add_cascade(label="Mantenimiento", menu=menu_mantenimiento)

    # Submenú de inserción
    menu_insercion = tk.Menu(menu_mantenimiento, tearoff=0, bg=color, fg=color2, activebackground='grey', font=fuente)
    menu_insercion.add_command(label="Insertar Propietario", command=insertar_propietario)
    menu_insercion.add_command(label="Insertar Playlist de un Propietario", command=insertar_playlist)
    menu_insercion.add_command(label="Insertar Genero", command=insertar_genero)
    menu_insercion.add_command(label="Insertar Artista", command=insertar_artista)
    menu_insercion.add_command(label="Insertar Album", command=insertar_elalbum)
    menu_insercion.add_command(label="Insertar Canción", command=insertar_canciones)
    menu_insercion.add_command(label="Insertar Administrador", command=insertar_administradores)
    menu_mantenimiento.add_cascade(label="Inserción", menu=menu_insercion)

    # Submenú de búsqueda
    menu_busqueda = tk.Menu(menu_mantenimiento, tearoff=0, bg=color, fg=color2, activebackground='grey', font=fuente)
    menu_busqueda.add_command(label="Buscar Propietario", command=buscar_propietario)
    menu_busqueda.add_command(label="Buscar Playlist de un Propietario", command=buscar_playlist)
    menu_busqueda.add_command(label="Buscar Genero", command=buscar_genero)
    menu_busqueda.add_command(label="Buscar Artista", command=buscar_artista)
    menu_busqueda.add_command(label="Buscar Album", command=buscar_album)
    menu_busqueda.add_command(label="Buscar Canción", command=buscar_cancion)
    menu_busqueda.add_command(label="Buscar Administrador", command=buscar_admin)
    menu_mantenimiento.add_cascade(label="Búsqueda", menu=menu_busqueda)

    # Submenú de eliminación
    menu_eliminacion = tk.Menu(menu_mantenimiento, tearoff=0, bg=color, fg=color2, activebackground='grey', font=fuente)
    menu_eliminacion.add_command(label="Eliminar Propietario", command=eliminar_propietario)
    menu_eliminacion.add_command(label="Eliminar Playlist de un Propietario", command=eliminar_playlist)
    menu_eliminacion.add_command(label="Eliminar Genero", command=eliminar_genero)
    menu_eliminacion.add_command(label="Eliminar Artista", command=eliminar_artista)
    menu_eliminacion.add_command(label="Eliminar Album", command=eliminar_album)
    menu_eliminacion.add_command(label="Eliminar Canción", command=eliminar_cancion)
    menu_eliminacion.add_command(label="Eliminar Administrador", command=eliminar_admin)
    menu_mantenimiento.add_cascade(label="Eliminación", menu=menu_eliminacion)

    # Submenú de modificación
    menu_modificacion = tk.Menu(menu_mantenimiento, tearoff=0, bg=color, fg=color2, activebackground='grey', font=fuente)
    menu_modificacion.add_command(label="Cambiar Nombre de Propietario", command=modificar_propietario)
    menu_modificacion.add_command(label="Cambiar Nombre de Playlist de un Propietario", command=modificar_playlist)
    menu_modificacion.add_command(label="Cambiar Nombre de Genero", command=modificar_genero)
    menu_modificacion.add_command(label="Cambiar Nombre de un Artista de un Genero", command=modificar_artista)
    menu_modificacion.add_command(label="Cambiar Nombre de un Albúm", command=modificar_album)
    menu_modificacion.add_command(label="Cambiar Nombre de una Canción", command=modificar_cancion)
    menu_modificacion.add_command(label="Cambiar Nombre de un Administrador", command=modificar_admin)
    menu_mantenimiento.add_cascade(label="Modificación", menu=menu_modificacion)
 
    
    # Submenú de reproduccion
    menu_reproduccion = tk.Menu(barra_herramientas, tearoff=0, bg=color, fg=color2, activebackground='grey', font=fuente)
    menu_reproduccion.add_command(label="Reproducir Canción", command=reproduccion)
    menu_reproduccion.add_command(label="Cola de Reproducción", command=coladereproduccion_comando)
    barra_herramientas.add_cascade(label="Reproducción", menu=menu_reproduccion)
    
    # Submenú de reportes
    menu_reportes = tk.Menu(barra_herramientas, tearoff=0, bg=color, fg=color2, activebackground='grey', font=fuente)
    menu_reportes.add_command(label="Reporte de Listas de Propietarios", command=reporte_propietarios)
    menu_reportes.add_command(label="Reporte de Playlists de Propietario", command=reporte_playlists)
    menu_reportes.add_command(label="Reporte de Genero", command=reporte_generos)
    menu_reportes.add_command(label="Reporte de Artistas de un Genero", command=reporte_artistas)
    menu_reportes.add_command(label="Reporte de Albums de un Artista", command=reporte_albumes)
    menu_reportes.add_command(label="Reporte de Canciones de un Artista de un Genero", command=reporte_canciones)
    menu_reportes.add_command(label="Reporte de Canción más reproducida", command=reporte_cancion_mas_reproducida) 
    menu_reportes.add_command(label="Reporte de Artista con más Canciones", command=reporte_artista_mayor_canciones) 
    menu_reportes.add_command(label="Reporte de Album con más Canciones", command=reporte_album_mayor_canciones)
    menu_reportes.add_command(label="Reporte de Genero más solicitado", command=reporte_genero_mas_solicitado)
    menu_reportes.add_command(label="Reporte de Propietario con más Playlists", command=reporte_propietario_mayor_playlist) 
    menu_reportes.add_command(label="Reporte de Album más solicitado", command=reporte_album_mas_solicitado)
    menu_reportes.add_command(label="Reporte de Playlist con más Canciones", command=reporte_playlist_mayor_canciones) 
    menu_reportes.add_command(label="Reporte de Genero con más Artistas", command=reporte_genero_mayor_artistas) 
    menu_reportes.add_command(label="Reporte de Genero con más Albumes", command=reporte_genero_mayor_albumes) 
    menu_reportes.add_command(label="Reporte de Artista con más Albumes", command=reporte_artista_mayor_albumes) 
    menu_reportes.add_command(label="Reporte de Album nunca buscado", command=reporte_albumes_nunca_buscados)
    menu_reportes.add_command(label="Reporte de Artista nunca buscado", command=reporte_artistas_nunca_buscados)
    menu_reportes.add_command(label="Reporte de Propietario sin Playlist", command=reporte_propietarios_sin_playlist)
    menu_reportes.add_command(label="Reporte de Canciones nunca reproducidas", command=reporte_canciones_nunca_reproducidas)
    barra_herramientas.add_cascade(label="Reportes", menu=menu_reportes)
    

    # Submenú de PAGOS
    menu_facturacion = tk.Menu(barra_herramientas, tearoff=0, bg=color, fg=color2, activebackground='grey', font=fuente)
    generar = menu_facturacion.add_command(label="Generar", command=generarfacturasadmin)
    menu_facturacion.add_command(label="Pagar", command=pagodefacturasvencidas)
    descuentos = menu_facturacion.add_command(label="Descuentos", command=descuentos_comando)
    barra_herramientas.add_cascade(label="Facturación", menu=menu_facturacion)
    
    #acerca de
    barra_herramientas.add_command(label="Acerca de", command=sobrenosotros)

    #contacto
    barra_herramientas.add_cascade(label="Contacto", command=contacto)

    #DESACTIVAR
    if bandera == 0: #####################Esto funciona para desabilitar opciones si no es administrador
        menu_insercion.entryconfig("Insertar Propietario", state='disabled')
        menu_insercion.entryconfig("Insertar Playlist de un Propietario", state='disabled')
        menu_insercion.entryconfig("Insertar Genero", state='disabled')
        menu_insercion.entryconfig("Insertar Artista", state='disabled')
        menu_insercion.entryconfig("Insertar Album", state='disabled')
        menu_insercion.entryconfig("Insertar Canción", state='disabled')
        menu_insercion.entryconfig("Insertar Administrador", state='disabled')
        menu_busqueda.entryconfig("Buscar Administrador", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Propietario", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Playlist de un Propietario", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Genero", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Artista", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Album", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Canción", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Administrador", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de Propietario", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de Playlist de un Propietario", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de Genero", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de un Artista de un Genero", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de un Albúm", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de una Canción", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de un Administrador", state='disabled')
        menu_facturacion.entryconfig("Generar", state='disabled')
        menu_facturacion.entryconfig("Descuentos", state='disabled')
        menu_reportes.entryconfig("Reporte de Listas de Propietarios", state='disabled')
        menu_reportes.entryconfig("Reporte de Playlists de Propietario", state='disabled')
        menu_reportes.entryconfig("Reporte de Genero", state='disabled')
        menu_reportes.entryconfig("Reporte de Artistas de un Genero", state='disabled')
        menu_reportes.entryconfig("Reporte de Albums de un Artista", state='disabled')
        menu_reportes.entryconfig("Reporte de Canciones de un Artista de un Genero", state='disabled')
        menu_reportes.entryconfig("Reporte de Canción más reproducida", state='disabled')
        menu_reportes.entryconfig("Reporte de Artista con más Canciones", state='disabled')
        menu_reportes.entryconfig("Reporte de Album con más Canciones", state='disabled')
        menu_reportes.entryconfig("Reporte de Genero más solicitado", state='disabled')
        menu_reportes.entryconfig("Reporte de Propietario con más Playlists", state='disabled')
        menu_reportes.entryconfig("Reporte de Album más solicitado", state='disabled')
        menu_reportes.entryconfig("Reporte de Playlist con más Canciones", state='disabled')
        menu_reportes.entryconfig("Reporte de Genero con más Artistas", state='disabled')
        menu_reportes.entryconfig("Reporte de Genero con más Albumes", state='disabled')
        menu_reportes.entryconfig("Reporte de Artista con más Albumes", state='disabled')
        menu_reportes.entryconfig("Reporte de Album nunca buscado", state='disabled')
        menu_reportes.entryconfig("Reporte de Artista nunca buscado", state='disabled')
        menu_reportes.entryconfig("Reporte de Propietario sin Playlist", state='disabled')
        menu_reportes.entryconfig("Reporte de Canciones nunca reproducidas", state='disabled')  
    if bandera == 10:
        menu_insercion.entryconfig("Insertar Propietario", state='disabled')
        menu_insercion.entryconfig("Insertar Playlist de un Propietario", state='disabled')
        menu_insercion.entryconfig("Insertar Genero", state='disabled')
        menu_insercion.entryconfig("Insertar Artista", state='disabled')
        menu_insercion.entryconfig("Insertar Album", state='disabled')
        menu_insercion.entryconfig("Insertar Canción", state='disabled')
        menu_insercion.entryconfig("Insertar Administrador", state='disabled')
        menu_busqueda.entryconfig("Buscar Propietario", state='disabled')
        menu_busqueda.entryconfig("Buscar Playlist de un Propietario", state='disabled')
        menu_busqueda.entryconfig("Buscar Genero", state='disabled')
        menu_busqueda.entryconfig("Buscar Artista", state='disabled')
        menu_busqueda.entryconfig("Buscar Album", state='disabled')
        menu_busqueda.entryconfig("Buscar Canción", state='disabled')     
        menu_busqueda.entryconfig("Buscar Administrador", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Propietario", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Playlist de un Propietario", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Genero", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Artista", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Album", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Canción", state='disabled')
        menu_eliminacion.entryconfig("Eliminar Administrador", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de Propietario", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de Playlist de un Propietario", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de Genero", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de un Artista de un Genero", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de un Albúm", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de una Canción", state='disabled')
        menu_modificacion.entryconfig("Cambiar Nombre de un Administrador", state='disabled')
        menu_facturacion.entryconfig("Generar", state='disabled')
        menu_facturacion.entryconfig("Descuentos", state='disabled')
        menu_reproduccion.entryconfig("Reproducir Canción", state='disabled')
        menu_reproduccion.entryconfig("Cola de Reproducción", state='disabled')
        barra_herramientas.entryconfig("Acerca de", state='disabled')
        barra_herramientas.entryconfig("Contacto", state='disabled')
        menu_reportes.entryconfig("Reporte de Listas de Propietarios", state='disabled')
        menu_reportes.entryconfig("Reporte de Playlists de Propietario", state='disabled')
        menu_reportes.entryconfig("Reporte de Genero", state='disabled')
        menu_reportes.entryconfig("Reporte de Artistas de un Genero", state='disabled')
        menu_reportes.entryconfig("Reporte de Albums de un Artista", state='disabled')
        menu_reportes.entryconfig("Reporte de Canciones de un Artista de un Genero", state='disabled')
        menu_reportes.entryconfig("Reporte de Canción más reproducida", state='disabled')
        menu_reportes.entryconfig("Reporte de Artista con más Canciones", state='disabled')
        menu_reportes.entryconfig("Reporte de Album con más Canciones", state='disabled')
        menu_reportes.entryconfig("Reporte de Genero más solicitado", state='disabled')
        menu_reportes.entryconfig("Reporte de Propietario con más Playlists", state='disabled')
        menu_reportes.entryconfig("Reporte de Album más solicitado", state='disabled')
        menu_reportes.entryconfig("Reporte de Playlist con más Canciones", state='disabled')
        menu_reportes.entryconfig("Reporte de Genero con más Artistas", state='disabled')
        menu_reportes.entryconfig("Reporte de Genero con más Albumes", state='disabled')
        menu_reportes.entryconfig("Reporte de Artista con más Albumes", state='disabled')
        menu_reportes.entryconfig("Reporte de Album nunca buscado", state='disabled')
        menu_reportes.entryconfig("Reporte de Artista nunca buscado", state='disabled')
        menu_reportes.entryconfig("Reporte de Propietario sin Playlist", state='disabled')
        menu_reportes.entryconfig("Reporte de Canciones nunca reproducidas", state='disabled')        
        

    #Bucle principal
    ventana.mainloop()
####################################################################################################################
#######################################################INSERCION######################################################
####################################################################################################################
#######################################################INSERTAR PROPIETARIO##############################################
def comprobacionpropietario(activar, nombre, codpropietario, codmembresia, insertarpropietario):
    bandera = False
    bandera1 = False
    try:
        codpropietario = int(codpropietario)
        bandera = True
    except ValueError:
        pass
    try:
        codmembresia = int(codmembresia)
        bandera1 = True
    except ValueError:
        pass
    if bandera and bandera1:
        revisionrepetidopro(activar, nombre, codpropietario, codmembresia, insertarpropietario)
    else:
        messagebox.showerror("Error", "Los códigos deben ser números enteros. Intenta de nuevo.")
def revisionrepetidopro(activar, nombre, codpropietario, codmembresia, insertarpropietario):
    codpropietario = str(codpropietario)
    codmembresia = str(codmembresia)  
    membresia_en_uso=False
    propietario_en_uso=False
    for clave in dicpropietarios:
        if dicpropietarios[clave]['codmembresia']==codmembresia:
            membresia_en_uso = True
            break
    if codpropietario in dicpropietarios:
        propietario_en_uso=True
    if membresia_en_uso and propietario_en_uso:
        messagebox.showerror("Error", "Los códigos ya existen. Intenta de nuevo.")
    elif membresia_en_uso and not propietario_en_uso:
        messagebox.showerror("Error", "La membresia ya existe. Intenta de nuevo.")
    elif not membresia_en_uso and propietario_en_uso:
        messagebox.showerror("Error", "El propietario ya existe. Intenta de nuevo.")
    elif not membresia_en_uso and not propietario_en_uso:
        inserciondepropietario(activar, nombre, codpropietario, codmembresia, insertarpropietario)
def inserciondepropietario(activar, nombre, codpropietario, codmembresia, ventana):
    if activar=="No Activar":  
        dicpropietarios[codpropietario] = {'nombrepro': nombre, 'codmembresia': codmembresia, 'activo': '0'}
        ventana.destroy()
        messagebox.showinfo("Cuenta Creada", "Cuenta Creada con éxito, No fue activada.")
    if activar=="Activar":
        dicpropietarios[codpropietario] = {'nombrepro': nombre, 'codmembresia': codmembresia, 'activo': '1'}
        nombre_archivo = f"{codpropietario}.txt"
        if not os.path.exists("Cobros"):
            os.makedirs("Cobros")
        rutadecobro = os.path.join("Cobros", nombre_archivo)
        facturas[codpropietario]={'nombre': nombre, 'codmembresia': codmembresia, 'costo: $': costoinsercion()}
        with open(rutadecobro, "a") as file:
            file.write("-------------------------------------------------------------------------------------------------------------\n")
            file.write( "|Usuario: {nombre} | Codpropietario: {codpropietario} |Costo: ${costoinsercion()}|\n")
            file.write("-------------------------------------------------------------------------------------------------------------\n")
        ventana.destroy()
        messagebox.showinfo("Cuenta Creada", f"Cuenta Creada con éxito, Se realizó un cobro de ${costoinsercion()} y se registró en Cobro.txt.")
def revisionrepetido(activar, nombre, codpropietario, codmembresia):
    codpropietario = str(codpropietario)
    codmembresia = str(codmembresia)  
    membresia_en_uso=False
    propietario_en_uso=False
    for clave in dicpropietarios:
        if dicpropietarios[clave]['codmembresia']==codmembresia:
            membresia_en_uso = True
            break
    if codpropietario in dicpropietarios:
        propietario_en_uso=True
    if membresia_en_uso and propietario_en_uso:
        messagebox.showerror("Error", "Los códigos ya existen. Intenta de nuevo.")
    elif membresia_en_uso and not propietario_en_uso:
        messagebox.showerror("Error", "El codmembresia ya existe. Intenta de nuevo.")
    elif not membresia_en_uso and propietario_en_uso:
        messagebox.showerror("Error", "El codpropietario ya existe. Intenta de nuevo.")
    elif not membresia_en_uso and not propietario_en_uso:
        inserciondepropietario(activar, nombre, codpropietario, codmembresia)
def insertar_propietario():
        insertarpropietario = tk.Toplevel()
        insertarpropietario.title("Inserción de Propietario")
        insertarpropietario.geometry("800x625")
        insertarpropietario.resizable(False, False)
        insertarpropietario.configure(bg=color)

        fuente = ("Console", 12)
        fuenteg = ("Console", 16)
        activar = StringVar(value="No Activar")
        input2 = tk.Label(insertarpropietario, text="Insertar Propietario" , bg=color , fg=color2, font=fuenteg)
        input_usuario = tk.Label(insertarpropietario, text="Nombre" , bg=color , fg=color2, font=fuente)
        nombre = tk.Entry(insertarpropietario, fg=color, bg=color2, font=fuente)
        input_codpropietario = tk.Label(insertarpropietario, text="Codpropietario" , bg=color , fg=color2, font=fuente)
        codpropietario = tk.Entry(insertarpropietario, fg=color, bg=color2, font=fuente)        
        input_codmembresia = tk.Label(insertarpropietario, text="Codmembresia" , bg=color , fg=color2, font=fuente)
        codmembresia = tk.Entry(insertarpropietario, fg=color, bg=color2, font=fuente)

        input2.pack(pady=(10))
        input_usuario.pack(pady=(10))
        nombre.pack(pady=(10))
        input_codpropietario.pack(pady=(10))
        codpropietario.pack(pady=(10))        
        input_codmembresia.pack(pady=(10))
        codmembresia.pack(pady=(10))    
        sobretexto2 = Label(insertarpropietario, text="¿Deseas Activarla?", bg=color, fg=color2, font=fuente)
        sobretexto3 = Label(insertarpropietario, text=f"Se te cobrará ${costoinsercion()} anuales", bg=color, fg=color2, font=fuente)

        
        sobretexto2.pack(pady=(50, 10))
        sobretexto3.pack(pady=10)

        radio_usuario = Radiobutton(insertarpropietario, text="Activar", variable=activar, value="Activar", bg=color, fg=color2, font=fuente, selectcolor=color)
        radio_admin = Radiobutton(insertarpropietario, text="No Activar", variable=activar, value="No Activar", bg=color, fg=color2, font=fuente, selectcolor=color)

        radio_usuario.pack(pady=10)
        radio_admin.pack(pady=10)

        boton_login = Button(insertarpropietario, text="Aceptar", command=lambda: comprobacionpropietario(activar.get(), nombre.get(), codpropietario.get(), codmembresia.get(), insertarpropietario), bg=color, fg=color2, font=fuente)

        boton_login.pack(pady=30)

        insertarpropietario.mainloop()
#######################################################INSERTAR PLAYLIST#################################################
def comprobacionplaylist(nombre, codplaylist, codpropietario, insertarplaylist):
    bandera = False
    bandera1 = False
    try:
        codpropietario = int(codpropietario)
        bandera = True
    except ValueError:
        pass
    try:
        codplaylist = int(codplaylist)
        bandera1 = True
    except ValueError:
        pass
    if bandera and bandera1:
        revisionrepetido2(nombre, codplaylist, codpropietario, insertarplaylist)
    else:
        messagebox.showerror("Error", "Los códigos deben ser números enteros. Intenta de nuevo.")
def revisionrepetido2(nombre, codplaylist, codpropietario, insertarplaylist):
    codpropietario = str(codpropietario)
    codplaylist = str(codplaylist)  
    playlist_en_uso=False
    propietario_en_uso=False
    if codpropietario in dicpropietarios:
        propietario_en_uso=True
    if codplaylist in dicplaylist:
        playlist_en_uso=True
    if playlist_en_uso and propietario_en_uso:
        messagebox.showerror("Error", "El codplaylist ya existe. Intenta de nuevo.")
    elif playlist_en_uso and not propietario_en_uso:
        messagebox.showerror("Error", "El codplaylist ya existe y no existe el codpropietario. Intenta de nuevo.")
    elif not playlist_en_uso and not propietario_en_uso:
        messagebox.showerror("Error", "El codpropietario no existe. Intenta de nuevo.")
    elif not playlist_en_uso and propietario_en_uso:
        inserciondeplaylist(nombre, codplaylist, codpropietario, insertarplaylist)
def inserciondeplaylist(nombre, codplaylist, codpropietario, ventana):
        dicplaylist[codplaylist] = {'nombreplay': nombre, 'codpropietario': codpropietario}
        ventana.destroy()
        messagebox.showinfo("Playlist Creada", "'Playlist Creada con éxito")
def insertar_playlist():
        insertarplaylist = tk.Toplevel()
        insertarplaylist.title("Inserción de Playlist")
        insertarplaylist.geometry("800x625")
        insertarplaylist.resizable(False, False)
        insertarplaylist.configure(bg=color)

        fuente = ("Console", 14)
        fuenteg = ("Console", 18)
        input2 = tk.Label(insertarplaylist, text="Insertar Playlist" , bg=color , fg=color2, font=fuenteg)
        input_usuario = tk.Label(insertarplaylist, text="Nombre" , bg=color , fg=color2, font=fuente)
        nombre = tk.Entry(insertarplaylist, fg=color, bg=color2, font=fuente)
        input_codpropietario = tk.Label(insertarplaylist, text="Codplaylist" , bg=color , fg=color2, font=fuente)
        codplaylist = tk.Entry(insertarplaylist, fg=color, bg=color2, font=fuente)        
        input_codmembresia = tk.Label(insertarplaylist, text="Codpropietario" , bg=color , fg=color2, font=fuente)
        codpropietario = tk.Entry(insertarplaylist, fg=color, bg=color2, font=fuente)

        input2.pack(pady=(10))        
        input_usuario.pack(pady=(10))
        nombre.pack(pady=(10))
        input_codpropietario.pack(pady=(10))
        codplaylist.pack(pady=(10))        
        input_codmembresia.pack(pady=(10))
        codpropietario.pack(pady=(10))


        boton_login = Button(insertarplaylist, text="Aceptar", command=lambda: comprobacionplaylist(nombre.get(), codplaylist.get(), codpropietario.get(), insertarplaylist), bg=color, fg=color2, font=fuente)

        boton_login.pack(pady=30)

        insertarplaylist.mainloop()
#######################################################INSERTAR GENERO#################################################
def inserciondegenero(nombre, codgenero,ventana):
        dicgenero[codgenero] = {'nombregen': nombre}
        ventana.destroy()
        messagebox.showinfo("Genero Creado", "'Genero Creado con éxito")
def revisionrepetido3(nombre, codgenero,insertargenero):
    codgenero = str(codgenero)
    genero_en_uso=False
    if codgenero in dicgenero:
        genero_en_uso=True
    if genero_en_uso:
        messagebox.showerror("Error", "El codgenero ya existe. Intenta de nuevo.")
    elif not genero_en_uso:
        inserciondegenero(nombre, codgenero,insertargenero)
def comprobaciongenero(nombre, codgenero,insertargenero):
    bandera = False
    try:
        codgenero = int(codgenero)
        bandera = True
    except ValueError:
        pass
    if bandera:
        revisionrepetido3(nombre, codgenero,insertargenero)
    if not bandera:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
def insertar_genero():
        insertargenero = tk.Toplevel()
        insertargenero.title("Inserción de Genero")
        insertargenero.geometry("800x625")
        insertargenero.resizable(False, False)
        insertargenero.configure(bg=color)

        fuente = ("Console", 14)
        fuenteg = ("Console", 18)
        input2 = tk.Label(insertargenero, text="Insertar Genero" , bg=color , fg=color2, font=fuenteg)
        input_usuario = tk.Label(insertargenero, text="Nombre" , bg=color , fg=color2, font=fuente)
        nombre = tk.Entry(insertargenero, fg=color, bg=color2, font=fuente)
        input_codmembresia = tk.Label(insertargenero, text="Codgenero" , bg=color , fg=color2, font=fuente)
        codgenero = tk.Entry(insertargenero, fg=color, bg=color2, font=fuente)

        input2.pack(pady=(10))        
        input_usuario.pack(pady=(10))
        nombre.pack(pady=(10))
        input_codmembresia.pack(pady=(10))
        codgenero.pack(pady=(10))


        boton_login = Button(insertargenero, text="Aceptar", command=lambda: comprobaciongenero(nombre.get(), codgenero.get(),insertargenero), bg=color, fg=color2, font=fuente)

        boton_login.pack(pady=30)

        insertargenero.mainloop()
#######################################################INSERTAR ARTISTA#################################################
def comprobacionartista(nombre, codartista, codgenero,insertarartista):
    bandera = False
    bandera1 = False
    try:
        codartista = int(codartista)
        bandera = True
    except ValueError:
        pass
    try:
        codgenero = int(codgenero)
        bandera1 = True
    except ValueError:
        pass
    if bandera and bandera1:
        revisionrepetido4(nombre, codartista, codgenero,insertarartista)
    else:
        messagebox.showerror("Error", "Los códigos deben ser números enteros. Intenta de nuevo.")
def revisionrepetido4(nombre, codartista, codgenero,insertarartista):
    codartista = str(codartista)
    codgenero = str(codgenero)  
    artista_en_uso=False
    genero_en_uso=False
    if codartista in dicartista:
        artista_en_uso=True
    if codgenero in dicgenero:
        genero_en_uso=True
    if artista_en_uso and genero_en_uso:
        messagebox.showerror("Error", "El codartista ya existe. Intenta de nuevo.")
    elif artista_en_uso and not genero_en_uso:
        messagebox.showerror("Error", "El codartista ya existe y no existe el codgenero. Intenta de nuevo.")
    elif not artista_en_uso and not genero_en_uso:
        messagebox.showerror("Error", "El codgenero no existe. Intenta de nuevo.")
    elif not artista_en_uso and genero_en_uso:
        inserciondeartista(nombre, codartista, codgenero,insertarartista)
def inserciondeartista(nombre, codartista, codgenero, ventana):
        dicartista[codartista] = {'nombreart': nombre, 'codgenero': codgenero}
        ventana.destroy()
        messagebox.showinfo("Artista Creada", "'Artista Creada con éxito")        
def insertar_artista():
        insertarartista = tk.Toplevel()
        insertarartista.title("Inserción de Artista")
        insertarartista.geometry("800x625")
        insertarartista.resizable(False, False)
        insertarartista.configure(bg=color)

        fuente = ("Console", 14)
        fuenteg = ("Console", 18)
        input2 = tk.Label(insertarartista, text="Insertar Artista" , bg=color , fg=color2, font=fuenteg)
        input_usuario = tk.Label(insertarartista, text="Nombre" , bg=color , fg=color2, font=fuente)
        nombre = tk.Entry(insertarartista, fg=color, bg=color2, font=fuente)
        input_codmembresia = tk.Label(insertarartista, text="Codartista" , bg=color , fg=color2, font=fuente)
        codartista = tk.Entry(insertarartista, fg=color, bg=color2, font=fuente)
        input_codmembresia2 = tk.Label(insertarartista, text="Codgenero" , bg=color , fg=color2, font=fuente)
        codgenero = tk.Entry(insertarartista, fg=color, bg=color2, font=fuente)
        

        input2.pack(pady=(10))        
        input_usuario.pack(pady=(10))
        nombre.pack(pady=(10))
        input_codmembresia.pack(pady=(10))
        codartista.pack(pady=(10))
        input_codmembresia2.pack(pady=(10))
        codgenero.pack(pady=(10))


        boton_login = Button(insertarartista, text="Aceptar", command=lambda: comprobacionartista(nombre.get(), codartista.get(),codgenero.get(),insertarartista), bg=color, fg=color2, font=fuente)

        boton_login.pack(pady=30)

        insertarartista.mainloop()
#######################################################INSERTAR ALBUM##################################################
def comprobacionalbum(nombre, codalbum, codartista,insertaralbum):
    bandera = False
    bandera1 = False
    try:
        codartista = int(codartista)
        bandera = True
    except ValueError:
        pass
    try:
        codalbum = int(codalbum)
        bandera1 = True
    except ValueError:
        pass
    if bandera and bandera1:
        revisionrepetido5(nombre, codalbum, codartista,insertaralbum)
    else:
        messagebox.showerror("Error", "Los códigos deben ser números enteros. Intenta de nuevo.")
def revisionrepetido5(nombre, codalbum, codartista,insertaralbum):
    codartista = str(codartista)
    codalbum = str(codalbum)  
    artista_en_uso=False
    genero_en_uso=False
    if codartista in dicartista:
        artista_en_uso=True
    if codalbum in dicalbum:
        genero_en_uso=True
    if artista_en_uso and genero_en_uso:
        messagebox.showerror("Error", "El codalbum ya existe. Intenta de nuevo.")
    elif not artista_en_uso and genero_en_uso:
        messagebox.showerror("Error", "El codalbum ya existe y no existe el codartista. Intenta de nuevo.")
    elif not artista_en_uso and not genero_en_uso:
        messagebox.showerror("Error", "El codartista no existe. Intenta de nuevo.")
    elif artista_en_uso and not genero_en_uso:
        inserciondealbum(nombre, codalbum, codartista,insertaralbum)
def inserciondealbum(nombre, codalbum, codartista,ventana):
        dicalbum[codalbum] = {'nombrealbum': nombre, 'codart': codartista}
        ventana.destroy() 
        messagebox.showinfo("Album Creada", "'Album Creada con éxito")        
def insertar_elalbum():
        insertaralbum = tk.Toplevel()
        insertaralbum.title("Inserción de Albúm")
        insertaralbum.geometry("800x625")
        insertaralbum.resizable(False, False)
        insertaralbum.configure(bg=color)

        fuente = ("Console", 14)
        fuenteg = ("Console", 18)
        input2 = tk.Label(insertaralbum, text="Insertar Albúm" , bg=color , fg=color2, font=fuenteg)
        input_usuario = tk.Label(insertaralbum, text="Nombre" , bg=color , fg=color2, font=fuente)
        nombre = tk.Entry(insertaralbum, fg=color, bg=color2, font=fuente)
        input_codmembresia = tk.Label(insertaralbum, text="Codalbum" , bg=color , fg=color2, font=fuente)
        codalbum = tk.Entry(insertaralbum, fg=color, bg=color2, font=fuente)
        input_codmembresia2 = tk.Label(insertaralbum, text="Codartista" , bg=color , fg=color2, font=fuente)
        codartista = tk.Entry(insertaralbum, fg=color, bg=color2, font=fuente)
        

        input2.pack(pady=(10))        
        input_usuario.pack(pady=(10))
        nombre.pack(pady=(10))
        input_codmembresia.pack(pady=(10))
        codalbum.pack(pady=(10))
        input_codmembresia2.pack(pady=(10))
        codartista.pack(pady=(10))


        boton_login = Button(insertaralbum, text="Aceptar", command=lambda: comprobacionalbum(nombre.get(), codalbum.get(),codartista.get(),insertaralbum), bg=color, fg=color2, font=fuente)

        boton_login.pack(pady=30)

        insertaralbum.mainloop()
#######################################################INSERTAR CANCIONES###############################################
def inserciondecanciones(nombre, codcancion, codartista, codalbum, codplaylist, codgenero, ventana):
    diccanciones[codcancion] = {'nombrecan': nombre,'codart': codartista,'codalbum': codalbum,'codgenero': codgenero,'codplaylist': codplaylist}
    ventana.destroy() 
    messagebox.showinfo("Canción Creada", "Canción Creada con éxito")
def comprobacioncanciones(nombre, codcancion, codalbum, codartista, codplaylist, ventana):
    try:
        codartista = int(codartista)
        codalbum = int(codalbum)
        codplaylist = int(codplaylist)
        codcancion = int(codcancion)
        revisionrepetido6(nombre, codcancion, codartista, codalbum, codplaylist, ventana)
    except ValueError:
        messagebox.showerror("Error", "Los códigos deben ser números enteros. Intenta de nuevo.")
def revisionrepetido6(nombre, codcancion, codartista, codalbum, codplaylist, ventana):
    codcancion=str(codcancion)
    codartista = str(codartista)
    codalbum = str(codalbum)
    codplaylist= str(codplaylist)
    codcancion_en_uso=False
    artista_en_uso=False
    genero_en_uso=False
    codplaylist_en_uso=False
    coincideartyalbum=False
    if codcancion in diccanciones:
        codcancion_en_uso=True
    if codartista in dicartista:
        artista_en_uso=True
    if codalbum in dicalbum:
        genero_en_uso=True
    if codplaylist in dicplaylist:
        codplaylist_en_uso=True
    if artista_en_uso:
        genero=dicartista[codartista]['codgenero']
    if artista_en_uso and genero_en_uso:
        if dicalbum[codalbum]['codart']==codartista:
            coincideartyalbum=True
    if artista_en_uso and genero_en_uso and codcancion_en_uso and codplaylist_en_uso and coincideartyalbum:
        messagebox.showerror("Error", "El codcancion ya existe. Intenta de nuevo.")
    elif not artista_en_uso and genero_en_uso and codcancion_en_uso and codplaylist_en_uso:
        messagebox.showerror("Error", "El codcancion ya existe y no existe el codartista. Intenta de nuevo.")
    elif artista_en_uso and genero_en_uso and codcancion_en_uso and not codplaylist_en_uso:
        messagebox.showerror("Error", "El codcancion ya existe y no existe el codplaylist. Intenta de nuevo.")
    elif artista_en_uso and not genero_en_uso and codcancion_en_uso and codplaylist_en_uso:
        messagebox.showerror("Error", "El codcancion ya existe y no existe el codalbum. Intenta de nuevo.")        
    elif not artista_en_uso and not genero_en_uso and codcancion_en_uso and codplaylist_en_uso:
        messagebox.showerror("Error", "El codcancion ya existe y codartista y el codalbum no existe. Intenta de nuevo.")
    elif not artista_en_uso and not genero_en_uso and codcancion_en_uso and not codplaylist_en_uso:
        messagebox.showerror("Error", "El codcancion ya existe y codartista, el codalbum y el codplaylist no existe. Intenta de nuevo.")
    elif not artista_en_uso and genero_en_uso and not codcancion_en_uso and codplaylist_en_uso:
        messagebox.showerror("Error", "No existe el codartista. Intenta de nuevo.")
    elif artista_en_uso and not genero_en_uso and not codcancion_en_uso and codplaylist_en_uso:
        messagebox.showerror("Error", "No existe el codalbum. Intenta de nuevo.")
    elif artista_en_uso and genero_en_uso and not codcancion_en_uso and not codplaylist_en_uso:
        messagebox.showerror("Error", "No existe el codplaylist. Intenta de nuevo.")        
    elif not artista_en_uso and not genero_en_uso and codcancion_en_uso and codplaylist_en_uso:
        messagebox.showerror("Error", "El codartista y el codalbum no existe. Intenta de nuevo.")
    elif not artista_en_uso and genero_en_uso and codcancion_en_uso and not codplaylist_en_uso:
        messagebox.showerror("Error", "El codartista y el codplaylist no existe. Intenta de nuevo.")
    elif artista_en_uso and not genero_en_uso and codcancion_en_uso and not codplaylist_en_uso:
        messagebox.showerror("Error", "El codalbum y el codplaylist no existe. Intenta de nuevo.")        
    elif not artista_en_uso and not genero_en_uso and codcancion_en_uso and not codplaylist_en_uso:
        messagebox.showerror("Error", "El codartista, el codalbum y el codplaylist no existe. Intenta de nuevo.")
    elif artista_en_uso and genero_en_uso and not codcancion_en_uso and codplaylist_en_uso and not coincideartyalbum:
        messagebox.showerror("Error", "El codalbum no pertenece a ese codartista. Intenta de nuevo.")
    elif artista_en_uso and genero_en_uso and not codcancion_en_uso and codplaylist_en_uso and coincideartyalbum:
        inserciondecanciones(nombre, codcancion, codartista, codalbum, codplaylist, genero, ventana)
    else:
        messagebox.showerror("Error", "Revisa que los codigos coincidan. Intenta de nuevo.")
def insertar_canciones():
    insertarcancion = tk.Toplevel()
    insertarcancion.title("Inserción de Canción")
    insertarcancion.geometry("800x625")
    insertarcancion.resizable(False, False)
    insertarcancion.configure(bg=color) 

    fuente = ("Consolas", 14)
    fuenteg = ("Consolas", 18)

    input2 = tk.Label(insertarcancion, text="Insertar Canción", bg=color, fg=color2, font=fuenteg)
    input_usuario = tk.Label(insertarcancion, text="Nombre", bg=color, fg=color2, font=fuente)
    nombre = tk.Entry(insertarcancion, fg=color, bg=color2, font=fuente)

    input_codmembresia3 = tk.Label(insertarcancion, text="Codcancion", bg=color, fg=color2, font=fuente)
    codcancion = tk.Entry(insertarcancion, fg=color, bg=color2, font=fuente)
    input_codmembresia = tk.Label(insertarcancion, text="Codartista", bg=color, fg=color2, font=fuente)
    codartista = tk.Entry(insertarcancion, fg=color, bg=color2, font=fuente)

    input_codmembresia2 = tk.Label(insertarcancion, text="Codalbum", bg=color, fg=color2, font=fuente)
    codalbum = tk.Entry(insertarcancion, fg=color, bg=color2, font=fuente)
    input_codmembresia4 = tk.Label(insertarcancion, text="Codplaylist",bg=color, fg=color2,font=fuente)
    codplaylist = tk.Entry(insertarcancion,fg=color, bg=color2, font=fuente) 

    input2.pack(pady=10)
    input_usuario.pack(pady=10)
    nombre.pack(pady=10)
    input_codmembresia3.pack(pady=10)
    codcancion.pack(pady=10)
    input_codmembresia.pack(pady=10)
    codartista.pack(pady=10)
    input_codmembresia2.pack(pady=10)
    codalbum.pack(pady=10)
    input_codmembresia4.pack(pady=10)
    codplaylist.pack(pady=10)

    boton_login = Button(insertarcancion, text="Aceptar", command=lambda: comprobacioncanciones(nombre.get(), codcancion.get(), codalbum.get(), codartista.get(), codplaylist.get(), insertarcancion), bg=color, fg=color2, font=fuente)
    boton_login.pack(pady=30)

    insertarcancion.mainloop()
#######################################################INSERTAR ADMINISTRADORES##########################################
def inserciondeadmin(nombre, codadmin, ventana):
    dicadmin[codadmin] = {'nombreadmin': nombre}
    ventana.destroy()
    messagebox.showinfo("Admin Creado", "Admin Creado con éxito")
def revisionrepetido7(nombre, codadmin, ventana):
    codadmin = str(codadmin) 
    if codadmin in dicadmin:
        messagebox.showerror("Error", "El codadmin ya existe. Intenta de nuevo.")
    else:
        inserciondeadmin(nombre, codadmin, ventana)
def comprobacionadmin(nombre, codgenero, ventana):
    try:
        codgenero = int(codgenero)
        revisionrepetido7(nombre, codgenero, ventana)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
def insertar_administradores():
    insertaradmin = tk.Toplevel()
    insertaradmin.title("Inserción de Administradores")
    insertaradmin.geometry("800x625")
    insertaradmin.resizable(False, False)
    insertaradmin.configure(bg=color)

    fuente = ("Consolas", 14)
    fuenteg = ("Consolas", 18)

    input2 = tk.Label(insertaradmin, text="Insertar Administrador", bg=color, fg=color2, font=fuenteg) 
    input_usuario = tk.Label(insertaradmin, text="Nombre", bg=color, fg=color2, font=fuente)
    nombre = tk.Entry(insertaradmin, bg=color2, fg=color, font=fuente)
    input_codmembresia = tk.Label(insertaradmin, text="Codadmin", bg=color, fg=color2, font=fuente)
    codgenero = tk.Entry(insertaradmin, bg=color2, fg=color, font=fuente)

    input2.pack(pady=10)
    input_usuario.pack(pady=10)
    nombre.pack(pady=10)
    input_codmembresia.pack(pady=10)
    codgenero.pack(pady=10)

    boton_login = Button(insertaradmin, text="Aceptar", command=lambda: comprobacionadmin(nombre.get(), codgenero.get(), insertaradmin), bg=color, fg=color2, font=fuente)
    boton_login.pack(pady=30)

    insertaradmin.mainloop()
####################################################################################################################
#######################################################BUSQUEDA######################################################
####################################################################################################################
#######################################################BUSCAR PROPIETARIO##############################################
def busqueda_propietario(codpropietario):
    codpropietario = str(codpropietario)
    for codigo in dicpropietarios:
        if codpropietario == codigo:
            messagebox.showinfo("Resultado", f"El dueño de la cuenta con ese código es {dicpropietarios[codigo]['nombrepro']}")
            buscarpropietario.destroy()
            break
    else:
        messagebox.showinfo("Resultado", "Propietario Inexistente")
        buscarpropietario.destroy()
def buscar_propietario():
    global buscarpropietario
    buscarpropietario = tk.Toplevel()
    buscarpropietario.title("Búsqueda de Propietario")
    buscarpropietario.geometry("600x400")
    buscarpropietario.resizable(False, False)
    buscarpropietario.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(buscarpropietario, text="Buscar Propietario", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(buscarpropietario, text="Codpropietario", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(buscarpropietario, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10))
    boton_buscar = tk.Button(buscarpropietario, text="Buscar", command=lambda: auxiliar_propietario(codpropietario_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    buscarpropietario.mainloop()
def auxiliar_propietario(codpropietario):
    try:
        codpropietario = int(codpropietario)
        busqueda_propietario(codpropietario)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        buscarpropietario.destroy()
#######################################################BUSCAR PLAYLIST#################################################
def busqueda_playlist(codplaylist):
    codplaylist = str(codplaylist)
    existecodpro = False
    existeplay = False
    for codigo in dicplaylist:
        if codigo == codplaylist:
            existeplay = True
            codpro = dicplaylist[codplaylist]['codpropietario']
            for codigo2 in dicpropietarios:
                if codigo2 == codpro:
                    existecodpro = True
                    break
            break
    if existecodpro:
        messagebox.showinfo("Resultado", f"Nombre de la Playlist: {dicplaylist[codplaylist]['nombreplay']} | Propietario: {dicpropietarios[codpro]['nombrepro']}")
        buscarplaylist.destroy()
    elif not existecodpro and existeplay:
        messagebox.showinfo("Resultado", f"Nombre de la Playlist: {dicplaylist[codplaylist]['nombreplay']} | Propietario: No ligado")
        buscarplaylist.destroy()
    else:
        messagebox.showinfo("Resultado", "Playlist inexistente")
        buscarplaylist.destroy()
def buscar_playlist():
    global buscarplaylist
    buscarplaylist = tk.Toplevel()
    buscarplaylist.title("Búsqueda de Playlist")
    buscarplaylist.geometry("600x400")
    buscarplaylist.resizable(False, False)
    buscarplaylist.configure(bg=color)

    fuente = ("Console", 14)
    fuenteg = ("Console", 18)

    input2 = tk.Label(buscarplaylist, text="Buscar Playlist", bg=color, fg=color2, font=fuenteg)
    input_codplaylist = tk.Label(buscarplaylist, text="Codplaylist", bg=color, fg=color2,font=fuente)
    codplaylist_entry = tk.Entry(buscarplaylist, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codplaylist.pack(pady=(10))
    codplaylist_entry.pack(pady=(10))
    boton_buscar = tk.Button(buscarplaylist, text="Buscar", command=lambda: auxiliar_playlist(codplaylist_entry.get()),bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    buscarplaylist.mainloop()
def auxiliar_playlist(codplaylist):
    try:
        codplaylist = int(codplaylist)
        busqueda_playlist(codplaylist)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        buscarplaylist.destroy()
#######################################################BUSCAR GENERO#################################################
def busqueda_genero(codgenero):
    codgenero=str(codgenero)
    for codigo in dicgenero:
        if codgenero == codigo:
            messagebox.showinfo("Resultado", f"El genero con ese código es {dicgenero[codigo]['nombregen']}")
            buscargenero.destroy()
            break
    else:
        messagebox.showinfo("Resultado", "Genero Inexistente")
        buscargenero.destroy()
def buscar_genero():
    global buscargenero
    buscargenero = tk.Toplevel()
    buscargenero.title("Búsqueda de Genero")
    buscargenero.geometry("600x400")
    buscargenero.resizable(False, False)
    buscargenero.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(buscargenero, text="Buscar Genero", bg=color, fg=color2, font=fuenteg)
    input_codgenero = tk.Label(buscargenero, text="Codgenero", bg=color, fg=color2, font=fuente)
    codgenero_entry = tk.Entry(buscargenero, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codgenero.pack(pady=(10))
    codgenero_entry.pack(pady=(10))
    boton_buscar = tk.Button(buscargenero, text="Buscar", command=lambda: auxiliar_genero(codgenero_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    buscargenero.mainloop()
def auxiliar_genero(codgenero):
    try:
        codgenero = int(codgenero)
        busqueda_genero(codgenero)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        buscargenero.destroy()
#######################################################BUSCAR ARTISTA#################################################
def busqueda_artista(codart):
    global busqueda_artistas2
    existecodgen = False
    existeart = False
    codart=str(codart)
    for codigo in dicartista:
        if codigo == codart:
            existeart = True
            codgen = dicartista[codart]['codgenero']
            busqueda_artistas2 = list(busqueda_artistas2)
            busqueda_artistas2.append(codigo)
            for codigo2 in dicgenero:
                if codigo2 == codgen:
                    existecodgen = True
                    break
            break
    if existecodgen:
        messagebox.showinfo("Resultado", f"Nombre del Artista: {dicartista[codart]['nombreart']} | Género: {dicgenero[codgen]['nombregen']}")
        buscarartista.destroy()
    elif not existecodgen and existeart:
        messagebox.showinfo("Resultado", f"Nombre del Artista: {dicartista[codart]['nombreart']} | Género: No ligado")
        buscarartista.destroy()
    else:
        messagebox.showinfo("Resultado", "Artista inexistente")
        buscarartista.destroy()
def buscar_artista():
    global buscarartista
    buscarartista = tk.Toplevel()
    buscarartista.title("Búsqueda de Artista")
    buscarartista.geometry("600x400")
    buscarartista.resizable(False, False)
    buscarartista.configure(bg=color)

    fuente = ("Console", 14)
    fuenteg = ("Console", 18)

    input2 = tk.Label(buscarartista, text="Buscar Artista", bg=color, fg=color2, font=fuenteg)
    input_codart = tk.Label(buscarartista, text="Codart", bg=color, fg=color2, font=fuente)
    codart_entry = tk.Entry(buscarartista,bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codart.pack(pady=(10))
    codart_entry.pack(pady=(10))
    boton_buscar = tk.Button(buscarartista, text="Buscar", command=lambda: auxiliar_artista(codart_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    buscarartista.mainloop()
def auxiliar_artista(codart):
    try:
        codart = int(codart)
        busqueda_artista(codart)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        buscarartista.destroy()
#######################################################BUSCAR ALBUM##################################################
def busqueda_album(codalbum):
    global busqueda_album2
    existealbum = False
    existecodgen = False
    existeart = False
    codalbum = str(codalbum)
    for codigo in dicalbum:
        if codigo == codalbum:
            existealbum = True
            codart = dicalbum[codalbum]['codart']
            # Convertir el conjunto a lista antes de agregar un elemento
            busqueda_album2 = list(busqueda_album2)
            busqueda_album2.append(codigo)
            # Convertir de vuelta a conjunto si es necesario
            busqueda_album2 = set(busqueda_album2)
            for codigo2 in dicartista:
                if codigo2 == codart:
                    existecodgen = True
                    break
            break
    if existecodgen:
        messagebox.showinfo("Resultado", f"Nombre del Álbum: {dicalbum[codalbum]['nombrealbum']} | Del Artista: {dicartista[codart]['nombreart']}")
        buscaralbum.destroy()
    elif not existecodgen and existealbum:
        messagebox.showinfo("Resultado", f"Nombre del Álbum: {dicalbum[codalbum]['nombrealbum']} | Del Artista: No ligado")
        buscaralbum.destroy()
    else:
        messagebox.showinfo("Resultado", "Álbum inexistente")
        buscaralbum.destroy()
def buscar_album():
    global buscaralbum
    buscaralbum = tk.Toplevel()
    buscaralbum.title("Búsqueda de Álbum")
    buscaralbum.geometry("600x400")
    buscaralbum.resizable(False, False)
    buscaralbum.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(buscaralbum, text="Buscar Álbum", bg=color, fg=color2, font=fuenteg)
    input_codalbum = tk.Label(buscaralbum, text="Codalbum", bg=color, fg=color2, font=fuente)
    codalbum_entry = tk.Entry(buscaralbum,bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codalbum.pack(pady=(10))
    codalbum_entry.pack(pady=(10))
    boton_buscar = tk.Button(buscaralbum, text="Buscar", command=lambda: auxiliar_album(codalbum_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    buscaralbum.mainloop()
def auxiliar_album(codalbum):
    try:
        codalbum = int(codalbum)
        busqueda_album(codalbum)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        buscaralbum.destroy()
#######################################################BUSCAR CANCIÓN################################################
def busqueda_cancion(codcan):
    codcan = str(codcan)
    canexiste = False
    nombreart = "No ligado"
    nombregenero = "No ligado"
    nombrealbum = "No ligado"
    nombreplay = "No ligado"
    for codigo in diccanciones:
        if codigo == codcan:
            canexiste = True
            nombrecan = diccanciones[codcan]['nombrecan']
            codart = diccanciones[codcan]['codart']
            codalbum = diccanciones[codcan]['codalbum']
            codplay = diccanciones[codcan]['codplaylist']
            codgenero = diccanciones[codcan]['codgenero']
    if canexiste:
        for codigo in dicartista:
            if codart == codigo:
                nombreart = dicartista[codart]['nombreart']
                break
        for codigo in dicgenero:
            if codgenero == codigo:
                nombregenero = dicgenero[codgenero]['nombregen']
                break
        for codigo in dicalbum:
            if codalbum == codigo:
                nombrealbum = dicalbum[codalbum]['nombrealbum']
                break
        for codigo in dicplaylist:
            if codplay == codigo:
                nombreplay = dicplaylist[codplay]['nombreplay']
                break
        mensaje = f"| Nombre de la Canción: {nombrecan} | Del Álbum: {nombrealbum} | Del Artista: {nombreart} | Del Género: {nombregenero} | De la Playlist: {nombreplay} |"
        messagebox.showinfo("Resultado", mensaje)
        buscarcancion.destroy()
    else:
        messagebox.showinfo("Resultado", "Canción inexistente")
        buscarcancion.destroy()
def buscar_cancion():
    global buscarcancion
    buscarcancion = tk.Toplevel()
    buscarcancion.title("Búsqueda de Canción")
    buscarcancion.geometry("600x400")
    buscarcancion.resizable(False, False)
    buscarcancion.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(buscarcancion, text="Buscar Canción", bg=color, fg=color2, font=fuenteg)
    input_codcan = tk.Label(buscarcancion, text="Codcancion", bg=color, fg=color2, font=fuente)
    codcan_entry = tk.Entry(buscarcancion, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codcan.pack(pady=(10))
    codcan_entry.pack(pady=(10))
    boton_buscar = tk.Button(buscarcancion, text="Buscar", command=lambda: auxiliar_cancion(codcan_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    buscarcancion.mainloop()
def auxiliar_cancion(codcan):
    try:
        codcan = int(codcan)
        busqueda_cancion(codcan)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        buscarcancion.destroy()
#######################################################BUSCAR ADMINISTRADOR###########################################
def busqueda_admin(codadmin):
    codadmin = str(codadmin)
    for codigo in dicadmin:
        if codadmin == codigo:
            messagebox.showinfo("Resultado", f"El administrador de la cuenta con ese código es {dicadmin[codigo]['nombreadmin']}")
            buscaradmin.destroy()
            break
    else:
        messagebox.showinfo("Resultado", "Administrador Inexistente")
        buscaradmin.destroy()
def buscar_admin():
    global buscaradmin
    buscaradmin = tk.Toplevel()
    buscaradmin.title("Búsqueda de Administrador")
    buscaradmin.geometry("600x400")
    buscaradmin.resizable(False, False)
    buscaradmin.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(buscaradmin, text="Buscar Administrador", bg=color, fg=color2, font=fuenteg)
    input_codadmin = tk.Label(buscaradmin, text="Codadmin", bg=color, fg=color2, font=fuente)
    codadmin_entry = tk.Entry(buscaradmin, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codadmin.pack(pady=(10))
    codadmin_entry.pack(pady=(10))
    boton_buscar = tk.Button(buscaradmin, text="Buscar", command=lambda: auxiliar_admin(codadmin_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    buscaradmin.mainloop()
    
def auxiliar_admin(codadmin):
    try:
        codadmin = int(codadmin)
        busqueda_admin(codadmin)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        buscaradmin.destroy()
######################################################################################################################
#######################################################ELIMINACION######################################################
######################################################################################################################
#######################################################ELIMINAR PROPIETARIO################################################
def eliminacion_propietario(codpro):
    codpro = str(codpro)
    salida = False
    while not salida:
        if codpro == usuario:
            messagebox.showinfo("Resultado","No puedes borrar tu usuario.")
            eliminarpropietario.destroy()
        elif codpro != usuario:
            salida = True
    existepro = False
    if codpro in dicpropietarios:
        del dicpropietarios[codpro]
        messagebox.showinfo("Resultado","Propietario Eliminado")
        eliminarpropietario.destroy()
        existepro = True
    else:
        messagebox.showinfo("Resultado","Propietario inexistente")
        eliminarpropietario.destroy()
    claves_a_eliminar = []
    if existepro:
        for codigo in dicplaylist:
            if dicplaylist[codigo]['codpropietario'] == codpro:
                claves_a_eliminar.append(codigo)
    if existepro:
        for codigo in claves_a_eliminar:
            del dicplaylist[codigo]

def eliminar_propietario():
    global eliminarpropietario
    eliminarpropietario = tk.Toplevel()
    eliminarpropietario.title("Eliminación de Propietario")
    eliminarpropietario.geometry("600x400")
    eliminarpropietario.resizable(False, False)
    eliminarpropietario.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(eliminarpropietario, text="Eliminar Propietario", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(eliminarpropietario, text="Codpropietario", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(eliminarpropietario, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10))
    boton_buscar = tk.Button(eliminarpropietario, text="Eliminar", command=lambda: auxiliar_del_propietario(codpropietario_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    eliminarpropietario.mainloop()
    
def auxiliar_del_propietario(codpropietario):
    try:
        codpropietario = int(codpropietario)
        eliminacion_propietario(codpropietario)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        eliminarpropietario.destroy()

        
#######################################################ELIMINAR PLAYLIST###################################################
def eliminacion_playlist(codplay):
    codplay = str(codplay)
    existeplay = False
    if codplay in dicplaylist:
        del dicplaylist[codplay]
        messagebox.showinfo("Resultado","Playlist Eliminada")
        eliminarplaylist.destroy()
        existeplay = True
    else:
        messagebox.showinfo("Resultado","Playlist inexistente")
        eliminarplaylist.destroy()
    claves_a_eliminar = []
    if existeplay:
        for codigo in diccanciones:
            if diccanciones[codigo]['codplaylist'] == codplay:
                claves_a_eliminar.append(codigo)
    if existeplay:
        for codigo in claves_a_eliminar:
            del diccanciones[codigo]

def eliminar_playlist():
    global eliminarplaylist
    eliminarplaylist = tk.Toplevel()
    eliminarplaylist.title("Eliminación de Playlist")
    eliminarplaylist.geometry("600x400")
    eliminarplaylist.resizable(False, False)
    eliminarplaylist.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(eliminarplaylist, text="Eliminar Playlist", bg=color, fg=color2, font=fuenteg)
    input_codplaylist = tk.Label(eliminarplaylist, text="Código de Playlist", bg=color, fg=color2, font=fuente)
    codplaylist_entry = tk.Entry(eliminarplaylist, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codplaylist.pack(pady=(10))
    codplaylist_entry.pack(pady=(10))
    boton_eliminar = tk.Button(eliminarplaylist, text="Eliminar", command=lambda: auxiliar_del_playlist(codplaylist_entry.get()), bg=color, fg=color2, font=fuente)
    boton_eliminar.pack(pady=20)
    eliminarplaylist.mainloop()

def auxiliar_del_playlist(codplaylist):
    try:
        codplaylist = int(codplaylist)
        eliminacion_playlist(codplaylist)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        eliminarplaylist.destroy()
#####################################################ELIMINAR GENERO###################################################
def eliminacion_genero(codgenero):
    codgenero = str(codgenero)
    existe = False
    if codgenero in dicgenero:
        del dicgenero[codgenero]
        existe = True
    else:
        messagebox.showinfo("Resultado", "Género inexistente")
        eliminargenero.destroy() 
        return
    
    claves_a_eliminarart = []
    claves_a_eliminarcan = []
    claves_a_eliminaralbum = []
    
    if existe:
        for codigo in dicartista:
            if dicartista[codigo]['codgenero'] == codgenero:
                claves_a_eliminarart.append(codigo)
        
        for codigo in diccanciones:
            for codigo2 in claves_a_eliminarart:
                if diccanciones[codigo]['codart'] == codigo2:
                    claves_a_eliminarcan.append(codigo)
        
        for codigo in dicalbum:
            for codigo2 in claves_a_eliminarart:
                if dicalbum[codigo]['codart'] == codigo2:
                    claves_a_eliminaralbum.append(codigo)
    
    for codigo in claves_a_eliminaralbum:
        del dicalbum[codigo]                                 
    
    for codigo in claves_a_eliminarart:
        del dicartista[codigo]                            
    
    for codigo in claves_a_eliminarcan:
        del diccanciones[codigo]

    messagebox.showinfo("Resultado", "Género eliminado")
    eliminargenero.destroy()  

def eliminar_genero():
    global eliminargenero
    eliminargenero = tk.Toplevel()
    eliminargenero.title("Eliminación de Género")
    eliminargenero.geometry("600x400")
    eliminargenero.resizable(False, False)
    eliminargenero.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(eliminargenero, text="Eliminar Género", bg=color, fg=color2, font=fuenteg)
    input_codgenero = tk.Label(eliminargenero, text="Código de Género", bg=color, fg=color2, font=fuente)
    codgenero_entry = tk.Entry(eliminargenero, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codgenero.pack(pady=(10))
    codgenero_entry.pack(pady=(10))
    boton_eliminar = tk.Button(eliminargenero, text="Eliminar", command=lambda: auxiliar_del_genero(codgenero_entry.get()), bg=color, fg=color2, font=fuente)
    boton_eliminar.pack(pady=20)
    eliminargenero.mainloop()

def auxiliar_del_genero(codgenero):
    try:
        codgenero = int(codgenero)
        eliminacion_genero(codgenero)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        eliminargenero.destroy()

#######################################################ELIMINAR ARTISTA###################################################
def eliminacion_artista(codart):
    codart = str(codart)
    
    existe = False
    if codart in dicartista:
        del dicartista[codart]
        existe = True
    else:
        messagebox.showinfo("Resultado", "Artista inexistente")
        eliminarartista.destroy()  # Cerrar ventana si el artista no existe
        return
    
    claves_a_eliminarart = [codart]
    claves_a_eliminarcan = []
    claves_a_eliminaralbum = []
    
    if existe:
        for codigo in diccanciones:
            for codigo2 in claves_a_eliminarart:
                if diccanciones[codigo]['codart'] == codigo2:
                    claves_a_eliminarcan.append(codigo)
        
        for codigo in dicalbum:
            for codigo2 in claves_a_eliminarart:
                if dicalbum[codigo]['codart'] == codigo2:
                    claves_a_eliminaralbum.append(codigo)
    
    for codigo in claves_a_eliminaralbum:
        del dicalbum[codigo]                                 
    
    for codigo in claves_a_eliminarcan:
        del diccanciones[codigo]

    messagebox.showinfo("Resultado", "Artista eliminado")
    eliminarartista.destroy()  # Cerrar ventana después de mostrar el mensaje

def eliminar_artista():
    global eliminarartista
    eliminarartista = tk.Toplevel()
    eliminarartista.title("Eliminación de Artista")
    eliminarartista.geometry("600x400")
    eliminarartista.resizable(False, False)
    eliminarartista.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(eliminarartista, text="Eliminar Artista", bg=color, fg=color2, font=fuenteg)
    input_codart = tk.Label(eliminarartista, text="Código de Artista", bg=color, fg=color2, font=fuente)
    codart_entry = tk.Entry(eliminarartista, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codart.pack(pady=(10))
    codart_entry.pack(pady=(10))
    boton_eliminar = tk.Button(eliminarartista, text="Eliminar", command=lambda: auxiliar_del_artista(codart_entry.get()), bg=color, fg=color2, font=fuente)
    boton_eliminar.pack(pady=20)
    eliminarartista.mainloop()

def auxiliar_del_artista(codart):
    try:
        codart = int(codart)
        eliminacion_artista(codart)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        eliminarartista.destroy()

#######################################################ELIMINAR ALBUM####################################################
def eliminacion_album(codalbum):
    codalbum = str(codalbum)
    
    existe = False
    if codalbum in dicalbum:
        del dicalbum[codalbum]
        existe = True
    else:
        messagebox.showinfo("Resultado", "Álbum inexistente")
        eliminaralbum.destroy()  # Cerrar ventana si el álbum no existe
        return
    
    claves_a_eliminar = [codalbum]
    claves_a_eliminarcan = []
    
    if existe:
        for codigo in diccanciones:
            for codigo2 in claves_a_eliminar:
                if diccanciones[codigo]['codalbum'] == codigo2:
                    claves_a_eliminarcan.append(codigo)
    
    for codigo in claves_a_eliminarcan:
        del diccanciones[codigo]

    messagebox.showinfo("Resultado", "Álbum eliminado")
    eliminaralbum.destroy()  # Cerrar ventana después de mostrar el mensaje

def eliminar_album():
    global eliminaralbum
    eliminaralbum = tk.Toplevel()
    eliminaralbum.title("Eliminación de Álbum")
    eliminaralbum.geometry("600x400")
    eliminaralbum.resizable(False, False)
    eliminaralbum.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(eliminaralbum, text="Eliminar Álbum", bg=color, fg=color2, font=fuenteg)
    input_codalbum = tk.Label(eliminaralbum, text="Código de Álbum", bg=color, fg=color2, font=fuente)
    codalbum_entry = tk.Entry(eliminaralbum, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codalbum.pack(pady=(10))
    codalbum_entry.pack(pady=(10))
    boton_eliminar = tk.Button(eliminaralbum, text="Eliminar", command=lambda: auxiliar_del_album(codalbum_entry.get()), bg=color, fg=color2, font=fuente)
    boton_eliminar.pack(pady=20)
    eliminaralbum.mainloop()

def auxiliar_del_album(codalbum):
    try:
        codalbum = int(codalbum)
        eliminacion_album(codalbum)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        eliminaralbum.destroy()

#######################################################ELIMINAR CANCION##################################################
def eliminacion_cancion(codcan):
    codcan = str(codcan)
    
    existe = False
    if codcan in diccanciones:
        del diccanciones[codcan]
        existe = True
    else:
        messagebox.showinfo("Resultado", "Canción inexistente")
        eliminarcancion.destroy()  # Cerrar ventana si la canción no existe
        return
    
    messagebox.showinfo("Resultado", "Canción eliminada")
    eliminarcancion.destroy()  # Cerrar ventana después de mostrar el mensaje

def eliminar_cancion():
    global eliminarcancion
    eliminarcancion = tk.Toplevel()
    eliminarcancion.title("Eliminación de Canción")
    eliminarcancion.geometry("600x400")
    eliminarcancion.resizable(False, False)
    eliminarcancion.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(eliminarcancion, text="Eliminar Canción", bg=color, fg=color2, font=fuenteg)
    input_codcan = tk.Label(eliminarcancion, text="Código de Canción", bg=color, fg=color2, font=fuente)
    codcan_entry = tk.Entry(eliminarcancion, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codcan.pack(pady=(10))
    codcan_entry.pack(pady=(10))
    boton_eliminar = tk.Button(eliminarcancion, text="Eliminar", command=lambda: auxiliar_del_cancion(codcan_entry.get()), bg=color, fg=color2, font=fuente)
    boton_eliminar.pack(pady=20)
    eliminarcancion.mainloop()

def auxiliar_del_cancion(codcan):
    try:
        codcan = int(codcan)
        eliminacion_cancion(codcan)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        eliminarcancion.destroy()
    
#######################################################ELIMINAR ADMINISTRADOR#############################################
def eliminacion_admin(codadmin):
    codadmin = str(codadmin)
    existepro = False
    if codadmin in dicadmin:
        if codadmin==str(usuario):
            messagebox.showinfo("Resultado","No puedes borrar tu usuario.")
            eliminaradmin.destroy()
        else:
            del dicadmin[codadmin]
            messagebox.showinfo("Resultado","Administrador Eliminado")
            eliminaradmin.destroy()
            existepro = True
    else:
        messagebox.showinfo("Resultado","Administrador inexistente")
        eliminaradmin.destroy()

def eliminar_admin():
    global eliminaradmin
    eliminaradmin = tk.Toplevel()
    eliminaradmin.title("Eliminación de Administrador")
    eliminaradmin.geometry("600x400")
    eliminaradmin.resizable(False, False)
    eliminaradmin.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(eliminaradmin, text="Eliminar Administrador", bg=color, fg=color2, font=fuenteg)
    input_codadmin = tk.Label(eliminaradmin, text="Codadmin", bg=color, fg=color2, font=fuente)
    codadmin_entry = tk.Entry(eliminaradmin, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codadmin.pack(pady=(10))
    codadmin_entry.pack(pady=(10))
    boton_buscar = tk.Button(eliminaradmin, text="Eliminar", command=lambda: auxiliar_del_admin(codadmin_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    eliminaradmin.mainloop()
    
def auxiliar_del_admin(codadmin):
    try:
        codadmin = int(codadmin)
        eliminacion_admin(codadmin)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        eliminaradmin.destroy()
######################################################################################################################
#######################################################MODIFICACION####################################################
######################################################################################################################
#######################################################MODIFICAR PROPIETARIO##############################################
def modifica_propietario(codpropietario, nombre):
    codpropietario = str(codpropietario)
    nombre = str(nombre)
    for codigo in dicpropietarios:
        if codpropietario == codigo:
            dicpropietarios[codpropietario]['nombrepro']=nombre
            modificarpropietario.destroy()
            messagebox.showinfo("Resultado", f"El dueño de la cuenta con ese código ahora es {dicpropietarios[codigo]['nombrepro']}")
            break
    else:
        messagebox.showinfo("Resultado", "Propietario Inexistente")
def auxiliarmodpropietario(codpropietario, nombre):
    try:
        codpropietario = int(codpropietario)
        modifica_propietario(codpropietario, nombre)
    except ValueError:
        messagebox.showerror("Error", "El codpropietario debe ser un número entero. Intenta de nuevo.")
def modificar_propietario():
    global modificarpropietario
    modificarpropietario = tk.Toplevel()
    modificarpropietario.title("Modificar Propietario")
    modificarpropietario.geometry("600x400")
    modificarpropietario.resizable(False, False)
    modificarpropietario.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(modificarpropietario, text="Modificar Nombre de Propietario", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(modificarpropietario, text="Codpropietario", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(modificarpropietario, bg=color2, fg=color, font=fuente)
    input_codpropietario2 = tk.Label(modificarpropietario, text="Nombre", bg=color, fg=color2, font=fuente)
    codpropietario_entry2 = tk.Entry(modificarpropietario, bg=color2, fg=color, font=fuente)    
    input2.pack(pady=(10))
    input_codpropietario2.pack(pady=(10))
    codpropietario_entry2.pack(pady=(10))  
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10))
    boton_buscar = tk.Button(modificarpropietario, text="Modificar", command=lambda: auxiliarmodpropietario(codpropietario_entry.get(),codpropietario_entry2.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    modificarpropietario.mainloop()
#######################################################MODIFICAR PLAYLIST#################################################
def modifica_playlist(codplaylist, nombre):
    codplaylist = str(codplaylist)
    nombre = str(nombre)
    for codigo in dicplaylist:
        if codplaylist == codigo:
            dicplaylist[codplaylist]['nombreplay']=nombre
            modificarplaylist.destroy()
            messagebox.showinfo("Resultado", f"El Nombre de la playlist con ese código ahora es {dicplaylist[codigo]['nombreplay']}")
            break
    else:
        messagebox.showinfo("Resultado", "Playlist Inexistente")
def auxiliarmodplaylist(codplaylist, nombre):
    try:
        codplaylist = int(codplaylist)
        modifica_playlist(codplaylist, nombre)
    except ValueError:
        messagebox.showerror("Error", "El codplaylist debe ser un número entero. Intenta de nuevo.")
def modificar_playlist():
    global modificarplaylist
    modificarplaylist = tk.Toplevel()
    modificarplaylist.title("Modificar Playlist")
    modificarplaylist.geometry("600x400")
    modificarplaylist.resizable(False, False)
    modificarplaylist.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(modificarplaylist, text="Modificar Nombre de Playlist", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(modificarplaylist, text="Codplaylist", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(modificarplaylist, bg=color2, fg=color, font=fuente)
    input_codpropietario2 = tk.Label(modificarplaylist, text="Nombre", bg=color, fg=color2, font=fuente)
    codpropietario_entry2 = tk.Entry(modificarplaylist, bg=color2, fg=color, font=fuente)    
    input2.pack(pady=(10))
    input_codpropietario2.pack(pady=(10))
    codpropietario_entry2.pack(pady=(10))   
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10)) 
    boton_buscar = tk.Button(modificarplaylist, text="Modificar", command=lambda: auxiliarmodplaylist(codpropietario_entry.get(),codpropietario_entry2.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    modificarplaylist.mainloop()
#######################################################MODIFICAR GENERO#################################################
def modifica_genero(codgenero, nombre):
    codgenero = str(codgenero)
    nombre = str(nombre)
    for codigo in dicgenero:
        if codgenero == codigo:
            dicgenero[codgenero]['nombregen']=nombre
            modificargenero.destroy()
            messagebox.showinfo("Resultado", f"El Nombre del genero con ese código ahora es {dicgenero[codigo]['nombregen']}")
            break
    else:
        messagebox.showinfo("Resultado", "Genero Inexistente")
def auxiliarmodgenero(codgenero, nombre):
    try:
        codgenero = int(codgenero)
        modifica_genero(codgenero, nombre)
    except ValueError:
        messagebox.showerror("Error", "El codgenero debe ser un número entero. Intenta de nuevo.")
def modificar_genero():
    global modificargenero
    modificargenero = tk.Toplevel()
    modificargenero.title("Modificar Genero")
    modificargenero.geometry("600x400")
    modificargenero.resizable(False, False)
    modificargenero.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(modificargenero, text="Modificar Nombre de Genero", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(modificargenero, text="Codgenero", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(modificargenero, bg=color2, fg=color, font=fuente)
    input_codpropietario2 = tk.Label(modificargenero, text="Nombre", bg=color, fg=color2, font=fuente)
    codpropietario_entry2 = tk.Entry(modificargenero, bg=color2, fg=color, font=fuente)    
    input2.pack(pady=(10))
    input_codpropietario2.pack(pady=(10))
    codpropietario_entry2.pack(pady=(10))   
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10)) 
    boton_buscar = tk.Button(modificargenero, text="Modificar", command=lambda: auxiliarmodgenero(codpropietario_entry.get(),codpropietario_entry2.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    modificargenero.mainloop()
#######################################################MODIFICAR ARTISTA#################################################
def modifica_artista(codartista, nombre):
    codartista = str(codartista)
    nombre = str(nombre)
    for codigo in dicartista:
        if codartista == codigo:
            modificarartista.destroy()
            dicartista[codartista]['nombreart']=nombre
            messagebox.showinfo("Resultado", f"El Nombre del artista con ese código ahora es {dicartista[codigo]['nombreart']}")
            break
    else:
        messagebox.showinfo("Resultado", "Artista Inexistente")
def auxiliarmodartista(codartista, nombre):
    try:
        codartista = int(codartista)
        modifica_artista(codartista, nombre)
    except ValueError:
        messagebox.showerror("Error", "El codartista debe ser un número entero. Intenta de nuevo.")
def modificar_artista():
    global modificarartista
    modificarartista = tk.Toplevel()
    modificarartista.title("Modificar Artista")
    modificarartista.geometry("600x400")
    modificarartista.resizable(False, False)
    modificarartista.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(modificarartista, text="Modificar Nombre de Artista", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(modificarartista, text="Codartista", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(modificarartista, bg=color2, fg=color, font=fuente)
    input_codpropietario2 = tk.Label(modificarartista, text="Nombre", bg=color, fg=color2, font=fuente)
    codpropietario_entry2 = tk.Entry(modificarartista, bg=color2, fg=color, font=fuente)    
    input2.pack(pady=(10))
    input_codpropietario2.pack(pady=(10))
    codpropietario_entry2.pack(pady=(10))   
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10)) 
    boton_buscar = tk.Button(modificarartista, text="Modificar", command=lambda: auxiliarmodartista(codpropietario_entry.get(),codpropietario_entry2.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    modificarartista.mainloop()
#######################################################MODIFICAR ALBUM##################################################
def modifica_album(codalbum, nombre):
    codalbum = str(codalbum)
    nombre = str(nombre)
    for codigo in dicalbum:
        if codalbum == codigo:
            dicalbum[codalbum]['nombrealbum']=nombre
            modificaralbum.destroy()
            messagebox.showinfo("Resultado", f"El Nombre del album con ese código ahora es {dicalbum[codigo]['nombrealbum']}")
            break
    else:
        messagebox.showinfo("Resultado", "Album Inexistente")
def auxiliarmodalbum(codalbum, nombre):
    try:
        codalbum = int(codalbum)
        modifica_album(codalbum, nombre)
    except ValueError:
        messagebox.showerror("Error", "El codalbum debe ser un número entero. Intenta de nuevo.")
def modificar_album():
    global modificaralbum
    modificaralbum = tk.Toplevel()
    modificaralbum.title("Modificar Album")
    modificaralbum.geometry("600x400")
    modificaralbum.resizable(False, False)
    modificaralbum.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(modificaralbum, text="Modificar Nombre de Album", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(modificaralbum, text="Codalbum", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(modificaralbum, bg=color2, fg=color, font=fuente)
    input_codpropietario2 = tk.Label(modificaralbum, text="Nombre", bg=color, fg=color2, font=fuente)
    codpropietario_entry2 = tk.Entry(modificaralbum, bg=color2, fg=color, font=fuente)    
    input2.pack(pady=(10))
    input_codpropietario2.pack(pady=(10))
    codpropietario_entry2.pack(pady=(10))   
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10)) 
    boton_buscar = tk.Button(modificaralbum, text="Modificar", command=lambda: auxiliarmodalbum(codpropietario_entry.get(),codpropietario_entry2.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    modificaralbum.mainloop()
#######################################################MODIFICAR CANCION################################################
def modifica_cancion(codcan, nombre):
    codcan = str(codcan)
    nombre = str(nombre)
    for codigo in diccanciones:
        if codcan == codigo:
            diccanciones[codcan]['nombrecan']=nombre
            modificarcancion.destroy()
            messagebox.showinfo("Resultado", f"El Nombre de la canción con ese código ahora es {diccanciones[codigo]['nombrecan']}")
            break
    else:
        messagebox.showinfo("Resultado", "Canción Inexistente")
def auxiliarmodcancion(codcan, nombre):
    try:
        codcan = int(codcan)
        modifica_cancion(codcan, nombre)
    except ValueError:
        messagebox.showerror("Error", "El codcanción debe ser un número entero. Intenta de nuevo.")
def modificar_cancion():
    global modificarcancion
    modificarcancion = tk.Toplevel()
    modificarcancion.title("Modificar Canción")
    modificarcancion.geometry("600x400")
    modificarcancion.resizable(False, False)
    modificarcancion.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(modificarcancion, text="Modificar Nombre de una Canción", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(modificarcancion, text="Codcanción", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(modificarcancion, bg=color2, fg=color, font=fuente)
    input_codpropietario2 = tk.Label(modificarcancion, text="Nombre", bg=color, fg=color2, font=fuente)
    codpropietario_entry2 = tk.Entry(modificarcancion, bg=color2, fg=color, font=fuente)    
    input2.pack(pady=(10))
    input_codpropietario2.pack(pady=(10))
    codpropietario_entry2.pack(pady=(10))   
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10)) 
    boton_buscar = tk.Button(modificarcancion, text="Modificar", command=lambda: auxiliarmodcancion(codpropietario_entry.get(),codpropietario_entry2.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    modificarcancion.mainloop()
#######################################################MODIFICAR ADMINISTRADOR###########################################
def modifica_admin(codadmin, nombre):
    codadmin = str(codadmin)
    nombre = str(nombre)
    for codigo in dicadmin:
        if codadmin == codigo:
            dicadmin[codadmin]['nombreadmin']=nombre
            modificaradmin.destroy()
            messagebox.showinfo("Resultado", f"El Nombre del administrador con ese código ahora es {dicadmin[codigo]['nombreadmin']}")
            break
    else:
        messagebox.showinfo("Resultado", "Canción Inexistente")
def auxiliarmodadmin(codadmin, nombre):
    try:
        codadmin = int(codadmin)
        modifica_admin(codadmin, nombre)
    except ValueError:
        messagebox.showerror("Error", "El codadmin debe ser un número entero. Intenta de nuevo.")
def modificar_admin():
    global modificaradmin
    modificaradmin = tk.Toplevel()
    modificaradmin.title("Modificar Administrador")
    modificaradmin.geometry("600x400")
    modificaradmin.resizable(False, False)
    modificaradmin.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(modificaradmin, text="Modificar Nombre de un Administrador", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(modificaradmin, text="Codadmin", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(modificaradmin, bg=color2, fg=color, font=fuente)
    input_codpropietario2 = tk.Label(modificaradmin, text="Nombre", bg=color, fg=color2, font=fuente)
    codpropietario_entry2 = tk.Entry(modificaradmin, bg=color2, fg=color, font=fuente)    
    input2.pack(pady=(10))
    input_codpropietario2.pack(pady=(10))
    codpropietario_entry2.pack(pady=(10))   
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10)) 
    boton_buscar = tk.Button(modificaradmin, text="Modificar", command=lambda: auxiliarmodadmin(codpropietario_entry.get(),codpropietario_entry2.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    modificaradmin.mainloop()
######################################################################################################################
#######################################################REPRODUCCION####################################################
######################################################################################################################
def reproduccion_comando():
    global reproducciontop
    reproducciontop = tk.Toplevel()
    reproducciontop.title("Modificar Administrador")
    reproducciontop.geometry("600x400")
    reproducciontop.resizable(False, False)
    reproducciontop.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(reproducciontop, text="Añadir cancion a la cola de reproducción", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(reproducciontop, text="Codcanción", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(reproducciontop, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10)) 
    boton_buscar = tk.Button(reproducciontop, text="Añadir", command=lambda: auxiliareprocola(codpropietario_entry.get(), coladereproducciontop), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    reproducciontop.mainloop()

#################Reproduccion(Kevin)######################################
def cargar_musica20():
    global cancion_actual, canciones, lista_canciones, reproductor

    if not cola:
        messagebox.showinfo("Error", "La cola de reproducción está vacía.")
        return

    # Limpiar la lista de canciones actual
    canciones.clear()
    
    # Agregar las canciones de la cola a la lista de canciones del reproductor
    for cancion in cola:
        codcancion = cancion[0]
        canciones.append(codcancion)
    
    for codcancion in canciones:
        nombrecan = "No asignado"
        nombreart = "No asignado"
        
        if str(codcancion) in diccanciones:
            nombrecan = diccanciones[str(codcancion)]['nombrecan']
            codartista = diccanciones[str(codcancion)]['codart']
            
            if str(codartista) in dicartista:
                nombreart = dicartista[str(codartista)]['nombreart']
        
    
    # Seleccionar la primera canción de la lista para reproducir
    cancion_actual = cola[0][0] 
def cargar_musica():
    global cancion_actual, canciones, lista_canciones, reproductor

    if not cola:
        messagebox.showinfo("Error", "La cola de reproducción está vacía.")
        reproductor.destroy()
        return

    # Limpiar la lista de canciones actual
    canciones.clear()
    lista_canciones.delete(0, 'end')
    
    # Agregar las canciones de la cola a la lista de canciones del reproductor
    for cancion in cola:
        codcancion = cancion[0]
        canciones.append(codcancion)
    
    for codcancion in canciones:
        nombrecan = "No asignado"
        nombreart = "No asignado"
        
        if str(codcancion) in diccanciones:
            nombrecan = diccanciones[str(codcancion)]['nombrecan']
            codartista = diccanciones[str(codcancion)]['codart']
            
            if str(codartista) in dicartista:
                nombreart = dicartista[str(codartista)]['nombreart']
        
        lista_canciones.insert("end", f" {codcancion} | {nombrecan} - {nombreart}")
    
    # Seleccionar la primera canción de la lista para reproducir
    lista_canciones.selection_set(0)
    cancion_actual = cola[0][0] 

    

def reproducir_musica():
    global cancion_actual, pausado, historial, cola

    if not cola:
        messagebox.showinfo("Error", "La cola de reproducción está vacía.")
        return

    if not pausado:
        # Buscar la información de la canción actual en la cola
        for cancion_info in cola:
            if cancion_info[0] == cancion_actual:
                # Cargar la canción actual desde la cola
                pygame.mixer.music.load(cancion_info[0] + ".mp3")
                pygame.mixer.music.play()
                historial.append(int(cancion_info[0]))
                break
    else:
        pygame.mixer.music.unpause()
        pausado = False


def siguiente_musica():
    global cancion_actual, lista_canciones,canciones
    if cancion_actual in canciones:
        index_actual = canciones.index(cancion_actual)
        if index_actual < len(canciones) - 1:
            cancion_actual = canciones[index_actual + 1]
            lista_canciones.selection_clear(0, END)
            lista_canciones.selection_set(index_actual + 1)
            lista_canciones.see(index_actual + 1)
            reproducir_musica()

def pausar_musica():
    global pausado
    pygame.mixer.music.pause()
    pausado = True

def anterior_musica20():
    global cancion_actual, lista_canciones,canciones
    if cancion_actual in canciones:
        index_actual = canciones.index(cancion_actual)
        if index_actual > 0:
            cancion_actual = canciones[index_actual - 1]
            reproducir_musica()

def siguiente_musica20():
    global cancion_actual, lista_canciones,canciones
    if cancion_actual in canciones:
        index_actual = canciones.index(cancion_actual)
        if index_actual < len(canciones) - 1:
            cancion_actual = canciones[index_actual + 1]
            reproducir_musica()

def anterior_musica():
    global cancion_actual, lista_canciones,canciones
    if cancion_actual in canciones:
        index_actual = canciones.index(cancion_actual)
        if index_actual > 0:
            cancion_actual = canciones[index_actual - 1]
            lista_canciones.selection_clear(0, END)
            lista_canciones.selection_set(index_actual - 1)
            lista_canciones.see(index_actual - 1)
            reproducir_musica()


def reproduccion():
    global reproductor, canciones, lista_canciones
    reproductor = tk.Toplevel()
    reproductor.title("Reproductor de Música")
    reproductor.geometry("500x370")
    reproductor.resizable(False, False)
    reproductor.configure(bg=color)

    menubar = Menu(reproductor)
    reproductor.config(menu=menubar)
    menubar.add_command(label="Cargar música", command=cargar_musica)

    lista_canciones = Listbox(reproductor, bg=color, fg=color2, width=100, height=15)
    lista_canciones.pack()

    play_btn_image = PhotoImage(file=play_btn_file).subsample(tamaño*2)
    pause_btn_image = PhotoImage(file=pause_btn_file).subsample(tamaño*2)
    next_btn_image = PhotoImage(file=next_btn_file).subsample(tamaño*2)
    prev_btn_image = PhotoImage(file=prev_btn_file).subsample(tamaño*2)

    control_frame = Frame(reproductor)
    control_frame.pack()

    play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=reproducir_musica)
    pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pausar_musica)
    next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=lambda: siguiente_musica())
    previous_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=lambda: anterior_musica())

    play_btn.grid(row=0, column=1, padx=7, pady=10)
    pause_btn.grid(row=0, column=2, padx=7, pady=10)
    next_btn.grid(row=0, column=3, padx=7, pady=10)
    previous_btn.grid(row=0, column=0, padx=7, pady=10)

    reproductor.mainloop()
#######################################################COLA DE REPRODUCCION##############################################
def buscacancioncola(codplaylist3,codgenero,codartista,codalbum,codcancion,ventana):
    global cola
    codplaylist10 = str(codplaylist3)
    codartista = str(codartista)
    codalbum = str(codalbum)
    codgenero = str(codgenero)
    codcancion=str(codcancion)
    codcancion_existe = False
    codartista_existe = False
    codalbum_existe = False
    codplaylist_existe = False
    codgenero_existe = False
    codalbum_existe = False
    codalbum_funciona=False
    if len(cola)<5:
        for clave_can in diccanciones:
            if codcancion == clave_can:
                codcancion_existe = True
                codartistadecan=diccanciones[codcancion]['codart']
                codplaylistdecan=diccanciones[codcancion]['codplaylist']
                codgenerodecan=diccanciones[codcancion]['codgenero']
                codalbumdecan=diccanciones[codcancion]['codalbum']
                break
        if codcancion_existe:
            if codartistadecan in dicartista:
                if codartistadecan==codartista:
                    codartista_existe = True

            if codalbumdecan in dicalbum:
                if codalbumdecan==codalbum:
                    codalbum_existe = True
                
            if codgenerodecan in dicgenero:
                if codgenerodecan==codgenero:
                    codgenero_existe = True
                    
            if codplaylistdecan in dicplaylist:
                if codplaylistdecan==codplaylist10:
                    codplaylist_existe = True

            if codcancion in diccanciones:
                nombrecan=diccanciones[codcancion]['nombrecan']
                cancion_info = diccanciones[codcancion]
                codartista = cancion_info['codart']
                codalbum = cancion_info['codalbum']
                codplaylist = cancion_info['codplaylist']
                if codartista in dicartista:
                    nombreart = dicartista[codartista]['nombreart']
                if codalbum in dicalbum:
                    album_info = dicalbum[codalbum]
                    albumpertenece = album_info['codart'] 
                if codalbum_existe and codartista_existe:
                    if albumpertenece != codartista:
                        codalbum_funciona = False
                    else:
                        codalbum_funciona = True
        if codcancion_existe and codartista_existe and codalbum_existe and codplaylist_existe and codalbum_funciona and codgenero_existe:
            cola.append([codcancion, cancion_info['nombrecan'], nombreart])
            messagebox.showinfo("Resultado",f"{nombrecan} añadida a cola")
            coladereproducciontop.destroy()
        elif not codcancion_existe:
            messagebox.showinfo("Resultado",f"El Codcanción proporcionado no esta ligado a una canción, vuelva a intentarlo")
        elif codcancion_existe and (not codartista_existe or not codalbum_existe or not codplaylist_existe or not codalbum_funciona or not codgenero_existe):
            messagebox.showinfo("Resultado",f"Los últimos códigos proporcionados no están ligados con esta canción, vuelva a intentarlo")
        else:
            messagebox.showinfo("Resultado",f"El Codcanción proporcionado no esta ligado a una canción, vuelva a intentarlo")
    else:
        messagebox.showerror("Máximo Alcanzado","Ya tiene 5 canciones en cola")
        coladereproducciontop.destroy()
        
def auxiliareprocola(codplaylist,codgenero,codartista,codalbum,codcancion,ventana):
    try:
        codcancion = int(codcancion)
        codplaylist = int(codplaylist)
        codcodartista = int(codartista)
        codgenero = int(codgenero)
        codalbum = int(codalbum)
        buscacancioncola(codplaylist,codgenero,codartista,codalbum,codcancion,ventana)
    except ValueError:
        messagebox.showerror("Error", "Los códigos deben ser un número entero. Intenta de nuevo.")
        
def coladereproduccion_comando():
    global coladereproducciontop
    coladereproducciontop = tk.Toplevel()
    coladereproducciontop.title("Cola de reproducción")
    coladereproducciontop.geometry("600x700")
    coladereproducciontop.resizable(False, False)
    coladereproducciontop.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(coladereproducciontop, text="Añadir cancion a la cola de reproducción", bg=color, fg=color2, font=fuenteg)
    input_codplaylist = tk.Label(coladereproducciontop, text="Codplaylist", bg=color, fg=color2, font=fuente)
    codplaylist_entry = tk.Entry(coladereproducciontop, bg=color2, fg=color, font=fuente)
    input_codgenero = tk.Label(coladereproducciontop, text="Codgenero", bg=color, fg=color2, font=fuente)
    codgenero_entry = tk.Entry(coladereproducciontop, bg=color2, fg=color, font=fuente)
    input_codartista = tk.Label(coladereproducciontop, text="Codartista", bg=color, fg=color2, font=fuente)
    codartista_entry = tk.Entry(coladereproducciontop, bg=color2, fg=color, font=fuente)
    input_codalbum = tk.Label(coladereproducciontop, text="Codalbum", bg=color, fg=color2, font=fuente)
    codalbum_entry = tk.Entry(coladereproducciontop, bg=color2, fg=color, font=fuente)
    input_codcancion = tk.Label(coladereproducciontop, text="Codcancion", bg=color, fg=color2, font=fuente)
    codcancion_entry = tk.Entry(coladereproducciontop, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codplaylist.pack(pady=(10))
    codplaylist_entry.pack(pady=(10))
    input_codgenero.pack(pady=(10))
    codgenero_entry.pack(pady=(10))
    input_codartista.pack(pady=(10))
    codartista_entry.pack(pady=(10))
    input_codalbum.pack(pady=(10))
    codalbum_entry.pack(pady=(10))
    input_codcancion.pack(pady=(10))
    codcancion_entry.pack(pady=(10))
    boton_buscar = tk.Button(coladereproducciontop, text="Añadir", command=lambda: auxiliareprocola(codplaylist_entry.get(),codgenero_entry.get(),codartista_entry.get(),codalbum_entry.get(),codcancion_entry.get(),coladereproducciontop), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    coladereproducciontop.mainloop()
######################################################################################################################
#######################################################REPORTES#######################################################
######################################################################################################################
def reporte_propietarios():
    with open("reportepro.txt", "a") as file:
        file.write("------------------------------------------Estos son todos los propietarios------------------------------------------"+ "\n")
        for clave in dicpropietarios:
            nombre_pro = dicpropietarios[clave]['nombrepro']
            file.write("|"+"El codigo y nombre de este propietario es:"+"|"+ clave +"|" +nombre_pro+"|"+"\n")
        file.write("-----------------------------------------------------------------------------------------------------------\n")
    messagebox.showinfo("Reporte generado", "Los propietarios se han guardado en reportepro.txt")

def reportes_comando():
    pass
########################################################Reporte Playlist#######################################
def reporte_playlists():
    global ventana2
    ventana2 = tk.Toplevel()
    ventana2.title("Reporte Playlist")
    ventana2.geometry("600x400")
    ventana2.resizable(False, False)
    ventana2.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input2 = tk.Label(ventana2, text="Generar Reporte Playlist De un Propietario", bg=color, fg=color2, font=fuenteg)
    input_codpropietario = tk.Label(ventana2, text="Codpropietario", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(ventana2, bg=color2, fg=color, font=fuente)
    input2.pack(pady=(10))
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10))
    boton_buscar = tk.Button(ventana2, text="Generar", command=lambda: auxiliar_reporte_playlists(codpropietario_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    ventana2.mainloop()
def auxiliar_reporte_playlists(codpropietario):
    try:
        codpropietario = int(codpropietario)
        generacion_reporte_playlists(codpropietario)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero. Intenta de nuevo.")
        ventana2.destroy()
def generacion_reporte_playlists(codpro):
    global ventana2
    codpro = str(codpro)
    codpro_existe = False
    for codplaylist in dicplaylist:
        if dicplaylist[codplaylist]['codpropietario'] == codpro:
            codpro_existe = True
    if codpro_existe:
        with open("reporteplaylist.txt", "a") as file:
            file.write("-----------------Estas son todas las playlist del propietario:" + codpro+"------------------"+ "\n")
            for codplaylist in dicplaylist:
                if dicplaylist[codplaylist]['codpropietario'] == codpro:
                    nombre = dicplaylist[codplaylist]['nombreplay']
                    file.write("|"+"Codplaylist:"+ codplaylist +"|" + "Nombre de la playlist:" +"|"+nombre+"|" + "\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Reporte generado", "Las playlists del propietario fueron añadidos a reporteplaylist.txt")
        ventana2.destroy()
    else:
        messagebox.showinfo("Error", "No existe una playlist con ese código de propietario")
        ventana2.destroy()

#####################################################Reporte Generos#######################
def reporte_generos():
    with open("reportegen.txt", "a") as file:
        file.write("------------------------------------------Estos son todos los géneros------------------------------------------" + "\n")
        for clave in dicgenero:
            nombre_gen = dicgenero[clave]['nombregen']
            file.write("|" + "El código y nombre de este género es:" + "|" + clave + "|" + nombre_gen + "|" + "\n")
        file.write("-----------------------------------------------------------------------------------------------------------\n")
    messagebox.showinfo("Resultado","Los géneros se han guardado en reportegen.txt")
############################################################Reporte artistas de un genero###############################################
def reporte_artistas():
    global ventana_artistas
    ventana_artistas = tk.Toplevel()
    ventana_artistas.title("Reporte de Artistas por Género")
    ventana_artistas.geometry("600x400")
    ventana_artistas.resizable(False, False)
    ventana_artistas.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input1 = tk.Label(ventana_artistas, text="Generar Reporte de Artistas", bg=color, fg=color2, font=fuenteg)
    input_codgenero = tk.Label(ventana_artistas, text="Codgenero", bg=color, fg=color2, font=fuente)
    cod_genero_entry = tk.Entry(ventana_artistas, bg=color2, fg=color, font=fuente)
    input1.pack(pady=(10))
    input_codgenero.pack(pady=(10))
    cod_genero_entry.pack(pady=(10))
    boton_generar = tk.Button(ventana_artistas, text="Generar", command=lambda: auxiliar_reporte_artistas(cod_genero_entry.get()), bg=color, fg=color2, font=fuente)
    boton_generar.pack(pady=20)
    ventana_artistas.mainloop()

def auxiliar_reporte_artistas(cod_genero):
    try:
        cod_genero = int(cod_genero)
        generar_reporte_artistas(cod_genero)
    except ValueError:
        messagebox.showerror("Error", "El código del género debe ser un número entero. Intenta de nuevo.")

def generar_reporte_artistas(codgen):
    global ventana_artistas
    codgen = str(codgen)
    codgenero_existe = False
    for codgenero in dicgenero:
        if codgenero == codgen:
            codgenero_existe = True
            break
    if codgenero_existe:
        with open("reporte_artistas.txt", "a") as file:
            file.write("----------------- Estos son todos los artistas del género: " + codgen + " ------------------\n")
            for codartista in dicartista:
                if dicartista[codartista]['codgenero'] == codgen:
                    nombre = dicartista[codartista]['nombreart']
                    file.write("| Codartista: " + codartista + " | Nombre del artista: " + nombre + " |\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Reporte generado", "Los artistas del género fueron añadidos al reporte_artistas.txt")
        ventana_artistas.destroy()
    else:
        messagebox.showinfo("Error", "No existen artistas asociados a ese código de género")
        ventana_artistas.destroy()




#####################################################################################################
# Reporte de albumes de un artista
#####################################################################################################

def reporte_albumes():
    global ventana_albumes
    ventana_albumes = tk.Toplevel()
    ventana_albumes.title("Reporte de Álbumes por Artista")
    ventana_albumes.geometry("600x400")
    ventana_albumes.resizable(False, False)
    ventana_albumes.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input1 = tk.Label(ventana_albumes, text="Generar Reporte de Álbumes", bg=color, fg=color2, font=fuenteg)
    input_codartista = tk.Label(ventana_albumes, text="Codartista", bg=color, fg=color2, font=fuente)
    cod_artista_entry = tk.Entry(ventana_albumes, bg=color2, fg=color, font=fuente)
    input1.pack(pady=(10))
    input_codartista.pack(pady=(10))
    cod_artista_entry.pack(pady=(10))
    boton_generar = tk.Button(ventana_albumes, text="Generar", command=lambda: auxiliar_reporte_albumes(cod_artista_entry.get()), bg=color, fg=color2, font=fuente)
    boton_generar.pack(pady=20)
    ventana_albumes.mainloop()

def auxiliar_reporte_albumes(cod_artista):
    try:
        cod_artista = int(cod_artista)
        generar_reporte_albumes(cod_artista)
    except ValueError:
        messagebox.showerror("Error", "El código del artista debe ser un número entero. Intenta de nuevo.")

def generar_reporte_albumes(codart):
    global ventana_albumes
    codart = str(codart)
    codartista_existe = False
    for codartista in dicartista:
        if codartista == codart:
            codartista_existe = True
    if codartista_existe:
        with open("reporte_albumes.txt", "a") as file:
            file.write("----------------- Estos son todos los álbumes del artista: " + codart + " ------------------\n")
            for codalbum in dicalbum:
                if dicalbum[codalbum]['codart'] == codart:
                    nombre = dicalbum[codalbum]['nombrealbum']
                    file.write("| Codalbum: " + codalbum + " | Nombre del álbum: " + nombre + " |\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Reporte generado", "Los álbumes del artista fueron añadidos al reporte_albumes.txt")
        ventana_albumes.destroy()
    else:
        messagebox.showinfo("Error", "No existe ningún álbum de ese artista")
        ventana_albumes.destroy()

#####################################################################################################
# Reporte de canciones de un artista
#####################################################################################################

def reporte_canciones():
    global ventana_canciones
    ventana_canciones = tk.Toplevel()
    ventana_canciones.title("Reporte de Canciones por Artista")
    ventana_canciones.geometry("600x400")
    ventana_canciones.resizable(False, False)
    ventana_canciones.configure(bg=color)
    fuente = ("Console", 14)
    fuenteg = ("Console", 18)
    input1 = tk.Label(ventana_canciones, text="Generar Reporte de Canciones", bg=color, fg=color2, font=fuenteg)
    input_codartista = tk.Label(ventana_canciones, text="Codartista", bg=color, fg=color2, font=fuente)
    cod_artista_entry = tk.Entry(ventana_canciones, bg=color2, fg=color, font=fuente)
    input1.pack(pady=(10))
    input_codartista.pack(pady=(10))
    cod_artista_entry.pack(pady=(10))
    boton_generar = tk.Button(ventana_canciones, text="Generar", command=lambda: auxiliar_reporte_canciones(cod_artista_entry.get()), bg=color, fg=color2, font=fuente)
    boton_generar.pack(pady=20)
    ventana_canciones.mainloop()

def auxiliar_reporte_canciones(cod_artista):
    global ventana_canciones
    try:
        cod_artista = int(cod_artista)
        generar_reporte_canciones(cod_artista)
    except ValueError:
        messagebox.showerror("Error", "El código del artista debe ser un número entero. Intenta de nuevo.")

def generar_reporte_canciones(codart):
    global ventana_canciones
    
    codart = str(codart)
    codartista_existe = False
    for codartista in dicartista:
        if codartista == codart:
            codartista_existe = True
    if codartista_existe:
        with open("reporte_canciones.txt", "a") as file:
            file.write("----------------- Estas son todas las canciones del artista: " + codart + " ------------------\n")
            for codcancion in diccanciones:
                if diccanciones[codcancion]['codart'] == codart:
                    nombre = diccanciones[codcancion]['nombrecan']
                    file.write("| Codcancion: " + codcancion + " | Nombre de la canción: " + nombre + " |\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Reporte generado", "Las canciones del artista fueron añadidas al reporte_canciones.txt")
        ventana_canciones.destroy()
    else:
        messagebox.showinfo("Error", "No existen canciones asociadas a ese código de artista")
        ventana_canciones.destroy()
##############################################Reporte cancion mas reproducida##################################
def reporte_cancion_mas_reproducida():
    if historial:
        contador = 0
        temp = 0
        indice = 0
        for x in range(len(historial)):
            temp = historial.count(historial[x])
            if temp > contador:
                contador = temp
                indice = x
        codcancion_frecuente = str(historial[indice])
        for codcancion in diccanciones:
            if codcancion == codcancion_frecuente:
                nombre_codcancion = diccanciones[codcancion]['nombrecan']
                break
        with open("reporte_cancion_mas_reproducida.txt", "a") as file:
            file.write("------------------------------------------ Canción más reproducida ------------------------------------------\n")
            file.write("| Código y nombre de la canción más reproducida: |" + codcancion_frecuente + "| " + nombre_codcancion + "| | Reproducciones: |" + str(contador) + "|\n")
            file.write("------------------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Reporte generado", "Se agregó la canción más reproducida a reporte_cancion_mas_reproducida.txt")
    else:
        messagebox.showinfo("Error", "No se puede crear el reporte, no hay canciones reproducidas.")
        
##########################################################Artista mayor canciones##################################
def reporte_artista_mayor_canciones():
    lista_codart = []
    for sublista in diccanciones:
        lista_codart.append(diccanciones[sublista]['codart'])
    if lista_codart:
        contador = 0
        temp = 0
        indice = 0
        for x in range(len(lista_codart)):
            temp = lista_codart.count(lista_codart[x])
            if temp > contador:
                contador = temp
                indice = x
        codart_frecuente = lista_codart[indice]
        for codartista in dicartista:
            if codartista == codart_frecuente:
                nombre_codart = dicartista[codartista]['nombreart']
                break
        if dicartista:
            with open("reporte_artista_mayor_canciones.txt", "a") as file:
                file.write("------------------------------------------ Artista con más canciones ------------------------------------------\n")
                file.write("| Código y nombre del artista con más canciones: |" + codart_frecuente + "|" + nombre_codart + "| | Número de Canciones: |" + str(contador) + "|\n")
                file.write("------------------------------------------------------------------------------------------------------------------\n")
            messagebox.showinfo("Resultado","Se agregó el artista con más canciones a reporte_artista_mayor_canciones.txt")
        else:
           messagebox.showinfo("Resultado","No hay ningún artista para hacer el reporte")
    else:
        messagebox.showinfo("Resultado","No hay ninguna canción para hacer el reporte")

def reporte_album_mayor_canciones():
    lista_codalbum = []
    for codcancion in diccanciones:
        lista_codalbum.append(diccanciones[codcancion]['codalbum'])

    if lista_codalbum:
        contador = 0
        temp = 0
        indice = 0
        for x in range(len(lista_codalbum)):
            temp = lista_codalbum.count(lista_codalbum[x])
            if temp > contador:
                contador = temp
                indice = x
        
        codalbum_frecuente = lista_codalbum[indice]
        
        for codalbum in dicalbum:
            if codalbum == codalbum_frecuente:
                nombre_codalbum = dicalbum[codalbum]['nombrealbum']
                break
        
        with open("reporte_album_mayor_canciones.txt", "a") as file:
            file.write("------------------------------------------ Album con más canciones ------------------------------------------\n")
            file.write("| Código y nombre del álbum con más canciones: |" + codalbum_frecuente + "|" + nombre_codalbum + "| | Número de Canciones: |" + str(contador) + "|\n")
            file.write("------------------------------------------------------------------------------------------------------------------\n")
        
        messagebox.showinfo("Resultado", "Se agregó el álbum con más canciones al reporte_album_mayor_canciones.txt")

    else:
        messagebox.showinfo("Resultado", "No hay ninguna canción para hacer el reporte")




def reporte_genero_mas_solicitado():
    if historial:
        contador = 0
        temp = 0
        indice = 0
        for x in range(len(historial)):
            temp = historial.count(historial[x])
            if temp > contador:
                contador = temp
                indice = x
        
        codcancion_frecuente = str(historial[indice])
        
        for codcancion in diccanciones:
            if codcancion == codcancion_frecuente:
                codgenero = diccanciones[codcancion]['codgenero']
                break
        
        for codgen in dicgenero:
            if codgen == codgenero:
                nombre_genero = dicgenero[codgen]['nombregen']
                break
        
        with open("reporte_genero_mas_solicitado.txt", "a") as file:
            file.write("------------------------------------------ Género más solicitado ------------------------------------------\n")
            file.write("| Código y nombre del género más solicitado: |" + codgenero + "|" + nombre_genero + "|\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        
        messagebox.showinfo("Reporte generado", "Se agregó el género más solicitado a reporte_genero_mas_solicitado.txt")
    
    else:
        messagebox.showinfo("Error", "No se puede crear el reporte, no hay canciones reproducidas.")



def reporte_propietario_mayor_playlist():
    lista_codpropietarios = []
    bandera = True

    # Crear la lista de códigos de propietarios
    for codplaylist in dicplaylist:
        lista_codpropietarios.append(int(dicplaylist[codplaylist]['codpropietario']))
    
    if lista_codpropietarios:
        contador = 0
        temp = 0
        indice = 0

        # Contar la frecuencia de cada código de propietario
        for x in range(len(lista_codpropietarios)):
            temp = lista_codpropietarios.count(lista_codpropietarios[x])
            if temp > contador:
                contador = temp
                indice = x
        
        codpropietario_frecuente = str(lista_codpropietarios[indice])

        # Encontrar el nombre del propietario más frecuente
        for codpropietario in dicpropietarios:
            if codpropietario == codpropietario_frecuente:
                nombre_propietario = dicpropietarios[codpropietario]['nombrepro']
                bandera = True
                break
            else:
                bandera = False
        
        # Si se encontró el propietario, escribir el reporte en el archivo
        if bandera:
            with open("reporte_propietario_mayor_playlist.txt", "a") as file:
                file.write("------------------------------------------ Propietario con más playlists ------------------------------------------\n")
                file.write("| Código y nombre del propietario con más playlists: |" + codpropietario_frecuente + "|" + nombre_propietario + "| Número de playlists: |" + str(contador) + "|\n")
                file.write("------------------------------------------------------------------------------------------------------------------------------\n")
            
            messagebox.showinfo("Reporte generado", "Se agregó el propietario con más playlists a reporte_propietario_mayor_playlist.txt")
        else:
            messagebox.showinfo("Error", "No se encontró el propietario en el diccionario de propietarios.")
    else:
        messagebox.showinfo("Error", "No se puede crear el reporte, no hay playlists en el diccionario.")
        
def reporte_album_mas_solicitado():
    if historial:
        contador = 0
        temp = 0
        indice = 0

        # Contar la frecuencia de cada canción en el historial
        for x in range(len(historial)):
            temp = historial.count(historial[x])
            if temp > contador:
                contador = temp
                indice = x

        # Código de la canción más frecuente en el historial
        codcancion_frecuente = str(historial[indice])

        # Encontrar el código del álbum correspondiente a la canción más frecuente
        for codcancion in diccanciones:
            if codcancion == codcancion_frecuente:
                codalbum = diccanciones[codcancion]['codalbum']
                break

        # Encontrar el nombre del álbum correspondiente al código de álbum
        for clave in dicalbum:
            if codalbum == clave:
                nombre_album = dicalbum[clave]['nombrealbum']
                break

        # Escribir el reporte en el archivo
        with open("reporte_album_mas_solicitado.txt", "a") as file:
            file.write("------------------------------------------ Álbum más solicitado ------------------------------------------\n")
            file.write("| Código y nombre del álbum más solicitado: |" + codalbum + "|" + nombre_album + "|\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        
        messagebox.showinfo("Reporte generado", "Se agregó el álbum más solicitado a reporte_album_mas_solicitado.txt")
    else:
        messagebox.showinfo("Error", "No se puede crear el reporte, no hay canciones reproducidas.")





def reporte_playlist_mayor_canciones():
    lista_canciones = []

    # Crear la lista de códigos de playlists desde diccanciones
    for sublista in diccanciones:
        lista_canciones.append(diccanciones[sublista]['codplaylist'])

    if lista_canciones:
        contador = 0
        temp = 0
        indice = 0

        # Contar la frecuencia de cada código de playlist
        for x in range(len(lista_canciones)):
            temp = lista_canciones.count(lista_canciones[x])
            if temp > contador:
                contador = temp
                indice = x

        # Código de la playlist más frecuente
        codcan_frecuente = lista_canciones[indice]

        # Encontrar el nombre de la playlist correspondiente al código más frecuente
        for codplaylist in dicplaylist:
            if codplaylist == codcan_frecuente:
                nombre_codplaylist = dicplaylist[codplaylist]['nombreplay']
                break

        # Escribir el reporte en el archivo
        with open("reporte_playlist_mayor_canciones.txt", "a") as file:
            file.write("------------------------------------------ Playlist con más canciones ------------------------------------------\n")
            file.write("| Código y nombre de la playlist con más canciones: |" + codcan_frecuente + "|" + nombre_codplaylist + "| Número de Canciones: |" + str(contador) + "|\n")
            file.write("----------------------------------------------------------------------------------------------------------------------------\n")

        messagebox.showinfo("Reporte generado", "Se agregó la playlist con más canciones a reporte_playlist_mayor_canciones.txt")
    else:
        messagebox.showinfo("Error", "No se puede crear el reporte, no hay canciones en las playlists.")

def reporte_genero_mayor_artistas():
    lista_generos = []

    # Crear la lista de códigos de géneros desde dicartista
    for sublista in dicartista:
        lista_generos.append(dicartista[sublista]['codgenero'])

    if lista_generos:
        contador = 0
        temp = 0
        indice = 0

        # Contar la frecuencia de cada código de género
        for x in range(len(lista_generos)):
            temp = lista_generos.count(lista_generos[x])
            if temp > contador:
                contador = temp
                indice = x

        # Código del género más frecuente
        codgenero_frecuente = lista_generos[indice]

        if contador > 1:
            # Encontrar el nombre del género correspondiente al código más frecuente
            for codartista in dicartista:
                if dicartista[codartista]['codgenero'] == codgenero_frecuente:
                    nombre_codgenero = dicgenero[codgenero_frecuente]['nombregen']
                    break

            # Escribir el reporte en el archivo
            with open("reporte_genero_mayor_artistas.txt", "a") as file:
                file.write("------------------------------------------ Género con más artistas ------------------------------------------\n")
                file.write("| Código y nombre del género con más artistas: |" + codgenero_frecuente + "|" + nombre_codgenero + "| Número de artistas: |" + str(contador) + "|\n")
                file.write("-------------------------------------------------------------------------------------------------------------\n")

            messagebox.showinfo("Reporte generado", "Se agregó el género con más artistas a reporte_genero_mayor_artistas.txt")
        else:
            messagebox.showinfo("Información", "Todos los géneros tienen la misma cantidad de artistas.")
    else:
        messagebox.showinfo("Error", "No se puede crear el reporte, no hay géneros en los artistas.")




def reporte_genero_mayor_albumes():
    lista_artista = []

    # Crear la lista de códigos de artistas desde dicalbum
    for sublista in dicalbum:
        lista_artista.append(dicalbum[sublista]['codart'])

    if lista_artista:
        contador = 0
        temp = 0
        indice = 0

        # Contar la frecuencia de cada código de artista
        for x in range(len(lista_artista)):
            temp = lista_artista.count(lista_artista[x])
            if temp > contador:
                contador = temp
                indice = x

        # Código del artista más frecuente
        codartista_frecuente = lista_artista[indice]

        if contador > 1:
            # Encontrar el código del género correspondiente al artista más frecuente
            for codartista in dicartista:
                if codartista == codartista_frecuente:
                    codgenero = dicartista[codartista]['codgenero']
                    for clave in dicgenero:
                        if codgenero == clave:
                            nombre_codgenero = dicgenero[codgenero]['nombregen']
                            break

            # Escribir el reporte en el archivo
            with open("reporte_genero_mayor_albumes.txt", "a") as file:
                file.write("------------------------------------------ Género con más álbumes ------------------------------------------\n")
                file.write("| Código y nombre del género con más álbumes: |" + codgenero + "|" + nombre_codgenero + "| Número de álbumes: |" + str(contador) + "|\n")
                file.write("-------------------------------------------------------------------------------------------------------------\n")

            messagebox.showinfo("Reporte generado", "Se agregó el género con más álbumes a reporte_genero_mayor_albumes.txt")
        else:
            messagebox.showinfo("Información", "Todos los géneros tienen la misma cantidad de álbumes.")
    else:
        messagebox.showinfo("Error", "No se puede crear el reporte, no hay álbumes en los artistas.")

def reporte_artista_mayor_albumes():
    lista_artista = []

    # Crear la lista de códigos de artistas desde dicalbum
    for sublista in dicalbum:
        lista_artista.append(dicalbum[sublista]['codart'])

    if lista_artista:
        contador = 0
        temp = 0
        indice = 0

        # Contar la frecuencia de cada código de artista
        for x in range(len(lista_artista)):
            temp = lista_artista.count(lista_artista[x])
            if temp > contador:
                contador = temp
                indice = x

        # Código del artista más frecuente
        codartista_frecuente = lista_artista[indice]

        if contador > 1:
            # Encontrar el nombre del artista correspondiente al código más frecuente
            for codartista in dicartista:
                if codartista == codartista_frecuente:
                    nombre_codartista = dicartista[codartista]['nombreart']
                    break

            # Escribir el reporte en el archivo
            with open("reporte_artista_mayor_albumes.txt", "a") as file:
                file.write("------------------------------------------ Artista con más álbumes ------------------------------------------\n")
                file.write("| Código y nombre del artista con más álbumes: |" + codartista_frecuente + "|" + nombre_codartista + "| Número de álbumes: |" + str(contador) + "|\n")
                file.write("-------------------------------------------------------------------------------------------------------------\n")

            messagebox.showinfo("Reporte generado", "Se agregó el artista con más álbumes a reporte_artista_mayor_albumes.txt")
        else:
            messagebox.showinfo("Información", "Todos los artistas tienen la misma cantidad de álbumes.")
    else:
        messagebox.showinfo("Error", "No se puede crear el reporte, no hay álbumes en los artistas.")


def reporte_albumes_nunca_buscados():
    global busqueda_album2
    # Convertir busqueda_album a un conjunto para eliminar duplicados
    busqueda_album2 = set(busqueda_album2)

    # Crear una lista con todos los códigos de álbumes en dicalbum
    lista_codalbumes = []
    for codalbum in dicalbum:
        lista_codalbumes.append(codalbum)

    # Verificar si todos los álbumes fueron buscados
    if busqueda_album2 == set(lista_codalbumes):
        messagebox.showinfo("Resultado","No se puede crear el reporte, debido a que todos los álbumes fueron buscados.")
    else:
        # Abrir el archivo para escribir los álbumes que nunca fueron buscados
        with open("reporte_albumes_nunca_buscados.txt", "a") as file:
            file.write("------------------------------------------ Álbumes nunca buscados ------------------------------------------\n")
            for codalbum in dicalbum:
                if codalbum not in busqueda_album2:
                    file.write("| Código y nombre del álbum nunca buscado: |" + codalbum + "|" + dicalbum[codalbum]['nombrealbum'] + "|\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Resultado","Se agregó el álbum nunca buscado a reporte_albumes_nunca_buscados.txt")


def reporte_artistas_nunca_buscados():
    global busqueda_album2
    busqueda_album2 = set(busqueda_artistas2)
    lista_codartistas = set(dicartista.keys())

    if busqueda_artistas2 == lista_codartistas:
        messagebox.showinfo("Reporte", "No se puede crear el reporte, debido a que todos los artistas fueron buscados.")
    else:
        with open("reporte_artistas_nunca_buscados.txt", "a") as file:
            file.write("------------------------------------------ Artistas nunca buscados ------------------------------------------\n")
            for codartista in dicartista:
                if codartista not in busqueda_artistas2:
                    file.write("| Código y nombre del artista nunca buscado: |" + codartista + "|" + dicartista[codartista]['nombreart'] + "|\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Reporte generado", "Se agregaron los artistas nunca buscados a reporte_artistas_nunca_buscados.txt")



def reporte_propietarios_sin_playlist():
    propietarios_playlist = []
    for codplaylist in dicplaylist:
        propietarios_playlist.append(dicplaylist[codplaylist]['codpropietario'])
    propietarios_playlist_set = set(propietarios_playlist)

    if len(propietarios_playlist_set) == 0:
        messagebox.showinfo("Reporte", "No se puede crear el reporte, debido a que no hay propietarios.")
    else:
        with open("reporte_propietarios_sin_playlist.txt", "a") as file:
            file.write("------------------------------------------ Propietarios sin playlists ------------------------------------------\n")
            for codpropietario in dicpropietarios:
                if codpropietario not in propietarios_playlist_set:
                    file.write("| Código y nombre del propietario sin playlist: |" + codpropietario + "|" + dicpropietarios[codpropietario]['nombrepro'] + "|\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Reporte generado", "Se agregaron los propietarios sin playlist a reporte_propietarios_sin_playlists.txt")



def reporte_artistas_nunca_buscados():
    global busqueda_album2, busqueda_artistas2
    busqueda_album2 = set(busqueda_artistas2)
    lista_codartistas = set(dicartista.keys())

    if busqueda_artistas2 == lista_codartistas:
        messagebox.showinfo("Reporte", "No se puede crear el reporte, debido a que todos los artistas fueron buscados.")
    else:
        with open("reporte_artistas_nunca_buscados.txt", "a") as file:
            file.write("------------------------------------------ Artistas nunca buscados ------------------------------------------\n")
            for codartista in dicartista:
                if codartista not in busqueda_artistas2:
                    file.write("| Código y nombre del artista nunca buscado: |" + codartista + "|" + dicartista[codartista]['nombreart'] + "|\n")
            file.write("-----------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Reporte generado", "Se agregaron los artistas nunca buscados a reporte_artistas_nunca_buscados.txt")


def reporte_canciones_nunca_reproducidas():
    global historial
    historial = [str(cancion) for cancion in historial]
    lista_canciones = list(diccanciones.keys())
    noreproducida = False

    with open("reporte_canciones_nunca_reproducidas.txt", "a") as file:
        file.write("------------------------------------------ Canciones nunca reproducidas ------------------------------------------\n")
        for cancion in lista_canciones:
            if cancion not in historial:
                file.write("| Código y nombre de la canción nunca reproducida: |" + cancion + "|" + diccanciones[cancion]['nombrecan'] + "|\n")
                noreproducida = True
        file.write("-----------------------------------------------------------------------------------------------------------\n")

    if noreproducida:
        messagebox.showinfo("Reporte generado", "Se agregaron las canciones nunca reproducidas a reporte_canciones_nunca_reproducidas.txt")
    else:
        messagebox.showinfo("Reporte", "Todas las canciones fueron reproducidas")




######################################################################################################################
#######################################################FACTURAS#######################################################
######################################################################################################################
from datetime import datetime
def crearfacturaadmin(usuario, descuento, ventana):
    global facturasgeneradaadmin
    global sizedicfacturasadmin
    cont = buscarcuantasfacturadmins() 
    costo = 39.99 - (39.99 * (descuento / 100))
    nombre_archivo = f"{usuario}({cont}).txt"
    if not os.path.exists("Cobros"):
        os.makedirs("Cobros")
    rutadecobro = os.path.join("Cobros", nombre_archivo)
    facturasgeneradaadmin[sizedicfacturasadmin] = {'codpropietario': usuario, 'costo: $': round(costo, 2)}
    with open(rutadecobro, "w") as file:
        file.write("-------------------------------------------------------------------------------------------------------------\n")
        fecha = datetime.now() 
        file.write(f"|Fecha: {fecha.strftime('%Y-%m-%d %H:%M:%S')} | Usuario: {usuario} | Costo: ${round(costo, 2)} |\n")
        file.write("-------------------------------------------------------------------------------------------------------------\n")
    sizedicfacturasadmin += 1
    messagebox.showinfo("Exito", "Factura creada con exito.")
    if ventana and isinstance(ventana, tk.Tk):
        ventana.destroy()
def buscarcuantasfacturadmins():
    global facturasgeneradaadmin
    if facturasgeneradaadmin!={}:
        global cantidadasunombre2
        cantidadasunombre2=0
        user=str(usuarioparaveri)
        if sizedicfacturasadmin==0:
            return 0
        for i in facturasgeneradaadmin:
                if facturasgeneradaadmin[i]['codpropietario']==user:
                    cantidadasunombre2=cantidadasunombre2+1
        return cantidadasunombre2
    else:
        return 0
def tamanodedigitos(valor):
    global facturasgeneradaadmin
    num_str = str(valor)
    num_digitos = len(num_str)
    if num_digitos > 2:
        return False
    else:
        return True
def verificaciondeexistencias2(usuario,descuento, ventana):
    global facturasgeneradaadmin
    if tamanodedigitos(descuento):
        usuario=str(usuario)
        if descuento==0:
            descuento=0.000000000000001
        if usuario in dicpropietarios:
            crearfacturaadmin(usuario, descuento, ventana)
        else:
            messagebox.showerror("Error", "No existe ese usuario. Intenta de nuevo.")
    else:
        messagebox.showerror("Error", "El descuento no puede ser mayor a 99%. Intenta de nuevo.")
def validarint30(usuario_entrada, usuario_admin, ventana):
    global facturasgeneradaadmin
    try:
        usuario = int(usuario_entrada)
        descuento = int(usuario_admin)
        verificaciondeexistencias2(usuario, descuento, ventana) #Si es entero lo manda a revisar si necesita activacion
    except ValueError:
        messagebox.showerror("Error", "Los codigos debe ser un número entero. Intenta de nuevo.")
def generarfacturasadmin():
    global facturasgeneradaadmin
    global generarfacturasadmins
    generarfacturasadmins = tk.Tk()
    generarfacturasadmins.title("Generar Facturas")
    generarfacturasadmins.geometry("600x400")
    generarfacturasadmins.resizable(False, False)
    generarfacturasadmins.configure(bg=color)
    fuente = ("Console", 16)
    fuenteg = ("Console", 18)
    input2 = tk.Label(generarfacturasadmins, text="Añadir una factura a un propietario", bg=color, fg=color2, font=fuenteg)
    input2.pack(pady=(10))
    input_codpropietario = tk.Label(generarfacturasadmins, text="Codpropietario", bg=color, fg=color2, font=fuente)
    codpropietario_entry = tk.Entry(generarfacturasadmins, bg=color2, fg=color, font=fuente)
    input_codpropietario.pack(pady=(10))
    codpropietario_entry.pack(pady=(10))
    input_codpropietario2 = tk.Label(generarfacturasadmins, text="Costo Regular 39.99 dolares", bg=color, fg=color2, font=fuente)
    input_codpropietario3 = tk.Label(generarfacturasadmins, text="Porcentaje de Descuento (Si no hay descuento introduzca 0)", bg=color, fg=color2, font=fuente)
    codpropietario_entry2 = tk.Entry(generarfacturasadmins, bg=color2, fg=color, font=fuente)
    input_codpropietario2.pack(pady=(10))
    input_codpropietario3.pack(pady=(10))
    codpropietario_entry2.pack(pady=(10)) 
    boton_buscar = tk.Button(generarfacturasadmins, text="Añadir", command=lambda: validarint30(codpropietario_entry.get(), codpropietario_entry2.get(),generarfacturasadmins), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    generarfacturasadmins.mainloop()
######################################################################################################################
global seahechounpagobandera
seahechounpagobandera=False
def verificacantidadfacturas():
    global facturasgeneradaadmin
    global cantidadasunombre
    cantidadasunombre=0
    user=str(usuarioparaveri)
    for i in facturasgeneradaadmin:
            if facturasgeneradaadmin[i]['codpropietario']==user:
                cantidadasunombre=cantidadasunombre+1
    return cantidadasunombre
def facturas_comando():
    user=str(usuarioparaveri)
    print(facturas[usuario]['costo: $'])
espacioeni=0
def pagocompletodecuenta(bandera, costo, usuario, codigollave, ventana):
    global facturasgeneradaadmin
    global seahechounpagobandera
    global espacioeni
    cant=espacioeni
    if not os.path.exists("Cobros"):
        os.makedirs("Cobros")
    carpeta = 'cobros'
    if not os.path.exists('comprobantes'):
        os.makedirs('comprobantes')
    carpeta2 = 'comprobantes'
    usuarioint=int(usuario)
    if bandera==0:
        nombre_archivo = f'{usuarioint}.txt'
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
        else:
            pass
        del facturas[usuario]
        nombre_archivo2 = f'{usuarioint}.txt'
        ruta_archivo2 = os.path.join(carpeta2, nombre_archivo)
        with open(ruta_archivo2, "w") as file:
            file.write("-------------------------------------------------------------------------------------------------------------\n")
            fecha = datetime.now() 
            file.write(f"|Pagado el: {fecha.strftime('%Y-%m-%d %H:%M:%S')} | Usuario: {usuario} | Costo: ${costo} |\n")
            file.write("-------------------------------------------------------------------------------------------------------------\n")
        messagebox.showinfo("Haz pagado la factura", f"Tu comprobante se encuentra en la carpeta comprobantes, en el archivo {usuario}.txt")
        seahechounpagobandera=True
        intermediariafacturas(ventana)
    elif bandera==1:
        nombre_archivo = f'{usuarioint}({espacioeni}).txt'
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
        else:
            pass
        espacioeni+=1
        for i in facturasgeneradaadmin:
                if facturasgeneradaadmin[i]['codpropietario']==usuarioparaveri:
                    del facturasgeneradaadmin[i]
                    break

        nombre_archivo2 = f'{usuarioint}({espacioeni}).txt'
        ruta_archivo2 = os.path.join(carpeta2, nombre_archivo)
        
        with open(ruta_archivo2, "w") as file:
            file.write("-------------------------------------------------------------------------------------------------------------\n")
            fecha = datetime.now() 
            file.write(f"|Pagado el: {fecha.strftime('%Y-%m-%d %H:%M:%S')} | Usuario: {usuario} | Costo: ${costo} |\n")
            file.write("-------------------------------------------------------------------------------------------------------------\n")        
        messagebox.showinfo("Haz pagado la factura", f"Tu comprobante se encuentra en la carpeta comprobantes, en el archivo {usuario}({espacioeni}).txt")
        seahechounpagobandera=True
        intermediariafacturas(ventana)
    else:
        messagebox.showerror("Error", "Desconocido, en seccion pagocompletodecuenta.")
def pagarlacuenta(dedonde):
    global facturacionnormal
    global seahechounpagobandera
    global facturasgeneradaadmin
    user=str(usuarioparaveri)    
    if dedonde=="factura":
        facturacionnormal = tk.Tk()
        facturacionnormal.title("Pagar Factura")
        facturacionnormal.geometry("600x400")
        facturacionnormal.resizable(False, False)
        facturacionnormal.configure(bg=color)
        fuente = ("Console", 14)
        fuenteg = ("Console", 20)
        monto = facturas[user]['costo: $']
        input2 = tk.Label(facturacionnormal, text="¿Deseas pagar la factura?", bg=color, fg=color2, font=fuenteg)
        input3 = tk.Label(facturacionnormal, text=f"Tiene costo de: ${monto}", bg=color, fg=color2, font=fuenteg)
        input2.pack(pady=(10))
        input3.pack(pady=(10))
        boton_buscar = tk.Button(facturacionnormal, text="Pagar", command=lambda: pagocompletodecuenta(0, monto, user, 0, facturacionnormal), bg=color, fg=color2, font=fuente)
        boton_buscar.pack(pady=20)
        facturacionnormal.mainloop()        
    elif dedonde=="generadaporadmin":
        facturasgeneradaadmin2 = tk.Tk()
        facturasgeneradaadmin2.title("Pagar Factura")
        facturasgeneradaadmin2.geometry("600x400")
        facturasgeneradaadmin2.resizable(False, False)
        facturasgeneradaadmin2.configure(bg=color)
        fuente = ("Console", 14)
        fuenteg = ("Console", 20)
        for clave in facturasgeneradaadmin:
                if facturasgeneradaadmin[clave]['codpropietario']==usuarioparaveri:
                    monto = facturasgeneradaadmin[clave]['costo: $']
                    codigollave=clave
                    break
        input2 = tk.Label(facturasgeneradaadmin2, text="¿Deseas pagar la factura?", bg=color, fg=color2, font=fuenteg)
        input3 = tk.Label(facturasgeneradaadmin2, text=f"Tiene costo de: ${monto}", bg=color, fg=color2, font=fuenteg)
        input2.pack(pady=(10))
        input3.pack(pady=(10))
        boton_buscar = tk.Button(facturasgeneradaadmin2, text="Pagar", command=lambda: pagocompletodecuenta(1, monto, user,codigollave, facturasgeneradaadmin2), bg=color, fg=color2, font=fuente)
        boton_buscar.pack(pady=20)
        facturasgeneradaadmin2.mainloop()  
def intermediariafacturas(ventana):
    if ventana and isinstance(ventana, tk.Tk):
        ventana.destroy()
    pagodefacturasvencidas()
def usuariorevisiondeestancia(usuario):
    for codigo in facturasgeneradaadmin:
            if facturasgeneradaadmin[codigo]["codpropietario"] == usuario:
                return True
    else:
        return False
def pagodefacturasvencidas():
    usuario22 = str(usuarioparaveri)
    global seahechounpagobandera
    global cuentaenbeta
    if eventousuario == "administrador":
        messagebox.showerror("Error", "No tienes facturas pendientes, eres un admin.")
    elif cuentaenbeta and not usuario22 in facturas and not usuariorevisiondeestancia(usuario22) and seahechounpagobandera:
        ventanaprincipal100.destroy()
        cuentaenbeta=False
        seahechounpagobandera=False
        inicio()
    elif usuario22 in facturas and usuariorevisiondeestancia(usuario22) and not seahechounpagobandera:
        pagarlacuenta("factura")
    elif usuario22 not in facturas and not usuariorevisiondeestancia(usuario22) and seahechounpagobandera:
        messagebox.showinfo("PAGO EXITOSO", "GRACIAS POR PAGAR")
        seahechounpagobandera = False
    elif usuario22 not in facturas and not usuariorevisiondeestancia(usuario22) and not seahechounpagobandera:
        messagebox.showerror("Error", "No tienes facturas pendientes.")
    elif usuario22 in facturas and not seahechounpagobandera:
        pagarlacuenta("factura")
    elif usuariorevisiondeestancia(usuario22) and not seahechounpagobandera:
        pagarlacuenta("generadaporadmin")
    elif usuario22 in facturas and seahechounpagobandera:
        messagebox.showinfo("Tienes más cuentas para pagar", "Tu cuenta aún tiene pagos restantes")
        pagarlacuenta("factura")
    elif usuariorevisiondeestancia(usuario22) and seahechounpagobandera:
        messagebox.showinfo("Tienes más cuentas para pagar", "Tu cuenta aún tiene pagos restantes")
        pagarlacuenta("generadaporadmin")
    else:
        messagebox.showerror("Error", "No tienes facturas pendientes.")
######################################################################################################################
def cambiarlosdescuentos(inactivo, creados, insercion):
    global descuentoactividad
    global descuentocreacion
    global descuentoinsercion
    descuentoactividad = inactivo
    descuentocreacion = creados
    descuentoinsercion = insercion
def revisiondescuentos(inactivo, creados, insercion):
    global facturasgeneradaadmin
    num_str = str(inactivo)
    num_str2 = str(creados)
    num_str3 = str(insercion)
    num_digitos = len(num_str)
    num_digitos2 = len(num_str2)
    num_digitos3 = len(num_str3)
    if num_digitos <= 2 and num_digitos2 <= 2 and num_digitos3 <= 2:
        cambiarlosdescuentos(inactivo, creados, insercion)
    else:
        messagebox.showerror("Error", "El porcentaje maximo es de 99%. Intenta de nuevo.")
def validarenteros2(inactivo, creados, insercion):
    try:
        inactivo=int(inactivo)
        creados=int(creados)
        insercion=int(insercion)
        revisiondescuentos(inactivo, creados, insercion) #Si es entero lo manda a revisar si necesita activacion
    except ValueError:
        messagebox.showerror("Error", "El usuario debe ser un número entero. Intenta de nuevo.")
def descuentos_comando():
    descuentospara = tk.Tk()
    descuentospara.title("Generar Facturas")
    descuentospara.geometry("700x500")
    descuentospara.resizable(False, False)
    descuentospara.configure(bg=color)
    fuente = ("Console", 18)
    fuenteg = ("Console", 22)
    facturas = tk.Label(descuentospara, text="Manejar los descuentos", bg=color, fg=color2, font=fuenteg)
    facturas.pack(pady=(10))
    
    usuariosinactivos = tk.Label(descuentospara, text="Porcentaje para Usuarios Inactivos", bg=color, fg=color2, font=fuente)
    usuariosinactivos.pack(pady=(10))
    usuariosinactivos_entry = tk.Entry(descuentospara, bg=color2, fg=color, font=fuente)
    usuariosinactivos_entry.pack(pady=(10))

    usuarioscreados = tk.Label(descuentospara, text="Porcentaje para Nuevos Usuarios", bg=color, fg=color2, font=fuente)
    usuarioscreados.pack(pady=(10))
    usuarioscreados_entry = tk.Entry(descuentospara, bg=color2, fg=color, font=fuente)
    usuarioscreados_entry.pack(pady=(10))

    usuariosinsercion = tk.Label(descuentospara, text="Porcentaje para Usuarios Insertados", bg=color, fg=color2, font=fuente)
    usuariosinsercion.pack(pady=(10))
    usuariosinsercion_entry = tk.Entry(descuentospara, bg=color2, fg=color, font=fuente)
    usuariosinsercion_entry.pack(pady=(10))
    
    boton_buscar = tk.Button(descuentospara, text="Cambiar", command=lambda: validarenteros2(usuariosinactivos_entry.get(),usuarioscreados_entry.get(),usuariosinsercion_entry.get()), bg=color, fg=color2, font=fuente)
    boton_buscar.pack(pady=20)
    descuentospara.mainloop()
######################################################################################################################
#######################################################ACERCA DE#######################################################
######################################################################################################################
def sobrenosotros():
    sobre = Toplevel()
    sobre.title("Acerca de")
    sobre.geometry("500x400")
    sobre.resizable(False, False)
    sobre.configure(bg=color)
    fuente=("Console",16)
    sobretexto=Label(sobre, text="Bienvenid@", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto2=Label(sobre, text="Esta es la ventana sobre Pinguify", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto3=Label(sobre, text="El peor reproductor de música", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto4=Label(sobre, text="Creadores", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto5=Label(sobre, text="Isaac V y Kevin V", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto.pack(expand=True)
    sobretexto2.pack(expand=True)
    sobretexto3.pack(expand=True)
    sobretexto4.pack(expand=True)
    sobretexto5.pack(expand=True)
    sobre.mainloop()
######################################################################################################################
#######################################################CONTACTO#######################################################
######################################################################################################################
def contacto():
    contacto = Toplevel()
    contacto.geometry("500x400")
    contacto.resizable(False, False)
    contacto.configure(bg=color)
    fuente=("Console",16)
    sobretexto=Label(contacto, text="Contactos", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto2=Label(contacto, text="Email", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto3=Label(contacto, text="Pinguify@10minutemail.com", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto4=Label(contacto, text="Teléfono", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto5=Label(contacto, text="2001-0911", bg=color, fg=color2, activebackground='white', font=fuente, anchor='center')
    sobretexto.pack(expand=True)
    sobretexto2.pack(expand=True)
    sobretexto3.pack(expand=True)
    sobretexto4.pack(expand=True)
    sobretexto5.pack(expand=True)
    contacto.mainloop()
#################
#################
elegircolor()
#################
#################

