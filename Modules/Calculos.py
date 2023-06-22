import pandas as pd
import numpy as np

def floatInput (message) -> float:
    while True:
        try:
            return float(input(message))
        except:
            print("Error: No es número.\n")

#TODO Añadir sistema de unidades

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
