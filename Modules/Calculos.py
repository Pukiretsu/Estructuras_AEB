import pandas as pd
import numpy as np
import math as mt 
from os import system

# Configuraciones para display

pd.set_option('display.float_format', '{:.1f}'.format)




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
        print("\n0. Volver")
        
        match input("\nIngrese el tipo de seccion: "):
            case "1": 
                return "Cercha"
            case "2": 
                return "Viga"
            case "3":
                return "Portico"
            case "0":
                return False
            case _:
                print("Error: No se reconoce la opcion ingresada.\n\n")

#Sistema de elementos

def get_index(index_list,message, edit = False, default = None):
    while True:
        try:
            if edit:
                index = input(message) or default
                if index:
                    index = int(index)
            else:
                index = int(input(message))      
            if index_list.count(index) == 0:
                raise Exception() 
            break
        except:
            print("Error: id inválido.\n")
    return index

def set_nodos(nodos, ID_i = None, ID_j = None,edit = False):
    if not nodos.empty:   
        print("\nNodos actuales:\n")
        print(nodos)
        index_list = nodos.index.values.tolist()
        
        if edit:
            index_i = get_index(index_list,f"\nSeleccione el id del nodo i({ID_i}): ", edit, ID_i)
        else:
            index_i = get_index(index_list,"\nSeleccione el id del nodo i: ")
            
        print(f"\nNodo i selecionado id [{index_i}]: ") 
        print(nodos.loc[[index_i]])
        
        while True: 
            if edit:
                index_j = get_index(index_list,f"\nSeleccione el id del nodo j({ID_j}): ", edit, ID_j)
            else:
                index_j = get_index(index_list,"\nSeleccione el id del nodo j: ")
                
            if index_i != index_j:
                print(f"\nNodo j selecionado id [{index_j}]: ") 
                print(nodos.loc[[index_j]])
                break
            else: 
                print("\nEste nodo ya ha sido asignado al elemento.")
                
        return ((index_i,nodos.loc[index_i,'Nombre']),(index_j,nodos.loc[index_j,'Nombre']))
    else: 
        print("\nNo se encuentran nodos en la base de datos.\n")
        print("\t0. Volver")
        input("Seleciona una opción: ")
        return False

def get_longitud(nodos,nodoi,nodoj,units):
    delta_x = nodos.loc[nodoj,'Coordenada x'] - nodos.loc[nodoi,'Coordenada x']
    delta_y = nodos.loc[nodoj,'Coordenada y'] - nodos.loc[nodoi,'Coordenada y']

    longitud = (delta_x**2 + delta_y**2)**(1/2)
        
    return (longitud, (delta_x, delta_y))

def get_angulo(longitud,delta_x,delta_y,units):
    if delta_x < 0 :
        seno = -delta_y/longitud
    else:
        seno = delta_y/longitud
        
    if delta_x > 0:
        if delta_y >= 0:
            angulo = np.arcsin(seno)
        elif delta_y < 0:
            angulo = (2 * np.pi) + np.arcsin(seno)
    if delta_x < 0:
        if delta_y > 0:
            angulo = (np.pi) + np.arcsin(seno)
        elif delta_y <= 0:
            angulo = (np.pi) + np.arcsin(seno)
    else: 
        if delta_y >= 0:
            angulo = np.arcsin(seno)
        elif delta_y < 0:
            angulo = (np.pi) - np.arcsin(seno)
    
    return angulo * get_conversion_angulo("rad",units)
          
def set_material(material, last_material = None, edit = False):
    if not material.empty:  
        print("\nMateriales actuales:\n")
        print(material)
        index_list = material.index.values.tolist()
        
        if edit:
            index = get_index(index_list,f"\nSeleccione el id del material({last_material[0]}): ", True, last_material[0])
        else:        
            index = get_index(index_list,"\nSeleccione el id del material: ")
        print(f"\nMaterial selecionado id [{index}]: ") 
        print(material.loc[[index]])
                
        return (index, material.loc[index, "Nombre"])
    else: 
        print("\nNo se encuentran materiales en la base de datos.\n")
        input("Pulse enter para continuar.")
        
        return (False,False)

