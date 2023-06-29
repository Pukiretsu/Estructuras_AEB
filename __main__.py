import os
import Modules.Modelo as mod
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import date


# Configuraciones para display

pd.set_option('display.float_format', '{:.2f}'.format)

# Miscelaneos

def systemWait():
    input("\nPresione enter para continuar.")
    os.system("cls")

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

def save_model(model: mod.model):
    filename = asksaveasfilename(title="Guardar Modelo",initialfile= model.nombre, defaultextension='.json', filetypes=[("Modelos JSON",".json")])
    
    dt = date.today()
    fecha = dt.strftime("%d-%m-%y")
    
    model.save_model(filename,fecha)
    
    os.system("cls")
    print(f"Se guardo con exito el Modelo en {filename}\n")

# Configuracion del modelo

def nodos_settings(modelo: mod.model):
    os.system("cls")
    
    def showTittle():
        divideBar()      
        print("Nodos.")
        divideBar()    
    
    while True:
        showTittle()   
        if not modelo.nodos.empty:
            print("\nNodos actuales:\n")
            match modelo.tipo_estructura:
                case "Cercha":
                    print(modelo.nodos.loc[:,~modelo.nodos.columns.isin(['Phi'])])
                    pass
                case "Viga":
                    print(modelo.nodos.loc[:,~modelo.nodos.columns.isin(['U'])])
                    pass
                case "Portico":
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

def elementos_settings(modelo: mod.model):
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
            print(modelo.elementos.loc[:,~modelo.elementos.columns.isin(["ID ni", "ID nj", "ID Mat", "ID Sec", "ID_cargas"])])
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

def secciones_settings(modelo: mod.model):
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

def materiales_settings(modelo: mod.model):
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

