from sqlalchemy import Column, Integer, String, Enum, DateTime, DECIMAL, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from Database import Base
from pydantic import BaseModel, EmailStr
from typing import Optional
 
# ================================================================
#  MODELOS SQLALCHEMY  (tablas de la BD)
# ================================================================
 
class Usuario(Base):
    __tablename__ = "usuarios"
 
    id         = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(100), nullable=False)
    correo     = Column(String(150), unique=True, nullable=False, index=True)
    contrasena = Column(String(255), nullable=False)
    rol        = Column(Enum("cliente", "vendedor", "gerente"), nullable=False, default="cliente")
    activo     = Column(Integer, default=1)
    creado_en  = Column(DateTime, default=datetime.utcnow)
 
    pedidos_cliente  = relationship("Pedido", back_populates="cliente",  foreign_keys="Pedido.cliente_id")
    pedidos_vendedor = relationship("Pedido", back_populates="vendedor", foreign_keys="Pedido.vendedor_id")
    ordenes          = relationship("OrdenCompra", back_populates="gerente")
 
 
class Categoria(Base):
    __tablename__ = "categorias"
 
    id     = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), unique=True, nullable=False)
 
    productos = relationship("Producto", back_populates="categoria")
 
 
class Proveedor(Base):
    __tablename__ = "proveedores"
 
    id        = Column(Integer, primary_key=True, index=True)
    nombre    = Column(String(150), nullable=False)
    contacto  = Column(String(100))
    telefono  = Column(String(20))
    correo    = Column(String(150))
    direccion = Column(String(255))
 
    productos = relationship("Producto", back_populates="proveedor")
    ordenes   = relationship("OrdenCompra", back_populates="proveedor")
 
 
class Producto(Base):
    __tablename__ = "productos"
 
    id           = Column(Integer, primary_key=True, index=True)
    codigo       = Column(String(30), unique=True, nullable=False)
    nombre       = Column(String(150), nullable=False)
    descripcion  = Column(Text)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    precio       = Column(DECIMAL(10, 2), nullable=False)
    presentacion = Column(Enum("50ml", "80ml", "100ml", "otro"), default="50ml")
    stock        = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)
    imagen_url   = Column(String(255))
    activo       = Column(Integer, default=1)
    creado_en    = Column(DateTime, default=datetime.utcnow)
 
    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
 
 
class Pedido(Base):
    __tablename__ = "pedidos"
 
    id          = Column(Integer, primary_key=True, index=True)
    cliente_id  = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    vendedor_id = Column(Integer, ForeignKey("usuarios.id"))
    estado      = Column(Enum("pendiente", "enviado", "entregado", "cancelado"), default="pendiente")
    total       = Column(DECIMAL(10, 2), default=0.00)
    creado_en   = Column(DateTime, default=datetime.utcnow)
 
    cliente  = relationship("Usuario", back_populates="pedidos_cliente",  foreign_keys=[cliente_id])
    vendedor = relationship("Usuario", back_populates="pedidos_vendedor", foreign_keys=[vendedor_id])
    detalles = relationship("DetallePedido", back_populates="pedido")
    venta    = relationship("Venta", back_populates="pedido", uselist=False)
 
 
class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
 
    id          = Column(Integer, primary_key=True, index=True)
    pedido_id   = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad    = Column(Integer, nullable=False)
    precio_unit = Column(DECIMAL(10, 2), nullable=False)
 
    pedido   = relationship("Pedido",   back_populates="detalles")
    producto = relationship("Producto")
 
 
class Venta(Base):
    __tablename__ = "ventas"
 
    id             = Column(Integer, primary_key=True, index=True)
    pedido_id      = Column(Integer, ForeignKey("pedidos.id"), unique=True, nullable=False)
    numero_factura = Column(String(30), unique=True, nullable=False)
    total          = Column(DECIMAL(10, 2), nullable=False)
    fecha_venta    = Column(DateTime, default=datetime.utcnow)
 
    pedido = relationship("Pedido", back_populates="venta")
    facturas = relationship("Factura", back_populates="venta")

 
 
class OrdenCompra(Base):
    __tablename__ = "ordenes_compra"
 
    id           = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    gerente_id   = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estado       = Column(Enum("enviada", "validada", "recibida"), default="enviada")
    total        = Column(DECIMAL(10, 2), default=0.00)
    creado_en    = Column(DateTime, default=datetime.utcnow)
 
    proveedor = relationship("Proveedor", back_populates="ordenes")
    gerente   = relationship("Usuario",   back_populates="ordenes")
    detalles  = relationship("DetalleOrden", back_populates="orden")
 
 
class DetalleOrden(Base):
    __tablename__ = "detalle_orden"
 
    id          = Column(Integer, primary_key=True, index=True)
    orden_id    = Column(Integer, ForeignKey("ordenes_compra.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad    = Column(Integer, nullable=False)
    precio_unit = Column(DECIMAL(10, 2), nullable=False)
 
    orden    = relationship("OrdenCompra", back_populates="detalles")
    producto = relationship("Producto")

class Factura(Base):
    __tablename__ = "facturas"

    id         = Column(Integer, primary_key=True, index=True)
    venta_id   = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    numero     = Column(String(30), unique=True, nullable=False)
    fecha      = Column(DateTime, default=datetime.utcnow)
    total      = Column(DECIMAL(10, 2), nullable=False)
    tipo       = Column(Enum("venta", "compra"), default="venta")

    venta = relationship("Venta", back_populates="facturas")
 
 
# ================================================================
#  SCHEMAS PYDANTIC  (validación de requests/responses)
# ================================================================
 
class LoginRequest(BaseModel):
    correo:     str
    contrasena: str
    rol:        Optional[str] = None   # opcional, se valida en Auth.py
 
class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    rol:          str
    nombre:       str
    id:           int
 

DetalleOrdenCompra = DetalleOrden