def set_seccion(seccion, last_seccion = None, edit = False):
    if not seccion.empty:  
        print("\nSecciones actuales:\n")
        print(seccion)
        index_list = seccion.index.values.tolist()
        
        if edit:
            index = get_index(index_list,f"\nSeleccione el id de la sección({last_seccion[0]}): ", True, last_seccion[0])
        else:        
            index= get_index(index_list,"\nSeleccione el id de la sección: ")
        
        print(f"\nSección selecionada id [{index}]: ") 
        print(seccion.loc[[index]])      
        return (index, seccion.loc[index, 'Nombre'])
    
    else: 
        print("\nNo se encuentran secciones en la base de datos.\n")
        input("Pulse enter para continuar.")
        return (None,False)
    
# Sistema de nodos

def set_coords(previousCoords=None,edit=False):
    if not edit:
        coord_x = floatInput("Coordenada x del nodo: ")
        coord_y = floatInput("Coordenada y del nodo: ")
    else:
        while True:
            print("\nCoordenada a editar.\n")
            print("\t1. Coordenada x.")
            print("\t2. Coordenada y.")
            print("\t3. Ambas.")
            print("\n4. Mantener coordenadas")
            match input("\nIngrese una opción: "):
                case "1": 
                    coord_x = floatInput("Coordenada x del nodo: ")
                    coord_y = previousCoords[1]
                    break
                case "2": 
                    coord_x = previousCoords[0]
                    coord_y = floatInput("Coordenada y del nodo: ")
                    break
                case "3":
                    coord_x = floatInput("Coordenada x del nodo: ")
                    coord_y = floatInput("Coordenada y del nodo: ")
                    break
                case "4":
                    return False
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")
    return(coord_x,coord_y)

def get_grados_Libertad(structureType):
    match structureType:
        case "Cercha":
            u =     intInput("\nIngrese el grado de libertad u del nodo: ")
            v =     intInput("\nIngrese el grado de libertad v del nodo: ")
            return (u,v)
        case "Viga":
            v =     intInput("\nIngrese el grado de libertad u del nodo: ")
            phi =   intInput("\nIngrese el grado de libertad phi del nodo: ")
            return (v,phi)
        case "Portico":
            u =     intInput("\nIngrese el grado de libertad u del nodo: ")
            v =     intInput("\nIngrese el grado de libertad v del nodo: ")
            phi =   intInput("\nIngrese el grado de libertad phi del nodo: ")
            return (u,v,phi)

def get_support(structureType, edit=False):
    while True:
        print("\nTipos de apoyo:\n")  
        match structureType:
            case "Cercha":
                print("\t 1. Primer Grado restriccion en Y (Apoyo simple)")
                print("\t 2. Primer Grado restriccion en X (Apoyo simple)")
                print("\t 3. Segundo Grado (Apoyo articulado)") 
                if edit:
                    print("\n\t 4. No editar apoyos")
                
                support = intInput("\nElija una opción: ")
                match support:
                    case 1:
                        return (True,"Y")
                    case 2:
                        return (True,"X")
                    case 3:
                        return (True,"XY")
                    case 4:
                        if edit:
                            return False
                        else:
                            print("Apoyo no válido")
                    case _:
                        print("\nApoyo no válido.")
            case "Viga":
                print("\t 1. Primer Grado restriccion en Y (Apoyo simple)")
                print("\t 2. Segundo Grado (Apoyo articulado)")
                print("\t 3. Tercer Grado (Empotrado)")
                if edit:
                    print("\n\t 4. No editar apoyos")
                
                support = intInput("\nElija una opción: ")
                match support:
                    case 1:
                        return (True,"Y")
                    case 2:
                        return (True,"XY")
                    case 3:
                        return (True,"XYM")
                    case 4:
                        if edit:
                            return False
                        else:
                            print("Apoyo no válido")
                    case _:
                        print("\nApoyo no válido.")
            case "Portico":
                print("\t 1. Primer Grado restriccion en Y (Apoyo simple)")
                print("\t 2. Primer Grado restriccion en X (Apoyo simple)")
                print("\t 3. Segundo Grado (Apoyo articulado)")
                print("\t 4. Tercer Grado (Empotrado)")
                if edit:
                    print("\n\t 5. No editar apoyos")
                
                support = intInput("\nElija una opción: ")
                match support:
                    case 1:
                        return (True,"Y")
                    case 2:
                        return (True,"X")
                    case 3:
                        return (True,"XY")
                    case 4:
                        return (True,"XYM")
                    case 5:
                        if edit:
                            return False
                        else:
                            print("Apoyo no válido")
                    case _:
                        print("\nApoyo no válido.")

