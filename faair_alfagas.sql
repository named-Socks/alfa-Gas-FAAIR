-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 22-11-2026 a las 22:08:53
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `faair_alfa_gas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `id_adm` int(11) NOT NULL,
  `id_sucursal` int(11) DEFAULT NULL COMMENT 'NULL = acceso a todas las sucursales',
  `nombre_adm` varchar(150) NOT NULL,
  `correo_adm` varchar(120) DEFAULT NULL,
  `numero_adm` varchar(16) NOT NULL,
  `nombre_usuario_adm` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `activo_adm` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`id_adm`, `id_sucursal`, `nombre_adm`, `correo_adm`, `numero_adm`, `nombre_usuario_adm`, `password`, `activo_adm`) VALUES
(1, NULL, 'Administrador General', 'admin@alfagas.com', '4491234567', 'admin', '$2b$12$q8RKvmbX5y.anT0RUDQcyOQL1tTt.zUErxWkcSFm.xKIYEIQ5Tec.', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` int(11) NOT NULL,
  `id_sucursal` int(11) NOT NULL,
  `nombre_cliente` varchar(150) NOT NULL,
  `telefono_whatsapp_cliente` varchar(10) NOT NULL,
  `estado_cliente` enum('PENDIENTE_REGISTRO','ACTIVO','INACTIVO','BAJA') NOT NULL DEFAULT 'PENDIENTE_REGISTRO',
  `acepta_notificaciones` tinyint(1) NOT NULL DEFAULT 0,
  `fecha_registro_cliente` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `id_sucursal`, `nombre_cliente`, `telefono_whatsapp_cliente`, `estado_cliente`, `acepta_notificaciones`, `fecha_registro_cliente`) VALUES
(1, 1, 'Juan Pérez López', '4491112233', 'ACTIVO', 0, '2026-11-18 21:19:22'),
(2, 1, 'María Fernanda Ruiz', '4494445566', 'ACTIVO', 0, '2026-11-18 21:19:22'),
(3, 1, 'Carlos Ramírez', '4493334455', 'ACTIVO', 1, '2026-11-19 09:53:58'),
(4, 1, 'Tortillería El Sol', '4492223344', 'ACTIVO', 1, '2026-11-19 10:07:21');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `colonia`
--

