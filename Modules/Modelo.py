import pandas as pd
import numpy as np

# Definicion de dataframes en el contexto
MATERIALES = pd.DataFrame({'Nombre': pd.Series(dtype='str'), 'Modulo Young': pd.Series(dtype="float")})
SECCIONES = pd.DataFrame({'Nombre': pd.Series(dtype='str'), 'Area': pd.Series(dtype="float"), 'Inercia': pd.Series(dtype="float")})



