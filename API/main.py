from fastapi import FastAPI

# Inicializamos la aplicación
app = FastAPI(
    title="MYOREHAB API",
    description="Backend para consulta de datos cinemáticos y EMG del proyecto multicéntrico",
    version="0.1.0"
)

@app.get("/")
def root():
    """Endpoint de comprobación de estado."""
    return {"status": "ok", "message": "MYOREHAB API funcionando correctamente"}

@app.get("/api/v1/subjects")
def get_subjects():
    """
    Retorna la lista de sujetos registrados.
    TODO: Conectar a PostgreSQL (Tabla: subjects)
    """
    # Datos simulados temporalmente
    return [
        {"subject_id": "BR-CMP-S001", "age": 28, "lateral_dominance": "Right"},
        {"subject_id": "BR-CMP-S002", "age": 35, "lateral_dominance": "Left"}
    ]

@app.get("/api/v1/tasks/{subject_id}")
def get_subject_tasks(subject_id: str):
    """
    Retorna las tareas realizadas por un sujeto específico.
    TODO: Conectar a PostgreSQL (Tabla: tasks)
    """
    return {"subject_id": subject_id, "tasks": ["M111", "M112", "M113"]}

@app.get("/api/v1/recordings/{task_id}")
def get_recordings(task_id: str):
    """
    Retorna las rutas a los archivos físicos de EMG y Cinemática de una tarea.
    TODO: Conectar a PostgreSQL (Tabla: recordings)
    """
    return {
        "task_id": task_id,
        "files": {
            "emg": f"data/raw/emg/{task_id}_emg.csv",
            "kinematics": f"data/raw/kin/{task_id}_pose.csv"
        }
    }