from typing import Annotated
from pydantic import BaseModel,Field

StrProducto = Annotated[str,Field(min_length=1,max_length=30)]
FltPrecio = Annotated[float,Field(gt = 0,lt=999999999)] 
BoolActivo = Annotated[bool,Field(description="Estado?")]
IdProducto = Annotated[int,Field(gt=0,description="ID producto")]


class ProductoSchema(BaseModel):
    id : IdProducto
    nombre:StrProducto
    marca:StrProducto
    precio:FltPrecio
    activo:BoolActivo = True


class ProductoUpdateSchema(BaseModel):
    nombre:StrProducto
    marca : StrProducto
    precio:FltPrecio
    activo:BoolActivo = True



