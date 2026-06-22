Readme · MD
Copiar

# 🌸 Sistema de Gestión de Ventas — Perfumería

 
## 📋 Descripción
 
Sistema web para la gestión de ventas de una tienda de perfumería. Permite a **clientes** consultar el catálogo y realizar pedidos, a **vendedores** gestionar el estado de los pedidos, y al **gerente** supervisar ventas, reportes y el abastecimiento de productos.
 
 
## 🗂️ Estructura del Proyecto
 
```
Perfumeria/
├── Backend/
│   ├── Routers/
│   │   ├── Auth.py          # Login, registro y autenticación JWT
│   │   ├── Pedidos.py       # CRUD de pedidos
│   │   ├── Productos.py     # CRUD de productos / catálogo
│   │   ├── Ventas.py        # Registro y reporte de ventas
│   │   └── Ordenes.py       # Órdenes de compra a proveedores
│   ├── Database.py          # Conexión a MySQL con SQLAlchemy
│   ├── Models.py            # Modelos SQLAlchemy y schemas Pydantic
│   ├── Main.py              # Entrada FastAPI, CORS y registro de routers
│   ├── .env                 # Variables de entorno (NO subir a Git)
│   ├── venv/                # Entorno virtual Python (NO subir a Git)
│   └── requirements.txt     # Dependencias Python
├── BD/
│   └── schema.sql           # Script de creación de la base de datos
├── Frontend/
│   ├── API.js               # Funciones fetch hacia el backend
│   ├── Login.html           # Pantalla de inicio de sesión
│   ├── Catalogo.html        # Vista cliente — catálogo de productos
│   ├── Vendedor.html        # Panel vendedor
│   ├── Gerente.html         # Panel gerente
│   ├── Pedidos_proveedor.html
│   └── style.css
├── .vscode/
│   └── settings.json        # Configuración Live Server para VS Code
├── .gitignore
└── README.md
```
 
---
 
## ⚙️ Requisitos Previos
 
Antes de clonar el proyecto asegúrate de tener instalado:
 
| Herramienta | Versión usada | Descarga |
|---|---|---|
| Python | 3.12 | https://www.python.org/downloads/ |
| MySQL Server | 8.0+ | https://dev.mysql.com/downloads/ |
| MySQL Workbench | Cualquier versión reciente | https://dev.mysql.com/downloads/workbench/ |
| Visual Studio Code | Cualquier versión reciente | https://code.visualstudio.com/ |
| Git | Cualquier versión reciente | https://git-scm.com/ |
 
### Extensiones de VS Code necesarias
 
- **Live Server** (Ritwick Dey) — para abrir el frontend
- **Python** (Microsoft) — para soporte del lenguaje
---
 
## 🚀 Instalación paso a paso
 
### 1. Clonar el repositorio
 
Abre la terminal integrada de VS Code (`Ctrl+ñ`) y ejecuta:
 
```bash
git clone https://github.com/Wilmer2003/Perfumeria.git
cd Perfumeria
```
 
---
 
### 2. Crear y activar el entorno virtual
 
```bash
cd Backend
python -m venv venv
```
 
Activar en Windows (PowerShell):
```bash
venv\Scripts\activate
```
 
> Si aparece error de permisos en PowerShell, ejecuta primero:
> ```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Luego vuelve a activar con `venv\Scripts\activate`
 
Cuando está activo verás `(venv)` al inicio de la línea en la terminal.
 
---
 
### 3. Instalar dependencias
 
Con el `(venv)` activo:
 
```bash
pip install -r requirements.txt
```
 
> Si `passlib` y `bcrypt` dan error de compatibilidad, ejecuta:
> ```bash
> pip uninstall bcrypt -y
> pip install bcrypt==4.0.1
> ```
 
---
 
### 4. Crear la base de datos en MySQL Workbench
 
1. Abre **MySQL Workbench** y conéctate a tu instancia local
2. Ve a **File → Open SQL Script** y selecciona `BD/schema.sql`
3. Presiona el rayo ⚡ para ejecutar todo el script
Esto crea la base de datos `perfumeria` con todas las tablas y datos de prueba.
 
---
 
### 5. Regenerar el hash de contraseñas
 
> Este paso es necesario porque el hash debe generarse en tu propia máquina.
 
Con el `(venv)` activo en la terminal, ejecuta:
 
```bash
python -c "from passlib.context import CryptContext; ctx = CryptContext(schemes=['bcrypt']); print(ctx.hash('Admin123'))"
```
 
Copia el hash que te genera (algo como `$2b$12$xxxx...`) y en MySQL Workbench ejecuta:
 
```sql
USE perfumeria;
 
