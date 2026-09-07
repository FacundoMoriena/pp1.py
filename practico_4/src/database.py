from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


#conexion a base de datos
sqlite_url = "sqlite:///./db_productos.db"
engine = create_engine(sqlite_url,connect_args={"check_same_thread" : False})
session_local = sessionmaker(autocommit = False,autoflush=False,bind = engine)

#modelos de las tablas en bd,base comun a todos los modelos
Base = declarative_base()


def get_database():
    db = session_local()
    try:
        yield db
    finally:
        db.close()