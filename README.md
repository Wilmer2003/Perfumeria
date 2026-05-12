# 🌸 Sistema de Gestión de Ventas — Perfumería
 
---
 
## 📋 Descripción
 
Sistema web para la gestión de ventas de una tienda de perfumería. Permite a **clientes** consultar el catálogo y realizar pedidos, a **vendedores** gestionar el estado de los pedidos, y al **gerente** supervisar ventas, reportes y el abastecimiento de productos.
 
 
## 🗂️ Estructura del Proyecto
 
```
Perfumeria/
├── Backend/
│   ├── Routers/
│   │   ├── Auth.py          # Login y autenticación JWT
│   │   ├── Pedidos.py       # CRUD de pedidos
│   │   ├── Productos.py     # CRUD de productos / catálogo
│   │   ├── Ventas.py        # Registro y reporte de ventas
│   │   └── Ordenes.py       # Órdenes de compra a proveedores
│   ├── Database.py          # Conexión a MySQL
│   ├── Models.py            # Modelos SQLAlchemy / Pydantic
│   ├── Main.py              # Entrada FastAPI, registro de routers
│   ├── .env                 # Variables de entorno (NO subir a Git)
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
├── .gitignore
└── README.md
```
 
---
 
## ⚙️ Requisitos Previos
 
Antes de clonar el proyecto asegúrate de tener instalado:
 
| Herramienta | Versión mínima | Descarga |
|---|---|---|
| Python | 3.10+ | https://www.python.org/downloads/ |
| MySQL Server | 8.0+ | https://dev.mysql.com/downloads/ |
| Visual Studio Code | Cualquier versión reciente | https://code.visualstudio.com/ |
| Git | Cualquier versión reciente | https://git-scm.com/ |
 
> **Nota:** Solo necesitas Python instalado en el sistema para correr el backend. 
 
---
 
## 🚀 Instalación y Configuración
 
### 1. Clonar el repositorio
 
Abre una terminal (PowerShell o la terminal integrada de VS Code) y ejecuta:
 
```bash
git clone https://github.com/Wilmer2003/Perfumeria.git
cd Perfumeria
```
 
---
 
### 2. Crear y activar el entorno virtual
 
```bash
# Crear el entorno virtual
python -m venv venv
 
# Activar en Windows
venv\Scripts\activate
 
# Activar en macOS/Linux
source venv/bin/activate
```
 
> En VS Code puedes seleccionar el intérprete del entorno con `Ctrl+Shift+P` → **Python: Select Interpreter** → elegir el `venv`.
 
---
 
### 3. Instalar dependencias
 
```bash
cd Backend
pip install -r requirements.txt
```
 
El archivo `requirements.txt` incluye:
 
```
fastapi
uvicorn
sqlalchemy
pymysql
python-dotenv
python-jose[cryptography]
passlib[bcrypt]
```
 
---
 
### 4. Configurar la base de datos MySQL
 
#### 4.1 Crear la base de datos
 
Abre MySQL Workbench o la terminal de MySQL y ejecuta:
 
```sql
CREATE DATABASE perfumeria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
 
#### 4.2 Importar el esquema
 
```bash
# Desde la raíz del proyecto
mysql -u root -p perfumeria < BD/schema.sql
```
 
O en MySQL Workbench: **File → Run SQL Script** → selecciona `BD/schema.sql`.
 
---
 
### 5. Configurar variables de entorno
 
En la carpeta `Backend/` crea un archivo `.env` con el siguiente contenido:
 
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=perfumeria
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
 
SECRET_KEY=clave_secreta_muy_larga_y_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
 
> ⚠️ Este archivo **nunca** se sube a Git (ya está en `.gitignore`).
 
---
 
### 6. Ejecutar el backend
 
```bash
# Asegúrate de estar en la carpeta Backend/ con el venv activado
cd Backend
uvicorn Main:app --reload
```
 
### 7. Abrir el frontend
 
Como el frontend es HTML puro, simplemente abre los archivos en el navegador:
 
- **Opción 1 (recomendada):** Instala la extensión **Live Server** en VS Code, haz clic derecho en `Login.html` → **Open with Live Server**.
- **Opción 2:** Abre directamente el archivo `Frontend/Login.html` en Chrome, Edge o Firefox.
> Asegúrate de que el backend esté corriendo antes de hacer login.
 
---
 
## 🔐 Roles y Accesos
 
| Rol | Credenciales de prueba | Redirige a |
|---|---|---|
| Cliente | Registrado en la tienda | `Catalogo.html` |
| Vendedor | Panel administrativo | `Vendedor.html` |
| Gerente | Panel administrativo | `Gerente.html` |
 
> Los permisos están diferenciados por rol según **RNF-02**: el gerente accede a reportes y órdenes de compra; el vendedor solo a pedidos.
 
---
 
## 📌 Funcionalidades Principales
 
### Cliente
- Consultar catálogo sin registrarse (RF-01)
- Iniciar sesión y agregar productos al carrito (RF-02, RF-03)
- Seleccionar presentación del perfume (50 ml / 80 ml) (RF-05)
- Recibir notificación de confirmación de pedido (RF-04)
### Vendedor
- Gestionar estado de pedidos: Pendiente → Enviado → Entregado (RF-05 Control)
- Ver historial de ventas
### Gerente
- Dashboard con reporte de ventas (exportable PDF/Excel) (RF-02 Control)
- Generar órdenes de compra a proveedores (RF-01 Abastecimiento)
- Recibir alertas de stock mínimo (RF-02 Abastecimiento)
- Registrar facturas de proveedores (RF-04 Abastecimiento)
---
 
## 🛡️ Seguridad
 
- Autenticación con JWT (tokens de sesión)
- Sesión se cierra automáticamente tras **30 minutos** de inactividad (RNF-09)
- Contraseñas hasheadas con bcrypt
- Validación en tiempo real de formularios (RNF-03)
---
 
## 🌐 Compatibilidad
 
El sistema es compatible con las versiones actuales de:
- Google Chrome ✅
- Microsoft Edge ✅
- Mozilla Firefox ✅
---
 
## 🤝 Contribuir
 
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