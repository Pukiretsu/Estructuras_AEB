import pandas as pd
import json
import Modules.Calculos as calc
import os

# Definicion de dataframes en el contexto

UNIDADES = pd.DataFrame({"Longitud": ["m"],
                         "Fuerza": ["kN"],
                         "Esfuerzo": ["mpa"],
                         "Angulo": ["°"]}) # Se añaden las unidades del SI por defecto

NODOS = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                     "Coordenada x": pd.Series(dtype="float"),
                     "Coordenada y": pd.Series(dtype="float"),
                     "U": pd.Series(dtype="int"),
                     "V": pd.Series(dtype="int"), 
                     "Phi": pd.Series(dtype="int"),
                     "Soporte": pd.Series(dtype="bool"),
                     "Restriccion": pd.Series(dtype="int")})

ELEMENTOS = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                          "ID ni": pd.Series(dtype="int64"),
                          "Nodo i": pd.Series(dtype="str"),
                          "ID nj": pd.Series(dtype="int64"), 
                          "Nodo j": pd.Series(dtype="str"), 
                          "Longitud": pd.Series(dtype="float"),
                          "Angulo": pd.Series(dtype="float"), 
                          "ID Mat": pd.Series(dtype="int64"),
                          "Material": pd.Series(dtype="str"),
                          "ID Sec": pd.Series(dtype="int64"),
                          "Seccion": pd.Series(dtype="str")}) 

MATERIALES = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                           "Modulo Young": pd.Series(dtype="float")})

SECCIONES = pd.DataFrame({"Nombre": pd.Series(dtype="str"), 
                          "Area": pd.Series(dtype="float"), 
                          "Inercia": pd.Series(dtype="float")})

CARGAS_PUNTUALES = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                                 "Valor": pd.Series(dtype="float"),
                                 "Direccion": pd.Series(dtype="str"),
                                 "Nodo" : pd.Series(dtype="str"),
                                 "ID_n" : pd.Series(dtype="int"),
                                 "Elemento": pd.Series(dtype="str"),
                                 "ID_e": pd.Series(dtype="int"),
                                 "Distancia": pd.Series(dtype="float")})

CARGAS_DISTRIBUIDAS = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                                    "Carga i": pd.Series(dtype="float"),
                                    "Carga f": pd.Series(dtype="float"),
                                    "Elemento": pd.Series(dtype="str"),
                                    "ID_e": pd.Series(dtype="int"),
                                    "Distancia i": pd.Series(dtype="float"),
                                    "Distancia f": pd.Series(dtype="float")})

MOMENTOS = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                         "Valor": pd.Series(dtype="float"),
                         "Nodo" : pd.Series(dtype="str"),
                         "ID_n" : pd.Series(dtype="int"),
                         "Elemento": pd.Series(dtype="str"),
                         "ID_e": pd.Series(dtype="int"),
                         "Distancia": pd.Series(dtype="float")})

# Funciones de soporte

def confirmation(message) -> bool:
    while True:
        print(f"\n{message}")
        response = input("(s/N): ") or "N"
        if response == "s" or response == "S":
            return True
        elif response == "n" or response == "N":
            return False
        else:
            pass

def get_index(Index_list) -> bool:
    while True:
            try:
                index = int(input("\nIngrese el id a seleccionar: "))
                if Index_list.count(index) == 0:
                    raise Exception() 
                break
            except:
                print("Error: id inválido.\n")
    return index

def check_index(lookupDf, lookupQuery, value) -> bool:
    check_series = lookupDf.loc[:, lookupQuery]
    if value in check_series.values:
        return True

