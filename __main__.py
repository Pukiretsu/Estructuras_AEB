import os
import Modules.Modelo as mod
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import date

# Miscelaneos

def new_model():
    os.system("cls")
    modelo = mod.model()
    modelo.set_structureType()
    if modelo.tipo_estructura:
        os.system("cls")
        model_system(modelo)    

def load_model():
    os.system("cls")
    
    modelo = mod.model()
    
    filename = askopenfilename(title="Cargar Modelo", filetypes=[("Modelos JSON",".json")])
    
    modelo.load_model(filename) 
    
    model_system(modelo)

def save_model(model):
    filename = asksaveasfilename(title="Guardar Modelo",initialfile= model.nombre, defaultextension='.json', filetypes=[("Modelos JSON",".json")])
    
    dt = date.today()
    fecha = dt.strftime("%d-%m-%y")
    
    model.save_model(filename,fecha)
    
    os.system("cls")
    print(f"Se guardo con exito el Modelo en {filename}\n")

# Configuracion del modelo

def nodos_settings(modelo):
    os.system("cls")
           
    while True:
        if not modelo.nodos.empty:
            print("\nNodos actuales:\n")
            print(modelo.nodos)
        else:
            print("\nNo hay Nodos en la base de datos.")
        
        print("\n¿Qué desea hacer?\n")
        print("\t1. Nuevo Nodo.")
        
        if not modelo.nodos.empty:
            print("\t2. Modificar Nodo existente.")
            print("\t3. Eliminar Nodo existente.")
        
        print("\t4. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                modelo.add_node()
                os.system("cls")
            case "2":
                if not modelo.nodos.empty:
                    os.system("cls")
                    modelo.edit_node()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opcion ingresada.\n\n")
            case "3":
                if not modelo.nodos.empty:
                    os.system("cls")
                    modelo.delete_node()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opcion ingresada.\n\n")
            case "4":
                return modelo
            case _:
                print("Error: no se reconoce la opcion ingresada.\n\n")

def elementos_settings(modelo):
    os.system("cls")
           
    while True:
        if not modelo.elementos.empty:
            print("\nElementos actuales:\n")
            print(modelo.elementos)
        else:
            print("\nNo hay Elementos en la base de datos.")
        
        print("\n¿Qué desea hacer?\n")
        print("\t1. Nuevo Elemento.")
        
        if not modelo.elementos.empty:
            print("\t2. Modificar elemento existente.")
            print("\t3. Eliminar elemento existente.")
        
        print("\t4. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                modelo.add_element()
                os.system("cls")
            case "2":
                if not modelo.elementos.empty:
                    os.system("cls")
                    modelo.edit_element()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "3":
                if not modelo.elementos.empty:
                    os.system("cls")
                    modelo.delete_element()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "4":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def secciones_settings(modelo):
    os.system("cls")
    
    def show_units():
        print("Unidades.")
        print("---------------------")
        print(f"Area: {modelo.unidades.loc[0,'Longitud']}^2")
        print(f"Inercia: {modelo.unidades.loc[0,'Longitud']}^4")
           
    while True:
        show_units()
        if not modelo.secciones.empty:
            print("\nSecciones actuales:\n")
            print(modelo.secciones)
        else:
            print("\nNo hay secciones en la base de datos.")
        
        print("\n¿Qué desea hacer?\n")
        print("\t1. Nueva Sección.")
        
        if not modelo.secciones.empty:
            print("\t2. Modificar sección existente.")
            print("\t3. Eliminar sección existente.")
        
        print("\t4. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                show_units()
                modelo.add_section()
                os.system("cls")
            case "2":
                if not modelo.secciones.empty:
                    os.system("cls")
                    show_units()
                    modelo.edit_section()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opcóon ingresada.\n\n")
            case "3":
                if not modelo.secciones.empty:
                    os.system("cls")
                    show_units()
                    modelo.delete_section()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "4":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def materiales_settings(modelo):
    os.system("cls")
    
    def show_units():
        print("Unidades.")
        print("---------------------")
        print(f"Modulo de Young: {modelo.unidades.loc[0,'Esfuerzo']}")
    
    while True:
        show_units()
        if not modelo.materiales.empty:
            print("\nMateriales actuales:\n")
            print(modelo.materiales)
        else:
            print("\nNo hay materiales en la base de datos.")
        
        print("\n¿Qué desea hacer?\n")
        print("\t1. Nuevo Material.")
        
        if not modelo.materiales.empty:
            print("\t2. Modificar material existente.")
            print("\t3. Eliminar material existente.")
        
        print("\t4. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                show_units()
                modelo.add_material()
                os.system("cls")
            case "2":
                if not modelo.materiales.empty:
                    os.system("cls")
                    show_units()
                    modelo.edit_material()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "3":
                if not modelo.materiales.empty:
                    os.system("cls")
                    show_units()
                    modelo.delete_material()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "4":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")                

def cargas_puntuales_settings(modelo):
    #TODO: Menu de Cargas Puntuales
    pass

def cargas_distribuidas_settings(modelo):
    #TODO: Menu de Cargas distribuidas
    pass

def momentos_settings(modelo):
    #TODO: Menu de momentos
    pass

def units_settings(modelo):
    os.system("cls")
    while True:
        print("Unidades actuales:\n")
        print(modelo.unidades)
        print("\n¿Qué desea hacer?.\n")
        
        print("\t1. Editar Unidades.")
        print("\t2. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                modelo.set_units()
                os.system("cls")
            case "2":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def model_settings(modelo):
    os.system("cls")
    while True:
        print("Estructura:")
        print("-------------------------")
        print("\t1. Nodos.")
        print("\t2. Elementos.")
        print("\t3. Secciones.")
        print("\t4. Materiales.")
        
        print("\nCargas:")
        print("-------------------------")
        print("\t5. Cargas Puntuales.")
        print("\t6. Cargas Distribuidas.")
        print("\t7. Momentos.")
        
        print("\nMiscelaneos:")
        print("-------------------------")
        print("\t8. Unidades del modelo.")
        
        print("\n9. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                modelo = nodos_settings(modelo)
                os.system("cls")
            case "2":        
                modelo = elementos_settings(modelo)
                os.system("cls")
                pass
            case "3":
                modelo = secciones_settings(modelo)
                os.system("cls")
            case "4":
                modelo = materiales_settings(modelo)
                os.system("cls")
                pass
            case "5":
                modelo = cargas_puntuales_settings(modelo)
                os.system("cls")
            case "6":
                modelo = cargas_distribuidas_settings(modelo)
                os.system("cls")
            case "7":
                modelo = momentos_settings(modelo)
                os.system("cls")
            case "8":
                modelo = units_settings(modelo)
                os.system("cls")
            case "9":
                os.system("cls")
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

# Menú del modelo

def model_system(modelo):
    while True:
        print(f"Trabajando en: {modelo.nombre}")
        print("\n¿Qué desea hacer?:\n")
        
        print("\t1. Configurar estructura.")
        print("\t2. Información de la estructura.")
        print("\t3. Computar estructura.")
        print("\t4. Resultados.")
        print("\t5. Guardar estructura.")
        print("\t6. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                modelo = model_settings(modelo)
            case "2": 
                #TODO Punto de entrada Información estructura.
                pass
            case "3": 
                #TODO Punto de entrada Computar estructura.
                pass
            case "4": 
                #TODO Punto de entrada Resultados.
                pass
            case "5": 
                save_model(modelo)
            case "6":
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")
                pass 

def main():
    while True:
        os.system("cls")
        print("Solucionador de estructuras:\n")
        
        print("\t1. Nuevo modelo.")
        print("\t2. Cargar Modelo.")
        print("\t3. Finalizar el programa")
        
        match input("\nIngrese una opción: "):
            case "1":
                new_model()
            case "2":        
                load_model()
            case "3":
                break
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")
                pass 

if __name__ == "__main__":
    main() 
