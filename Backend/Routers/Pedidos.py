from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from Database import get_db
from Models import Pedido, DetallePedido, Producto, Venta, Factura
from pydantic import BaseModel
from typing import List
from datetime import datetime
from Routers.Auth import verificar_token

router = APIRouter(prefix="/api/pedidos", tags=["Pedidos"])

class ItemPedido(BaseModel):
    producto_id: int
    cantidad: int

class PedidoIn(BaseModel):
    items: List[ItemPedido]

def get_usuario(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    return verificar_token(token)

@router.post("/")
def crear_pedido(data: PedidoIn, db: Session = Depends(get_db), usuario=Depends(get_usuario)):
    total = 0
    detalles = []
    for item in data.items:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no existe")
        if producto.stock < item.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {producto.nombre}")
        subtotal = producto.precio * item.cantidad
        total += subtotal
        detalles.append({"producto": producto, "cantidad": item.cantidad,
                          "precio_unitario": producto.precio, "subtotal": subtotal})

    pedido = Pedido(cliente_id=usuario["id"], total=total, estado="pendiente")
    db.add(pedido)
    db.flush()

    for d in detalles:
        det = DetallePedido(
            pedido_id=pedido.id,
            producto_id=d["producto"].id,
            cantidad=d["cantidad"],
            precio_unitario=d["precio_unitario"],
            subtotal=d["subtotal"]
        )
        db.add(det)
        d["producto"].stock -= d["cantidad"]

    db.commit()
    return {"mensaje": "Pedido creado", "pedido_id": pedido.id, "total": total}

@router.get("/mis-pedidos")
def mis_pedidos(db: Session = Depends(get_db), usuario=Depends(get_usuario)):
    pedidos = db.query(Pedido).filter(Pedido.cliente_id == usuario["id"]).all()
    return [
        {"id": p.id, "estado": p.estado, "total": p.total,
         "fecha": p.creado_en.strftime("%d/%m/%Y %H:%M"),
         "items": len(p.detalles)}
        for p in pedidos
    ]

@router.get("/todos")
def todos_pedidos(db: Session = Depends(get_db), usuario=Depends(get_usuario)):
    if usuario["rol"] not in ["vendedor", "gerente"]:
        raise HTTPException(status_code=403, detail="Sin permiso")
    pedidos = db.query(Pedido).order_by(Pedido.creado_en.desc()).all()
    return [
        {"id": p.id, "cliente": p.cliente.nombre if p.cliente else "",
         "estado": p.estado, "total": p.total,
         "fecha": p.creado_en.strftime("%d/%m/%Y %H:%M")}
        for p in pedidos
    ]

@router.put("/{id}/estado")
def cambiar_estado(id: int, body: dict, db: Session = Depends(get_db), usuario=Depends(get_usuario)):
    if usuario["rol"] not in ["vendedor", "gerente"]:
        raise HTTPException(status_code=403, detail="Sin permiso")
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido.estado = body.get("estado")
    pedido.vendedor_id = usuario["id"]
    if body.get("estado") == "entregado":
        venta_existente = db.query(Venta).filter(Venta.pedido_id == id).first()
        if not venta_existente:
            venta = Venta(pedido_id=pedido.id, vendedor_id=usuario["id"],
                          cliente_id=pedido.cliente_id, total=pedido.total)
            db.add(venta)
            db.flush()
            numero = f"F-{datetime.now().strftime('%Y%m%d')}-{venta.id:04d}"
            factura = Factura(venta_id=venta.id, numero=numero, total=pedido.total)
            db.add(factura)
    db.commit()
    return {"mensaje": f"Estado actualizado a {body.get('estado')}"}