import os
import re
import glob
import pandas as pd

def parse_filename_metadata(filename: str) -> dict:
    """
    Extrae variables desglosadas a partir de la nomenclatura 'SNNN_PGA.csv'.
    
    Estructura esperada: S<NNN>_<P><G><A>.csv
    - subject_id   : BR-CMP-S<NNN> (Código único de sujeto)
    - arm_position : P (1: Distal/AE, 2: Proximal/AF)
    - task_id      : G (Grasp type -> 1: 1FP, 2: 2FP, 3: FG)
    - hand_angle   : A (Angle code -> 1: 0°, 2: 45°, 3: 90°, 4: 135°, 5: 180°)
    """
    pattern = r"S(\d{3})_(\d)(\d)(\d)\.csv"
    match = re.match(pattern, filename)
    
    if not match:
        raise ValueError(f"El archivo '{filename}' no cumple con la nomenclatura estándar 'SNNN_PGA.csv'.")
        
    s_num, p, g, a = match.groups()
    
    return {
        "subject_id": f"BR-CMP-S{s_num}",
        "arm_position": int(p),
        "task_id": int(g),
        "hand_angle": int(a)
    }

def process_file(file_path: str) -> pd.DataFrame:
    """
    Lee el CSV detectando si es Cinemática (con encabezados) o sEMG (datos numéricos).
    Normaliza todos los nombres de columnas a minúsculas sin espacios adicionales.
    """
    filename = os.path.basename(file_path)
    meta = parse_filename_metadata(filename)
    
    # 1. Leer solo la primera fila para comprobar si contiene encabezados de texto
    df_check = pd.read_csv(file_path, nrows=1, header=None)
    
    try:
        pd.to_numeric(df_check.iloc[0])
        has_header = False  # Es sEMG crudo
    except ValueError:
        has_header = True   # Es Cinemática (con encabezados)

    # 2. Cargar el DataFrame y normalizar encabezados
    if has_header:
        df = pd.read_csv(file_path, header=0)
        # Convertir todos los nombres de columnas a minúsculas y limpiar espacios
        df.columns = df.columns.str.strip().str.lower()
    else:
        df = pd.read_csv(file_path, header=None)
        num_channels = df.shape[1]
        
        if num_channels == 128:
            flex_cols = [f"flex_ch{i}" for i in range(1, 65)]
            exte_cols = [f"exte_ch{i}" for i in range(1, 65)]
            df.columns = flex_cols + exte_cols
        else:
            df.columns = [f"ch_{i+1}" for i in range(num_channels)]

    # 3. Inyectar las 4 columnas de metadata al inicio
    df.insert(0, "hand_angle", meta["hand_angle"])
    df.insert(0, "task_id", meta["task_id"])
    df.insert(0, "arm_position", meta["arm_position"])
    df.insert(0, "subject_id", meta["subject_id"])

    return df

def run_etl_pipeline(input_dir: str, output_dir: str, keep_subfolders: bool = True):
    """
    Recorre de manera recursiva todas las subcarpetas (S001, S002...) dentro de input_dir.
    
    :param input_dir: Carpeta raíz de entrada (ej: 'raw/emg' o 'emg-raw')
    :param output_dir: Carpeta destino (ej: 'processed/emg' o 'emg-processed')
    :param keep_subfolders: Si es True, mantiene la subcarpeta del sujeto en la salida (ej: 'processed/emg/S001/')
    """
    if not os.path.exists(input_dir):
        print(f"❌ La carpeta de entrada '{input_dir}' no existe en {os.getcwd()}")
        return

    # Buscar todos los archivos .csv dentro de input_dir y sus subcarpetas
    csv_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().startswith("s") and file.lower().endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    if not csv_files:
        print(f"⚠️ No se encontraron archivos 'S*.csv' en '{input_dir}' ni en sus subcarpetas.")
        return

    print(f"🚀 Iniciando proceso ETL para {len(csv_files)} archivos encontrados en '{input_dir}'...")

    processed_count = 0
    error_count = 0

    for fpath in csv_files:
        try:
            df_processed = process_file(fpath)
            filename = os.path.basename(fpath)

            if keep_subfolders:
                # Obtener el nombre de la subcarpeta (ej: 'S001')
                rel_path = os.path.relpath(fpath, input_dir)
                target_path = os.path.join(output_dir, rel_path)
            else:
                # Guardar todo directamente en output_dir
                target_path = os.path.join(output_dir, filename)

            # Crear carpeta destino si no existe
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Guardar el archivo procesado
            df_processed.to_csv(target_path, index=False)
            processed_count += 1
            print(f"  [OK] Procesado: {os.path.relpath(target_path, output_dir)}")

        except Exception as e:
            error_count += 1
            print(f"  [ERROR] Fallo al procesar {fpath}: {e}")

    print(f"\n✅ ETL Finalizado: {processed_count} exitosos, {error_count} errores.")

if __name__ == "__main__":
    # Procesar EMG:
    run_etl_pipeline(input_dir="data/raw/emg", output_dir="data/processed/emg", keep_subfolders=True)
    
    # Procesar Cinemática:
    run_etl_pipeline(input_dir="data/raw/kinematics", output_dir="data/processed/kinematics", keep_subfolders=True)
