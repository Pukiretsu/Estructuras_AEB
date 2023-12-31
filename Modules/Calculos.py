import pandas as pd
import numpy as np
import math as mt 
from os import system

# Configuraciones para display

pd.set_option('display.float_format', '{:.2f}'.format)

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
            
        return (index, seccion.loc[index, 'Nombre'])
    
    else: 
        print("\nNo se encuentran secciones en la base de datos.\n")
        input("Pulse enter para continuar.")
        return (None,False)
    
# Sistema de nodos

def set_coords(previousCoords = None, edit = False):
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
                    loads = set_carga_Triangular(loads, longitud, nodos, id_NodoI, id_NodoJ, units)
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

def set_carga_Triangular(loads, longitud, nodos, id_NodoI, id_NodoJ, units):
    while True:
        print("\nIndique el nodo donde está aplicada la carga.\n")
        
        print(f"\t1. Nodo i [{nodos.loc[id_NodoI,'Nombre']}].")
        print(f"\t2. Nodo j [{nodos.loc[id_NodoJ,'Nombre']}].")
        
        print("\n0. Volver.")
        match input("\nIngrese una opción: "):
                case "1":
                    valor = floatInput(f"\nIngrese el valor de la carga ({units.loc[0,'Fuerza']}/{units.loc[0,'Longitud']}): ")
                    nodo = "i"
                    break
                case "2":
                    valor = floatInput(f"\nIngrese el valor de la carga ({units.loc[0,'Fuerza']}/{units.loc[0,'Longitud']}): ")
                    nodo = "j"
                    break
                case "0":
                    return loads
                case _:
                    print("Error: no se reconoce la opción ingresada.\n")
    
    if nodo == "i":
        loads[1] = loads[1] + (7 * valor * longitud / 20)   # Vi
        loads[2] = loads[2] + (valor * longitud**2 / 20)    # Mi
        loads[4] = loads[4] + (3 * valor * longitud / 20)   # Vj
        loads[5] = loads[5] + ((-valor) * longitud**2 / 30) # Mj
    else:
        loads[1] = loads[1] + (3 * valor * longitud / 20)   # Vi
        loads[2] = loads[2] + (valor * longitud**2 / 30) # Mi
        loads[4] = loads[4] + (7 * valor * longitud / 20)   # Vi
        loads[5] = loads[5] + ((-valor) * longitud**2 / 20)    # Mj
    
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
    loads[5] = loads[5] + ((-valor) * a / longitud) * (2 - (3 * a / longitud))  # Mj
    
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
                case "kgf":
                    return 1000 / 9.81
                case "ton":
                    return 1 / 9.81
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
                case "kgf":
                    return 1/9.81
                case "ton":
                    return 1000 * 9.81
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
                case "kgf":
                    return 2.2046
                case "ton":
                    return 1/2204.622
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
                case "kgf":
                    return 1000 / 2.2046
                case "ton":
                    return 1/2.2046
                case _:
                    return 1
        case "ton":
            match unit_out:
                case "kN":
                    return 9.81
                case "N": 
                    return 1/(1000 * 9.81)
                case "lbf":
                    return 2204.622
                case "kipf":
                    return 2.2046
                case "kgf":
                    return 1000
                case _:
                    return 1
        case "kgf":
            match unit_out:
                case "kN":
                    return 9.81/1000 
                case "N": 
                    return 9.81
                case "lbf":
                    return 1/2.2046
                case "kipf":
                    return 2.2046/1000 
                case "ton":
                    return 1/1000
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
        print("\t5. Kilogramo fuerza. (kg)")
        print("\t6. Tonelada fuerza. (ton)")
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
                case "5": 
                    return "kg"
                case "6": 
                    return "ton"
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

def get_units(secondary = False):
    print("\n¿Qué unidad desea cambiar?: ")
    while True:
        print("\n\tUnidades.\n")
        print("\t1. Longitud.")
        print("\t2. Fuerza.")
        if not secondary:
            print("\t3. Esfuerzo.")
        print("\t4. Angulo.")
        print("\n0. Volver.")
        
        match input("\nSeleccione el tipo de Unidad: "):
                case "1": 
                    return ("L",unit_Longitud())
                case "2": 
                    return ("F",unit_Fuerza())
                case "3":
                    if not secondary:
                        return ("E",unit_Esfuerzo())
                    else:
                        print("Error: No se reconoce la opcion ingresada.\n\n")
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

# Matrices

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

# Grados de libertad

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

