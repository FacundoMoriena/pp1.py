from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.producto import productos_routers
from database import Base,engine
import models

Base.metadata.create_all(bind = engine)

app=FastAPI()

app.title = "tiendaZapatillas"

app.include_router(productos_routers,tags=["Productos"],prefix="/productos")



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)