class model():
    def __init__(self) -> None:
        self.nombre = "Modelo Nuevo"
        self.tipo_estructura = None
        self.unidades = UNIDADES 
        self.nodos = NODOS
        self.elementos = ELEMENTOS
        self.materiales = MATERIALES
        self.secciones = SECCIONES
        self.cargas_Puntuales = CARGAS_PUNTUALES
        self.cargas_Distribuidas = CARGAS_DISTRIBUIDAS
        self.momentos = MOMENTOS
        self.resultados = None

    #Carga y descarga de modelos
    def load_model(self, path) -> None:
        with open(path,"r") as f:
            data = json.loads(f.read())
            
        self.nombre                 = data["Model-meta"]["Model_Name"]
        self.tipo_estructura        = data["Model-meta"]["STRUCTURETYPE"]
        self.unidades               = pd.json_normalize(data, record_path = ["UNIDADES"])
        self.nodos                  = pd.concat([self.nodos, pd.json_normalize(data, record_path = ["NODOS"])])
        self.elementos              = pd.concat([self.elementos, pd.json_normalize(data, record_path = ["ELEMENTOS"])])
        self.materiales             = pd.concat([self.materiales, pd.json_normalize(data, record_path = ["MATERIALES"])])
        self.secciones              = pd.concat([self.secciones, pd.json_normalize(data, record_path = ["SECCIONES"])]) 
        self.cargas_Puntuales       = pd.concat([self.cargas_Puntuales, pd.json_normalize(data, record_path = ["CARGAS_PUNTUALES"])]) 
        self.cargas_Distribuidas    = pd.concat([self.cargas_Distribuidas, pd.json_normalize(data, record_path = ["CARGAS_DISTRIBUIDAS"])]) 
        self.momentos               = pd.concat([self.momentos, pd.json_normalize(data, record_path = ["MOMENTOS"])]) 

    def save_model(self, path, date) -> None:
        file = os.path.basename(path)
        self.nombre = os.path.splitext(file)[0]
        data = {'Model-meta': 
                            {'STRUCTURETYPE': self.tipo_estructura,
                            'Date_Saved': date,
                            'Model_Name': self.nombre},
                            
                'UNIDADES':             self.unidades.to_dict('records'),
                'NODOS':                self.nodos.to_dict('records'),
                'ELEMENTOS':            self.elementos.to_dict('records'),
                'MATERIALES':           self.materiales.to_dict('records'),
                'SECCIONES':            self.secciones.to_dict('records'),
                'CARGAS_PUNTUALES':     self.cargas_Puntuales.to_dict('records'),
                'CARGAS_DISTRIBUIDAS':  self.cargas_Distribuidas.to_dict('records'),
                'MOMENTOS':             self.momentos.to_dict('records')}
        
        with open(path, "w") as f:
            json.dump(data,f,indent=6)

    # Unidades        
    def convert_Longitud(self, factor_conversion) -> None:
        # Area y inercia
        for idx in self.secciones.index:
            self.secciones.loc[idx,"Area"] = self.secciones.loc[idx,"Area"] * (factor_conversion**2)
            self.secciones.loc[idx,"Inercia"] = self.secciones.loc[idx,"Inercia"] * (factor_conversion**4)
        # Distancia de elementos
        for idx in self.elementos.index:
            self.elementos.loc[idx,"Longitud"] = self.elementos.loc[idx, "Longitud"] * (factor_conversion)

    def convert_Fuerza(self, factor_conversion) -> None:
        pass #TODO
    
    def convert_Esfuerzo(self, factor_conversion) -> None:
        # Modulo young
        for idx in self.materiales.index:
            self.materiales.loc[idx,"Modulo Young"] = self.materiales.loc[idx,"Modulo Young"]*factor_conversion #BUG HAY PROBLEMA CON LA CONVERSION
    
    def convert_Angulo(self, factor_conversion) -> None:
        # Grados de elementos
        for idx in self.elementos.index:
            self.elementos.loc[idx,"Angulo"] = self.elementos.loc[idx, "Angulo"] * (factor_conversion)
        
    def set_units(self) -> None:
        units = {"Longitud": [], "Fuerza": [], "Esfuerzo": [], "Angulo": [], }
        
        print("Unidades actuales:\n")
        print(self.unidades)
        
        units["Longitud"].append(self.unidades.loc[0,'Longitud'])
        units["Fuerza"].append(self.unidades.loc[0,'Fuerza'])
        units["Esfuerzo"].append(self.unidades.loc[0,'Esfuerzo'])
        units["Angulo"].append(self.unidades.loc[0,'Angulo'])
        
        unidades = calc.get_units()
        
        if not (unidades[1]):
            pass
        else:    
            match unidades[0]:
                case "L":
                    units["Longitud"].pop(0)
                    units["Longitud"].append(unidades[1])
                    
                    fact_conversion = calc.get_conversion_longitud(self.unidades.loc[0,'Longitud'],unidades[1])
                    self.convert_Longitud(fact_conversion) 
                
                case "F":
                    units["Fuerza"].pop(0)
                    units["Fuerza"].append(unidades[1])
                    
                    fact_conversion = calc.get_conversion_fuerza(self.unidades.loc[0,'Fuerza'],unidades[1])
                    self.convert_Fuerza(fact_conversion) 
                
                case "E":
                    units["Esfuerzo"].pop(0)
                    units["Esfuerzo"].append(unidades[1])
                    
                    fact_conversion = calc.get_conversion_esfuerzo(self.unidades.loc[0,'Esfuerzo'],unidades[1])
                    self.convert_Esfuerzo(fact_conversion) 
                
                case "G":
                    units["Angulo"].pop(0)
                    units["Angulo"].append(unidades[1])
                    
                    fact_conversion = calc.get_conversion_angulo(self.unidades.loc[0,'Angulo'],unidades[1])
                    self.convert_Angulo(fact_conversion) 
                
                case _:
                    pass
        
        self.unidades = self.unidades.drop([0])
        new_units = pd.DataFrame(units)
        self.unidades = pd.concat([self.unidades, new_units])

    # Miscelaneos
    def set_structureType(self) -> None:
        self.tipo_estructura = calc.set_structure_type()

    # Nodos
    def add_node(self) -> None:
        node = {"Nombre": [], "Coordenada x": [], "Coordenada y": [], "U": [], "V": [], "Phi": [], "Soporte": [], "Restriccion": []}
        
        print("\nNuevo nodo.")
        
        try:
            index = max(self.nodos.index) + 1
        except:
            index = len(self.nodos.index)
        
        nombre = input("\nIngrese un nombre para el nodo (En blanco nombre por defecto): ")
        if not (nombre):
            nombre = f"Nodo {index}"

        coordenadas = calc.set_coords()
        gdl = calc.get_grados_Libertad(self.tipo_estructura)
        
        confirm = confirmation("¿El Nodo es apoyo?.")
        if confirm:
            soporte = calc.get_support(self.tipo_estructura)
        else:
            soporte = (False,"")
        
        node["Nombre"].append(nombre)
        node["Coordenada x"].append(coordenadas[0])
        node["Coordenada y"].append(coordenadas[1])
        
        match self.tipo_estructura:
            case "Cercha":
                node["U"].append(gdl[0])
                node["V"].append(gdl[1])
                node["Phi"].append(None)
            case "Viga":
                node["U"].append(gdl[0])
                node["V"].append(None)
                node["Phi"].append(gdl[1])
            case "Portico":
                node["U"].append(gdl[0])
                node["V"].append(gdl[1])
                node["Phi"].append(gdl[2])
        
        node["Soporte"] = soporte[0]
        node["Restriccion"] = soporte[1]
        node["Restriccion"] = soporte[1]
        
        new_node = pd.DataFrame(node, index=[index])
        self.nodos = pd.concat([self.nodos,new_node]) 
     
    def edit_node(self) -> None:
        print("\nNodos actuales:\n")
        print(self.nodos)
        
        node = {"Nombre": [], "Coordenada x": [], "Coordenada y": [], "U": [], "V": [], "Phi": [], "Soporte": [], "Restriccion": []}
    
        indexes = self.nodos.index.values.tolist()
        index = get_index(indexes)
        
        print(f"\nNodo seleccionado id: [{index}]")
        print(self.nodos.loc[[index]])
        
        nombre = input(f"\nNombre ({self.nodos.loc[index,'Nombre']}): ") or self.nodos.loc[index,'Nombre']
        last_coords = (self.nodos.loc[index,'Coordenada x'],self.nodos.loc[index,'Coordenada y'])
        coordenadas = calc.set_coords(last_coords,True) or last_coords
        gdl = calc.get_grados_Libertad(self.tipo_estructura)       
        
        confirm = confirmation("¿El Nodo es apoyo?.")
        if confirm:
            if self.nodos.loc[index, 'Soporte']:
                soporte = calc.get_support(self.tipo_estructura, True) or (self.nodos.loc[index,'Soporte'], self.nodos.loc['Restriccion'])
            else:
                soporte = calc.get_support(self.tipo_estructura)
        else:
            soporte = (False,"")
        
        node["Nombre"].append(nombre)
        node["Coordenada x"].append(coordenadas[0])
        node["Coordenada y"].append(coordenadas[1])
        
        match self.tipo_estructura:
            case "Cercha":
                node["U"].append(gdl[0])
                node["V"].append(gdl[1])
                node["Phi"].append(None)
            case "Viga":
                node["U"].append(gdl[0])
                node["V"].append(None)
                node["Phi"].append(gdl[1])
            case "Portico":
                node["U"].append(gdl[0])
                node["V"].append(gdl[1])
                node["Phi"].append(gdl[2])
                
        node["Soporte"] = soporte[0]
        node["Restriccion"] = soporte[1]
        
        self.nodos = self.nodos.drop([index])
        new_node = pd.DataFrame(node, index=[index])
        
        self.nodos = pd.concat([self.nodos,new_node])
        self.nodos = self.nodos.sort_index()
        
    def delete_node(self) -> None:
        print("\nNodos actuales:\n")
        print(self.nodos)
        
        indexes = self.nodos.index.values.tolist()
        index = get_index(indexes)
        
        # Verificacion de asociatividad con elementos
        check_elements_ni = check_index(self.elementos, "ID ni", index)
        check_elements_nj = check_index(self.elementos, "ID nj", index)
        
        if check_elements_ni or check_elements_nj:
            print("\nEl Nodo no puede ser eliminado porque se encuentra en uso.")
            input("\nPresione enter para continuar.")
        else:
            print(f"\nNodo seleccionado id: [{index}]")
            print(self.nodos.loc[[index]])
        
            confirmacion = confirmation(f"Confirmar eliminación {self.nodos.loc[index,'Nombre']} id:{index}")
            if confirmacion:
                print(self.nodos)
                self.nodos = self.nodos.drop([index])
     
    # Elementos
    def add_element(self) -> None:
        elemento = {"Nombre": [], "ID ni": [], "Nodo i": [], "ID nj": [], "Nodo j": [], "Longitud": [], "Angulo": [], "ID Mat": [], "Material": [], "ID Sec": [], "Seccion": []}
        
        print("\nNuevo elemento.")
        
        try:
            index = max(self.elementos.index) + 1
        except:
            index = len(self.elementos.index)   
        
        nombre = input("\nIngrese un nombre para el elemento (En blanco nombre por defecto): ")
        if not (nombre):
            nombre = f"Elemento {index}"
            
        nodos = calc.set_nodos(self.nodos) 
        
        if nodos: 
            longitud = calc.get_longitud(self.nodos, nodos[0][0],nodos[1][0], self.unidades.loc[0,'Longitud'])
            angulo = calc.get_angulo(longitud[0],longitud[1][0],longitud[1][1], self.unidades.loc[0,'Angulo'])     
            
            print(f"\nLa longitud del elemento es: {longitud[0]:.2f} {self.unidades.loc[0, 'Longitud']}")
            print(f"\nEl ángulo del elemento es: {angulo:.2f} {self.unidades.loc[0, 'Angulo']}")
        
        material = calc.set_material(self.materiales)
        seccion = calc.set_seccion(self.secciones) 
        
        elemento["Nombre"].append(nombre)
        elemento["ID ni"].append(nodos[0][0])
        elemento["Nodo i"].append(nodos[0][1])
        elemento["ID nj"].append(nodos[1][0])
        elemento["Nodo j"].append(nodos[1][1])
        elemento["Longitud"].append(longitud[0])
        elemento["Angulo"].append(angulo)
        elemento["ID Mat"].append(material[0])
        elemento["Material"].append(material[1])
        elemento["ID Sec"].append(seccion[0])
        elemento["Seccion"].append(seccion[1])
        
        new_element = pd.DataFrame(elemento, index=[index])
        
        self.elementos = pd.concat([self.elementos,new_element])
        
    def edit_element(self) -> None:
        print("\nElementos actuales: \n")
        print(self.elementos)

        elemento = {"Nombre": [], "ID ni": [], "Nodo i": [], "ID nj": [], "Nodo j": [], "Longitud": [], "Angulo": [], "ID Mat": [], "Material": [], "ID Sec": [], "Seccion": []}

        indexes = self.elementos.index.values.tolist()
        index = get_index(indexes)
        
        print(f"\nElemento seleccionado id: [{index}]")
        print(self.elementos.loc[[index]])
        
        nombre = input(f"\nNombre ({self.elementos.loc[index, 'Nombre']}): ") or self.elementos.loc[index, 'Nombre']
        
        last_nodos = ((self.elementos.loc[index,"ID ni"],self.elementos.loc[index,"Nodo i"]),(self.elementos.loc[index,"ID nj"],self.elementos.loc[index,"Nodo j"]))
        
        confirm = confirmation("\n¿Editar nodos?")
        if confirm :
            nodos = calc.set_nodos(self.nodos, last_nodos[0][0], last_nodos[1][0], True)  
        else:
            nodos = last_nodos
            
        if nodos: 
            longitud = calc.get_longitud(self.nodos, nodos[0][0],nodos[1][0], self.unidades.loc[0,'Longitud'])
            angulo = calc.get_angulo(longitud[0],longitud[1][0],longitud[1][1], self.unidades.loc[0,'Angulo'])
        
        if confirm:
            print(f"\nLa longitud del elemento es: {longitud[0]:.2f} {self.unidades.loc[0, 'Longitud']}")
            print(f"\nEl ángulo del elemento es: {angulo:.2f} {self.unidades.loc[0, 'Angulo']}")
        
        last_material = (self.elementos.loc[index, "ID Mat"],self.elementos.loc[index,"Material"])
        confirm = confirmation("\n¿Editar material?")
        
        if confirm:
            if last_material:
                material = calc.set_material(self.materiales, last_material, True)
            else:
                material = calc.set_material(self.materiales)
        else: 
            material = last_material
        
        last_seccion = (self.elementos.loc[index, "ID Sec"],self.elementos.loc[index,"Seccion"])
        confirm =confirmation("\n¿Editar la sección?")
        if confirm:
            if last_seccion:
                seccion =  calc.set_seccion(self.secciones, last_seccion, True)
            else:
                seccion =  calc.set_seccion(self.secciones)
        else:
            seccion = last_seccion
        
        elemento["Nombre"].append(nombre)
        elemento["ID ni"].append(nodos[0][0])
        elemento["Nodo i"].append(nodos[0][1])
        elemento["ID nj"].append(nodos[1][0])
        elemento["Nodo j"].append(nodos[1][1])
        elemento["Longitud"].append(longitud[0])
        elemento["Angulo"].append(angulo)
        elemento["ID Mat"].append(material[0])
        elemento["Material"].append(material[1])
        elemento["ID Sec"].append(seccion[0])
        elemento["Seccion"].append(seccion[1])
        
        self.elementos = self.elementos.drop([index])
        new_element = pd.DataFrame(elemento, index=[index])
        
        self.elementos = pd.concat([self.elementos,new_element])
        self.elementos = self.elementos.sort_index() 
            
    def delete_element(self) -> None:
        print("\nElementos actuales:\n")
        print(self.elementos)
        
        indexes = self.elementos.index.values.tolist()
        index = get_index(indexes)
        
        print(f"\nElemento seleccionado id: [{index}]")
        print(self.elementos.loc[[index]])
        
        confirmacion = confirmation(f"Confirmar eliminación {self.elementos.loc[index,'Nombre']} id:{index}")
        if confirmacion: 
            self.elementos = self.elementos.drop([index])

    # Secciones
    def add_section(self) -> None:
        section = {"Nombre": [], "Area": [], "Inercia": []}
        
        print("\nNueva sección.")
        
        try:
            index = max(self.secciones.index) + 1
        except:
            index = len(self.secciones.index)
        
        nombre = input("\nIngrese un nombre para la sección (En blanco nombre por defecto): ")
        if not (nombre):
            nombre = f"Seccion {index}"
            
        sectionCalcs = calc.get_section_calcs(self.unidades.loc[0,"Longitud"])
        
        # Consolidación de entrada
        
        section["Nombre"].append(nombre)
        section["Area"].append(sectionCalcs[0])
        section["Inercia"].append(sectionCalcs[1])
        
        new_Sect = pd.DataFrame(section, index=[index])

        # Ingreso a Dataframe de nueva entrada
        
        self.secciones = pd.concat([self.secciones,new_Sect])
        
    def edit_section(self) -> None:
        print("\nSecciones actuales:\n")
        print(self.secciones)
        
        section = {"Nombre": [], "Area": [], "Inercia": []}
        indexes = self.secciones.index.values.tolist()
        index = get_index(indexes)
                
        print(f"\nSeccion seleccionada id: [{index}]")
        print(self.secciones.loc[[index]])
        
        nombre = input(f"\nNombre ({self.secciones.loc[index,'Nombre']}): ") or self.secciones.loc[index,'Nombre']
        sectionCalcs = calc.get_section_calcs(self.unidades.loc[0,"Longitud"],True) or (self.secciones.loc[index,'Area'],self.secciones.loc[index,'Inercia'])
        
        section["Nombre"].append(nombre)
        section["Area"].append(sectionCalcs[0])
        section["Inercia"].append(sectionCalcs[1])
        
        self.secciones = self.secciones.drop([index])
        new_Sect = pd.DataFrame(section, index=[index])
        
        self.secciones = pd.concat([self.secciones,new_Sect])
        self.secciones = self.secciones.sort_index()
    
    def delete_section(self) -> None:
        print("\nSecciones actuales:\n")
        print(self.secciones)
        
        indexes = self.secciones.index.values.tolist()
        index = get_index(indexes)
        
        check_elements_IDSec = check_index(self.elementos, "ID Sec", index)
        
        if check_elements_IDSec:
            print("\nLa sección no puede ser eliminada porque se encuentra en uso.")
            input("\nPresione enter para continuar.")
        else:
            print(f"\nSeccion seleccionada id:{index}")
            print(self.secciones.loc[[index]])
            
            confirmacion = confirmation(f"Confirmar eliminación {self.secciones.loc[index,'Nombre']} id:{index}")
            if confirmacion:
                self.secciones = self.secciones.drop([index])

    # Materiales
    def add_material(self) -> None:
        material = {"Nombre": [], "Modulo Young": []}
        
        print("\nNuevo Material.")
        
        try:
            index = max(self.materiales.index) + 1
        except:
            index = len(self.materiales.index)
        
        nombre = input("\nIngrese un nombre para el material (En blanco nombre por defecto): ")
        if not (nombre):
            nombre = f"Material {index}"

        moduloY = calc.get_moduloYoung(self.unidades)
        
        # Consolidación de entrada
        
        material["Nombre"].append(nombre)
        material["Modulo Young"].append(moduloY)
        
        new_Mate = pd.DataFrame(material, index=[index])
        
        self.materiales = pd.concat([self.materiales,new_Mate])
        
    def edit_material(self) -> None:
        print("\nMateriales actuales:\n")
        print(self.materiales)
    
        material = {"Nombre": [], "Modulo Young": []}
        indexes = self.materiales.index.values.tolist()
        index = get_index(indexes)
        
        print(f"\nMaterial seleccionada id: [{index}]")
        print(self.materiales.loc[[index]])
        
        nombre = input(f"\nNombre ({self.materiales.loc[index,'Nombre']}): ") or self.materiales.loc[index,'Nombre']
        
        last_moduloY = self.materiales.loc[index,'Modulo Young']
        
        confirm = confirmation("\n¿Modificar el modulo de young?")
        if confirm:
            moduloY = calc.get_moduloYoung(self.unidades,last_moduloY,True) or last_moduloY
        else:
            moduloY = last_moduloY
        
        material["Nombre"].append(nombre)
        material["Modulo Young"].append(moduloY)
        
        self.materiales = self.materiales.drop([index])
        new_Mate = pd.DataFrame(material, index=[index])
        
        self.materiales = pd.concat([self.materiales,new_Mate])
        self.materiales = self.materiales.sort_index()
        
    def delete_material(self) -> None:
        print("\nMateriales actuales:\n")
        print(self.materiales)
        
        indexes = self.materiales.index.values.tolist()
        index = get_index(indexes)
        
        check_elements_IDMat = check_index(self.elementos, "ID Mat", index)
        
        if check_elements_IDMat:
            print("\nEl Material no puede ser eliminado porque se encuentra en uso.")
            input("\nPresione enter para continuar.")
        else:
            print(f"\nMaterial seleccionado id:{index}")
            print(self.materiales.loc[[index]])
            
            confirmacion = confirmation(f"Confirmar eliminación {self.materiales.loc[index,'Nombre']} id:{index}")
            if confirmacion:
                self.materiales = self.materiales.drop([index])

    # Cargas puntales
    def add_cargapuntual(self) -> None: 
        carga_puntual = {"Nombre": [], "Valor": [], "Direccion": [], "Nodo": [], "ID_n": [], "Elemento": [], "ID_e": [], "Distancia": []}
        print("\nNueva carga puntual.")
        
        try:
            index = max(self.cargas_Puntuales.index) + 1
        except:
            index =len(self.cargas_Puntuales.index)
        
        nombre = input("\nIngrese un nombre para la carga puntual (En blanco nombre por defecto): ")
        if not (nombre):
            nombre = f"Carga puntual {index}"
            
        carga = calc.get_cargaP(self.unidades) 
        valor = carga[0]
        direccion = carga[1]
        
        ubicacion = calc.get_ubicacionCarga(self.nodos, self.elementos, self.unidades)
        
        id_n = ubicacion[0][0]
        nodo = ubicacion[0][1]
        id_e = ubicacion[1][0]
        elemento = ubicacion [1][1]
        distancia = ubicacion[1][2]
        
        carga_puntual["Nombre"].append(nombre)
        carga_puntual["Valor"].append(valor)
        carga_puntual["Direccion"].append(direccion)
        carga_puntual["Nodo"].append(nodo)
        carga_puntual["ID_n"].append(id_n)
        carga_puntual["Elemento"].append(elemento)
        carga_puntual["ID_e"].append(id_e)
        carga_puntual["Distancia"].append(distancia)
        
        new_cargaP = pd.DataFrame(carga_puntual, index=[index])
        
        self.cargas_Puntuales = pd.concat([self.cargas_Puntuales,new_cargaP])
        
    def edit_cargapuntual(self) -> None: 
        print("\nCargas puntuales actuales: \n")
        print(self.cargas_Puntuales)
        
        carga_puntual = {"Nombre": [], "Valor": [], "Direccion": [], "Nodo": [], "ID_n": [], "Elemento": [], "ID_e": [], "Distancia": []}

        indexes = self.cargas_Puntuales.index.values.tolist()
        index = get_index(indexes)
        
        print(f"\nCarga puntual seleccionada id: [{index}]")
        print(self.cargas_Puntuales.loc[[index]])
        
        nombre = input(f"\nNombre ({self.cargas_Puntuales.loc[index, 'Nombre']}): ") or self.cargas_Puntuales.loc[index, 'Nombre']
        
        last_carga = (self.cargas_Puntuales.loc[index,'Valor'],self.cargas_Puntuales.loc[index, 'Direccion'])
        confirmacion = confirmation( "\n¿Cambiar valores?")
        if confirmacion:
            carga = calc.get_cargaP(self.unidades, last_carga, True)
        else:
            carga = last_carga  
        
        valor = carga[0]
        direccion = carga[1]

        last_ubicacion = ((self.cargas_Puntuales.loc[index, 'ID_n'],self.cargas_Puntuales.loc[index, 'Nodo']),(self.cargas_Puntuales.loc[index, 'ID_e'],self.cargas_Puntuales.loc[index, 'Elemento'],self.cargas_Puntuales.loc[index, 'Distancia']))
        confirmacion = confirmation("¿Quiere editar la ubicacion de la carga?")
        if confirmacion: 
            ubicacion = calc.get_ubicacionCarga(self.nodos, self.elementos, self.unidades, last_ubicacion[0][0], last_ubicacion[1][0], True)
        else :
            ubicacion = last_ubicacion
            
        id_n = ubicacion[0][0]
        nodo = ubicacion[0][1]
        id_e = ubicacion[1][0]
        elemento = ubicacion [1][1]
        distancia = ubicacion[1][2]
        
        carga_puntual["Nombre"].append(nombre)
        carga_puntual["Valor"].append(valor)
        carga_puntual["Direccion"].append(direccion)
        carga_puntual["Nodo"].append(nodo)
        carga_puntual["ID_n"].append(id_n)
        carga_puntual["Elemento"].append(elemento)
        carga_puntual["ID_e"].append(id_e)
        carga_puntual["Distancia"].append(distancia)
        
        self.cargas_Puntuales = self.cargas_Puntuales.drop([index])
        new_cargaP = pd.DataFrame(carga_puntual, index=[index])
        
        self.cargas_Puntuales = pd.concat([self.cargas_Puntuales,new_cargaP])
        self.cargas_Puntuales = self.cargas_Puntuales.sort_index() 
    
    def delete_cargapuntual(self) -> None: 
        print("\nCargas puntuales actuales: \n")
        print(self.cargas_Puntuales)
        
        indexes = self.cargas_Puntuales.index.values.tolist()
        index = get_index(indexes)
        
        confirmacion = confirmation(f"Confirmar eliminación {self.cargas_Puntuales.loc[index,'Nombre']} id:{index}")
        if confirmacion: 
            self.cargas_Puntuales = self.cargas_Puntuales.drop([index])

    # Cargas Distribuidas
    def add_cargadistribuida(self) -> None:
        carga_distribuida = {"Nombre": [], "Carga i": [], "Carga f": [], "Direcccion": [], "Elemento": [], "ID_e": [], "Distancia i": [], "Distancia f": []}
        print("\nNueva carga distribuida")
        
        try:
            index = max(self.cargas_Distribuidas.index) + 1
        except:
            index = len(self.cargas_Distribuidas.index) 
            
        nombre = input("\nIngrese un nombre para la carga distribuida (En blanco nombre por defecto):")
        if not (nombre):
            nombre = f"Carga distribuida {index}"
            
        carga = calc.get_cargaD(self.unidades)
        carga_i = carga[0][0]
        carga_f = carga[0][1]
        
        ubicacion = calc.set_elementoCD(self.elementos, self.unidades)
        
        id_e = ubicacion[0][0]
        elemento = ubicacion[0][1]
        distancia_i = ubicacion[0][2]
        distancia_f = ubicacion[0][3]
        
        carga_distribuida["Nombre"].append(nombre)
        carga_distribuida["Carga i"].append(carga_i)
        carga_distribuida["Carga f"].append(carga_f)
        carga_distribuida["Elemento"].append(elemento)
        carga_distribuida["ID_e"].append(id_e)
        carga_distribuida["Distancia i"].append(distancia_i)
        carga_distribuida["Distancia f"].append(distancia_f)
        
        new_cargaD = pd.DataFrame(carga_distribuida, index=[index])
        
        self.cargas_Distribuidas = pd.concat([self.cargas_Distribuidas,new_cargaD])
        
    def edit_cargadistribuida(self) -> None:
        print("\nCargas distribuidas actuales: \n")
        print(self.cargas_Distribuidas)
        
        carga_distribuida = {"Nombre": [], "Carga i": [], "Carga f": [], "Direcccion": [], "Elemento": [], "ID_e": [], "Distancia i": [], "Distancia f": []}
        
        indexes = self.cargas_Distribuidas.index.values.tolist()
        index = get_index(indexes)
        
        print(f"\nCarga distribuida selecionada id: [{index}]")
        print(self.cargas_Distribuidas.loc[[index]])
        
        nombre = input(f"\nNombre ({self.cargas_Distribuidas.loc[index, 'Nombre']}): ") or self.cargas_Distribuidas.loc[index, 'Nombre']

        last_cargas = (self.cargas_Distribuidas.loc[index, 'Carga i', self.cargas_Distribuidas.loc[index, 'Carga f']])
        confirmacion = confirmation("\n¿Cambiar los valores de la carga?")
        if confirmacion:
            cargas = calc.get_cargaD(self.unidades, last_cargas, True)
        else:
            cargas = last_cargas
            
        carga_i = cargas[0][0]
        carga_f = cargas[0][1]
        
        last_ubicacion = ((self.cargas_Distribuidas.loc[index, 'ID_e'], self.cargas_Distribuidas.loc[index,'Elemento']), (self.cargas_Distribuidas.loc[index, 'Distancia i'], self.cargas_Distribuidas.loc[index, 'Distancia f']))
        confirmacion = confirmation("\n¿Quiere editar la ubicación de la carga?")
        if confirmacion:
            ubicacion = calc.set_elementoCD(self.elementos, self.unidades, last_ubicacion[0][0], last_ubicacion[1][0], True)
        else: 
            ubicacion = last_ubicacion
        
        id_e = ubicacion[0][0]
        elemento = ubicacion[0][1]
        distancia_i = ubicacion[0][2]
        distancia_f = ubicacion[0][3]
        
        carga_distribuida["Nombre"].append(nombre)
        carga_distribuida["Carga i"].append(carga_i)
        carga_distribuida["Carga f"].append(carga_f)
        carga_distribuida["Elemento"].append(elemento)
        carga_distribuida["ID_e"].append(id_e)
        carga_distribuida["Distancia i"].append(distancia_i)
        carga_distribuida["Distancia f"].append(distancia_f)
        
        self.cargas_Distribuidas = self.cargas_Distribuidas.drop([index])
        new_cargaD = pd.DataFrame(carga_distribuida, index=[index])
        
        self.cargas_Distribuidas = pd.concat([self.cargas_Distribuidas,new_cargaD])
        self.cargas_Distribuidas = self.cargas_Distribuidas.sort_index() 
        
    def delete_cargadistribuida(self) -> None:
        print("\nCargas distribuidas actuales: \n")
        print(self.cargas_Distribuidas)
        
        indexes = self.cargas_Puntuales.index.values.tolist()
        index = get_index(indexes)
        
        confirmacion = confirmation(f"Confirmar eliminación {self.cargas_Distribuidas.loc[index,'Nombre']} id:{index}")
        if confirmacion: 
            self.cargas_Distribuidas = self.cargas_Distribuidas.drop([index])
    
    # Momentos
    def add_momento(self) -> None:
        momento = {"Nombre": [], "Valor": [], "Nodo": [], "ID_n": [], "Elemento": [], "ID_e": [], "Distancia": []}
        print("\nNuevo momento.") 
        
        try:
            index = max(self.momentos.index) + 1
        except:
            index = len(self.momentos.index)    
            
        nombre = input("\nIngrese un nombre para el momento (En blanco nombre por defecto): ")
        if not (nombre):
            nombre = f"Momento {index}"
            
        carga = calc.get_momento(self.unidades)
        valor = carga[0]
        
        ubicacion = calc.get_ubicacionmomento(self.nodos, self.elementos, self.unidades)
        
        id_n = ubicacion[0][0]
        nodo = ubicacion[0][1]
        id_e = ubicacion[1][0]
        elemento = ubicacion [1][1]
        distancia = ubicacion[1][2]
        
        momento["Nombre"].append(nombre)
        momento["Valor"].append(valor)
        momento["Nodo"].append(nodo)
        momento["ID_n"].append(id_n)
        momento["Elemento"].append(elemento)
        momento["ID_e"].append(id_e)
        momento["Distancia"].append(distancia)
        
        new_momento = pd.DataFrame(momento, index = [index])
        
        self.momentos = pd.concat([self.momentos, new_momento])
    
    def edit_momento(self) -> None:
        print("\nMomentos actuales: \n")
        print(self.momentos)
        
        momento = {"Nombre": [], "Valor": [], "Nodo": [], "ID_n": [], "Elemento": [], "ID_e": [], "Distancia": []}
        
        indexes = self.momentos.index.values.tolist()
        index = get_index(indexes)
        
        print(f"\nMomento seleccionado id: [{index}]")
        print(self.momentos.loc[[index]])
    
        nombre = input(f"\nNombre ({self.momentos.loc[index, 'Nombre']}): ") or self.momentos.loc[index, 'Nombre']
    
        last_carga = self.momentos.loc[index,'Valor']
        confirmacion = confirmation( "\n¿Cambiar el valor del momento?")
        if confirmacion:
            carga = calc.get_momento(self.unidades, last_carga, True)
        else:
            carga = last_carga
        
        valor = carga[0]
        
        last_ubicacion = ((self.momentos.loc[index, 'ID_n'],self.momentos.loc[index, 'Nodo']),(self.momentos.loc[index, 'ID_e'],self.momentos.loc[index, 'Elemento'],self.momentos.loc[index, 'Distancia']))
        confirmacion = confirmation("¿Quiere editar la ubicacion del momento?")
        if confirmacion: 
            ubicacion = calc.get_ubicacionmomento(self.nodos, self.elementos, self.unidades, last_ubicacion[0][0], last_ubicacion[1][0], True)
        else :
            ubicacion = last_ubicacion
            
        id_n = ubicacion[0][0]
        nodo = ubicacion[0][1]
        id_e = ubicacion[1][0]
        elemento = ubicacion [1][1]
        distancia = ubicacion[1][2]
        
        momento["Nombre"].append(nombre)
        momento["Valor"].append(valor)
        momento["Nodo"].append(nodo)
        momento["ID_n"].append(id_n)
        momento["Elemento"].append(elemento)
        momento["ID_e"].append(id_e)
        momento["Distancia"].append(distancia)
        
        self.momentos = self.momentos.drop([index])
        new_momento = pd.DataFrame(momento, index=[index])
        
        self.momentos = pd.concat([self.momentos,new_momento])
        self.momentos = self.momentos.sort_index()
        
    def delete_momento(self) -> None:
        print("\nMomentos actuales: \n")
        print(self.momentos)
        
        indexes = self.momentos.index.values.tolist()
        index = get_index(indexes)
        
        confirmacion = confirmation(f"Confirmar eliminación {self.momentos.loc[index,'Nombre']} id:{index}")
        if confirmacion: 
            self.momentos = self.momentos.drop([index])
    
    # Calculos de estructura
    def calculate(self) -> None:
        self.resultados = calc.calculos(self.elementos,self.nodos,self.materiales,self.secciones,self.unidades,self.tipo_estructura)

if __name__ == "__main__": 
    pass
    