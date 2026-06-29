from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
 
from Database import get_db
from Models import Usuario, LoginRequest, TokenResponse
 
load_dotenv()
 
router = APIRouter(prefix="/api/auth", tags=["Autenticación"])
 
# ── configuración JWT ──────────────────────────────────────────
SECRET_KEY  = os.getenv("SECRET_KEY", "cambia_esta_clave_secreta")
ALGORITHM   = os.getenv("ALGORITHM", "HS256")
EXPIRE_MIN  = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
 
# ── bcrypt ─────────────────────────────────────────────────────
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
def verificar_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)
 
def hashear_password(plain: str) -> str:
    return pwd_ctx.hash(plain)
 
def crear_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MIN)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
 
def verificar_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "id":     int(payload.get("sub")),
            "rol":    payload.get("rol"),
            "nombre": payload.get("nombre")
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado."
        ) 
# ================================================================
#  POST /api/auth/login
# ================================================================
@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    # 1. Buscar usuario por correo
    usuario = db.query(Usuario).filter(
        Usuario.correo == body.correo,
        Usuario.activo == 1
    ).first()
 
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )
 
    # 2. Verificar contraseña
    if not verificar_password(body.contrasena, usuario.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )
 
    # 3. Verificar que el rol solicitado coincide con el real
    #    (si el front envía un rol, lo validamos)
    if body.rol and body.rol != usuario.rol:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Tu cuenta no tiene el rol '{body.rol}'. Tu rol es '{usuario.rol}'."
        )
 
    # 4. Crear token JWT
    token = crear_token({
        "sub": str(usuario.id),
        "rol": usuario.rol,
        "nombre": usuario.nombre
    })
 
    return TokenResponse(
        access_token=token,
        rol=usuario.rol,
        nombre=usuario.nombre,
        id=usuario.id
    )
 
 
# ================================================================
#  POST /api/auth/registro  (solo para clientes)
# ================================================================
@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registro(body: LoginRequest, db: Session = Depends(get_db)):
    # Verificar si ya existe
    existe = db.query(Usuario).filter(Usuario.correo == body.correo).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una cuenta con ese correo."
        )
 
    nuevo = Usuario(
        nombre     = body.correo.split("@")[0],   # nombre provisional
        correo     = body.correo,
        contrasena = hashear_password(body.contrasena),
        rol        = "cliente"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
 
    return {"mensaje": "Cuenta creada correctamente.", "id": nuevo.id}
 