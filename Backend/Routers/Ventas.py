from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from Database import get_db
from Models import Venta, Producto
from Routers.Auth import verificar_token

router = APIRouter(prefix="/api/ventas", tags=["Ventas"])

def get_usuario(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    return verificar_token(token)

@router.get("/reporte")
def reporte_ventas(db: Session = Depends(get_db), usuario=Depends(get_usuario)):
    if usuario["rol"] != "gerente":
        raise HTTPException(status_code=403, detail="Solo el gerente puede ver reportes")
    ventas = db.query(Venta).order_by(Venta.fecha.desc()).all()
    total_general = sum(v.total for v in ventas)
    return {
        "total_ventas": len(ventas),
        "ingresos_totales": total_general,
        "ventas": [
            {"id": v.id, "cliente": v.cliente.nombre if v.cliente else "",
             "vendedor": v.vendedor.nombre if v.vendedor else "",
             "total": v.total, "fecha": v.fecha.strftime("%d/%m/%Y %H:%M")}
            for v in ventas
        ]
    }

@router.get("/stock-bajo")
def stock_bajo(db: Session = Depends(get_db), usuario=Depends(get_usuario)):
    if usuario["rol"] not in ["gerente", "vendedor"]:
        raise HTTPException(status_code=403, detail="Sin permiso")
    productos = db.query(Producto).filter(
        Producto.stock <= Producto.stock_minimo,
        Producto.activo == True
    ).all()
    return [
        {"id": p.id, "nombre": p.nombre, "codigo": p.codigo,
         "stock": p.stock, "stock_minimo": p.stock_minimo}
        for p in productos
    ]