CREATE TABLE `colonia` (
  `id_colonia` int(11) NOT NULL,
  `id_municipio` int(11) NOT NULL,
  `nombre_colonia` varchar(100) NOT NULL,
  `codigo_postal` char(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `colonia`
--

INSERT INTO `colonia` (`id_colonia`, `id_municipio`, `nombre_colonia`, `codigo_postal`) VALUES
(1, 1, 'Casa Blanca', '20190'),
(2, 1, 'Zona Centro', '20000'),
(3, 1, 'Jardines de la Asunción', '20270'),
(4, 1, 'Bosques del Prado Norte', '20130');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_pedido`
--

CREATE TABLE `detalle_pedido` (
  `id_detalle_pedido` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `id_precio` int(11) NOT NULL,
  `cantidad_litros` decimal(9,2) NOT NULL,
  `precio_unitario` decimal(8,2) NOT NULL,
  `subtotal` decimal(11,2) NOT NULL DEFAULT 0.00
) ;

--
-- Volcado de datos para la tabla `detalle_pedido`
--

INSERT INTO `detalle_pedido` (`id_detalle_pedido`, `id_pedido`, `id_producto`, `id_precio`, `cantidad_litros`, `precio_unitario`, `subtotal`) VALUES
(1, 1, 1, 1, 120.00, 10.50, 1260.00),
(2, 2, 1, 1, 85.00, 10.50, 892.50),
(3, 4, 1, 1, 120.00, 10.50, 1260.00),
(4, 5, 1, 1, 150.00, 10.50, 1575.00),
(5, 6, 1, 1, 200.00, 10.50, 2100.00),
(6, 7, 1, 1, 100.00, 10.50, 1050.00),
(7, 8, 1, 1, 300.00, 10.50, 3150.00);

--
-- Disparadores `detalle_pedido`
--
DELIMITER $$
CREATE TRIGGER `trg_detalle_pedido_ad` AFTER DELETE ON `detalle_pedido` FOR EACH ROW BEGIN
  UPDATE pedido
  SET total_pedido = (
    SELECT COALESCE(SUM(subtotal), 0.00)
    FROM detalle_pedido
    WHERE id_pedido = OLD.id_pedido
  )
  WHERE id_pedido = OLD.id_pedido;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_detalle_pedido_ai` AFTER INSERT ON `detalle_pedido` FOR EACH ROW BEGIN
  UPDATE pedido
  SET total_pedido = (
    SELECT COALESCE(SUM(subtotal), 0.00)
    FROM detalle_pedido
    WHERE id_pedido = NEW.id_pedido
  )
  WHERE id_pedido = NEW.id_pedido;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_detalle_pedido_au` AFTER UPDATE ON `detalle_pedido` FOR EACH ROW BEGIN
  UPDATE pedido
  SET total_pedido = (
    SELECT COALESCE(SUM(subtotal), 0.00)
    FROM detalle_pedido
    WHERE id_pedido = NEW.id_pedido
  )
  WHERE id_pedido = NEW.id_pedido;

  IF OLD.id_pedido <> NEW.id_pedido THEN
    UPDATE pedido
    SET total_pedido = (
      SELECT COALESCE(SUM(subtotal), 0.00)
      FROM detalle_pedido
      WHERE id_pedido = OLD.id_pedido
    )
    WHERE id_pedido = OLD.id_pedido;
  END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_detalle_pedido_bi` BEFORE INSERT ON `detalle_pedido` FOR EACH ROW BEGIN
  DECLARE v_precio DECIMAL(8,2);

  SELECT precio_producto INTO v_precio
  FROM precio_producto
  WHERE id_precio = NEW.id_precio;

  IF NEW.precio_unitario IS NULL OR NEW.precio_unitario <= 0 THEN
    SET NEW.precio_unitario = v_precio;
  END IF;

  SET NEW.subtotal = ROUND(NEW.cantidad_litros * NEW.precio_unitario, 2);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_detalle_pedido_bu` BEFORE UPDATE ON `detalle_pedido` FOR EACH ROW BEGIN
  DECLARE v_precio DECIMAL(8,2);

  IF NEW.id_precio <> OLD.id_precio THEN
    SELECT precio_producto INTO v_precio
    FROM precio_producto
    WHERE id_precio = NEW.id_precio;
    SET NEW.precio_unitario = v_precio;
  END IF;

  SET NEW.subtotal = ROUND(NEW.cantidad_litros * NEW.precio_unitario, 2);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `direccion`
--

CREATE TABLE `direccion` (
  `id_direccion` int(11) NOT NULL,
  `id_colonia` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `direccion_recurrente_cliente` tinyint(1) NOT NULL DEFAULT 0,
  `id_cliente_activo` int(11) GENERATED ALWAYS AS (if(`direccion_recurrente_cliente` = 1,`id_cliente`,NULL)) VIRTUAL,
  `calle` varchar(100) NOT NULL,
  `num_exterior` varchar(10) NOT NULL,
  `num_interior` varchar(10) DEFAULT NULL,
  `referencias` varchar(255) DEFAULT NULL,
  `fecha_creacion_direccion` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `direccion`
--

INSERT INTO `direccion` (`id_direccion`, `id_colonia`, `id_cliente`, `direccion_recurrente_cliente`, `calle`, `num_exterior`, `num_interior`, `referencias`, `fecha_creacion_direccion`) VALUES
(1, 1, 1, 1, 'Av. Aguascalientes', '104', NULL, NULL, '2026-11-18 21:19:22'),
(2, 2, 2, 1, 'Calle Madero', '318', NULL, NULL, '2026-11-18 21:19:22'),
(4, 2, 2, 0, 'Calle General Ignacio Zaragoza', '304', NULL, 'Fachada amarilla', '2026-11-19 09:53:58'),
(5, 3, 3, 1, 'Boulevard José María Chávez', '1520', NULL, 'Esquina con segundo anillo', '2026-11-19 09:53:58'),
(6, 4, 4, 1, 'Avenida Universidad', '810', NULL, 'Frente al parque', '2026-11-19 10:07:21');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entidad_federativa`
--

CREATE TABLE `entidad_federativa` (
  `id_entidad_fede` int(11) NOT NULL,
  `clave_entidad_fede` char(3) NOT NULL,
  `nombre_entidad_fede` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `entidad_federativa`
--

INSERT INTO `entidad_federativa` (`id_entidad_fede`, `clave_entidad_fede`, `nombre_entidad_fede`) VALUES
(1, 'AGS', 'Aguascalientes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `municipio`
--

CREATE TABLE `municipio` (
  `id_municipio` int(11) NOT NULL,
  `id_entidad_fede` int(11) NOT NULL,
  `nombre_municipio` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `municipio`
--

INSERT INTO `municipio` (`id_municipio`, `id_entidad_fede`, `nombre_municipio`) VALUES
(1, 1, 'Aguascalientes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificacion`
--

CREATE TABLE `notificacion` (
  `id_notificacion` bigint(20) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_prediccion` int(11) DEFAULT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `tipo_notificacion` enum('RECORDATORIO','CONFIRMACION_PEDIDO') NOT NULL,
  `id_notificacion_origen` bigint(20) DEFAULT NULL COMMENT 'Primer envío, en caso de reintento',
  `numero_intento` tinyint(4) NOT NULL DEFAULT 1,
  `estado_envio` enum('PENDIENTE','ENVIADO','ENTREGADO','LEIDO','FALLIDO') NOT NULL DEFAULT 'PENDIENTE',
  `resultado_notificacion` enum('SIN_RESPUESTA','ACEPTO','RECHAZO') NOT NULL DEFAULT 'SIN_RESPUESTA',
  `fecha_creacion` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `id_pedido` int(11) NOT NULL,
  `folio` varchar(20) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_sucursal` int(11) NOT NULL,
  `id_direccion_entrega` int(11) NOT NULL,
  `total_pedido` decimal(11,2) NOT NULL DEFAULT 0.00,
  `metodo_pago` enum('EFECTIVO','TARJETA') NOT NULL DEFAULT 'EFECTIVO',
  `estado_pedido` enum('REGISTRADO','ENTREGADO','CANCELADO','FALLIDO') NOT NULL DEFAULT 'REGISTRADO',
  `origen_pedido` enum('WHATSAPP','ADMIN') NOT NULL DEFAULT 'WHATSAPP',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp(),
  `fecha_entrega_real` datetime DEFAULT NULL,
  `fecha_actualizacion` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `pedido`
--

INSERT INTO `pedido` (`id_pedido`, `folio`, `id_cliente`, `id_sucursal`, `id_direccion_entrega`, `total_pedido`, `metodo_pago`, `estado_pedido`, `origen_pedido`, `fecha_registro`, `fecha_entrega_real`, `fecha_actualizacion`) VALUES
(1, 'PED-0001', 1, 1, 1, 1260.00, 'EFECTIVO', 'REGISTRADO', 'WHATSAPP', '2026-11-18 21:19:22', NULL, '2026-11-18 21:19:22'),
(2, 'PED-0002', 2, 1, 2, 892.50, 'TARJETA', 'CANCELADO', 'ADMIN', '2026-11-18 21:19:22', '2026-11-18 21:20:39', '2026-11-19 09:45:42'),
(4, 'PED-004', 3, 1, 5, 1260.00, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-17 09:53:58', '2026-11-17 09:53:58', '2026-11-19 09:53:58'),
(5, 'PED-0005', 1, 1, 1, 1575.00, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-18 10:30:00', '2026-11-18 11:15:00', '2026-11-19 10:07:21'),
(6, 'PED-0006', 2, 1, 2, 2100.00, 'TARJETA', 'ENTREGADO', 'ADMIN', '2026-11-18 14:00:00', '2026-11-18 14:40:00', '2026-11-19 10:07:21'),
(7, 'PED-0007', 2, 1, 4, 1050.00, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-19 08:20:00', '2026-11-19 09:00:00', '2026-11-19 10:07:21'),
(8, 'PED-0008', 4, 1, 6, 3150.00, 'TARJETA', 'ENTREGADO', 'ADMIN', '2026-11-19 09:10:00', '2026-11-19 09:50:00', '2026-11-19 10:07:21');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `precio_producto`
--

CREATE TABLE `precio_producto` (
  `id_precio` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `precio_producto` decimal(8,2) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL COMMENT 'NULL = precio vigente',
  `id_adm` int(11) DEFAULT NULL,
  `fecha_creacion_productos` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `precio_producto`
--

INSERT INTO `precio_producto` (`id_precio`, `id_producto`, `precio_producto`, `fecha_inicio`, `fecha_fin`, `id_adm`, `fecha_creacion_productos`) VALUES
(1, 1, 10.50, '2026-11-18', '2026-11-21', 1, '2026-11-18 21:19:22'),
(2, 1, 11.67, '2026-11-22', NULL, 1, '2026-11-22 14:09:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prediccion`
--

CREATE TABLE `prediccion` (
  `id_prediccion` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `fecha_calculo` datetime NOT NULL DEFAULT current_timestamp(),
  `cantidad_pedidos_base` tinyint(4) NOT NULL,
  `promedio_dias_consumo` decimal(6,2) NOT NULL,
  `fecha_ultimo_ped` date NOT NULL,
  `fecha_estimada_agotamiento` date NOT NULL,
  `fecha_recordatorio` date DEFAULT NULL,
  `cantidad_estimada` decimal(9,2) DEFAULT NULL,
  `probabilidad` decimal(5,2) DEFAULT NULL,
  `vigente` tinyint(1) NOT NULL DEFAULT 1,
  `id_pedido_resultado` int(11) DEFAULT NULL,
  `dias_diferecia` smallint(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id_producto` int(11) NOT NULL,
  `codigo_producto` varchar(8) NOT NULL,
  `nombre_producto` varchar(50) NOT NULL,
  `tipo_producto` enum('GAS_ESTACIONARIO','CILINDRO_PORTATIL') NOT NULL COMMENT 'GAS_ESTACIONARIO = se vende por litro; CILINDRO_PORTATIL = por pieza',
  `capacidad_kg` decimal(5,2) DEFAULT NULL COMMENT 'Solo para cilindros',
  `activo_producto` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id_producto`, `codigo_producto`, `nombre_producto`, `tipo_producto`, `capacidad_kg`, `activo_producto`) VALUES
(1, 'GLP-01', 'Gas LP Estacionario', 'GAS_ESTACIONARIO', NULL, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursal`
--

CREATE TABLE `sucursal` (
  `id_sucursal` int(11) NOT NULL,
  `clave_sucursal` char(3) NOT NULL,
  `nombre_sucursal` varchar(80) NOT NULL,
  `id_municipio_sede` int(11) NOT NULL,
  `telefono_whatsapp` varchar(10) DEFAULT NULL,
  `activa_sucursal` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_creacion_sucursal` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `sucursal`
--

INSERT INTO `sucursal` (`id_sucursal`, `clave_sucursal`, `nombre_sucursal`, `id_municipio_sede`, `telefono_whatsapp`, `activa_sucursal`, `fecha_creacion_sucursal`) VALUES
(1, 'S01', 'Sucursal Matriz Aguascalientes', 1, '4490000000', 1, '2026-11-18 21:19:22');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`id_adm`),
  ADD UNIQUE KEY `uk_adm_numero` (`numero_adm`),
  ADD UNIQUE KEY `uk_adm_usuario` (`nombre_usuario_adm`),
  ADD UNIQUE KEY `uk_adm_correo` (`correo_adm`),
  ADD KEY `fk_administrador_sucursal` (`id_sucursal`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `uk_cliente_whatsapp` (`telefono_whatsapp_cliente`),
  ADD KEY `fk_cliente_sucursal` (`id_sucursal`);

--
-- Indices de la tabla `colonia`
--
ALTER TABLE `colonia`
  ADD PRIMARY KEY (`id_colonia`),
  ADD KEY `fk_colonia_municipio` (`id_municipio`);

--
-- Indices de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD PRIMARY KEY (`id_detalle_pedido`),
  ADD KEY `fk_detalle_pedido` (`id_pedido`),
  ADD KEY `fk_detalle_producto` (`id_producto`),
  ADD KEY `fk_detalle_precio` (`id_precio`);

--
-- Indices de la tabla `direccion`
--
ALTER TABLE `direccion`
  ADD PRIMARY KEY (`id_direccion`),
  ADD UNIQUE KEY `uk_cliente_direccion_activa` (`id_cliente_activo`),
  ADD KEY `idx_direccion_cliente_recurrente` (`id_cliente`,`direccion_recurrente_cliente`),
  ADD KEY `fk_direccion_colonia` (`id_colonia`);

--
-- Indices de la tabla `entidad_federativa`
--
ALTER TABLE `entidad_federativa`
  ADD PRIMARY KEY (`id_entidad_fede`),
  ADD UNIQUE KEY `uk_entidad_clave` (`clave_entidad_fede`),
  ADD UNIQUE KEY `uk_entidad_nombre` (`nombre_entidad_fede`);

--
-- Indices de la tabla `municipio`
--
ALTER TABLE `municipio`
  ADD PRIMARY KEY (`id_municipio`),
  ADD KEY `fk_municipio_entidad` (`id_entidad_fede`);

--
-- Indices de la tabla `notificacion`
--
ALTER TABLE `notificacion`
  ADD PRIMARY KEY (`id_notificacion`),
  ADD KEY `fk_notificacion_cliente` (`id_cliente`),
  ADD KEY `fk_notificacion_prediccion` (`id_prediccion`),
  ADD KEY `fk_notificacion_pedido` (`id_pedido`),
  ADD KEY `fk_notificacion_origen` (`id_notificacion_origen`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id_pedido`),
  ADD UNIQUE KEY `uk_pedido_folio` (`folio`),
  ADD KEY `fk_pedido_cliente` (`id_cliente`),
  ADD KEY `fk_pedido_sucursal` (`id_sucursal`),
  ADD KEY `fk_pedido_direccion` (`id_direccion_entrega`);

--
-- Indices de la tabla `precio_producto`
--
ALTER TABLE `precio_producto`
  ADD PRIMARY KEY (`id_precio`),
  ADD KEY `fk_precio_producto` (`id_producto`),
  ADD KEY `fk_precio_adm` (`id_adm`);

--
-- Indices de la tabla `prediccion`
--
ALTER TABLE `prediccion`
  ADD PRIMARY KEY (`id_prediccion`),
  ADD KEY `idx_prediccion_vigente_cliente` (`vigente`,`id_cliente`),
  ADD KEY `fk_prediccion_cliente` (`id_cliente`),
  ADD KEY `fk_prediccion_producto` (`id_producto`),
  ADD KEY `fk_prediccion_pedido_resultado` (`id_pedido_resultado`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_producto`),
  ADD UNIQUE KEY `uk_producto_codigo` (`codigo_producto`);

--
-- Indices de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  ADD PRIMARY KEY (`id_sucursal`),
  ADD UNIQUE KEY `uk_sucursal_clave` (`clave_sucursal`),
  ADD UNIQUE KEY `uk_sucursal_whatsapp` (`telefono_whatsapp`),
  ADD KEY `fk_sucursal_municipio` (`id_municipio_sede`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `id_adm` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `colonia`
--
ALTER TABLE `colonia`
  MODIFY `id_colonia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id_detalle_pedido` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `direccion`
--
ALTER TABLE `direccion`
  MODIFY `id_direccion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `entidad_federativa`
--
ALTER TABLE `entidad_federativa`
  MODIFY `id_entidad_fede` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `municipio`
--
ALTER TABLE `municipio`
  MODIFY `id_municipio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `notificacion`
--
ALTER TABLE `notificacion`
  MODIFY `id_notificacion` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `precio_producto`
--
ALTER TABLE `precio_producto`
  MODIFY `id_precio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `prediccion`
--
ALTER TABLE `prediccion`
  MODIFY `id_prediccion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  MODIFY `id_sucursal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD CONSTRAINT `fk_administrador_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `fk_cliente_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `colonia`
--
ALTER TABLE `colonia`
  ADD CONSTRAINT `fk_colonia_municipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD CONSTRAINT `fk_detalle_pedido` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_detalle_precio` FOREIGN KEY (`id_precio`) REFERENCES `precio_producto` (`id_precio`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_detalle_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `direccion`
--
ALTER TABLE `direccion`
  ADD CONSTRAINT `fk_direccion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_direccion_colonia` FOREIGN KEY (`id_colonia`) REFERENCES `colonia` (`id_colonia`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `municipio`
--
ALTER TABLE `municipio`
  ADD CONSTRAINT `fk_municipio_entidad` FOREIGN KEY (`id_entidad_fede`) REFERENCES `entidad_federativa` (`id_entidad_fede`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `notificacion`
--
ALTER TABLE `notificacion`
  ADD CONSTRAINT `fk_notificacion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_notificacion_origen` FOREIGN KEY (`id_notificacion_origen`) REFERENCES `notificacion` (`id_notificacion`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_notificacion_pedido` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_notificacion_prediccion` FOREIGN KEY (`id_prediccion`) REFERENCES `prediccion` (`id_prediccion`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `fk_pedido_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pedido_direccion` FOREIGN KEY (`id_direccion_entrega`) REFERENCES `direccion` (`id_direccion`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pedido_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `precio_producto`
--
ALTER TABLE `precio_producto`
  ADD CONSTRAINT `fk_precio_adm` FOREIGN KEY (`id_adm`) REFERENCES `administrador` (`id_adm`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_precio_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `prediccion`
--
ALTER TABLE `prediccion`
  ADD CONSTRAINT `fk_prediccion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_prediccion_pedido_resultado` FOREIGN KEY (`id_pedido_resultado`) REFERENCES `pedido` (`id_pedido`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_prediccion_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `sucursal`
--
ALTER TABLE `sucursal`
  ADD CONSTRAINT `fk_sucursal_municipio` FOREIGN KEY (`id_municipio_sede`) REFERENCES `municipio` (`id_municipio`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