def cargas_settings(modelo: mod.model):
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
        pd.set_option('display.float_format', '{:.2f}'.format)
        show_units()
        if not modelo.cargas.empty:
            print("\nCargas Locales actuales:\n")
            match modelo.tipo_estructura:
                case "Cercha":
                    cercha_df = modelo.cargas.copy()
                    cercha_df.rename(columns = {'N_i':'Xi', 'N_j':'Xj', 'V_i':'Yi', 'V_j':'Yj'}, inplace=True)
                    print(cercha_df.loc[:,~cercha_df.columns.isin(["ID_Elem", "M_i", "M_j"])])
                    pass
                case "Viga":
                    print(modelo.cargas.loc[:,~modelo.cargas.columns.isin(["ID_Elem", "N_i", "N_j"])])
                    pass
                case "Portico":
                    print(modelo.cargas.loc[:,~modelo.cargas.columns.isin(["ID_Elem"])])
                    
        else:
            print("\nNo hay elementos en la base de datos.")
        
        print("\n¿Qué desea hacer?\n")
        
        if not modelo.cargas.empty:
            print("\t1. Añadir cargas a un elemento.")
            print("\t2. Reiniciar cargas de un elemento.")
        
        print("\n0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                if not modelo.cargas.empty:
                    os.system("cls")
                    show_units()
                    modelo.add_cargas()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "2":
                if not modelo.cargas.empty:
                    os.system("cls")
                    show_units()
                    modelo.reset_cargas(manual=True)
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opción ingresada.\n\n")
            case "0":
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

def units_settings(modelo: mod.model):
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

def model_settings(modelo: mod.model):
    os.system("cls")
    while True:
        print("Configuración modelo.")
        divideBar()
        
        print("\nEstructura:")
        divideBar()
        print("\t1. Nodos.")
        print("\t2. Secciones.")
        print("\t3. Materiales.")
        print("\t4. Elementos.")
        
        print("\nCargas:")
        divideBar()
        print("\t5. Añadir cargas.")
        
        print("\nMiscelaneos:")
        divideBar()
        print("\t6. Unidades del modelo.")
        
        print("\n0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                modelo = nodos_settings(modelo)
                os.system("cls")
            case "2":
                modelo = secciones_settings(modelo)
                os.system("cls")
            case "3":
                modelo = materiales_settings(modelo)
                os.system("cls")
            case "4":        
                modelo = elementos_settings(modelo)
                os.system("cls")
            case "5":
                modelo = cargas_settings(modelo)
                os.system("cls")
            case "6":
                modelo = units_settings(modelo)
                os.system("cls")
            case "0":
                os.system("cls")
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

# Calculo de la estructura

def model_calculate(modelo: mod.model):
    os.system("cls")
    modelo.calculate()
    return modelo  

# Resultados del calculo

def print_matriz_rigidez(modelo: mod.model):
    os.system("cls")
    def showTittle():
        divideBar()     
        print("Matriz de rigidez.")
        divideBar()
    
    while True:
        showTittle()
        print("\n¿Cual desea ver?\n")
        
        print("\t1. Global consolidada.")
        print("\t2. Elementos.")
        
        print("\n0. Volver.")
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                showTittle()
                print("\nMatriz Global.\n")
                print(modelo.resultados["Matriz Global"])
                systemWait()
            case "2":
                os.system("cls")
                showTittle()
                modelo.show_results_by_elemento("k rigidez local")
                systemWait()
            case "0":
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")
                os.system("cls") 
                
    return modelo

def print_vector_carga(modelo: mod.model):
    os.system("cls")
    def showTittle():
        divideBar()     
        print("Vectores de carga globales.")
        divideBar()
    
    while True:
        showTittle()
        print("\n¿Cual desea ver?\n")
        
        print("\t1. Global consolidado.")
        print("\t2. Elementos.")
        
        print("\n0. Volver.")
        match input("\nIngrese una opción: "):
            case "1":
                os.system("cls")
                showTittle()
                print("\nCarga Global.\n")
                
                unidades = modelo.resultados["unidades_resultados"]["Carga"]
                print_df = pd.concat([modelo.resultados["Vector Cargas Global"], unidades], axis = 1)
                print_df.columns = ["Q", ""]
                
                print(print_df)
                systemWait()
            case "2":
                os.system("cls")
                showTittle()
                modelo.show_results_by_elemento("Carga Global")
                systemWait()
            case "0":
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")
                os.system("cls") 
                
    return modelo

def print_vector_desp(modelo: mod.model):
    os.system("cls")
    divideBar()     
    print("Vectores de Desplazamiento.")
    divideBar()
    
    unidades = modelo.resultados["unidades_resultados"]["Desplazamiento"]
    print_df = pd.concat([modelo.resultados["Desplazamientos"], unidades], axis = 1)
    print_df.columns = ["Desplazamiento", ""]
    
    print(print_df)
    systemWait()
    os.system("cls")
    
    return modelo

def print_vector_reaciones(modelo: mod.model):
    os.system("cls")
    divideBar()     
    print("Vector de Reacciones.")
    divideBar()
    
    unidades = modelo.resultados["unidades_resultados"]["Carga"]
    print_df = pd.concat([modelo.resultados["Reacciones"], unidades], axis = 1)
    print_df.columns = ["Reacciones", ""]
    
    print(print_df)
    systemWait()
    os.system("cls")
    return modelo

def print_AIF(modelo: mod.model):
    os.system("cls")
    divideBar()     
    print("Acciones internas de fuerza.")
    divideBar()
    
    modelo.show_results_by_elemento("AIF")
    systemWait()
    os.system("cls")
    
    return modelo

def model_results(modelo: mod.model):
    os.system("cls")
    while True:
        print("Resumen de calculos.")
        divideBar()
        
        print("\n¿Qué desea ver?:\n")
        
        print("\t1. Matriz de rigidez.")
        print("\t2. Vector de carga.")
        print("\t3. Vector de desplazamiento.")
        print("\t4. Vector de reacciones.")
        print("\t5. Fuerzas internas de los elementos")
        
        print("\n\t6. unidades de resultados.")
        print("\n0. volver")

        match input("\nIngrese una opción: "):
            case "1":
                modelo = print_matriz_rigidez(modelo)
            case "2":
                modelo = print_vector_carga(modelo)
            case "3":
                modelo = print_vector_desp(modelo)
            case "4":
                modelo = print_vector_reaciones(modelo)
            case "5":
                modelo = print_AIF(modelo)
            case "6":
                pass
            case "0":
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")
                os.system("cls") 
            
    return modelo

# Menú del modelo

def model_system(modelo: mod.model):
    while True:
        print(f"Trabajando en: {modelo.nombre}")
        print(f"Tipo de estructura: {modelo.tipo_estructura}")
        divideBar()
        print("\n¿Qué desea hacer?:\n")
        
        print("\t1. Configurar estructura.")
        print("\t2. Computar estructura.")
        print("\t3. Resultados.")
        print("\t4. Guardar estructura.")
        print("\n0. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                modelo = model_settings(modelo)
            case "2": 
                modelo = model_calculate(modelo)
            case "3": 
                modelo = model_results(modelo)
                pass
            case "4": 
                save_model(modelo)
            case "0":
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")
                os.system("cls") 

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