# Sistema de cargas

def add_Cargas_Locales(longitud, nodos, id_NodoI, id_NodoJ, last_carga, units, structureType):
    def print_loads(loads):
        
        system("cls")
        print("Vector de carga local actual:\n")
        match structureType:
            case "Cercha":
                print(f"Nodo i x: {loads[0]} {units.loc[0,'Fuerza']}")
                print(f"Nodo i y: {loads[1]} {units.loc[0,'Fuerza']}")
                print(f"Nodo j x: {loads[3]} {units.loc[0,'Fuerza']}")
                print(f"Nodo j y: {loads[4]} {units.loc[0,'Fuerza']}")
            case "Viga":
                print(f"Vi: {loads[1]} {units.loc[0,'Fuerza']}")
                print(f"Mi: {loads[2]} {units.loc[0,'Fuerza']}.{units.loc[0,'Longitud']}")
                print(f"Vj: {loads[4]} {units.loc[0,'Fuerza']}")
                print(f"Mj: {loads[5]} {units.loc[0,'Fuerza']}.{units.loc[0,'Longitud']}")
            case "Portico":
                print(f"Ni: {loads[0]} {units.loc[0,'Fuerza']}")
                print(f"Vi: {loads[1]} {units.loc[0,'Fuerza']}")
                print(f"Mi: {loads[2]} {units.loc[0,'Fuerza']}.{units.loc[0,'Longitud']}")
                print(f"Nj: {loads[3]} {units.loc[0,'Fuerza']}")
                print(f"Vj: {loads[4]} {units.loc[0,'Fuerza']}")
                print(f"Mj: {loads[5]} {units.loc[0,'Fuerza']}.{units.loc[0,'Longitud']}")
    
    loads = last_carga
    
    while True:
        print_loads(loads)
        print("\nAgregar cargas.\n")
        if structureType == "Cercha":
            print("\t 1. Manualmente.")
        else:    
            print("\t 1. Puntual.")
            print("\t 2. Distribuida.")
            print("\t 3. Triangular.")
            print("\t 4. Momento.")
            print("\t 5. Manualmente.")
        
        print("\n0. Volver.")
        if structureType == "Cercha":
            match input("\nIngrese una opción: "):
                case "1":
                    loads = set_carga_nodo(loads, nodos, id_NodoI, id_NodoJ, units)
                case "0":
                    break
                case _:
                    print("Error: no se reconoce la opción ingresada.\n")
        else:    
            match input("\nIngrese una opción: "):
                case "1":
                    loads = set_carga_Puntual(loads, longitud, id_NodoI,units)
                case "2":
                    loads = set_carga_Distribuida(loads, longitud, units)
                case "3":
                    loads = set_carga_Triangular(loads, longitud, units)
                case "4":
                    loads = set_carga_Momento(loads, longitud, id_NodoI, units)
                case "5":
                    loads = set_carga_manual(loads,units,structureType)
                case "0":
                    break
                case _:
                    print("Error: no se reconoce la opción ingresada.\n")

    return loads

def validate_longitud(longitud, message):
    while True:
        long_carga = floatInput(message)
        if long_carga < longitud:
            break
        else:
            print(f"Error, La distancia no puede ser mayor a la longitud ({longitud}) del elemento ")
    return long_carga

