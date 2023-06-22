import os
import Modules.Modelo as mod

def new_model():
    os.system("cls")
    modelo = mod.model()
    model_system(modelo)

def load_model():
    os.system("cls")
    #TODO Implementar sistema de cargado
    modelo = mod.model()
    modelo.load_model()
    model_system(modelo)

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
                    print("Error: no se reconoce la opcion ingresada.\n\n")
            case "3":
                if not modelo.secciones.empty:
                    os.system("cls")
                    show_units()
                    modelo.delete_section()
                    os.system("cls")
                else:
                    print("Error: no se reconoce la opcion ingresada.\n\n")
            case "4":
                return modelo
            case _:
                print("Error: no se reconoce la opcion ingresada.\n\n")

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
                #TODO Punto de entrada Nodos.
                pass
            case "2":        
                #TODO Punto de entrada Elementos.
                pass
            case "3":
                modelo = secciones_settings(modelo)
                os.system("cls")
            case "4":
                modelo = materiales_settings(modelo)
                os.system("cls")
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
                modelo = units_settings(modelo)
                os.system("cls")
            case "9":
                os.system("cls")
                return modelo
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")

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
                os.system("cls")
                break
            case _:
                print("Error: no se reconoce la opción ingresada.\n\n")
                pass 

def main():
    os.system("cls")
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
                print("Error: no se reconoce la opción ingresada.\n\n")
                pass 

if __name__ == "__main__":
    main() 
