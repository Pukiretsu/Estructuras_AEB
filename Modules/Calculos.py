import pandas as pd
import numpy as np

def floatInput (message) -> float:
    while True:
        try:
            return float(input(message))
        except:
            print("Error: No es número.\n")

# Sistema de unidades:
def unit_Longitud():
    while True:
        print("\n\tLongitud.")
        print("\t1. Metros. (m)")
        print("\t2. Centimetros. (cm)")
        print("\t3. Milimetros. (mm)")
        print("\t4. Pulgadas. (in)")
        print("\t5. Pies. (ft)")
        print("\t6. Volver.") # Siempre es la ultima
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return "m"
                case "2": 
                    return "cm"
                case "3": 
                    return "mm"
                case "4": 
                    return "in"
                case "5": 
                    return "ft"
                case "6":
                    return False
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")

def unit_Fuerza():
    while True:
        print("\n\tFuerza.")
        print("\t1. Kilonewton. (kN)")
        print("\t2. Newton. (N)")
        print("\t3. Libras. (lb)")
        print("\t4. Volver.") # Siempre es la ultima
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return "kN"
                case "2": 
                    return "N"
                case "3": 
                    return "lb"
                case "4":
                    return False
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")
                    
def unit_Esfuerzo():
    while True:
        print("\n\tEsfuerzo.")
        print("\t1. Gigapascales. (Gpa)")
        print("\t2. Megapascales. (Mpa)")
        print("\t3. Kilopascales. (Kpa)")
        print("\t4. Pascales. (pa)")
        print("\t5. Kilolibra por pulgada cuadrada. (Kpsi)")
        print("\t6. Megalibra por pulgada cuadrada. (Mpsi)")
        print("\t7. Volver.") # Siempre es la ultima
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return "Gpa"
                case "2": 
                    return "Mpa"
                case "3": 
                    return "Kpa"
                case "4": 
                    return "pa"
                case "5": 
                    return "Kpsi"
                case "6": 
                    return "Mpsi"
                case "7":
                    return False
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")

def unit_Grados():
    while True:
        print("\n\tGrados.")
        print("\t1. Sexagesimal. (°)")
        print("\t2. Radianes. (rad)")
        print("\t3. Volver.") # Siempre es la ultima
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return "°"
                case "2": 
                    return "rad"
                case "3":
                    return False
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")


#TODO Añadir sistema de unidades
def get_units():
    print("\n¿Qué unidad desea cambiar?: ")
    while True:
        print("\n\tUnidades.\n")
        print("\t1. Longitud.")
        print("\t2. Fuerza.")
        print("\t3. Esfuerzo.")
        print("\t4. Angulo.")
        print("\t5. Volver.")
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return ("L",unit_Longitud())
                case "2": 
                    return ("F",unit_Fuerza())
                case "3":
                    return ("E",unit_Esfuerzo())
                case "4":
                    return ("G",unit_Grados())
                case "5":
                    return "N"
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")
    

# Calculos de sección

def get_section_calcs(edit=False):
        while True:
            print("\n\tSecciones.")
            print("\t1. Rectangular.")
            print("\t2. Tubular Rectangular.")
            print("\t3. Añadir valor de area y inercia manualmente.")
            if edit:
                print("\t4. No modificar valores")
            
            match input("\nIngrese el tipo de seccion: "):
                case "1": 
                    return section_Rectangular()
                case "2": 
                    return section_TubularRectangular()
                case "3":
                    return (area_custom(), inercia_custom())
                case "4":
                    if edit:
                        return False
                    else:
                        print("Error: No se reconoce la opcion ingresada.\n\n")
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")

def section_Rectangular() -> float: 
    base = floatInput("Ingrese el valor de la base: ")
    altura = floatInput("Ingrese el valor de la altura: ")
    
    return (base*altura, # Area
            (base*altura**3)/12) # Inercia

def section_TubularRectangular() -> float: 
    base = floatInput("Ingrese el valor de la base: ")
    altura = floatInput("Ingrese el valor de la altura: ")
    espesor = floatInput("Ingrese el valor del espesor: ")
    
    return ((base*altura)-((base-espesor*2)*(altura-espesor*2)), # Area
            ((base*altura**3)/12)-(((base-espesor*2)*(altura-espesor*2)**3)/12)) # Inercia

def area_custom() -> float: return floatInput("Ingrese el valor del area:")

def inercia_custom() -> float: return floatInput("Ingrese el valor de la inercia: ")
