#tablas de bd

from database import Base
from sqlalchemy import Column,Integer,String,Boolean,Float

class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer,primary_key=True,index=True)
    nombre = Column(String)
    marca = Column(String)
    precio = Column(Float)
    activo = Column(Boolean)

    