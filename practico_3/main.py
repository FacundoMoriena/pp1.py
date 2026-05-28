from fastapi import FastAPI,HTTPException,Path,Query,Body
from pydantic import BaseModel,Field 
from typing import Annotated


app = FastAPI()

app.title = "CelularesTienda"

celulares = [{"id" : 1,"nombre": "Samsung J7","marca" : "Samsung","precio" : 1500000,"activo" : True},
            {"id" : 2,"nombre": "Moto G15","marca" : "Motorola","precio" : 400000,"activo" : True},
            {"id" : 3,"nombre": "Iphone 15","marca" : "Apple","precio" : 2000000,"activo" : True}]



StrCorto = Annotated[str,Field(max_length=25)]
MaxPrecio = Annotated[float,Field(lt=100000000)]
DefaultBool = Annotated[bool,Field(description = "Estado?")]


class CelularSchema(BaseModel):
    id:Annotated[int,Field(gt=0,description="ID celular",deprecated = True)]
    nombre:StrCorto
    marca:StrCorto
    precio:MaxPrecio
    activo:DefaultBool = True


class CelularUpdateSchema(BaseModel):
    nombre:StrCorto
    marca:StrCorto
    precio:MaxPrecio
    activo:DefaultBool = True


noEncontrado ={
    404:{
        "description":"celular no encontrado",
        "content":{
            "application/json":{
                "example":{
                    "detail":"celular no encontrado",
                }
            }
        },
    },
}

    
@app.get("/celulares/{id}",
         response_model=CelularSchema,
         responses=noEncontrado,
         )
async def obtenerCelularesId(
    id: Annotated[int, Path(gt=0)]
)->CelularSchema:
    for celular in celulares:
        if celular["id"] == id:
            return celular
    raise HTTPException(status_code=404, detail="celular no encontrado")


@app.get("/celulares",
         response_model=list[CelularSchema]
         )
async def ObtenerCelularesEstado(
    estado: Annotated[bool, Query()]=True
)->list[CelularSchema]:
    celulares_filtrados = []

    for celular in celulares:
        if celular["activo"] == estado:
            celulares_filtrados.append(celular)

    return celulares_filtrados


@app.post("/celulares",
          response_model=CelularSchema)
async def postCelular(
    celular_nuevo: CelularSchema
)->CelularSchema:
    celulares.append(celular_nuevo.model_dump())

    return celular_nuevo


@app.put("/celulares/{id}",
         responses=noEncontrado,
         response_model=CelularSchema
         )
async def modificarCelular(
    id: Annotated[int, Path(gt=0)],
    celular_editado: CelularUpdateSchema
)->CelularSchema:
    for celular in celulares:
        if celular["id"] == id:

            celular["nombre"] = celular_editado.nombre
            celular["marca"] = celular_editado.marca
            celular["precio"] = celular_editado.precio
            celular["activo"] = celular_editado.activo

            return celular

    raise HTTPException(status_code=404, detail="celular no encontrado")


@app.delete("/celulares/{id}",
            responses=noEncontrado,
            response_model=CelularSchema)
async def borrarCelular(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[
        bool,
        Query(description="Mantener registro?")
    ]=False
)->CelularSchema:
    for celular in celulares:

        if celular["id"] == id:

            if logico:
                celular["activo"] = False
            else:
                celulares.remove(celular)

            return celular

    raise HTTPException(status_code=404, detail="celular no encontrado")