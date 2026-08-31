# Biblia de Uso y Arquitectura de Datos — Proyecto MYOREHAB

Guía integral para la ingesta, lectura, análisis y reproducibilidad de las señales electromiográficas (HD-sEMG) y cinemáticas 3D de la base de datos MYOREHAB.

---

## 1. Estructura del Repositorio y Datos

El proyecto aplica una arquitectura estricta de capas para garantizar la integridad de los datos de investigación:

```text
MYOREHAB/
├── data/
│   ├── raw/                      <-- CAPA CRUDA (Lectura únicamente, NUNCA modificar)
│   │   ├── emg/
│   │   │   └── S001/             <-- Subcarpetas por sujeto (S001, S002, ...)
│   │   │       ├── S001_111.csv
│   │   │       └── ... (30 tareas)
│   │   └── kinematics/
│   │       └── S001/
│   │           ├── pose-3d_S001_111.csv
│   │           └── ... (30 tareas)
│   └── processed/                <-- CAPA PROCESADA (Optimizada en Parquet)
│       ├── emg/
│       │   └── S001/
│       │       └── S001_111.parquet
│       └── kinematics/
│           └── S001/
│               └── pose-3d_S001_111.parquet
├── docs/
│   ├── DATA_DICTIONARY.md
│   └── DATA_USAGE_GUIDE.md
├── utils/
│   ├── __init__.py
│   └── cleaners.py               <-- Funciones Regex de estandarización
├── run_etl.py                    <-- Script automatizado de conversión RAW -> Parquet
└── README.md
```

---

## 2. Flujo de Trabajo (Pipeline ETL)

### Paso A: Depositar archivos crudos
Sube los archivos generados por las estaciones de adquisición a la carpeta `data/raw/` respetando el identificador del sujeto:
- **EMG:** `data/raw/emg/S<ID>/`
- **Cinemática:** `data/raw/kinematics/S<ID>/`

### Paso B: Ejecutar la estandarización
Ejecuta el script principal de ETL en la terminal:

```bash
uv run python run_etl.py
```

#### Proceso automatizado:
1. Recorre recursivamente todas las carpetas de sujetos.
2. Lee los archivos EMG sin encabezado y les asigna los 128 canales estandarizados (`flex_ch1..64`, `exte_ch1..64`).
3. Lee las tablas cinemáticas de Anipose y limpia los encabezados a `snake_case` mediante expresiones regulares (limpiando espacios, acentos y caracteres no alfanuméricos).
4. Genera los archivos en formato binario **Parquet** en `data/processed/` manteniendo la misma jerarquía de carpetas.

---

## 3. Guía de Consumo en Python / Data Science

Para realizar análisis exploratorio, procesamiento de señales o entrenamiento de modelos, **lee siempre desde la carpeta `data/processed/`**.

### Ejemplo 1: Cargar y analizar señales EMG de un sujeto
```python
import pandas as pd

# Lectura directa del archivo Parquet
df_emg = pd.read_parquet("data/processed/emg/S001/S001_111.parquet")

# Extraer solo canales flexores
flex_data = df_emg.filter(like="flex_")

# Extraer un canal específico
ch1 = df_emg["flex_ch1"]
```

### Ejemplo 2: Cargar y filtrar la cinemática de la muñeca
```python
import pandas as pd

df_kin = pd.read_parquet("data/processed/kinematics/S001/pose-3d_S001_111.parquet")

# Seleccionar trayectorias 3D de la muñeca y sus métricas de error
wrist_cols = [c for c in df_kin.columns if c.startswith("wrist_")]
df_wrist = df_kin[["fnum"] + wrist_cols]

# Filtrar frames donde la reconstrucción tuvo baja confianza (score < 0.5)
df_valid = df_kin[df_kin["wrist_score"] >= 0.5]
```

---

## 4. Estándares y Buenas Prácticas del Proyecto

1. **Inmutabilidad Cruda:** Los archivos bajo `data/raw/` no deben ser reescritos ni editados manualmente bajo ninguna circunstancia.
2. **Nombres en Código:** Utilizar siempre las variables normalizadas (`snake_case`) definidas en `DATA_DICTIONARY.md`. Evitar referencias duras a índices numéricos de columna (ej. usar `df['flex_ch1']` en lugar de `df.iloc[:, 0]`).
3. **Formatos de Exportación:** No volver a exportar la capa procesada a `.csv`. El uso de `.parquet` optimiza el consumo de memoria RAM y mantiene los tipos de datos exactos (`int64`, `float64`).