def get_indexes_desplazamiento(nodos, structureType):
    conocidos = list()
    for index in nodos.index:
        if nodos.loc[index,"Soporte"]:
            restricciones = nodos.loc[index,"Restriccion"]
            match restricciones:
                case "Y":
                    idx = nodos.loc[index,"V"]
                    conocidos.append(idx)
                case "X":
                    idx = nodos.loc[index,"U"]
                    conocidos.append(idx)
                case "XY":
                    if structureType != "Viga":
                        idx = nodos.loc[index,"U"]
                        conocidos.append(idx)
                    idx = nodos.loc[index,"V"]
                    conocidos.append(idx)
                case "XYM":
                    if structureType != "Viga":
                        idx = nodos.loc[index,"U"]
                        conocidos.append(idx)
                    idx = nodos.loc[index,"V"]
                    conocidos.append(idx)
                    idx = nodos.loc[index,"Phi"]
                    conocidos.append(idx)

    conocidos.sort()
    desconocidos = [*range(1,conocidos[0])]
    return (desconocidos,conocidos)

def get_Desplazamiento_Factor_per_GDL(nodos, factor, structureType):
    def set_units_GDL(unidades_gdl, idx, conf):
        unidades = {"Factor": []} 
        if conf == 1:
            unidades["Factor"].append(factor)
        else:
            unidades["Factor"].append(1)
            
        un_df = pd.DataFrame(unidades,index=[idx])
        unidades_gdl = pd.concat([unidades_gdl,un_df])
        return unidades_gdl
    
    unidades_gdl = pd.DataFrame({"Factor": pd.Series(dtype="float")})
    
    match structureType:
        case "Cercha":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
        case "Viga":
            for index in nodos.index:
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)
        case "Portico":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)

    unidades_gdl.sort_index()
    return unidades_gdl

def get_giro_Factor_per_GDL(nodos, factor, structureType):
    def set_units_GDL(unidades_gdl, idx, conf):
        unidades = {"Factor": []} 
        if conf == 2:
            unidades["Factor"].append(factor)
        else:
            unidades["Factor"].append(1)
            
        un_df = pd.DataFrame(unidades,index=[idx])
        unidades_gdl = pd.concat([unidades_gdl,un_df])
        return unidades_gdl
    
    unidades_gdl = pd.DataFrame({"Factor": pd.Series(dtype="float")})
    
    match structureType:
        case "Cercha":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
        case "Viga":
            for index in nodos.index:
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)
        case "Portico":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)

    unidades_gdl.sort_index()
    return unidades_gdl

def get_Carga_Factor_per_GDL(nodos, factor, structureType):
    def set_units_GDL(unidades_gdl, idx, conf):
        unidades = {"Factor": []} 
        if conf == 2:
            unidades["Factor"].append(factor)
        else:
            unidades["Factor"].append(factor)
            
        un_df = pd.DataFrame(unidades,index=[idx])
        unidades_gdl = pd.concat([unidades_gdl,un_df])
        return unidades_gdl
    
    unidades_gdl = pd.DataFrame({"Factor": pd.Series(dtype="float")})
    
    match structureType:
        case "Cercha":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
        case "Viga":
            for index in nodos.index:
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)
        case "Portico":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)

    unidades_gdl.sort_index()
    return unidades_gdl

def get_Momento_Factor_per_GDL(nodos, factor, structureType):
    def set_units_GDL(unidades_gdl, idx, conf):
        unidades = {"Factor": []} 
        if conf == 2:
            unidades["Factor"].append(factor)
        else:
            unidades["Factor"].append(1)
            
        un_df = pd.DataFrame(unidades,index=[idx])
        unidades_gdl = pd.concat([unidades_gdl,un_df])
        return unidades_gdl
    
    unidades_gdl = pd.DataFrame({"Factor": pd.Series(dtype="float")})
    
    match structureType:
        case "Cercha":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
        case "Viga":
            for index in nodos.index:
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)
        case "Portico":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)

    unidades_gdl.sort_index()
    return unidades_gdl

def get_units_per_GDL(nodos, units, structureType):
    
    def set_units_GDL(unidades_gdl, idx, conf):
        unidades = {"Desplazamiento": [], "Carga": []} 
        if conf == 1:
            unidades["Desplazamiento"].append(units.loc[1,"Longitud"])
            unidades["Carga"].append(units.loc[1,"Fuerza"])
        else:
            unidades["Desplazamiento"].append(units.loc[1,"Angulo"])
            unidades["Carga"].append(f"{units.loc[1,'Fuerza']}.{units.loc[1,'Longitud']}")
            
        un_df = pd.DataFrame(unidades,index=[idx])
        unidades_gdl = pd.concat([unidades_gdl,un_df])
        return unidades_gdl
    
    unidades_gdl = pd.DataFrame({"Desplazamiento": pd.Series(dtype="str"),
                                 "Carga" : pd.Series(dtype="str")})
    
    match structureType:
        case "Cercha":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
        case "Viga":
            for index in nodos.index:
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)
        case "Portico":
            for index in nodos.index:
                idx = nodos.loc[index,"U"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"V"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,1)
                idx = nodos.loc[index,"Phi"]
                unidades_gdl = set_units_GDL(unidades_gdl,idx,2)

    unidades_gdl.sort_index()
    return unidades_gdl

