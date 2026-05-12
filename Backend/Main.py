from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
 
from Database import engine, Base
 
# Importar todos los routers
from Routers.Auth import router as auth_router
# from Routers.Productos import router as productos_router  # descomenta cuando lo crees
# from Routers.Pedidos  import router as pedidos_router
# from Routers.Ventas   import router as ventas_router
# from Routers.Ordenes  import router as ordenes_router
 
# Crear todas las tablas si no existen
Base.metadata.create_all(bind=engine)
 
app = FastAPI(
    title="Sistema de Gestión — Perfumería",
    description="API REST para la tienda de perfumería. UPAO 2026.",
    version="1.0.0"
)
 
# ── CORS: permite que el frontend HTML llame a la API ──────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # en producción pon solo tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# ── Registrar routers ──────────────────────────────────────────
app.include_router(auth_router)
# app.include_router(productos_router)
# app.include_router(pedidos_router)
# app.include_router(ventas_router)
# app.include_router(ordenes_router)
 
# ── Servir el frontend estático (opcional) ─────────────────────
frontend_path = os.path.join(os.path.dirname(__file__), "..", "Frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
 
@app.get("/api/health")
def health():
    return {"status": "ok", "mensaje": "API Perfumería funcionando"}