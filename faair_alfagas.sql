-- =====================================================================
-- FAAIR – Alfa Gas · Script Completo (DDL + Datos Iniciales Aguascalientes)
-- =====================================================================

DROP DATABASE IF EXISTS faair_alfa_gas;
CREATE DATABASE faair_alfa_gas
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE faair_alfa_gas;

-- ---------------------------------------------------------------------
-- 1. Catálogos Geográficos
-- ---------------------------------------------------------------------

CREATE TABLE entidad_federativa (
  id_entidad_fede INT NOT NULL AUTO_INCREMENT,
  clave_entidad_fede CHAR(3) NOT NULL,
  nombre_entidad_fede VARCHAR(60) NOT NULL,
  PRIMARY KEY (id_entidad_fede),
  UNIQUE KEY uk_entidad_clave (clave_entidad_fede),
  UNIQUE KEY uk_entidad_nombre (nombre_entidad_fede)
) ENGINE=InnoDB;

CREATE TABLE municipio (
  id_municipio INT NOT NULL AUTO_INCREMENT,
  id_entidad_fede INT NOT NULL,
  nombre_municipio VARCHAR(80) NOT NULL,
  PRIMARY KEY (id_municipio),
  CONSTRAINT fk_municipio_entidad
    FOREIGN KEY (id_entidad_fede) REFERENCES entidad_federativa (id_entidad_fede)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE colonia (
  id_colonia INT NOT NULL AUTO_INCREMENT,
  id_municipio INT NOT NULL,
  nombre_colonia VARCHAR(100) NOT NULL,
  codigo_postal CHAR(5) NOT NULL,
  PRIMARY KEY (id_colonia),
  CONSTRAINT fk_colonia_municipio
    FOREIGN KEY (id_municipio) REFERENCES municipio (id_municipio)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- 2. Sucursales y Usuarios
-- ---------------------------------------------------------------------

CREATE TABLE sucursal (
  id_sucursal INT NOT NULL AUTO_INCREMENT,
  clave_sucursal CHAR(3) NOT NULL,
  nombre_sucursal VARCHAR(80) NOT NULL,
  id_municipio_sede INT NOT NULL,
  telefono_whatsapp VARCHAR(10) NULL,
  activa_sucursal TINYINT(1) NOT NULL DEFAULT 1,
  fecha_creacion_sucursal DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_sucursal),
  UNIQUE KEY uk_sucursal_clave (clave_sucursal),
  UNIQUE KEY uk_sucursal_whatsapp (telefono_whatsapp),
  CONSTRAINT fk_sucursal_municipio
    FOREIGN KEY (id_municipio_sede) REFERENCES municipio (id_municipio)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE administrador (
  id_adm INT NOT NULL AUTO_INCREMENT,
  id_sucursal INT NULL COMMENT 'NULL = acceso a todas las sucursales',
  nombre_adm VARCHAR(150) NOT NULL,
  correo_adm VARCHAR(120) NULL,
  numero_adm VARCHAR(16) NOT NULL,
  nombre_usuario_adm VARCHAR(20) NOT NULL,
  password VARCHAR(255) NOT NULL,
  activo_adm TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (id_adm),
  UNIQUE KEY uk_adm_correo (correo_adm),
  UNIQUE KEY uk_adm_numero (numero_adm),
  UNIQUE KEY uk_adm_usuario (nombre_usuario_adm),
  CONSTRAINT fk_administrador_sucursal
    FOREIGN KEY (id_sucursal) REFERENCES sucursal (id_sucursal)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE cliente (
  id_cliente INT NOT NULL AUTO_INCREMENT,
  id_sucursal INT NOT NULL,
  nombre_cliente VARCHAR(150) NOT NULL,
  telefono_whatsapp_cliente VARCHAR(10) NOT NULL,
  estado_cliente ENUM('PENDIENTE_REGISTRO', 'ACTIVO', 'INACTIVO', 'BAJA') NOT NULL DEFAULT 'PENDIENTE_REGISTRO',
  acepta_notificaciones TINYINT(1) NOT NULL DEFAULT 0,
  fecha_registro_cliente DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_cliente),
  UNIQUE KEY uk_cliente_whatsapp (telefono_whatsapp_cliente),
  CONSTRAINT fk_cliente_sucursal
    FOREIGN KEY (id_sucursal) REFERENCES sucursal (id_sucursal)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE direccion (
  id_direccion INT NOT NULL AUTO_INCREMENT,
  id_colonia INT NOT NULL,
  id_cliente INT NOT NULL,
  direccion_recurrente_cliente TINYINT(1) NOT NULL DEFAULT 0,
  id_cliente_activo INT GENERATED ALWAYS AS (IF(direccion_recurrente_cliente = 1, id_cliente, NULL)) VIRTUAL,
  calle VARCHAR(100) NOT NULL,
  num_exterior VARCHAR(10) NOT NULL,
  num_interior VARCHAR(10) NULL,
  referencias VARCHAR(255) NULL,
  fecha_creacion_direccion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_direccion),
  INDEX idx_direccion_cliente_recurrente (id_cliente, direccion_recurrente_cliente),
  UNIQUE KEY uk_cliente_direccion_activa (id_cliente_activo),
  CONSTRAINT fk_direccion_colonia
    FOREIGN KEY (id_colonia) REFERENCES colonia (id_colonia)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_direccion_cliente
    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- 3. Productos y Precios
-- ---------------------------------------------------------------------

CREATE TABLE producto (
  id_producto INT NOT NULL AUTO_INCREMENT,
  codigo_producto VARCHAR(8) NOT NULL,
  nombre_producto VARCHAR(50) NOT NULL,
  tipo_producto ENUM('GAS_ESTACIONARIO', 'CILINDRO_PORTATIL') NOT NULL COMMENT 'GAS_ESTACIONARIO = se vende por litro; CILINDRO_PORTATIL = por pieza',
  capacidad_kg DECIMAL(5,2) NULL COMMENT 'Solo para cilindros',
  activo_producto TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (id_producto),
  UNIQUE KEY uk_producto_codigo (codigo_producto)
) ENGINE=InnoDB;

CREATE TABLE precio_producto (
  id_precio INT NOT NULL AUTO_INCREMENT,
  id_producto INT NOT NULL,
  precio_producto DECIMAL(8,2) NOT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NULL COMMENT 'NULL = precio vigente',
  id_adm INT NULL,
  fecha_creacion_productos DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_precio),
  CONSTRAINT fk_precio_producto
    FOREIGN KEY (id_producto) REFERENCES producto (id_producto)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_precio_adm
    FOREIGN KEY (id_adm) REFERENCES administrador (id_adm)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- 4. Pedidos, Predicciones y Notificaciones
-- ---------------------------------------------------------------------

CREATE TABLE pedido (
  id_pedido INT NOT NULL AUTO_INCREMENT,
  folio VARCHAR(20) NOT NULL,
  id_cliente INT NOT NULL,
  id_sucursal INT NOT NULL,
  id_direccion_entrega INT NOT NULL,
  id_producto INT NOT NULL,
  id_precio INT NOT NULL,
  cantidad_litros DECIMAL(9,2) NOT NULL,
  total_pedido DECIMAL(11,2) NOT NULL DEFAULT 0.00,
  estado_pedido ENUM('REGISTRADO', 'ENTREGADO', 'CANCELADO', 'FALLIDO') NOT NULL DEFAULT 'REGISTRADO',
  origen_pedido ENUM('WHATSAPP', 'ADMIN') NOT NULL DEFAULT 'WHATSAPP',
  fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_entrega_real DATETIME NULL,
  fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_pedido),
  UNIQUE KEY uk_pedido_folio (folio),
  CONSTRAINT chk_pedido_cantidad_positiva CHECK (cantidad_litros > 0),
  CONSTRAINT fk_pedido_cliente
    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_pedido_sucursal
    FOREIGN KEY (id_sucursal) REFERENCES sucursal (id_sucursal)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_pedido_direccion
    FOREIGN KEY (id_direccion_entrega) REFERENCES direccion (id_direccion)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_pedido_producto
    FOREIGN KEY (id_producto) REFERENCES producto (id_producto)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_pedido_precio
    FOREIGN KEY (id_precio) REFERENCES precio_producto (id_precio)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE prediccion (
  id_prediccion INT NOT NULL AUTO_INCREMENT,
  id_cliente INT NOT NULL,
  id_producto INT NOT NULL,
  fecha_calculo DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  cantidad_pedidos_base TINYINT NOT NULL,
  promedio_dias_consumo DECIMAL(6,2) NOT NULL,
  fecha_ultimo_ped DATE NOT NULL,
  fecha_estimada_agotamiento DATE NOT NULL,
  fecha_recordatorio DATE NULL,
  cantidad_estimada DECIMAL(9,2) NULL,
  probabilidad DECIMAL(5,2) NULL,
  vigente TINYINT(1) NOT NULL DEFAULT 1,
  id_pedido_resultado INT NULL,
  dias_diferecia SMALLINT NULL,
  PRIMARY KEY (id_prediccion),
  INDEX idx_prediccion_vigente_cliente (vigente, id_cliente),
  CONSTRAINT fk_prediccion_cliente
    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_prediccion_producto
    FOREIGN KEY (id_producto) REFERENCES producto (id_producto)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_prediccion_pedido_resultado
    FOREIGN KEY (id_pedido_resultado) REFERENCES pedido (id_pedido)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE notificacion (
  id_notificacion BIGINT NOT NULL AUTO_INCREMENT,
  id_cliente INT NOT NULL,
  id_prediccion INT NULL,
  id_pedido INT NULL,
  tipo_notificacion ENUM('RECORDATORIO', 'CONFIRMACION_PEDIDO') NOT NULL,
  id_notificacion_origen BIGINT NULL COMMENT 'Primer envío, en caso de reintento',
  numero_intento TINYINT NOT NULL DEFAULT 1,
  estado_envio ENUM('PENDIENTE', 'ENVIADO', 'ENTREGADO', 'LEIDO', 'FALLIDO') NOT NULL DEFAULT 'PENDIENTE',
  resultado_notificacion ENUM('SIN_RESPUESTA', 'ACEPTO', 'RECHAZO') NOT NULL DEFAULT 'SIN_RESPUESTA',
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_notificacion),
  CONSTRAINT fk_notificacion_cliente
    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_notificacion_prediccion
    FOREIGN KEY (id_prediccion) REFERENCES prediccion (id_prediccion)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_notificacion_pedido
    FOREIGN KEY (id_pedido) REFERENCES pedido (id_pedido)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_notificacion_origen
    FOREIGN KEY (id_notificacion_origen) REFERENCES notificacion (id_notificacion)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- 5. Triggers para cálculo automático de total_pedido
-- ---------------------------------------------------------------------

DELIMITER $$

CREATE TRIGGER trg_pedido_bi_total
BEFORE INSERT ON pedido
FOR EACH ROW
BEGIN
  DECLARE v_precio DECIMAL(8,2);

  SELECT precio_producto INTO v_precio
  FROM precio_producto
  WHERE id_precio = NEW.id_precio;

  SET NEW.total_pedido = NEW.cantidad_litros * v_precio;
END$$

CREATE TRIGGER trg_pedido_bu_total
BEFORE UPDATE ON pedido
FOR EACH ROW
BEGIN
  DECLARE v_precio DECIMAL(8,2);

  IF NEW.cantidad_litros <> OLD.cantidad_litros OR NEW.id_precio <> OLD.id_precio THEN
    SELECT precio_producto INTO v_precio
    FROM precio_producto
    WHERE id_precio = NEW.id_precio;

    SET NEW.total_pedido = NEW.cantidad_litros * v_precio;
  END IF;
END$$

DELIMITER ;

-- ---------------------------------------------------------------------
-- 6. Datos Iniciales (Aguascalientes, Colonias, Sucursal, Producto y Admin)
-- ---------------------------------------------------------------------

INSERT INTO entidad_federativa (clave_entidad_fede, nombre_entidad_fede)
VALUES ('AGS', 'Aguascalientes');

INSERT INTO municipio (id_entidad_fede, nombre_municipio)
VALUES (1, 'Aguascalientes');

INSERT INTO colonia (id_municipio, nombre_colonia, codigo_postal)
VALUES 
  (1, 'Casa Blanca', '20190'),
  (1, 'Zona Centro', '20000'),
  (1, 'Jardines de la Asunción', '20270'),
  (1, 'Bosques del Prado Norte', '20130');

INSERT INTO sucursal (clave_sucursal, nombre_sucursal, id_municipio_sede, telefono_whatsapp, activa_sucursal)
VALUES ('S01', 'Sucursal Matriz Aguascalientes', 1, '4490000000', 1);

INSERT INTO administrador (id_sucursal, nombre_adm, correo_adm, numero_adm, nombre_usuario_adm, password, activo_adm)
VALUES (NULL, 'Administrador General', 'admin@alfagas.com', '4491234567', 'admin', '1236', 1);

INSERT INTO producto (codigo_producto, nombre_producto, tipo_producto, activo_producto)
VALUES ('GLP-01', 'Gas LP Estacionario', 'GAS_ESTACIONARIO', 1);

INSERT INTO precio_producto (id_producto, precio_producto, fecha_inicio, fecha_fin, id_adm)
VALUES (1, 10.50, CURDATE(), NULL, 1);