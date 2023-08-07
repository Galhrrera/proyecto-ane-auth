import pandas as pd
import glob

# Obtener la lista de archivos CSV en el directorio actual
archivos_csv = glob.glob('data\*.csv')

# Crear una lista para almacenar los dataframes de cada archivo CSV
dataframes = []

# Leer y procesar cada archivo CSV
for archivo in archivos_csv:
    # Leer solo las filas 19 a 1019 y las primeras 2 columnas del archivo CSV
    df = pd.read_csv(archivo, skiprows=18, nrows=1000, usecols=[0, 1])
    
    # Agregar una columna "N medición" con el nombre del archivo original
    df['N medición'] = archivo.replace("data", "")
    
    # Renombrar las columnas según los nombres requeridos
    df.columns = ['Freq', 'SA Max Hold', 'N medición']
    
    # Agregar el dataframe a la lista
    dataframes.append(df)

# Combinar los dataframes en uno solo
df_final = pd.concat(dataframes)

# Guardar el dataframe final en un archivo CSV llamado "datosCompletos.csv"
df_final.to_csv('datosCompletos.csv', index=False)