def set_carga_nodo(loads, nodos, id_NodoI, id_NodoJ, units):
    
    def direction():
     while True:
        print("\nIndique la dirección de la carga.\n")
        
        print(f"\t1. x")
        print(f"\t2. y.")
        
        match input("\nIngrese una opción: "):
                case "1":
                    return "x"
                case "2":
                    return "y"
                case _:
                    print("Error: no se reconoce la opción ingresada.\n")    
    
    while True:
        print("\nIndique el nodo donde está aplicada la carga.\n")
        
        print(f"\t1. Nodo i [{nodos.loc[id_NodoI,'Nombre']}].")
        print(f"\t2. Nodo j [{nodos.loc[id_NodoJ,'Nombre']}].")
        
        print("\n0. Volver.")
        match input("\nIngrese una opción: "):
                case "1":
                    valor = floatInput(f"\nIngrese el valor de la carga ({units.loc[0,'Fuerza']}): ")
                    direccion = direction()
                    nodo = "i"

                    break
                case "2":
                    valor = floatInput(f"\nIngrese el valor de la carga ({units.loc[0,'Fuerza']}): ")
                    direccion = direction()
                    nodo = "j"
                    break
                case "0":
                    return loads
                case _:
                    print("Error: no se reconoce la opción ingresada.\n")
    
    # Setear dirección y nodo
    if nodo == "i":
        if direccion == "x":
            loads[0] = loads[0] + valor
        else:
            loads[1] = loads[1] + valor
    else:
        if direccion == "x":
            loads[3] = loads[3] + valor
        else:
            loads[4] = loads[4] + valor
    
    return loads
        
def set_carga_manual(loads, units, structureType):
    print("\nIndique el valor a añadir.\n")
    match structureType:
            case "Cercha":
                loads[0] = loads[0] + floatInput(f"Ni ({loads[0]} {units.loc[0,'Fuerza']}): ")
                loads[3] = loads[3] + floatInput(f"Nj ({loads[3]} {units.loc[0,'Fuerza']}): ")
            case "Viga":
                loads[1] = loads[1] + floatInput(f"Vi ({loads[1]} {units.loc[0,'Fuerza']}): ")
                loads[2] = loads[2] + floatInput(f"Mi ({loads[2]} {units.loc[0,'Fuerza']}.{units.loc[0,'Longitud']}): ")
                loads[4] = loads[4] + floatInput(f"Vj ({loads[4]} {units.loc[0,'Fuerza']}): ")
                loads[5] = loads[5] + floatInput(f"Mj ({loads[5]} {units.loc[0,'Fuerza']}.{units.loc[0,'Longitud']}): ")
            case "Portico":
                loads[0] = loads[0] + floatInput(f"Ni ({loads[0]} {units.loc[0,'Fuerza']}): ")
                loads[1] = loads[1] + floatInput(f"Vi ({loads[1]} {units.loc[0,'Fuerza']}): ")
                loads[2] = loads[2] + floatInput(f"Mi ({loads[2]} {units.loc[0,'Fuerza']}.{units.loc[0,'Longitud']}): ")
                loads[3] = loads[3] + floatInput(f"Nj ({loads[3]} {units.loc[0,'Fuerza']}): ")
                loads[4] = loads[4] + floatInput(f"Vj ({loads[4]} {units.loc[0,'Fuerza']}): ")
                loads[5] = loads[5] + floatInput(f"Mj ({loads[5]} {units.loc[0,'Fuerza']}.{units.loc[0,'Longitud']}): ")
    return loads

def set_carga_Puntual(loads, longitud, id_NodoI, units):
    valor = floatInput(f"\nIngrese el valor de la carga ({units.loc[0,'Fuerza']}): ")  
    
    print(f"\nEl nodo i del elemento es: {id_NodoI}")
    print(f"\nLa longitud del elemento es: {longitud} {units.loc[0,'Longitud']}")
    
    distancia = validate_longitud(longitud, f"\nIngrese la distancia al nodo i ({units.loc[0,'Longitud']}): ")
    a = distancia
    b = longitud - distancia
    
    loads[1] = loads[1] + (valor * b**2 / longitud**2) * (3 - 2 * (b / longitud))   # Vi
    loads[2] = loads[2] + (valor * a * b**2) / longitud**2                          # Mi
    loads[4] = loads[4] + (valor * a**2 / longitud**2) * (3 - 2 * (a / longitud))   # Vj
    loads[5] = loads[5] + ((-valor) * a**2 * b) / longitud**2                       # Mj
    
    return loads

