import os
import Modules.Modelo as mod

def new_model():
    os.system("cls")
    modelo = mod.model()
    model_system(modelo)

def load_model():
    os.system("cls")
    #TODO
    modelo = mod.model()
    modelo.load_model()
    model_system(modelo)

def secciones_settings(modelo):
    os.system("cls")
    while True:
        if not modelo.secciones.empty:
            print("Secciones actuales:\n")
            print(modelo.secciones)
            print("\n¿Qué desea hacer?\n")
        
        print("\t1. Nueva Seccion.")
        print("\t2. Modificar seccion existente.")
        print("\t3. Eliminar seccion existente.")
        print("\t4. volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                modelo.add_section()
                os.system("cls")
            case "2":
                os.system("cls")
                modelo.edit_section()
                os.system("cls")
            case "3":
                pass
            case "4":
                break
            case _:
                print("Error: no se reconoce la opcion ingresada.\n\n")
                

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
                #TODO Punto de entrada Nodos.
                pass
            case "2":        
                #TODO Punto de entrada Elementos.
                pass
            case "3":
                modelo = secciones_settings(modelo)
                os.system("cls")
            case "4":
                #TODO Punto de entrada Materiales.
                pass
            case "5":
                #TODO Punto de entrada Cargas Puntuales.
                pass
            case "6":
                #TODO Punto de entrada Cargas Distribuidas.
                pass
            case "7":
                #TODO Punto de entrada Cargas Momentos.
                pass
            case "8":
                #TODO Punto de entrada Unidades del modelo.
                pass
            case "9":
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opcion ingresada.\n\n")

def model_system(modelo):
    while True:
        print("¿Qué desea hacer?:\n")
        
        print("\t1. Configurar estructura.")
        print("\t2. Información de la estructura.")
        print("\t3. Computar estructura.")
        print("\t4. Resultados.")
        print("\t5. Volver.")
        
        match input("\nIngrese una opción: "):
            case "1":
                model_settings(modelo)
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
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opcion ingresada.\n\n")
                pass 

def main():
    os.system("cls")
    #TODO loop con menu
    while True:
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
                print("Error: no se reconoce la opcion ingresada.\n\n")
                pass 

if __name__ == "__main__":
    main() 
