import pandas as pd
import numpy as np
import math as mt 

def intInput (message) -> int:
    while True:
        try:
            return int(input(message))
        except:
            print("Error: No es número.\n")

def floatInput (message) -> float:
    while True:
        try:
            return float(input(message))
        except:
            print("Error: No es número.\n")

# Tipo de estructura

def set_structure_type():
    while True:
        print("Tipo de estructura.\n")
        print("\t1. Cercha.")
        print("\t2. Viga.")
        print("\t3. Portico.")
        print("\n4. Volver")
        
        match input("\nIngrese el tipo de seccion: "):
            case "1": 
                return "Cercha"
            case "2": 
                return "Viga"
            case "3":
                return "Portico"
            case "4":
                return False
            case _:
                print("Error: No se reconoce la opcion ingresada.\n\n")

# Sistema de nodos

def set_coords():
    coord_x = floatInput("Coordenada x del nodo: ")
    coord_y = floatInput("Coordenada y del nodo: ")
    return(coord_x,coord_y)

def get_grados_Libertad(structureType):
    match structureType:
        case "Cercha":
            u = intInput("Ingrese el grado de libertad u del nodo: ")
            v = intInput("Ingrese el grado de libertad v del nodo: ")
            return (u,v)
        case "Viga":
            u = intInput("Ingrese el grado de libertad u del nodo: ")
            phi = intInput("Ingrese el grado de libertad phi del nodo: ")
            return (u,phi)
        case "Portico":
            u = intInput("Ingrese el grado de libertad u del nodo: ")
            v = intInput("Ingrese el grado de libertad v del nodo: ")
            phi = intInput("Ingrese el grado de libertad phi del nodo: ")
            return (u,v,phi)
            
# Sistema de unidades:

def get_conversion_longitud(unit_in, unit_out):
    match unit_in: 
        case "m":
            match unit_out:
                case "cm":
                    return 100
                case "mm":
                    return 1000
                case "in":
                    return 39.27
                case "ft":
                    return 3.28
                case _:
                    return 1
        case "cm":
            match unit_out:
                case "m":
                    return 1/100
                case "mm":
                    return 10
                case "in":
                    return 0.3927
                case "ft":
                    return 0.0328
                case _:
                    return 1
        case "mm":
            match unit_out:
                case "m":
                    return 1/1000
                case "cm":
                    return 1/10
                case "in":
                    return 0.03927
                case "ft":
                    return 0.00328
                case _:
                    return 1
        case "in":
            match unit_out:
                case "m": 
                    return 0.0254
                case "cm":
                    return 2.54
                case "mm":
                    return 25.4
                case "ft":
                    return 1/12
                case _:
                    return 1
        case "ft":
            match unit_out:
                case "m":
                    return 0.3048
                case "cm":
                    return 30.48
                case "mm":
                    return 304.8
                case "in":
                    return 12  
                case _:
                    return 1
        
def get_conversion_esfuerzo(unit_in, unit_out):
    match unit_in:
        case "Gpa":
            match unit_out:
                case "Mpa":
                    return 1*10**3
                case "Kpa":
                    return 1*10**6
                case "pa":
                    return 1*10**9
                case "psi":
                    return 145038
                case "Kpsi":
                    return 145.038
                case _:
                    return 1
        case "Mpa":
            match unit_out:
                case "Gpa": 
                    return 1/1000
                case "Kpa": 
                    return 1*10**3
                case "pa":
                    return 1*10*6
                case "psi":
                    return 145.038
                case "Kpsi":
                    return 0.145038
                case _:
                    return 1
        case "Kpa":
            match unit_out:
                case "Gpa":
                    return 1/(1*10**6)
                case "Mpa": 
                    return 1/1000
                case "pa":
                    return 1000
                case "psi":
                    return 0.145038
                case "Kpsi":
                    return 0.145038/1000
                case _:
                    return 1
        case "pa":
            match unit_out:
                case "Gpa":
                    return 1/(1*10**9)
                case "Mpa":
                    return 1/(1*10**6)
                case "Kpa":
                    return 1/1000
                case "psi":
                    return 0.145038/1000
                case "Kpsi":
                    return 0.145038/1000000
                case _:
                    return 1
                        
def get_conversion_fuerza(unit_in, unit_out):
    match unit_in:
        case "kN":
            match unit_out:
                case "N":
                    return 1000
                case "lbf":
                    return 0.2248/1000
                case "kipf":
                    return 0.2248/1000000
                case _:
                    return 1
        case "N": 
            match unit_out:
                case "kN": 
                    return 1/1000
                case "lbf":
                    return 0.2248
                case "kipf":
                    return 0.2248/1000
                case _:
                    return 1
        case "lbf":
            match unit_out:
                case "kN":
                    return 0.00448
                case "N":
                    return 4.482
                case "kipf":
                    return 1/1000
                case _:
                    return 1
        case "kipf":
            match unit_out:
                case "kN":
                    return 4.44822
                case "N": 
                    return 4448.22
                case "lbf":
                    return 1000
                case _:
                    return 1
    
def get_conversion_angulo(unit_in, unit_out):
    match unit_in:
        case "°":
            match unit_out:
                case "rad":
                    return (mt.pi)/180
                case _:
                    return 1
        case "rad":
            match unit_out:
                case "°":
                    return 180/(mt.pi)
                case _:
                    return 1
                
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
        print("\t3. Libra fuerza. (lbf)")
        print("\t4. KiloLibra fuerza. (kipf)")
        print("\t5. Volver.") # Siempre es la ultima
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return "kN"
                case "2": 
                    return "N"
                case "3": 
                    return "lbf"
                case "4": 
                    return "kipf"
                case "5":
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
        print("\t5. Libra por pulgada cuadrada. (psi)")
        print("\t6. Kilolibra por pulgada cuadrada. (Kpsi)")
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
                    return "psi"
                case "6": 
                    return "Kpsi"
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

def get_section_calcs(units,edit=False):
    while True:
        print("\n\tSecciones.")
        print("\t1. Rectangular.")
        print("\t2. Tubular Rectangular.")
        print("\t3. Añadir valor de area y inercia manualmente.")
        if edit:
            print("\t4. No modificar valores")
        
        match input("\nIngrese el tipo de seccion: "):
            case "1": 
                return section_Rectangular(units)
            case "2": 
                return section_TubularRectangular(units)
            case "3":
                return (area_custom(units), inercia_custom(units))
            case "4":
                if edit:
                    return False
                else:
                    print("Error: No se reconoce la opcion ingresada.\n\n")
            case _:
                print("Error: No se reconoce la opcion ingresada.\n\n")

def section_Rectangular(units) -> float: 
    base = floatInput(f"Ingrese el valor de la base ({units}): ")
    altura = floatInput(f"Ingrese el valor de la altura ({units}): ")
    
    return (base*altura, # Area
            (base*altura**3)/12) # Inercia

def section_TubularRectangular(units) -> float: 
    base = floatInput(f"Ingrese el valor de la base ({units}): ")
    altura = floatInput(f"Ingrese el valor de la altura ({units}): ")
    espesor = floatInput(f"Ingrese el valor del espesor ({units}): ")
    
    return ((base*altura)-((base-espesor*2)*(altura-espesor*2)), # Area
            ((base*altura**3)/12)-(((base-espesor*2)*(altura-espesor*2)**3)/12)) # Inercia

def area_custom(units) -> float: 
    return floatInput(f"Ingrese el valor del area ({units}^2): ")

def inercia_custom(units) -> float: 
    return floatInput(f"Ingrese el valor de la inercia ({units}^4): ")