def set_carga_Distribuida(loads, longitud , units):
    valor = floatInput(f"\nIngrese el valor de la carga ({units.loc[0,'Fuerza']}/{units.loc[0,'Longitud']}): ")  
    
    loads[1] = loads[1] + (valor * longitud / 2)        # Vi
    loads[2] = loads[2] + (valor * longitud**2 / 12)    # Mi
    loads[4] = loads[4] + (valor * longitud / 2)        # Vj
    loads[5] = loads[5] + ((-valor) * longitud**2 / 12) # Mj
    
    return loads

def set_carga_Triangular(loads, longitud, units):
    valor = floatInput(f"\nIngrese el valor de la carga ({units.loc[0,'Fuerza']}/{units.loc[0,'Longitud']}): ")  
    
    loads[1] = loads[1] + (7 * valor * longitud / 20)   # Vi
    loads[2] = loads[2] + (valor * longitud**2 / 20)    # Mi
    loads[4] = loads[4] + (3 * valor * longitud / 20)   # Vj
    loads[5] = loads[5] + ((-valor) * longitud**2 / 30) # Mj
    
    return loads

def set_carga_Momento(loads, longitud, id_NodoI, units):
    valor = floatInput(f"\nIngrese el valor del momento ({units.loc[0,'Fuerza']}.{units.loc[0,'Longitud']}): ")  
    
    print(f"\nEl nodo i del elemento es: {id_NodoI}")
    print(f"\nLa longitud del elemento es: {longitud} {units.loc[0,'Longitud']}")
    
    distancia = validate_longitud(longitud, f"\nIngrese la distancia al nodo i ({units.loc[0,'Longitud']}): ")
    a = distancia
    b = longitud - distancia
    
    loads[1] = loads[1] + (6 * (-valor) * a * b / longitud**3)                  # Vi
    loads[2] = loads[2] + (valor * b / longitud) * ((3 * b / longitud) - 2)     # Mi
    loads[4] = loads[4] + (6 * valor * a * b / longitud**3)                     # Vj
    loads[5] = loads[5] + ((-valor) * a / longitud) * (2 - (3 * a / longitud))     # Mj
    
    return loads

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
                    return (np.pi)/180
                case _:
                    return 1
        case "rad":
            match unit_out:
                case "°":
                    return 180/(np.pi)
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
        print("\t0. Volver.") # Siempre es la ultima
        
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
                case "0":
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
        print("\n0. Volver.") # Siempre es la ultima
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return "kN"
                case "2": 
                    return "N"
                case "3": 
                    return "lbf"
                case "4": 
                    return "kipf"
                case "0":
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
        print("\t0. Volver.") # Siempre es la ultima
        
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
                case "0":
                    return False
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")

def unit_Grados():
    while True:
        print("\n\tGrados.")
        print("\t1. Sexagesimal. (°)")
        print("\t2. Radianes. (rad)")
        print("\n0. Volver.") # Siempre es la ultima
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return "°"
                case "2": 
                    return "rad"
                case "0":
                    return False
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")

def get_units():
    print("\n¿Qué unidad desea cambiar?: ")
    while True:
        print("\n\tUnidades.\n")
        print("\t1. Longitud.")
        print("\t2. Fuerza.")
        print("\t3. Esfuerzo.")
        print("\t4. Angulo.")
        print("\n0. Volver.")
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return ("L",unit_Longitud())
                case "2": 
                    return ("F",unit_Fuerza())
                case "3":
                    return ("E",unit_Esfuerzo())
                case "4":
                    return ("G",unit_Grados())
                case "0":
                    return ("N", False)
                case _:
                    print("Error: No se reconoce la opcion ingresada.\n\n")

# Material

def get_moduloYoung(units,last_mod = None, edit = False):
    if edit:
        modulo = floatInput(f"\nIngresar el modulo de Young ({last_mod} {units.loc[0,'Esfuerzo']}): ")
    else:
        modulo = input(f"\nIngresar el modulo de Young ({units.loc[0,'Esfuerzo']}): ")
        if modulo:
            modulo =  float(modulo)
    
    return modulo
        
