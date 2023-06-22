import pandas as pd
import json
import Modules.Calculos as calc

# Definicion de dataframes en el contexto
MATERIALES = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                           "Modulo Young": pd.Series(dtype="float")})

SECCIONES = pd.DataFrame({"Nombre": pd.Series(dtype="str"), 
                          "Area": pd.Series(dtype="float"), 
                          "Inercia": pd.Series(dtype="float")})

NODOS = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                     "Coordenada X": pd.Series(dtype="float"),
                     "Coordenada y": pd.Series(dtype="float"),
                     "V": pd.Series(dtype="int"), 
                     "U": pd.Series(dtype="int"),
                     "Phi": pd.Series(dtype="int")})

ELEMENTOS = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                          "Nodo i": pd.Series(dtype="str"),
                          "Nodo j": pd.Series(dtype="str"), 
                          "longitud": pd.Series(dtype="float"),
                          "Angulo": pd.Series(dtype="float"), 
                          "Material": pd.Series(dtype="str"),
                          "Secciones": pd.Series(dtype="str")}) 

CARGAS_PUNTUALES = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                                 "Valor": pd.Series(dtype="float"),
                                 "Direccion": pd.Series(dtype="str"),
                                 "Nodo" : pd.Series(dtype="str"),
                                 "Elemento": pd.Series(dtype="str"),
                                 "Distancia": pd.Series(dtype="float")})

CARGAS_DISTRIBUIDAS = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                                    "Carga i": pd.Series(dtype="float"),
                                    "Carga f": pd.Series(dtype="float"),
                                    "Direccion": pd.Series(dtype="str"),
                                    "Elemento": pd.Series(dtype="str"),
                                    "Distancia i": pd.Series(dtype="float"),
                                    "Distancia f": pd.Series(dtype="float")})

MOMENTOS = pd.DataFrame({"Nombre": pd.Series(dtype="str"),
                         "Valor": pd.Series(dtype="float"),
                         "Direccion": pd.Series(dtype="str"),
                         "Nodo" : pd.Series(dtype="str"),
                         "Elemento": pd.Series(dtype="str"),
                         "Distancia": pd.Series(dtype="float")})

def confirmation(message) -> bool:
    while True:
        print(f"\n{message}")
        response = input("(s/N): ") or "N"
        if response == "s" or response == "S":
            return True
        elif response == "N" or response == "n":
            return False
        else:
            pass
            

def get_index(Index_list) -> bool:
    while True:
            try:
                index = int(input("\nIngrese el id del elemento: "))
                if Index_list.count(index) == 0:
                    raise Exception() 
                break
            except:
                print("Error: id inválido.\n")
    return index

class model():
    def __init__(self) -> None:
        self.materiales = MATERIALES
        self.secciones = SECCIONES
        self.Nodos = NODOS
        self.Elementos = ELEMENTOS
        self.Cargas_Puntuales = CARGAS_PUNTUALES
        self.Cargas_Distribuidas = CARGAS_DISTRIBUIDAS
        self.Momentos = MOMENTOS
    
    #TODO Carga y descarga de modelos
    
    def load_model(self) -> None:
        with open("dummy.json","r") as f: #TODO poner interfaz para seleccionar archivo
            data = json.loads(f.read())

        self.materiales = pd.concat([self.materiales, pd.json_normalize(data, record_path = ["MATERIALES"])])
        self.secciones = pd.concat([self.secciones, pd.json_normalize(data, record_path = ["SECCIONES"])]) 
    
    # Añadir secciones
    def add_section(self) -> None: #TODO añadir sistema de unidades
        section = {"Nombre": [], "Area": [], "Inercia": []}
        
        print("Nueva sección.")
        
        nombre = input("\nIngrese un nombre para la sección (En blanco nombre por defecto): ")
        sectionCalcs = calc.get_section_calcs()
        
        index = max(self.secciones.index)+1
        
        if not (nombre):
            nombre = f"Seccion {index}"
        
        # Consolidación de entrada
        
        section["Nombre"].append(nombre)
        section["Area"].append(sectionCalcs[0])
        section["Inercia"].append(sectionCalcs[1])
        
        new_Sect = pd.DataFrame(section, index=[index])

        # Ingreso a Dataframe de nueva entrada
        
        self.secciones = pd.concat([self.secciones,new_Sect])
        
    def edit_section(self) -> None:
        print("Secciones actuales:\n")
        print(self.secciones)
        
        section = {"Nombre": [], "Area": [], "Inercia": []}
        indexes = self.secciones.index.values.tolist()
        index = get_index(indexes)
                
        print(f"\nSeccion seleccionada id:{index}")
        print(self.secciones.loc[[index]])
        
        nombre = input(f"\nNombre ({self.secciones.loc[index,'Nombre']}): ") or self.secciones.loc[index,'Nombre']
        sectionCalcs = calc.get_section_calcs(True) or (self.secciones.loc[index,'Area'],self.secciones.loc[index,'Inercia'])
        
        section["Nombre"].append(nombre)
        section["Area"].append(sectionCalcs[0])
        section["Inercia"].append(sectionCalcs[1])
        
        self.secciones = self.secciones.drop(self.secciones.index[index])
        new_Sect = pd.DataFrame(section, index=[index])
        
        self.secciones = pd.concat([self.secciones,new_Sect])
        self.secciones = self.secciones.sort_index()
    
    def delete_section(self) -> None:
        #TODO Hacer la eliminacion de entradas
        print("Secciones actuales:\n")
        print(self.secciones)
        
        indexes = self.secciones.index.values.tolist()
        index = get_index(indexes)
                
        print(f"\nSeccion seleccionada id:{index}")
        print(self.secciones.loc[[index]])
        
        confirmacion = confirmation(f"Confirmar eliminación {self.secciones.loc[index,'Nombre']} id:{index}")
        if confirmacion:
            self.secciones = self.secciones.drop(self.secciones.index[index])

if __name__ == "__main__":
    model = model()
    model.add_section()
    print(model.secciones)
    