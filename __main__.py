import os
import Modules.Modelo as mod
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import date


# Configuraciones para display

pd.set_option('display.float_format', '{:.1f}'.format)

# Miscelaneos

def divideBar():
    print("-------------------------------")  

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
    
    def showTittle():
        divideBar()      
        print("Nodos.")
        divideBar()    
    
    while True:
        showTittle()   
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
        
        print("\n0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                showTittle()  
                modelo.add_node()
                os.system("cls")
            case "2":
                if not modelo.nodos.empty:
                    os.system("cls")
                    showTittle()  
                    modelo.edit_node()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opcion ingresada.\n\n")
            case "3":
                if not modelo.nodos.empty:
                    os.system("cls")
                    showTittle()  
                    modelo.delete_node()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opcion ingresada.\n\n")
            case "0":
                return modelo
            case _:
                print("Error: no se reconoce la opcion ingresada.\n\n")

def elementos_settings(modelo):
    os.system("cls")
    
    def show_units():
        divideBar()     
        print("Elementos.")
        divideBar()     
        print("Unidades.")
        print(f"Longitud: {modelo.unidades.loc[0,'Longitud']}")
        print(f"Ángulo: {modelo.unidades.loc[0,'Angulo']}")
        divideBar()     
    
    while True:
        show_units()
        if not modelo.elementos.empty:
            print("\nElementos actuales:\n")
            print(modelo.elementos.loc[:,~modelo.elementos.columns.isin(["ID ni", "ID nj", "ID Mat", "ID Sec"])])
        else:
            print("\nNo hay Elementos en la base de datos.")
        
        print("\n¿Qué desea hacer?\n")
        print("\t1. Nuevo Elemento.")
        
        if not modelo.elementos.empty:
            print("\t2. Modificar elemento existente.")
            print("\t3. Eliminar elemento existenste.")
        
        print("\n0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                show_units()
                modelo.add_element()
                os.system("cls")
            case "2":
                if not modelo.elementos.empty:
                    os.system("cls")
                    show_units()
                    modelo.edit_element()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "3":
                if not modelo.elementos.empty:
                    os.system("cls")
                    show_units()
                    modelo.delete_element()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "0":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def secciones_settings(modelo):
    os.system("cls")
    
    def show_units():
        divideBar()
        print("Secciones.")
        divideBar()
        print("Unidades:")
        print(f"Area: {modelo.unidades.loc[0,'Longitud']}^2")
        print(f"Inercia: {modelo.unidades.loc[0,'Longitud']}^4")
        divideBar()
           
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
        
        print("\n0. Volver.")
        
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
            case "0":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def materiales_settings(modelo):
    os.system("cls")
    
    def show_units():
        divideBar()
        print("Materiales.")
        divideBar()
        print("Unidades:")
        print(f"Modulo de Young: {modelo.unidades.loc[0,'Esfuerzo']}")
        divideBar()
    
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
        
        print("\n0. Volver.")
        
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
            case "0":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")                

def cargas_puntuales_settings(modelo):
    os.system("cls")
    
    def show_units():
        divideBar()     
        print("Cargas puntuales.")
        divideBar()     
        print("Unidades.")
        print(f"Longitud: {modelo.unidades.loc[0,'Longitud']}")
        print(f"Fuerza: {modelo.unidades.loc[0,'Fuerza']}")
        divideBar()     
    
    while True:
        show_units()
        if not modelo.cargas_Puntuales.empty:
            print("\nCargas puntules actuales:\n")
            print(modelo.cargas_Puntuales.loc[:,~modelo.cargas_Puntuales.columns.isin([""])])
        else:
            print("\nNo hay cargas puntuales en la base de datos.")
        
        print("\n¿Qué desea hacer?\n")
        print("\t1. Nueva carga puntual.")
        
        if not modelo.cargas_Puntuales.empty:
            print("\t2. Modificar carga puntual existente.")
            print("\t3. Eliminar carga puntual existenste.")
        
        print("\n0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                show_units()
                modelo.add_cargapuntual()
                os.system("cls")
            case "2":
                if not modelo.cargas_Puntuales.empty:
                    os.system("cls")
                    show_units()
                    modelo.edit_cargapuntual()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "3":
                if not modelo.cargas_Puntuales.empty:
                    os.system("cls")
                    show_units()
                    modelo.delete_cargapuntual()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "0":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def cargas_distribuidas_settings(modelo):
    os.system("cls")
    
    def show_units():
        divideBar()     
        print("Cargas distibuidas.")
        divideBar()     
        print("Unidades.")
        print(f"Longitud: {modelo.unidades.loc[0,'Longitud']}")
        print(f"Fuerza: {modelo.unidades.loc[0,'Fuerza']}")
        divideBar()     
    
    while True:
        show_units()
        if not modelo.cargas_Distribuidas.empty:
            print("\nCargas distribuidas actuales:\n")
            print(modelo.cargas_Distribuidas.loc[:,~modelo.cargas_Distribuidas.columns.isin([""])])
        else:
            print("\nNo hay cargas distribuidas en la base de datos.")
        
        print("\n¿Qué desea hacer?\n")
        print("\t1. Nueva carga distribuida.")
        
        if not modelo.cargas_Distribuidas.empty:
            print("\t2. Modificar carga distribuida existente.")
            print("\t3. Eliminar carga distribuida existenste.")
        
        print("\n0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                show_units()
                modelo.add_cargadistribuida()
                os.system("cls")
            case "2":
                if not modelo.cargas_Distribuidas.empty:
                    os.system("cls")
                    show_units()
                    modelo.edit_cargadistribuida()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "3":
                if not modelo.cagas_Distribuidas.empty:
                    os.system("cls")
                    show_units()
                    modelo.delete_cargadistribuida()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "0":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def momentos_settings(modelo):
    os.system("cls")
    
    def show_units():
        divideBar()     
        print("Momentos.")
        divideBar()     
        print("Unidades.")
        print(f"Longitud: {modelo.unidades.loc[0,'Longitud']}")
        print(f"Fuerza: {modelo.unidades.loc[0,'Fuerza']}")
        divideBar()     
    
    while True:
        show_units()
        if not modelo.momentos.empty:
            print("\nMomentos actuales:\n")
            print(modelo.momentos.loc[:,~modelo.momentos.columns.isin([""])])
        else:
            print("\nNo hay momentos en la base de datos.")
        
        print("\n¿Qué desea hacer?\n")
        print("\t1. Nuevo momento puntual.")
        
        if not modelo.momentos.empty:
            print("\t2. Modificar momento existente.")
            print("\t3. Eliminar momento existenste.")
        
        print("\n0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                show_units()
                modelo.add_momento()
                os.system("cls")
            case "2":
                if not modelo.momentos.empty:
                    os.system("cls")
                    show_units()
                    modelo.edit_momento()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "3":
                if not modelo.momentos.empty:
                    os.system("cls")
                    show_units()
                    modelo.delete_momento()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "0":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def units_settings(modelo):
    os.system("cls")
    while True:
        divideBar()      
        print("Unidades.")
        divideBar()   
        print("Unidades actuales:\n")
        print(modelo.unidades)
        print("\n¿Qué desea hacer?.\n")
        
        print("\t1. Editar Unidades.")
        print("\t0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                modelo.set_units()
                os.system("cls")
            case "0":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def model_settings(modelo):
    os.system("cls")
    while True:
        print("Configuración modelo.")
        divideBar()
        
        print("\nEstructura:")
        divideBar()
        print("\t1. Nodos.")
        print("\t2. Elementos.")
        print("\t3. Secciones.")
        print("\t4. Materiales.")
        
        print("\nCargas:")
        divideBar()
        print("\t5. Cargas Puntuales.")
        print("\t6. Cargas Distribuidas.")
        print("\t7. Momentos.")
        
        print("\nMiscelaneos:")
        divideBar()
        print("\t8. Unidades del modelo.")
        
        print("\n0. Volver.")
        
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
            case "0":
                os.system("cls")
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

# Calculo de la estructura

def model_calculate(modelo):
    os.system("cls")
    
    modelo.calculate()
    return modelo
    

# Menú del modelo

def model_system(modelo):
    while True:
        print(f"Trabajando en: {modelo.nombre}")
        print(f"Tipo de estructura: {modelo.tipo_estructura}")
        divideBar()
        print("\n¿Qué desea hacer?:\n")
        
        print("\t1. Configurar estructura.")
        print("\t2. Información de la estructura.")
        print("\t3. Computar estructura.")
        print("\t4. Resultados.")
        print("\t5. Guardar estructura.")
        print("\n0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                modelo = model_settings(modelo)
            case "2": 
                #TODO Punto de entrada Información estructura.
                pass
            case "3": 
                modelo = model_calculate(modelo)
            case "4": 
                #TODO Punto de entrada Resultados.
                pass
            case "5": 
                save_model(modelo)
            case "0":
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")
                pass 

def main():
    while True:
        os.system("cls")
        print("Solucionador de estructuras:\n")
        divideBar
        
        print("\t1. Nuevo modelo.")
        print("\t2. Cargar Modelo.")
        print("\n0. Finalizar el programa")
        
        match input("\nIngrese una opción: "):
            case "1":
                new_model()
            case "2":        
                load_model()
            case "0":
                break
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")
                pass 

if __name__ == "__main__":
    main() 
