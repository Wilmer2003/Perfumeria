from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database import get_db
from Models import Producto, Categoria
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/productos", tags=["Productos"])

class ProductoIn(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = ""
    categoria_id: int
    precio: float
    presentacion: str
    stock: int
    stock_minimo: int = 5

@router.get("/")
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).filter(Producto.activo == True).all()
    return [
        {
            "id": p.id,
            "codigo": p.codigo,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "categoria": p.categoria.nombre if p.categoria else "",
            "precio": p.precio,
            "presentacion": p.presentacion,
            "stock": p.stock,
            "stock_bajo": p.stock <= p.stock_minimo
        }
        for p in productos
    ]