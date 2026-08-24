from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Credenciales de acceso a tu contenedor Docker de PostgreSQL
DATABASE_URL = "postgresql://admin_fisiologia:super_password_seguro@localhost:5432/fisiologia_db"

# Creación del motor de conexión
engine = create_engine(DATABASE_URL)

# Fábrica de sesiones (para abrir y cerrar consultas a la BD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para definir nuestros futuros modelos de tablas
Base = declarative_base()

def get_db():
    """
    Función de dependencia para FastAPI. 
    Abre una conexión a la BD por cada petición y la cierra al terminar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()