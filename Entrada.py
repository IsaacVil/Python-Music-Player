import Leearchivos
import tkinter as tk
def leer_numero_entero(mensaje_al_usuario, mensaje_de_error = "Valor no válido"):
    ha_ingresado_valor_legal = False
    while ha_ingresado_valor_legal == False:    
        try:
            valor_del_usuario = int(input(mensaje_al_usuario))
            ha_ingresado_valor_legal = True
        except ValueError:
            print(mensaje_de_error)
    return valor_del_usuario

def leer_numero_flotante(mensaje_al_usuario, mensaje_de_error = "Valor no válido"):
    ha_ingresado_valor_legal = False
    while ha_ingresado_valor_legal == False:    
        try:
            valor_del_usuario = float(input(mensaje_al_usuario))
            ha_ingresado_valor_legal = True
        except ValueError:
            print(mensaje_de_error)
    return valor_del_usuario

def leer_str(mensaje_al_usuario, mensaje_de_error="Valor no válido"):
    ha_ingresado_valor_legal = False
    while ha_ingresado_valor_legal==False:
        valor_del_usuario = input(mensaje_al_usuario)
        ha_ingresado_valor_legal =True
    return valor_del_usuario

#validaciones para inputs en tkinter
def validarint(entrada):
    try:
        prueba = int(entrada.get())
        return True
    except ValueError:
        messagebox.showerror("Error", "El usuario debe ser un número entero. Intenta de nuevo.")

def validarfloat(entrada):
    try:
        prueba = float(entrada.get())
        return True
    except ValueError:
        messagebox.showerror("Error", "El usuario debe ser un número entero. Intenta de nuevo.")

def validarstring(entrada):
    try:
        prueba = str(entrada.get())
        return True
    except ValueError:
        messagebox.showerror("Error", "El usuario debe ser un número entero. Intenta de nuevo.")

