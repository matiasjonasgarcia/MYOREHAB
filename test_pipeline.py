from utils.cleaners import load_and_standardize_csv

# 1. Definimos la ruta de nuestro archivo en la carpeta data/raw/emg/
emg_file_path = "data/raw/emg/S001_111.csv"

print(f"Cargando y procesando: {emg_file_path}...")

# 2. Ejecutamos la función de limpieza y asignación de nombres
df_emg = load_and_standardize_csv(emg_file_path, signal_type="EMG")

# 3. Imprimimos en pantalla los resultados para verificar
print("\n¡Lectura exitosa!")
print(f"Dimensiones de la matriz: {df_emg.shape[0]} filas x {df_emg.shape[1]} columnas")
print("\nPrimeras 5 columnas Flexoras:", list(df_emg.columns[:5]))
print("Primeras 5 columnas Extensoras:", list(df_emg.columns[64:69]))
print("\nMuestra de los primeros datos:")
print(df_emg.head(3).iloc[:, [0, 1, 64, 65]])