# Calculos de sección

def get_section_calcs(units, edit=False):
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

###  Caculos de estructuras ###

def get_rigidez_local(structureType, L, A, E, I):
    match structureType:
        case "Cercha":
            rigidez_local = np.array([ [  A*E/L , -A*E/L ]
                                      ,[ -A*E/L ,  A*E/L ]])
        case "Viga":
            rigidez_local = np.array([ [  12*E*I/L**3 ,  6*E*I/L**2 , -12*E*I/L**3 ,  6*E*I/L**2 ]
                                      ,[   6*E*I/L**2 ,  4*E*I/L    ,  -6*E*I/L**2 ,  2*E*I/L    ]
                                      ,[ -12*E*I/L**3 , -6*E*I/L**2 ,  12*E*I/L**3 , -6*E*I/L**2 ]
                                      ,[   6*E*I/L**2 ,  2*E*I/L    ,  -6*E*I/L**2 ,  4*E*I/L    ]])
        case "Portico":
            rigidez_local = np.array([ [  A*E/L ,      0       ,     0       , -A*E/L ,       0      ,      0      ]
                                      ,[    0   ,  12*E*I/L**3 ,  6*E*I/L**2 ,    0   , -12*E*I/L**3 ,  6*E*I/L**2 ]
                                      ,[    0   ,   6*E*I/L**2 ,  4*E*I/L    ,    0   ,  -6*E*I/L**2 ,  2*E*I/L    ]
                                      ,[ -A*E/L ,      0       ,     0       ,  A*E/L ,       0      ,      0      ]
                                      ,[    0   , -12*E*I/L**3 , -6*E*I/L**2 ,    0   ,  12*E*I/L**3 , -6*E*I/L**2 ]
                                      ,[    0   ,   6*E*I/L**2 ,  2*E*I/L    ,    0   ,  -6*E*I/L**2 ,  4*E*I/L    ]])
    
    return rigidez_local

def get_Transformacion_GL(structureType, ang):
    match structureType:
        case "Cercha":
            Global_Local = np.array([ [ np.cos(ang) , np.sin(ang) ,      0      ,      0      ]
                                     ,[      0      ,      0      , np.cos(ang) , np.sin(ang) ]])
        case "Viga":
            return np.identity(4)
        case "Portico":
            Global_Local = np.array([ [  np.cos(ang) , np.sin(ang) , 0 ,       0      ,      0      , 0 ]
                                     ,[ -np.sin(ang) , np.cos(ang) , 0 ,       0      ,      0      , 0 ]
                                     ,[       0      ,      0      , 1 ,       0      ,      0      , 0 ]
                                     ,[       0      ,      0      , 0 ,  np.cos(ang) , np.sin(ang) , 0 ]
                                     ,[       0      ,      0      , 0 , -np.sin(ang) , np.cos(ang) , 0 ]
                                     ,[       0      ,      0      , 0 ,       0      ,      0      , 1 ]])
    return Global_Local

def consolidación_RigidezGLobal(structureType, Nnodos, results):
    match structureType:
        case "Cercha":
            index = Nnodos * 2
        case "Viga":
            index = Nnodos * 2
        case "Portico":
            index = Nnodos * 3
    
    matriz_Global = np.zeros((index,index), dtype="float64")
    matriz_Global = pd.DataFrame(matriz_Global)
    
    matriz_Global.index += 1
    matriz_Global.columns = matriz_Global.index
    
    for elemento in results["Elementos"].keys():
        dataf_K = results["Elementos"][elemento]["k rigidez local"]
        for index in dataf_K.index:
            for column in dataf_K.columns:
                matriz_Global.loc[index,column] = matriz_Global.loc[index,column] + dataf_K.loc[index,column]
    
    return matriz_Global