def get_AIF_Carga_factors(factor, structureType):
    match structureType:
        case "Cercha":
            factors = (factor, factor, factor, factor)
            return pd.DataFrame(factors)        
        case "Viga":
            factors = (factor, factor, factor, factor)
            return pd.DataFrame(factors)      
        case "Portico":
            factors = (factor, factor, factor, factor, factor, factor)
            return pd.DataFrame(factors)   

def get_AIF_Momento_factors(factor, structureType):
    match structureType:
        case "Cercha":
            factors = (1, 1, 1, 1)
            return pd.DataFrame(factors)        
        case "Viga":
            factors = (1, factor, 1, factor)
            return pd.DataFrame(factors)      
        case "Portico":
            factors = (1, 1, factor, 1, 1, factor)
            return pd.DataFrame(factors)    

def get_AIF_Indexes(structureType):
    match structureType:
        case "Cercha":
            labels = ("Ni", "Nj")
            return labels        
        case "Viga":
            labels = ("Vi", "Mi", "Vj", "Mj")
            return labels        
        case "Portico":
            labels = ("Ni", "Vi", "Mi", "Nj", "Vj", "Mj")
            return labels        

def get_AIF_units(units, structureType):
    Fuerza = units.loc[1,'Fuerza']
    Longitud = units.loc[1,'Longitud']
    Momento = f"{Fuerza}.{Longitud}"
    match structureType:
        case "Cercha":
            labels = (Fuerza, Fuerza)
            return labels        
        case "Viga":
            labels = (Fuerza, Momento, Fuerza, Momento)
            return labels        
        case "Portico":
            labels = (Fuerza, Fuerza, Momento, Fuerza, Fuerza, Momento)
            return labels        
        
# Cargas

def get_cargas_locales(loads, structureType):
    N_i = loads[0]
    V_i = loads[1]
    M_i = loads[2]
    N_j = loads[3]
    V_j = loads[4]
    M_j = loads[5]
    
    match structureType:
        case "Cercha":
            local_loads = (N_i, V_i, N_j, V_j)
            return pd.DataFrame(local_loads)        
        case "Viga":
            local_loads = (V_i, M_i, V_j, M_j)
            return pd.DataFrame(local_loads)        
        case "Portico":
            local_loads = (N_i, V_i, M_i, N_j, V_j, M_j)
            return pd.DataFrame(local_loads)        

def get_cargas_global(structureType, cargas_loc, TLG, GDL):
    match structureType:
        case "Cercha":
            cargas_globales = cargas_loc
        case "Viga":
            cargas_globales = cargas_loc
        case "Portico":
            cargas_globales = TLG.dot(cargas_loc)
            
    cargas_globales = pd.DataFrame(cargas_globales)
    cargas_globales.index = GDL
    
    
    return cargas_globales
    
# Consolidaciones

def consolidacion_cargasGlobal(structureType, Nnodos, results ):
    match structureType:
        case "Cercha":
            index = Nnodos * 2
        case "Viga":
            index = Nnodos * 2
        case "Portico":
            index = Nnodos * 3
            
    vector_Global = np.zeros((index), dtype="float64")
    vector_Global = pd.DataFrame(vector_Global)
    vector_Global.index += 1

    for elemento in results["Elementos"].keys():
        dataf_q = results["Elementos"][elemento]["Carga Global"]
        for index in dataf_q.index:
            vector_Global.loc[index] = vector_Global.loc[index] + dataf_q.loc[index]
    
    return vector_Global
            
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

# Calculos totales
      
