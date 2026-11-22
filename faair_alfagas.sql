-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 22-11-2026 a las 22:35:08
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
(4, 1, 'Tortillería El Sol', '4492223344', 'ACTIVO', 1, '2026-11-19 10:07:21'),
(21, 1, 'Sofía Hernández Martínez', '4495551001', 'ACTIVO', 1, '2026-11-12 09:15:00'),
(22, 1, 'Diego Alejandro Morales', '4495551002', 'ACTIVO', 1, '2026-11-12 11:30:00'),
(23, 1, 'Valeria Guadalupe Ortiz', '4495551003', 'ACTIVO', 0, '2026-11-13 10:05:00'),
(24, 1, 'Lavandería La Espuma', '4495551004', 'ACTIVO', 1, '2026-11-13 14:20:00'),
(25, 1, 'Roberto Carlos Mendoza', '4495551005', 'ACTIVO', 1, '2026-11-14 08:45:00'),
(26, 1, 'Ana Karen Castillo', '4495551006', 'ACTIVO', 0, '2026-11-14 16:10:00'),
(27, 1, 'Panadería Don Pepe', '4495551007', 'ACTIVO', 1, '2026-11-15 07:50:00'),
(28, 1, 'Luis Enrique Navarro', '4495551008', 'INACTIVO', 0, '2026-11-15 12:00:00'),
(29, 1, 'José Guadalupe López', '3465552001', 'ACTIVO', 1, '2026-11-12 10:15:00'),
(30, 1, 'María Elena Sandoval', '3465552002', 'ACTIVO', 1, '2026-11-12 15:40:00'),
(31, 1, 'Fonda Doña Lupe', '3465552003', 'ACTIVO', 1, '2026-11-13 08:30:00'),
(32, 1, 'Héctor Manuel Gutiérrez', '3465552004', 'ACTIVO', 0, '2026-11-13 17:00:00'),
(33, 1, 'Carmen Alicia Vázquez', '3465552005', 'ACTIVO', 1, '2026-11-14 09:20:00'),
(34, 1, 'Taquería El Fogón', '3465552006', 'ACTIVO', 1, '2026-11-14 19:10:00'),
(35, 1, 'Fernando Rivera Delgado', '3465552007', 'ACTIVO', 0, '2026-11-15 11:05:00'),
(36, 1, 'Patricia Esmeralda Ruiz', '3465552008', 'PENDIENTE_REGISTRO', 1, '2026-11-16 13:25:00');

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
(4, 1, 'Bosques del Prado Norte', '20130'),
(14, 1, 'Lindavista', '20270'),
(15, 1, 'Trojes de Oriente', '20116'),
(16, 1, 'Las Viñas', '20230'),
(17, 1, 'San Marcos', '20070'),
(18, 3, 'Barrio de Analco', '47202'),
(19, 3, 'La Villita', '47204'),
(20, 3, 'Loma Bonita', '47205'),
(21, 3, 'El Santuario', '47203'),
(22, 3, 'Centro Teocaltiche', '47200');

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
(7, 8, 1, 1, 300.00, 10.50, 3150.00),
(10, 46, 1, 2, 90.00, 11.67, 1050.30),
(11, 48, 1, 2, 140.00, 11.67, 1633.80),
(12, 50, 1, 2, 110.00, 11.67, 1283.70),
(13, 52, 1, 2, 260.00, 11.67, 3034.20),
(14, 53, 1, 2, 130.00, 11.67, 1517.10),
(15, 54, 1, 2, 95.00, 11.67, 1108.65),
(16, 55, 1, 2, 320.00, 11.67, 3734.40),
(17, 45, 1, 2, 100.00, 11.67, 1167.00),
(18, 49, 1, 2, 125.00, 11.67, 1458.75),
(19, 56, 1, 2, 80.00, 11.67, 933.60),
(20, 47, 1, 2, 150.00, 11.67, 1750.50),
(21, 51, 1, 2, 240.00, 11.67, 2800.80),
(22, 34, 1, 2, 115.00, 11.67, 1342.05),
(23, 36, 1, 2, 135.00, 11.67, 1575.45),
(24, 38, 1, 2, 280.00, 11.67, 3267.60),
(25, 39, 1, 2, 105.00, 11.67, 1225.35),
(26, 40, 1, 2, 90.00, 11.67, 1050.30),
(27, 42, 1, 2, 350.00, 11.67, 4084.50),
(28, 43, 1, 2, 120.00, 11.67, 1400.40),
(29, 33, 1, 2, 110.00, 11.67, 1283.70),
(30, 37, 1, 2, 260.00, 11.67, 3034.20),
(31, 41, 1, 2, 310.00, 11.67, 3617.70),
(32, 35, 1, 2, 75.00, 11.67, 875.25),
(33, 44, 1, 2, 85.00, 11.67, 991.95);

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
(6, 4, 4, 1, 'Avenida Universidad', '810', NULL, 'Frente al parque', '2026-11-19 10:07:21'),
(23, 1, 25, 1, 'Calle Guadalupe', '428', NULL, 'Frente a tienda de abarrotes', '2026-11-22 15:18:58'),
(24, 2, 26, 1, 'Calle Rivero y Gutiérrez', '118', '2', 'Edificio gris', '2026-11-22 15:18:58'),
(25, 3, 27, 1, 'Calle Héroe de Nacozari', '640', NULL, 'Acceso por lateral', '2026-11-22 15:18:58'),
(26, 4, 28, 1, 'Calle Sierra Morena', '309', NULL, 'Barda blanca', '2026-11-22 15:18:58'),
(27, 14, 24, 1, 'Av. Convención de 1914', '890', NULL, 'Local comercial', '2026-11-22 15:18:58'),
(28, 15, 23, 1, 'Calle Valle de los Romeros', '512', NULL, 'Casa de dos plantas', '2026-11-22 15:18:58'),
(29, 16, 22, 1, 'Av. Siglo XXI', '1402', 'B', 'Cerca de la glorieta', '2026-11-22 15:18:58'),
(30, 17, 21, 1, 'Calle Nieto', '215', NULL, 'Portón café', '2026-11-22 15:18:58'),
(31, 18, 33, 1, 'Calle Independencia', '56', NULL, 'Junto al templo', '2026-11-22 15:18:58'),
(32, 19, 32, 1, 'Calle Morelos', '210', NULL, 'Portón negro', '2026-11-22 15:18:58'),
(33, 20, 36, 1, 'Calle Vista Hermosa', '18', NULL, 'Frente a área verde', '2026-11-22 15:18:58'),
(34, 20, 31, 1, 'Calle Mirador', '95', NULL, 'Comedor principal', '2026-11-22 15:18:58'),
(35, 21, 35, 1, 'Calle Progreso', '302', NULL, 'Zaguán verde', '2026-11-22 15:18:58'),
(36, 21, 30, 1, 'Calle Hidalgo', '182', NULL, 'Casa con macetas', '2026-11-22 15:18:58'),
(37, 22, 34, 1, 'Calle Reforma', '129', NULL, 'Esquina con Guerrero', '2026-11-22 15:18:58'),
(38, 22, 29, 1, 'Calle Juárez', '74', NULL, 'A dos cuadras de la plaza', '2026-11-22 15:18:58');

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
(1, 'AGS', 'Aguascalientes'),
(3, 'JAL', 'Jalisco');

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
(1, 1, 'Aguascalientes'),
(3, 3, 'Teocaltiche');

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

