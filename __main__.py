import os
import Modules.Modelo as material

def new_model():
    os.system("cls")
    #TODO
    model_system()
    pass

def load_model():
    os.system("cls")
    #TODO
    model_system()
    pass

def model_settings():
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
        
        match int(input("\nIngrese una opción: ")):
            case 1:
                #TODO Punto de entrada Nodos.
                pass
            case 2:        
                #TODO Punto de entrada Elementos.
                pass
            case 3:
                #TODO Punto de entrada Secciones.
                pass
            case 4:
                #TODO Punto de entrada Materiales.
                pass
            case 5:
                #TODO Punto de entrada Cargas Puntuales.
                pass
            case 6:
                #TODO Punto de entrada Cargas Distribuidas.
                pass
            case 7:
                #TODO Punto de entrada Cargas Momentos.
                pass
            case 8:
                #TODO Punto de entrada Unidades del modelo.
                pass
            case 9:
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opcion ingresada.\n\n")
                pass 



def model_system():
    while True:
        print("Que desea hacer:\n")
        
        print("\t1. Configurar estructura.")
        print("\t2. Información de la estructura.")
        print("\t3. Computar estructura.")
        print("\t4. Resultados.")
        print("\t5. Volver.")
        
        match int(input("\nIngrese una opción: ")):
            case 1:
                model_settings()
            case 2: 
                #TODO Punto de entrada Información estructura.
                pass
            case 3: 
                #TODO Punto de entrada Computar estructura.
                pass
            case 4: 
                #TODO Punto de entrada Resultados.
                pass
            case 5:
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
        
        match int(input("\nIngrese una opción: ")):
            case 1:
                new_model()
            case 2:        
                load_model()
            case 3:
                break
            case _:
                print("Error: no se reconoce la opcion ingresada.\n\n")
                pass 

if __name__ == "__main__":
    main() 
