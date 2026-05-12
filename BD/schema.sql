-- ============================================================
--  PERFUMERÍA — Schema de Base de Datos
--  Ejecutar: mysql -u root -p perfumeria < schema.sql
-- ============================================================
 
CREATE DATABASE IF NOT EXISTS perfumeria
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
 
USE perfumeria;
 
-- ------------------------------------------------------------
-- USUARIOS  (clientes, vendedores, gerente)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL,
  correo      VARCHAR(150) NOT NULL UNIQUE,
  contrasena  VARCHAR(255) NOT NULL,          -- bcrypt hash
  rol         ENUM('cliente','vendedor','gerente') NOT NULL DEFAULT 'cliente',
  activo      TINYINT(1) NOT NULL DEFAULT 1,
  creado_en   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
 
-- ------------------------------------------------------------
-- CATEGORÍAS DE PRODUCTOS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorias (
  id     INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL UNIQUE
);
 
-- ------------------------------------------------------------
-- PROVEEDORES
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS proveedores (
  id        INT AUTO_INCREMENT PRIMARY KEY,
  nombre    VARCHAR(150) NOT NULL,
  contacto  VARCHAR(100),
  telefono  VARCHAR(20),
  correo    VARCHAR(150),
  direccion VARCHAR(255)
);
 
-- ------------------------------------------------------------
-- PRODUCTOS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS productos (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  codigo         VARCHAR(30)  NOT NULL UNIQUE,
  nombre         VARCHAR(150) NOT NULL,
  descripcion    TEXT,
  categoria_id   INT,
  proveedor_id   INT,
  precio         DECIMAL(10,2) NOT NULL,
  presentacion   ENUM('50ml','80ml','100ml','otro') DEFAULT '50ml',
  stock          INT NOT NULL DEFAULT 0,
  stock_minimo   INT NOT NULL DEFAULT 5,
  imagen_url     VARCHAR(255),
  activo         TINYINT(1) NOT NULL DEFAULT 1,
  creado_en      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
  FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE SET NULL
);
 
-- ------------------------------------------------------------
-- PEDIDOS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pedidos (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  cliente_id  INT NOT NULL,
  vendedor_id INT,
  estado      ENUM('pendiente','enviado','entregado','cancelado') NOT NULL DEFAULT 'pendiente',
  total       DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  creado_en   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cliente_id)  REFERENCES usuarios(id),
  FOREIGN KEY (vendedor_id) REFERENCES usuarios(id)
);
 
-- ------------------------------------------------------------
-- DETALLE DE PEDIDOS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS detalle_pedido (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  pedido_id   INT NOT NULL,
  producto_id INT NOT NULL,
  cantidad    INT NOT NULL,
  precio_unit DECIMAL(10,2) NOT NULL,
  subtotal    DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unit) STORED,
  FOREIGN KEY (pedido_id)   REFERENCES pedidos(id)  ON DELETE CASCADE,
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);
 
-- ------------------------------------------------------------
-- VENTAS  (factura generada al completar un pedido)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ventas (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  pedido_id       INT NOT NULL UNIQUE,
  numero_factura  VARCHAR(30) NOT NULL UNIQUE,
  total           DECIMAL(10,2) NOT NULL,
  fecha_venta     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);
 
-- ------------------------------------------------------------
-- ÓRDENES DE COMPRA  (gerente → proveedor)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ordenes_compra (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  proveedor_id  INT NOT NULL,
  gerente_id    INT NOT NULL,
  estado        ENUM('enviada','validada','recibida') NOT NULL DEFAULT 'enviada',
  total         DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  creado_en     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
  FOREIGN KEY (gerente_id)   REFERENCES usuarios(id)
);
 
-- ------------------------------------------------------------
-- DETALLE DE ORDEN DE COMPRA
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS detalle_orden (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  orden_id      INT NOT NULL,
  producto_id   INT NOT NULL,
  cantidad      INT NOT NULL,
  precio_unit   DECIMAL(10,2) NOT NULL,
  subtotal      DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unit) STORED,
  FOREIGN KEY (orden_id)    REFERENCES ordenes_compra(id) ON DELETE CASCADE,
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);
 
-- ------------------------------------------------------------
-- DATOS DE PRUEBA
-- ------------------------------------------------------------
INSERT INTO categorias (nombre) VALUES ('Floral'),('Oriental'),('Cítrico'),('Amaderado');
 
INSERT INTO proveedores (nombre, contacto, correo) VALUES
  ('Fragrance World', 'Carlos Pérez', 'carlos@fworld.com'),
  ('AromaSur',        'Lucía Ríos',  'lucia@aromasur.com');
 
-- Contraseñas: todas son "Admin123" hasheadas con bcrypt
INSERT INTO usuarios (nombre, correo, contrasena, rol) VALUES
  ('Gerente Admin',  'gerente@perfumeria.com',  '$2b$12$KIx2P3z7QwRtUvMnYlXeJOQh5fA8sD1gT6kWpB0cNqHmEuVyLwOiS', 'gerente'),
  ('Vendedor Juan',  'vendedor@perfumeria.com', '$2b$12$KIx2P3z7QwRtUvMnYlXeJOQh5fA8sD1gT6kWpB0cNqHmEuVyLwOiS', 'vendedor'),
  ('Cliente María',  'cliente@perfumeria.com',  '$2b$12$KIx2P3z7QwRtUvMnYlXeJOQh5fA8sD1gT6kWpB0cNqHmEuVyLwOiS', 'cliente');
 
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, precio, presentacion, stock, stock_minimo) VALUES
  ('PF-001', 'Rose Élite',    'Fragancia floral intensa con notas de rosa y jazmín', 1, 1, 89.90,  '50ml', 20, 5),
  ('PF-002', 'Oud Mystique',  'Aroma oriental profundo con notas de oud y vainilla',  2, 1, 120.00, '80ml', 15, 5),
  ('PF-003', 'Citrus Fresh',  'Fragancia cítrica fresca ideal para el día',            3, 2, 65.00,  '50ml', 30, 5),
  ('PF-004', 'Cedar & Wood',  'Notas amaderadas de cedro y sándalo',                  4, 2, 95.50,  '80ml', 8,  5);