--
-- Volcado de datos para la tabla `notificacion`
--

INSERT INTO `notificacion` (`id_notificacion`, `id_cliente`, `id_prediccion`, `id_pedido`, `tipo_notificacion`, `id_notificacion_origen`, `numero_intento`, `estado_envio`, `resultado_notificacion`, `fecha_creacion`) VALUES
(1, 29, 5, NULL, 'RECORDATORIO', NULL, 1, 'ENTREGADO', 'SIN_RESPUESTA', '2026-11-22 15:22:56'),
(2, 31, 7, NULL, 'RECORDATORIO', NULL, 1, 'ENTREGADO', 'SIN_RESPUESTA', '2026-11-22 15:22:56'),
(3, 1, 9, NULL, 'RECORDATORIO', NULL, 1, 'ENTREGADO', 'SIN_RESPUESTA', '2026-11-22 15:22:56'),
(4, 21, 13, NULL, 'RECORDATORIO', NULL, 1, 'ENTREGADO', 'SIN_RESPUESTA', '2026-11-22 15:22:56');

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
(8, 'PED-0008', 4, 1, 6, 3150.00, 'TARJETA', 'ENTREGADO', 'ADMIN', '2026-11-19 09:10:00', '2026-11-19 09:50:00', '2026-11-19 10:07:21'),
(33, 'PED-0028', 29, 1, 38, 1283.70, 'EFECTIVO', 'REGISTRADO', 'WHATSAPP', '2026-11-20 09:50:00', NULL, '2026-11-22 15:22:56'),
(34, 'PED-0021', 29, 1, 38, 1342.05, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-16 10:00:00', '2026-11-16 10:50:00', '2026-11-22 15:22:56'),
(35, 'PED-0031', 30, 1, 36, 875.25, 'TARJETA', 'CANCELADO', 'ADMIN', '2026-11-18 17:30:00', NULL, '2026-11-22 15:22:56'),
(36, 'PED-0022', 30, 1, 36, 1575.45, 'TARJETA', 'ENTREGADO', 'ADMIN', '2026-11-16 14:15:00', '2026-11-16 15:05:00', '2026-11-22 15:22:56'),
(37, 'PED-0029', 31, 1, 34, 3034.20, 'TARJETA', 'REGISTRADO', 'ADMIN', '2026-11-20 12:15:00', NULL, '2026-11-22 15:22:56'),
(38, 'PED-0023', 31, 1, 34, 3267.60, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-17 09:30:00', '2026-11-17 10:15:00', '2026-11-22 15:22:56'),
(39, 'PED-0024', 32, 1, 32, 1225.35, 'TARJETA', 'ENTREGADO', 'ADMIN', '2026-11-17 16:20:00', '2026-11-17 17:00:00', '2026-11-22 15:22:56'),
(40, 'PED-0025', 33, 1, 31, 1050.30, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-18 11:10:00', '2026-11-18 11:55:00', '2026-11-22 15:22:56'),
(41, 'PED-0030', 34, 1, 37, 3617.70, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-20 13:20:00', '2026-11-20 14:05:00', '2026-11-22 15:22:56'),
(42, 'PED-0026', 34, 1, 37, 4084.50, 'TARJETA', 'ENTREGADO', 'ADMIN', '2026-11-19 08:45:00', '2026-11-19 09:30:00', '2026-11-22 15:22:56'),
(43, 'PED-0027', 35, 1, 35, 1400.40, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-19 15:00:00', '2026-11-19 15:40:00', '2026-11-22 15:22:56'),
(44, 'PED-0032', 36, 1, 33, 991.95, 'EFECTIVO', 'FALLIDO', 'WHATSAPP', '2026-11-19 18:10:00', NULL, '2026-11-22 15:22:56'),
(45, 'PED-0016', 21, 1, 30, 1167.00, 'TARJETA', 'REGISTRADO', 'WHATSAPP', '2026-11-20 09:05:00', NULL, '2026-11-22 15:22:56'),
(46, 'PED-0009', 21, 1, 30, 1050.30, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-16 09:00:00', '2026-11-16 09:45:00', '2026-11-22 15:22:56'),
(47, 'PED-0019', 22, 1, 29, 1750.50, 'TARJETA', 'FALLIDO', 'ADMIN', '2026-11-19 17:20:00', NULL, '2026-11-22 15:22:56'),
(48, 'PED-0010', 22, 1, 29, 1633.80, 'TARJETA', 'ENTREGADO', 'ADMIN', '2026-11-16 11:20:00', '2026-11-16 12:05:00', '2026-11-22 15:22:56'),
(49, 'PED-0017', 23, 1, 28, 1458.75, 'EFECTIVO', 'REGISTRADO', 'ADMIN', '2026-11-20 11:40:00', NULL, '2026-11-22 15:22:56'),
(50, 'PED-0011', 23, 1, 28, 1283.70, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-17 08:40:00', '2026-11-17 09:25:00', '2026-11-22 15:22:56'),
(51, 'PED-0020', 24, 1, 27, 2800.80, 'TARJETA', 'ENTREGADO', 'WHATSAPP', '2026-11-20 14:00:00', '2026-11-20 14:45:00', '2026-11-22 15:22:56'),
(52, 'PED-0012', 24, 1, 27, 3034.20, 'TARJETA', 'ENTREGADO', 'ADMIN', '2026-11-17 13:15:00', '2026-11-17 14:00:00', '2026-11-22 15:22:56'),
(53, 'PED-0013', 25, 1, 23, 1517.10, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-18 15:10:00', '2026-11-18 15:55:00', '2026-11-22 15:22:56'),
(54, 'PED-0014', 26, 1, 24, 1108.65, 'TARJETA', 'ENTREGADO', 'ADMIN', '2026-11-19 10:15:00', '2026-11-19 10:50:00', '2026-11-22 15:22:56'),
(55, 'PED-0015', 27, 1, 25, 3734.40, 'EFECTIVO', 'ENTREGADO', 'WHATSAPP', '2026-11-19 12:30:00', '2026-11-19 13:10:00', '2026-11-22 15:22:56'),
(56, 'PED-0018', 28, 1, 26, 933.60, 'EFECTIVO', 'CANCELADO', 'WHATSAPP', '2026-11-18 16:00:00', NULL, '2026-11-22 15:22:56');

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

--
-- Volcado de datos para la tabla `prediccion`
--

INSERT INTO `prediccion` (`id_prediccion`, `id_cliente`, `id_producto`, `fecha_calculo`, `cantidad_pedidos_base`, `promedio_dias_consumo`, `fecha_ultimo_ped`, `fecha_estimada_agotamiento`, `fecha_recordatorio`, `cantidad_estimada`, `probabilidad`, `vigente`, `id_pedido_resultado`, `dias_diferecia`) VALUES
(5, 29, 1, '2026-11-22 15:22:56', 3, 6.00, '2026-11-16', '2026-11-22', '2026-11-20', 120.00, 88.40, 1, NULL, NULL),
(6, 30, 1, '2026-11-22 15:22:56', 2, 11.00, '2026-11-16', '2026-11-21', '2026-11-19', 135.00, 83.50, 1, NULL, NULL),
(7, 31, 1, '2026-11-22 15:22:56', 4, 9.00, '2026-11-17', '2026-11-24', '2026-11-22', 280.00, 85.00, 1, NULL, NULL),
(8, 34, 1, '2026-11-22 15:22:56', 4, 7.00, '2026-11-20', '2026-11-28', '2026-11-26', 330.00, 90.20, 1, NULL, NULL),
(9, 1, 1, '2026-11-22 15:22:56', 3, 12.00, '2026-11-18', '2026-11-20', '2026-11-18', 150.00, 93.50, 1, NULL, NULL),
(10, 4, 1, '2026-11-22 15:22:56', 5, 7.00, '2026-11-19', '2026-11-27', '2026-11-25', 300.00, 91.00, 1, NULL, NULL),
(11, 3, 1, '2026-11-22 15:22:56', 2, 15.00, '2026-11-17', '2026-11-24', '2026-11-22', 120.00, 84.20, 1, NULL, NULL),
(12, 2, 1, '2026-11-22 15:22:56', 4, 10.00, '2026-11-19', '2026-11-22', '2026-11-20', 200.00, 89.00, 1, NULL, NULL),
(13, 21, 1, '2026-11-22 15:22:56', 3, 8.00, '2026-11-16', '2026-11-21', '2026-11-19', 95.00, 87.50, 1, NULL, NULL),
(14, 22, 1, '2026-11-22 15:22:56', 3, 9.00, '2026-11-16', '2026-11-23', '2026-11-21', 140.00, 86.00, 1, NULL, NULL),
(15, 24, 1, '2026-11-22 15:22:56', 4, 7.00, '2026-11-20', '2026-11-26', '2026-11-24', 250.00, 90.00, 1, NULL, NULL);

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
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT de la tabla `colonia`
--
ALTER TABLE `colonia`
  MODIFY `id_colonia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id_detalle_pedido` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `direccion`
--
ALTER TABLE `direccion`
  MODIFY `id_direccion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT de la tabla `entidad_federativa`
--
ALTER TABLE `entidad_federativa`
  MODIFY `id_entidad_fede` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `municipio`
--
ALTER TABLE `municipio`
  MODIFY `id_municipio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `notificacion`
--
ALTER TABLE `notificacion`
  MODIFY `id_notificacion` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT de la tabla `precio_producto`
--
ALTER TABLE `precio_producto`
  MODIFY `id_precio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `prediccion`
--
ALTER TABLE `prediccion`
  MODIFY `id_prediccion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

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