def get_g_libertad_list(nodos, ID_I, ID_J, structureType):
    match structureType:
        case "Cercha":
            u_i = nodos.loc[ID_I, "U"]
            v_i = nodos.loc[ID_I, "V"]
            
            u_j = nodos.loc[ID_J, "U"]
            v_j = nodos.loc[ID_J, "V"]
            
            return (u_i,v_i,u_j,v_j)
        
        case "Viga":
            v_i = nodos.loc[ID_I, "V"]
            phi_i = nodos.loc[ID_I, "Phi"]
            
            v_j = nodos.loc[ID_J, "V"]
            phi_j = nodos.loc[ID_J, "Phi"]
            
            return (v_i,phi_i,v_j,phi_j)
        
        case "Portico":
            u_i = nodos.loc[ID_I, "U"]
            v_i = nodos.loc[ID_I, "V"]
            phi_i = nodos.loc[ID_I, "Phi"]
    
            u_j = nodos.loc[ID_J, "U"]
            v_j = nodos.loc[ID_J, "V"]
            phi_j = nodos.loc[ID_J, "Phi"]

            return (u_i,v_i,phi_i,u_j,v_j,phi_j)
        
def calculos(elementos, nodos, materiales, secciones, units, structureType):
    print("Calculando estructura...")
    matrices_Result = {"Elementos": dict(), "Matriz Global": [], "Vector_Cargas": []}
    
    fac_longitud = get_conversion_longitud(units.loc[0, "Longitud"], "m")
    fac_Fuerza = get_conversion_fuerza(units.loc[0, "Fuerza"], "kN")
    fac_Esfuerzo = get_conversion_esfuerzo(units.loc[0, "Esfuerzo"], "Kpa")
    fac_angulo = get_conversion_angulo(units.loc[0, "Angulo"], "rad")
    
    # Calculo de matrices de rigidez locales y transformacion a globales
    
    for index in elementos.index:
        
        nombre_Elemento = elementos.loc[index, "Nombre"]
        
        Longitud = elementos.loc[index, "Longitud"] * fac_longitud
        Angulo = elementos.loc[index, "Angulo"] * fac_angulo
        
        ID_Seccion = elementos.loc[index, "ID Sec"]
        Area = secciones.loc[ID_Seccion, "Area"] * fac_longitud ** 2
        Inercia = secciones.loc[ID_Seccion, "Inercia"] * fac_longitud ** 4
        
        ID_Material = elementos.loc[index, "ID Mat"] 
        Mod_Elasticidad = materiales.loc[ID_Material, "Modulo Young"] * fac_Esfuerzo
        
        ID_ni = elementos.loc[index, "ID ni"]
        ID_nj = elementos.loc[index, "ID nj"]
        
        grados_libertad = get_g_libertad_list(nodos,ID_ni,ID_nj, structureType)
        
        k_p = pd.DataFrame(get_rigidez_local(structureType, Longitud, Area, Mod_Elasticidad, Inercia))
        TGL = pd.DataFrame(get_Transformacion_GL(structureType, Angulo))
        TLG = TGL.transpose()
        k_rigidez = (TLG.dot(k_p)).dot(TGL)
        
        k_rigidez.index = grados_libertad
        k_rigidez.columns = k_rigidez.index
        
        matrices_Result["Elementos"][f"{nombre_Elemento}"] = {"rigidez": k_p, "TGL": TGL, "k rigidez local": k_rigidez}
    
    print("Matrices Globales [✅]")
    
    # Consolidacion de matrices globales.
    
    nnodos = len(nodos.index)
    matriz_global = consolidación_RigidezGLobal(structureType, nnodos, matrices_Result)
    
    matrices_Result["Matriz Global"] = matriz_global
    
    print("Matriz de rigidez global [✅]")
    
    # TODO: vectores de carga global
    # Obtener vectores de carga local y Global
    
    # TODO: Consolidar vectores de carga global
    
    # TODO: Algoritmo para buscar primer grado de libertad con desplazamiento conocido
    # Tal vez con las restricciones
    
    # TODO: Hallar vector de desplazamientos
    
    # TODO: Hallar vector de Reacciones
    
    # TODO: Hallar y consolidar AIF
     
    return matrices_Result 

if __name__ == "__main__":
    pass