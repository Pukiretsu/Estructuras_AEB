import pandas as pd
import numpy as np

# Definicion de dataframes en el contexto
MATERIALES = pd.DataFrame({'Nombre': pd.Series(dtype='str'),
                           'Modulo Young': pd.Series(dtype='float')})

SECCIONES = pd.DataFrame({'Nombre': pd.Series(dtype='str'), 
                          'Area': pd.Series(dtype='float'), 
                          'Inercia': pd.Series(dtype='float')})

NODOS = pd.DataFrame({'Nombre': pd.Series(dtype='str'),
                     'Coordenada X': pd.Series(dtype='float'),
                     'Coordenada y': pd.Series(dtype='float'),
                     'V': pd.Series(dtype='int'), 
                     'U': pd.Series(dtype='int'),
                     'Phi': pd.Series(dtype='int')})

ELEMENTOS = pd.DataFrame({'Nombre': pd.Series(dtype='str'),
                          'Nodo i': pd.Series(dtype='str'),
                          'Nodo j': pd.Series(dtype='str'), 
                          'longitud': pd.Series(dtype='float'),
                          'Angulo': pd.Series(dtype='float'), 
                          'Material': pd.Series(dtype='str'),
                          'Secciones': pd.Series(dtype='str')}) 

CARGAS_PUNTUALES = pd.DataFrame({'Nombre': pd.Series(dtype='str'),
                                 'Valor': pd.Series(dtype='float'),
                                 'Direccion': pd.Series(dtype='str'),
                                 'Nodo' : pd.Series(dtype='str'),
                                 'Elemento': pd.Series(dtype='str'),
                                 'Distancia': pd.Series(dtype='float')})

CARGAS_DISTRIBUIDAS = pd.DataFrame({'Nombre': pd.Series(dtype='str'),
                                    'Carga i': pd.Series(dtype='float'),
                                    'Carga f': pd.Series(dtype='float'),
                                    'Direccion': pd.Series(dtype='str'),
                                    'Elemento': pd.Series(dtype='str'),
                                    'Distancia i': pd.Series(dtype='float'),
                                    'Distancia f': pd.Series(dtype='float')})

MOMENTOS = pd.DataFrame({'Nombre': pd.Series(dtype='str'),
                         'Valor': pd.Series(dtype='float'),
                         'Direccion': pd.Series(dtype='str'),
                         'Nodo' : pd.Series(dtype='str'),
                         'Elemento': pd.Series(dtype='str'),
                         'Distancia': pd.Series(dtype='float')})
