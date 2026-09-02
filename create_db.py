import sqlite3
from pathlib import Path

# 1. Definir la ruta exacta (crea la carpeta data/ si no existe)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "myorehab_project.db"

# Conectar a la base de datos en la ruta correcta
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Activar el soporte para claves foráneas en SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# ==========================================
# TABLAS MAESTRAS
# ==========================================

# 1. Crear tabla centers
cursor.execute("""
CREATE TABLE IF NOT EXISTS centers (
    center_id TEXT PRIMARY KEY,
    center_name TEXT NOT NULL,
    country TEXT
);
""")

# 2. Crear tabla subjects
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    subject_id TEXT PRIMARY KEY,
    center_id TEXT NOT NULL,
    temporal_mark DATETIME,
    acronyms TEXT,
    age INTEGER,
    gender TEXT,
    weight REAL,
    height REAL,
    fa_circ REAL,
    lateral_dominance TEXT,
    laterality REAL,
    nhpeg_dominant REAL,
    nhpeg_nondominant REAL,
    injuries TEXT,
    injuries_description TEXT,
    sport TEXT,
    sport_type TEXT,
    sport_frequency INTEGER,
    FOREIGN KEY (center_id) REFERENCES centers(center_id)
);
""")

# 3. Crear tabla equipment
cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id TEXT PRIMARY KEY,
    center_id TEXT NOT NULL,
    signal_type TEXT,
    brand TEXT,
    model TEXT,
    channel_layout TEXT,
    total_channels INTEGER,
    FOREIGN KEY (center_id) REFERENCES centers(center_id)
);
""")

# ==========================================
# TABLAS DE ENSAYOS / PROTOCOLOS
# ==========================================

# 4. Crear tabla tasks
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL,
    condition_code TEXT,
    duration REAL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
""")

# 5. Crear tabla recordings
cursor.execute("""
CREATE TABLE IF NOT EXISTS recordings (
    recording_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    equipment_id TEXT NOT NULL,
    sampling_freq REAL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
);
""")

# ==========================================
# TABLAS DE SEÑALES (MODELO 3FN)
# ==========================================

# 6. Crear tabla emg_signals
cursor.execute("""
CREATE TABLE IF NOT EXISTS emg_signals (
    emg_id TEXT PRIMARY KEY,
    recording_id TEXT NOT NULL,
    equipment_id TEXT NOT NULL,
    file_path TEXT NOT NULL,
    FOREIGN KEY (recording_id) REFERENCES recordings(recording_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
);
""")

# 7. Crear tabla kinematics_3d
cursor.execute("""
CREATE TABLE IF NOT EXISTS kinematics_3d (
    kin_id TEXT PRIMARY KEY,
    recording_id TEXT NOT NULL,
    equipment_id TEXT NOT NULL,
    file_path TEXT NOT NULL,
    FOREIGN KEY (recording_id) REFERENCES recordings(recording_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
);
""")

# 8. Crear tabla videos_3d
cursor.execute("""
CREATE TABLE IF NOT EXISTS videos_3d (
    video_id TEXT PRIMARY KEY,
    recording_id TEXT NOT NULL,
    fps INTEGER,
    file_path TEXT NOT NULL,
    FOREIGN KEY (recording_id) REFERENCES recordings(recording_id)
);
""")

conn.commit()
conn.close()
print(f"Base de datos FAIR (3FN) estructurada y creada exitosamente en:\n{DB_PATH}")