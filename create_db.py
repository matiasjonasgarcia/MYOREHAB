import sqlite3

# Conectar (si no existe el archivo, SQLite lo crea automáticamente)
conn = sqlite3.connect("myorehab_project.db")
cursor = conn.cursor()

# Activar el soporte para claves foráneas en SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# 1. Crear tabla centers
cursor.execute("""
CREATE TABLE IF NOT EXISTS centers (
    center_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    ubicacion TEXT
);
""")

# 2. Crear tabla subjects
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    center_id INTEGER NOT NULL,
    edad INTEGER,
    genero TEXT,
    diagnostico TEXT,
    FOREIGN KEY (center_id) REFERENCES centers(center_id)
);
""")

# 3. Crear tabla equipment
cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    center_id INTEGER NOT NULL,
    marca TEXT,
    modelo TEXT,
    FOREIGN KEY (center_id) REFERENCES centers(center_id)
);
""")

# 4. Crear tabla tasks
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_tarea TEXT NOT NULL,
    descripcion TEXT
);
""")

# 5. Crear tabla recording
cursor.execute("""
CREATE TABLE IF NOT EXISTS recording (
    recording_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    fecha_hora TEXT,
    frecuencia_muestreo_hz REAL,
    ruta_archivo TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
);
""")

conn.commit()
conn.close()
print("Base de datos y tablas creadas exitosamente.")