from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from Database import get_db
from Models import OrdenCompra, DetalleOrdenCompra
from Routers.Auth import verificar_token
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/ordenes", tags=["Ordenes"])

class ItemOrden(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class OrdenIn(BaseModel):
    proveedor_id: int
    items: List[ItemOrden]

def get_usuario(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    return verificar_token(token)

@router.post("/")
def crear_orden(data: OrdenIn, db: Session = Depends(get_db), usuario=Depends(get_usuario)):
    if usuario["rol"] != "gerente":
        raise HTTPException(status_code=403, detail="Solo el gerente puede crear órdenes")
    total = sum(i.cantidad * i.precio_unitario for i in data.items)
    orden = OrdenCompra(proveedor_id=data.proveedor_id, gerente_id=usuario["id"], total=total)
    db.add(orden)
    db.flush()
    for item in data.items:
        det = DetalleOrdenCompra(
            orden_id=orden.id, producto_id=item.producto_id,
            cantidad=item.cantidad, precio_unitario=item.precio_unitario,
            subtotal=item.cantidad * item.precio_unitario
        )
        db.add(det)
    db.commit()
    return {"mensaje": "Orden creada", "orden_id": orden.id}

@router.get("/")
def listar_ordenes(db: Session = Depends(get_db), usuario=Depends(get_usuario)):
    if usuario["rol"] != "gerente":
        raise HTTPException(status_code=403, detail="Sin permiso")
    ordenes = db.query(OrdenCompra).order_by(OrdenCompra.creado_en.desc()).all()
    return [
        {"id": o.id, "proveedor": o.proveedor.nombre, "estado": o.estado,
         "total": o.total, "fecha": o.creado_en.strftime("%d/%m/%Y")}
        for o in ordenes
    ]