UPDATE usuarios SET contrasena = 'PEGA_TU_HASH_AQUI' WHERE correo = 'gerente@perfumeria.com';
UPDATE usuarios SET contrasena = 'PEGA_TU_HASH_AQUI' WHERE correo = 'vendedor@perfumeria.com';
UPDATE usuarios SET contrasena = 'PEGA_TU_HASH_AQUI' WHERE correo = 'cliente@perfumeria.com';
```
 
---
 
### 6. Configurar variables de entorno
 
Crea el archivo `Backend/.env` con tus datos de MySQL:
 
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=perfumeria
DB_USER=root
DB_PASSWORD=tu_contraseña_de_mysql
 
SECRET_KEY=perfumeria_clave_super_secreta_2026_upao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
 
> ⚠️ Este archivo **nunca** se sube a Git (ya está en `.gitignore`).
 
---
 
### 7. Levantar el servidor backend
 
Con el `(venv)` activo, estando en la carpeta `Backend/`:
 
```bash
uvicorn Main:app --reload
```
 
Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```
 
---
 
### 8. Verificar que la API funciona
 
Abre en el navegador: **http://127.0.0.1:8000/docs**
 
Ahí verás la documentación automática (Swagger UI). Para probar el login:
 
1. Clic en `POST /api/auth/login` → **Try it out**
2. Pega este body y dale **Execute**:
```json
{
  "correo": "gerente@perfumeria.com",
  "contrasena": "Admin123",
  "rol": "gerente"
}
```
 
Respuesta esperada (código **200**):
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "rol": "gerente",
  "nombre": "Gerente Admin",
  "id": 1
}
```
 
---
 
### 9. Abrir el frontend
 
**Opción A — Desde el explorador de Windows (más fácil):**
1. Abre `D:\Perfumeria\Frontend\`
2. Doble clic en `Login.html`
**Opción B — Con Live Server en VS Code:**
1. Crea el archivo `.vscode/settings.json` en la raíz del proyecto con:
```json
{
  "liveServer.settings.root": "/Frontend",
  "liveServer.settings.port": 5500
}
```
2. Clic derecho en `Frontend/Login.html` → **Open with Live Server**
3. Abre: **http://127.0.0.1:5500/Login.html**
---
 
## 🔐 Usuarios de prueba
 
| Rol | Correo | Contraseña | Redirige a |
|---|---|---|---|
| Gerente | gerente@perfumeria.com | Admin123 | `Gerente.html` |
| Vendedor | vendedor@perfumeria.com | Admin123 | `Vendedor.html` |
| Cliente | cliente@perfumeria.com | Admin123 | `Catalogo.html` |
 
---
 
## 📌 Funcionalidades implementadas
 
### ✅ Login (completado)
- Pantalla de login con diseño elegante para perfumería
- Selección de rol: Cliente, Vendedor, Gerente
- Validación en tiempo real de campos (RNF-03)
- Autenticación con JWT — el token se guarda en `localStorage`
- Redirección automática según el rol del usuario (RNF-02)
- Mensajes de error claros — credenciales incorrectas, sin conexión (RNF-10)
- Cierre de sesión automático tras 30 minutos de inactividad (RNF-09)
### 🔄 En desarrollo
- Catálogo de productos (Cliente)
- Carrito de compras y pedidos
- Panel de Vendedor — gestión de pedidos
- Panel de Gerente — reportes y órdenes de compra
---
 
## 🛠️ Stack tecnológico
 
| Capa | Tecnología |
|---|---|
| Backend | Python 3.12 + FastAPI + Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Base de datos | MySQL 8.0 |
| Autenticación | JWT (python-jose) + bcrypt (passlib) |
| Frontend | HTML5 + CSS3 + JavaScript vanilla |
| Fuentes | Google Fonts (Cormorant Garamond + Jost) |
 
---
 
## 🌐 Compatibilidad
 
| Navegador | Estado |
|---|---|
| Google Chrome | ✅ |
| Microsoft Edge | ✅ |
| Mozilla Firefox | ✅ |
 
---
 
## 🤝 Flujo de trabajo Git
 
```bash
# Crear una rama para tu feature
git checkout -b feature/nombre-feature
 
# Hacer commit de tus cambios
git add .
git commit -m "feat: descripción del cambio"
 
# Subir tu rama
git push origin feature/nombre-feature
```
 
Luego abre un **Pull Request** en GitHub hacia la rama `main`.
 
---
 
## 📄 Licencia
 
Proyecto académico — UPAO 2026. Todos los derechos reservados al equipo de desarrollo.