from typing import Annotated,Union
from fastapi import APIRouter,HTTPException,Path,Query,Depends
from schemas.zapatillas import ProductoSchema,ProductoUpdateSchema
from models import Producto
from sqlalchemy.orm import Session
from database import get_database


productos_routers = APIRouter()

NO_ENCONTRADO = {
    404:{
        "description":"Producto no encontrado",
        "content":{
            "application/json":{
                "example":{
                    "detail":"Producto no encontrado",
                }
            }
        },
    },
}

productos = Producto



@productos_routers.get("/",
        response_model=list[ProductoSchema]
        )

async def getProductos(db:Session = Depends(get_database)
)->list[ProductoSchema]:

    productos = db.query(Producto).all()
    return productos

 

@productos_routers.get("/{id}",
         response_model=ProductoSchema,
         responses=NO_ENCONTRADO,
         )
async def obtenerProductoId(
    id: Annotated[int,Path(gt=0)],
    db:Session = Depends(get_database),
)->ProductoSchema:
    producto_obtenido = db.query(Producto).filter(Producto.id == id).first()

    if producto_obtenido is not None:
        return producto_obtenido
    
    raise HTTPException(status_code=404, detail="Producto no encontrado")



@productos_routers.post("/",
          response_model=ProductoUpdateSchema)
async def postProducto(
    producto_nuevo: ProductoSchema,
    db:Session = Depends(get_database)
    )->ProductoSchema:

    nuevo_producto = Producto(

        nombre= producto_nuevo.nombre,
        marca = producto_nuevo.marca,
        precio = producto_nuevo.precio,
        activo = producto_nuevo.activo
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto



@productos_routers.put("/{id}",
         responses=NO_ENCONTRADO,
         response_model=ProductoSchema
         )
async def modificarProducto(
    id: Annotated[int, Path(gt=0)],
    producto_editado: ProductoUpdateSchema,
    db:Session = Depends(get_database)
)->ProductoSchema:
    producto_obtenido = db.query(Producto).filter(Producto.id == id).first()

    if not producto_obtenido:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto_obtenido.nombre = producto_editado.nombre
    producto_obtenido.marca = producto_editado.marca
    producto_obtenido.precio = producto_editado.precio
    producto_obtenido.activo = producto_editado.activo

    db.commit()
    db.refresh(producto_obtenido)

    return producto_obtenido


@productos_routers.delete("/{id}",
            responses=NO_ENCONTRADO,
            response_model=Union[ProductoSchema, list[ProductoSchema]])
async def borrarProducto(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[
        bool,
        Query(description="Mantener registro?")
    ]=False,
     db:Session = Depends(get_database)
)->Union[ProductoSchema, list[ProductoSchema]]:

    producto_obtenido = db.query(Producto).filter(Producto.id == id).first()

    if not producto_obtenido:
         raise HTTPException(status_code=404, detail="Producto no encontrado")



    if producto_obtenido.id == id:
        if logico:
            producto_obtenido.activo = False
            db.commit()
            db.refresh(producto_obtenido)
            return producto_obtenido
    
    db.delete(producto_obtenido)
    db.commit()

    return db.query(Producto).all()

   



