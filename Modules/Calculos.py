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
            angulo = (3/2 * np.pi) - np.arcsin(seno)
    if delta_x < 0:
        if delta_y > 0:
            angulo = (np.pi/2) -  np.arcsin(seno)
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
                case "2": 
                    coord_x = previousCoords[0]
                    coord_y = floatInput("Coordenada y del nodo: ")
                case "3":
                    coord_x = floatInput("Coordenada x del nodo: ")
                    coord_y = floatInput("Coordenada y del nodo: ")
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
            u =     intInput("\nIngrese el grado de libertad u del nodo: ")
            phi =   intInput("\nIngrese el grado de libertad phi del nodo: ")
            return (u,phi)
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
            
# Sistema de cargas puntuales
def get_carga(units, last_carga = None, edit = False):
    if edit:
        valor = intInput(f"\nIngrese el valor de la carga ({last_carga [0]})({units.loc[0,'Fuerza']}): ")
    else:
        valor = intInput(f"\nIngrese el valor de la carga ({units.loc[0,'Fuerza']}): ")
    
    while True:
        print("\nDirección la dirección de la carga : ")
        print("\n\t1. X")
        print("\n\t2. Y")
        
        if edit:
            seleccion = intInput(f"\nSeleccione la direccion de la carga ({last_carga [1]}): ")
        else :
            seleccion = intInput("\nSeleccione la direccion de la carga: ")
                
        match seleccion:
            case 1:
                direccion = "X"
                break
            case 2:
                direccion = "Y"
                break
            case _:
                print("\nOpción incorrecta")
    
    return (valor, direccion)
        
def get_ubicacionCarga(nodo, elemento, units, ID_n = None, ID_e = None, last_distancia = None, edit =False):
    while True:
        print("\nUbicación de la carga puntual.")
        print("\n\t1. En el nodo.")
        print("\n\t2. En el elemento.")
        match intInput("\nSeleccione la ubicación de la carga: "):
            case 1:
                ubicacion_n = set_nodoCarga(nodo, ID_n, edit)
                ubicacion_e = (False,False,False)
                break
            case 2:
                ubicacion_e = set_elementoCarga(elemento, units, last_distancia, ID_e, edit)
                ubicacion_n = (False,False)
                break
            case _:
                print("\nOpción incorrecta")
    return (ubicacion_n, ubicacion_e)

def set_nodoCarga(nodo, ID_n = None, edit = False):
    if not nodo.empty:   
        print("\nNodos actuales:\n")
        print(nodo)
        index_list = nodo.index.values.tolist()
        
        if edit:
            index = get_index(index_list,f"\nSeleccione el id del nodo en el que está ubicada la carga({ID_n}): ", edit, ID_n)
        else:
            index = get_index(index_list,"\nSeleccione el id del nodo en el que está ubicada la carga: ")

        print(f"\nNodo selecionado id [{index}]: ") 
        print(nodo.loc[[index]])
        
        return (index,nodo.loc[index,'Nombre'])
    else: 
        print("\nNo se encuentran nodos en la base de datos.\n")
        input("Presione enter para continuar.")
        return (False,False)
   
def set_elementoCarga(elemento, units, last_distancia = None, ID_e = None, edit = False):
    if not elemento.empty:
        print("\nElementos actuales:\n")
        print(elemento)
        index_list = elemento.index.values.tolist()
        
        if edit: 
            index = get_index(index_list,f"\nSeleccione el id del elemento en el cual está ubicada la carga({ID_e}): ", True, ID_e)
        else:
            index = get_index(index_list,f"\nSelecccione el id del elemento en el cual está ubicada la carga: ")
            
        print(f"\nElemento seleccionado id[{index}]: ")
        print(elemento.loc[[index]])
        
        print(f"\nEl nodo i del elemento {elemento.loc[index,'Nombre']} es: {elemento.loc[index,'Nodo i']} ")
         
        if edit: 
            distancia = floatInput(f"\nIngrese la distancia de la carga respecto al nodo i del elemento ({last_distancia})({units.loc[0,'Longitud']}): ")
        else:    
            distancia = floatInput(f"\nIngrese la distancia de la carga respecto al nodo i del elemento ({units.loc[0,'Longitud']}): ")
        
        return (index,elemento.loc[index,"Nombre"],distancia)
    else: 
        print("\nNo se encuentran elementos en la base de datos.\n")
        input("Presione enter para continuar.")
        return (False,False,False)
    
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
            Global_Local = np.array( [ np.cos(ang) , np.sin(ang) ,      0      ,      0      ]
                                    ,[      0      ,      0      , np.cos(ang) , np.sin(ang) ])
        case "Viga":
            return 1
        case "Portico":
            Global_Local = np.array([ [  np.cos(ang) , np.sin(ang) , 0 ,       0      ,      0      , 0 ]
                                     ,[ -np.sin(ang) , np.cos(ang) , 0 ,       0      ,      0      , 0 ]
                                     ,[       0      ,      0      , 1 ,       0      ,      0      , 0 ]
                                     ,[       0      ,      0      , 0 ,  np.cos(ang) , np.sin(ang) , 0 ]
                                     ,[       0      ,      0      , 0 , -np.sin(ang) , np.cos(ang) , 0 ]
                                     ,[       0      ,      0      , 0 ,       0      ,      0      , 1 ]])
    return Global_Local
if __name__ == "__main__":
    E = 27805574.98
    A = 0.25
    I = 0.005208333
    L = 5
    ang = 2.214297436

    
    estrutura = "Portico"
    k_p = pd.DataFrame(get_rigidez_local(estrutura,L,A,E,I))
    TGL = pd.DataFrame(get_Transformacion_GL(estrutura,ang))
    TLG = TGL.transpose()
    
    k_rigidez = (TLG.dot(k_p)).dot(TGL)
    
    """ print("K':\n")
    print(k_p)
    print("TGL:\n")
    print(TGL)
    print("TLG:\n")
    print(TLG)
    
    print("\n\nK_elemento:")
    print(k_rigidez)
     """
    matriz_global = np.zeros((6,6), dtype="float64")
    
    
    print(matriz_global)