def calculos(elementos, nodos, materiales, secciones, cargas, units, structureType):
    print("Calculando estructura...")
    Results = {"Elementos": dict(), "Matriz Global": [], "Vector Cargas Global": [], "Desplazamientos": [], "Reacciones":[], "unidades_resultados": []}
    
    fac_longitud = get_conversion_longitud(units.loc[0, "Longitud"], "m")
    fac_Fuerza = get_conversion_fuerza(units.loc[0, "Fuerza"], "kN")
    fac_Esfuerzo = get_conversion_esfuerzo(units.loc[0, "Esfuerzo"], "Kpa")
    fac_angulo = get_conversion_angulo(units.loc[0, "Angulo"], "rad")
    
    # Calculo de matrices de rigidez locales y transformacion a globales asi como de vectores globales
    
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
        
        ID_loads = elementos.loc[index,"ID_cargas"]
        
        N_i = cargas.loc[ID_loads,"N_i"] * fac_Fuerza
        V_i = cargas.loc[ID_loads,"V_i"] * fac_Fuerza
        M_i = cargas.loc[ID_loads,"M_i"] * fac_Fuerza / fac_longitud
        N_j = cargas.loc[ID_loads,"N_j"] * fac_Fuerza
        V_j = cargas.loc[ID_loads,"V_j"] * fac_Fuerza
        M_j = cargas.loc[ID_loads,"M_j"] * fac_Fuerza / fac_longitud
        
        loads = [N_i, V_i, M_i, N_j, V_j, M_j]
        cargas_locales = get_cargas_locales(loads,structureType)
                
        cargas_Globales = get_cargas_global(structureType, cargas_locales, TLG, grados_libertad)
        Results["Elementos"][f"{index}"] = {"Nombre": nombre_Elemento, 
                                            "rigidez": k_p, 
                                            "TGL": TGL, 
                                            "k rigidez local": k_rigidez, 
                                            "Carga local": cargas_locales, 
                                            "Carga Global": cargas_Globales}
    
    print("Configuracion de elementos [✅]")
    
    nnodos = len(nodos.index)
    
    unidades_resultados = get_units_per_GDL(nodos, units, structureType)
    Results["unidades_resultados"] = unidades_resultados
    
    # Consolidacion vectores carga global
    
    vector_global = consolidacion_cargasGlobal(structureType, nnodos, Results)
    Results["Vector Cargas Global"] = vector_global

    print("Vector de carga global [✅]")
    
    # Consolidacion de matrices globales.
    
    matriz_global = consolidación_RigidezGLobal(structureType, nnodos, Results)
    Results["Matriz Global"] = matriz_global
    
    print("Matriz de rigidez global [✅]")
    
    # Encontrar indices para matriz K11 y K12 (desplazamientos conocidos y desconocidos)
    
    indexes = get_indexes_desplazamiento(nodos, structureType)
    
    # Se hallan los desplazamientos
    
    K11 = np.linalg.inv(Results["Matriz Global"].loc[indexes[0],indexes[0]].values)
    Q11 = Results["Vector Cargas Global"].loc[indexes[0]].values
    
    desp_desconocidos = pd.DataFrame(np.dot(K11,Q11), index=indexes[0])
    desp_conocidos = pd.DataFrame(np.zeros(len(indexes[1])), index=indexes[1])
    desplazamientos = pd.concat([desp_desconocidos, desp_conocidos])
    
    Results["Desplazamientos"] = desplazamientos

    print("Desplazamientos [✅]")
    
    # Se hallan las reacciones
    
    K12 = Results["Matriz Global"].loc[indexes[1],indexes[0]].to_numpy()
    desp_desconocidos = desp_desconocidos.to_numpy()
    Q12 = Results["Vector Cargas Global"].loc[indexes[1]].to_numpy()
    
    calc_reacciones = np.dot(K12,desp_desconocidos)
    calc_reacciones = np.subtract(calc_reacciones, Q12)
    calc_reacciones = pd.DataFrame(calc_reacciones,index=indexes[1])
    
    empty_Reacciones = pd.DataFrame(np.zeros(len(indexes[0])), index=indexes[0])
    reacciones = pd.concat([empty_Reacciones, calc_reacciones])

    Results["Reacciones"] = reacciones
    
    
    print("Reacciones [✅]")
    
    # Acciones de fuerzas internas
    
    for elemento in Results["Elementos"].keys():
        grados_libertad = Results["Elementos"][elemento]["k rigidez local"].index
        
        k_local = Results["Elementos"][elemento]["rigidez"].to_numpy()
        TGL = Results["Elementos"][elemento]["TGL"].to_numpy()
        Q_local = Results["Elementos"][elemento]["Carga Global"].to_numpy()
        
        desplazamientos_locales = Results["Desplazamientos"].loc[grados_libertad].to_numpy()
        AIF = np.dot(k_local, TGL)
        AIF = np.dot(AIF, desplazamientos_locales)
        if structureType != "Cercha":
            AIF = np.subtract(AIF, Q_local)
        AIF = pd.DataFrame(AIF)
        Results["Elementos"][elemento]["AIF"] = AIF
      
    print("Acciones de Fuerzas internas [✅]")
    
    print("-------------------------------")  
    
    return Results 

if __name__ == "__main__":
    pass