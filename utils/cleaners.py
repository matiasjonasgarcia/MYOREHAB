import re
import unicodedata
import pandas as pd
from typing import List, Optional

# 1. Generador dinámico de nombres para HD-EMG (128 canales)
def get_emg_column_names(normalized: bool = True) -> List[str]:
    """Genera la lista de 128 nombres de columna para EMG (64 Flex + 64 Exte)."""
    if normalized:
        flex = [f"flex_ch{i}" for i in range(1, 65)]
        exte = [f"exte_ch{i}" for i in range(1, 65)]
    else:
        flex = [f"Flex - Ch{i}" for i in range(1, 65)]
        exte = [f"Exte - Ch{i}" for i in range(1, 65)]
    return flex + exte

# 2. Normalizador individual de texto a snake_case
def normalize_column_name(col_name: str) -> str:
    """Convierte cualquier nombre de columna a formato estándar snake_case."""
    if not isinstance(col_name, str):
        col_name = str(col_name)
    name = col_name.strip().lower()
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    name = re.sub(r'[\s\-]+', '_', name)
    name = re.sub(r'[^a-z0-9_]', '', name)
    return re.sub(r'_+', '_', name).strip('_')

# 3. Cargar y estandarizar cualquier tipo de archivo (EMG o Cinemática)
def load_and_standardize_csv(
    file_path: str, 
    signal_type: str = "EMG"
) -> pd.DataFrame:
    """
    Lee un archivo CSV y le asigna o limpia los nombres de las columnas.
    
    Parámetros:
    -----------
    file_path : str
        Ruta al archivo .csv.
    signal_type : str
        'EMG' (sin cabecera, 128 cols) o 'KINEMATICS' (con cabecera).
    """
    signal_type = signal_type.upper()
    
    if signal_type == "EMG":
        # Asignación directa de encabezados estandarizados para los 128 canales
        headers = get_emg_column_names(normalized=True)
        df = pd.read_csv(file_path, header=None, names=headers)
        
    elif signal_type == "KINEMATICS":
        # Lectura con cabecera y normalización de cada nombre (e.g. WRIST_x -> wrist_x)
        df = pd.read_csv(file_path)
        df.columns = [normalize_column_name(c) for c in df.columns]
        
    else:
        raise ValueError(f"Tipo de señal '{signal_type}' no soportado. Usa 'EMG' o 'KINEMATICS'.")
        
    return df