-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 20-11-2026 a las 16:52:19
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
  `id_adm` int(10) UNSIGNED NOT NULL,
  `id_sucursal` int(10) UNSIGNED DEFAULT NULL COMMENT 'NULL = acceso a todas las sucursales',
  `nombre_adm` varchar(150) NOT NULL,
  `correo_adm` varchar(120) DEFAULT NULL,
  `numero_adm` varchar(10) NOT NULL,
  `nombre_usuario_adm` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL COMMENT 'Hash bcrypt/argon2, nunca texto plano',
  `activo_adm` tinyint(1) NOT NULL DEFAULT 0
) ;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`id_adm`, `id_sucursal`, `nombre_adm`, `correo_adm`, `numero_adm`, `nombre_usuario_adm`, `password`, `activo_adm`) VALUES
(1, NULL, 'Administrador General', 'admin@alfagas.com', '4491234567', 'admin', '1236', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` int(10) UNSIGNED NOT NULL,
  `id_sucursal` int(10) UNSIGNED NOT NULL,
  `nombre_cliente` varchar(150) NOT NULL,
  `telefono_whatsapp_cliente` varchar(10) NOT NULL,
  `estado_cliente` enum('PENDIENTE_REGISTRO','ACTIVO','INACTIVO','BAJA') NOT NULL DEFAULT 'PENDIENTE_REGISTRO',
  `acepta_notificaciones` tinyint(1) NOT NULL DEFAULT 0,
  `fecha_registro_cliente` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `id_sucursal`, `nombre_cliente`, `telefono_whatsapp_cliente`, `estado_cliente`, `acepta_notificaciones`, `fecha_registro_cliente`) VALUES
(1, 1, 'Juan Pérez López', '4491112233', 'ACTIVO', 1, '2026-10-05 10:15:00'),
(2, 1, 'María Fernanda Ruiz', '4494445566', 'ACTIVO', 1, '2026-10-10 12:30:00'),
(3, 1, 'Carlos Ramírez', '4493334455', 'ACTIVO', 1, '2026-10-12 09:50:00'),
(4, 1, 'Tortillería El Sol', '4492223344', 'ACTIVO', 1, '2026-10-15 10:07:00'),
(5, 1, 'Rosa Elena Martínez', '4495556677', 'ACTIVO', 1, '2026-10-20 16:40:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `colonia`
--

CREATE TABLE `colonia` (
  `id_colonia` int(10) UNSIGNED NOT NULL,
  `id_municipio` int(10) UNSIGNED NOT NULL,
  `nombre_colonia` varchar(100) NOT NULL,
  `codigo_postal` char(5) NOT NULL
) ;

--
-- Volcado de datos para la tabla `colonia`
--

INSERT INTO `colonia` (`id_colonia`, `id_municipio`, `nombre_colonia`, `codigo_postal`) VALUES
(4, 1, 'Bosques del Prado Norte', '20130'),
(1, 1, 'Casa Blanca', '20190'),
(3, 1, 'Jardines de la Asunción', '20270'),
(2, 1, 'Zona Centro', '20000'),
(5, 2, 'Centro Jesús María', '20920');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_pedido`
--

CREATE TABLE `detalle_pedido` (
  `id_detalle` int(10) UNSIGNED NOT NULL,
  `id_pedido` int(10) UNSIGNED NOT NULL,
  `id_producto` int(10) UNSIGNED NOT NULL,
  `id_precio` int(10) UNSIGNED NOT NULL,
  `cantidad` decimal(9,2) NOT NULL
) ;

--
-- Volcado de datos para la tabla `detalle_pedido`
--

INSERT INTO `detalle_pedido` (`id_detalle`, `id_pedido`, `id_producto`, `id_precio`, `cantidad`) VALUES
(1, 1, 1, 1, 150.00),
(2, 2, 1, 1, 140.00),
(3, 3, 1, 1, 120.00),
(4, 4, 1, 1, 200.00),
(5, 5, 1, 1, 85.00),
(6, 6, 1, 1, 130.00),
(7, 7, 1, 1, 300.00),
(8, 8, 1, 1, 180.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `direccion`
--

CREATE TABLE `direccion` (
  `id_direccion` int(10) UNSIGNED NOT NULL,
  `id_colonia` int(10) UNSIGNED NOT NULL,
  `id_cliente` int(10) UNSIGNED NOT NULL,
  `direccion_recurrente_cliente` tinyint(1) NOT NULL DEFAULT 1 COMMENT '1 = dirección vigente; 0 = anterior (se conserva para el histórico)',
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
(1, 1, 1, 1, 'Av. Aguascalientes', '104', NULL, 'Portón blanco', '2026-11-20 09:51:47'),
(2, 2, 2, 1, 'Calle Madero', '318', NULL, 'Junto a la farmacia', '2026-11-20 09:51:47'),
(3, 2, 2, 0, 'Calle General Ignacio Zaragoza', '304', NULL, 'Fachada amarilla', '2026-11-20 09:51:47'),
(4, 3, 3, 1, 'Boulevard José María Chávez', '1520', NULL, 'Esquina con segundo anillo', '2026-11-20 09:51:47'),
(5, 4, 4, 1, 'Avenida Universidad', '810', NULL, 'Frente al parque', '2026-11-20 09:51:47'),
(6, 5, 5, 1, 'Calle Hidalgo', '215', 'B', 'Local comercial', '2026-11-20 09:51:47');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entidad_federativa`
--

CREATE TABLE `entidad_federativa` (
  `id_entidad_fede` int(10) UNSIGNED NOT NULL,
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
  `id_municipio` int(10) UNSIGNED NOT NULL,
  `id_entidad_fede` int(10) UNSIGNED NOT NULL,
  `nombre_municipio` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `municipio`
--

INSERT INTO `municipio` (`id_municipio`, `id_entidad_fede`, `nombre_municipio`) VALUES
(1, 1, 'Aguascalientes'),
(2, 1, 'Jesús María');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificacion`
--

CREATE TABLE `notificacion` (
  `id_notificacion` bigint(20) UNSIGNED NOT NULL,
  `id_cliente` int(10) UNSIGNED NOT NULL,
  `id_prediccion` int(10) UNSIGNED DEFAULT NULL,
  `id_pedido` int(10) UNSIGNED DEFAULT NULL,
  `tipo_notificacion` enum('RECORDATORIO','CONFIRMACION_PEDIDO') NOT NULL,
  `id_notificacion_origen` bigint(20) UNSIGNED DEFAULT NULL COMMENT 'Primer envío, en caso de reintento',
  `numero_intento` tinyint(3) UNSIGNED NOT NULL DEFAULT 1,
  `fecha_programada` datetime NOT NULL,
  `fecha_envio` datetime DEFAULT NULL,
  `estado_envio` enum('PENDIENTE','ENVIADO','ENTREGADO','LEIDO','FALLIDO') NOT NULL DEFAULT 'PENDIENTE',
  `resultado_notificacion` enum('SIN_RESPUESTA','ACEPTO','RECHAZO') NOT NULL DEFAULT 'SIN_RESPUESTA',
  `fecha_creacion` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Volcado de datos para la tabla `notificacion`
--

INSERT INTO `notificacion` (`id_notificacion`, `id_cliente`, `id_prediccion`, `id_pedido`, `tipo_notificacion`, `id_notificacion_origen`, `numero_intento`, `fecha_programada`, `fecha_envio`, `estado_envio`, `resultado_notificacion`, `fecha_creacion`) VALUES
(1, 1, 1, NULL, 'RECORDATORIO', NULL, 1, '2026-11-18 09:00:00', '2026-11-18 09:01:00', 'LEIDO', 'ACEPTO', '2026-11-20 09:51:47'),
(2, 2, 2, NULL, 'RECORDATORIO', NULL, 1, '2026-11-17 09:00:00', '2026-11-17 09:02:00', 'ENTREGADO', 'SIN_RESPUESTA', '2026-11-20 09:51:47'),
(3, 4, 3, NULL, 'RECORDATORIO', NULL, 1, '2026-11-19 09:00:00', NULL, 'PENDIENTE', 'SIN_RESPUESTA', '2026-11-20 09:51:47');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `id_pedido` int(10) UNSIGNED NOT NULL,
  `folio` varchar(20) NOT NULL,
  `id_cliente` int(10) UNSIGNED NOT NULL,
  `id_sucursal` int(10) UNSIGNED NOT NULL,
  `id_direccion_entrega` int(10) UNSIGNED NOT NULL,
  `estado_pedido` enum('REGISTRADO','ENTREGADO','CANCELADO','FALLIDO') NOT NULL DEFAULT 'REGISTRADO',
  `origen_pedido` enum('WHATSAPP','ADMIN') NOT NULL DEFAULT 'WHATSAPP',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp(),
  `fecha_entrega_real` datetime DEFAULT NULL,
  `fecha_actualizacion` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ;

--
-- Volcado de datos para la tabla `pedido`
--

INSERT INTO `pedido` (`id_pedido`, `folio`, `id_cliente`, `id_sucursal`, `id_direccion_entrega`, `estado_pedido`, `origen_pedido`, `fecha_registro`, `fecha_entrega_real`, `fecha_actualizacion`) VALUES
(1, 'PED-0001', 1, 1, 1, 'ENTREGADO', 'WHATSAPP', '2026-10-20 10:00:00', '2026-10-20 10:45:00', '2026-11-20 09:51:47'),
(2, 'PED-0002', 1, 1, 1, 'ENTREGADO', 'WHATSAPP', '2026-11-05 11:10:00', '2026-11-05 11:50:00', '2026-11-20 09:51:47'),
(3, 'PED-0003', 1, 1, 1, 'REGISTRADO', 'WHATSAPP', '2026-11-20 09:15:00', NULL, '2026-11-20 09:51:47'),
(4, 'PED-0004', 2, 1, 2, 'ENTREGADO', 'ADMIN', '2026-11-01 14:00:00', '2026-11-01 14:40:00', '2026-11-20 09:51:47'),
(5, 'PED-0005', 2, 1, 3, 'CANCELADO', 'ADMIN', '2026-11-12 16:00:00', NULL, '2026-11-20 09:51:47'),
(6, 'PED-0006', 3, 1, 4, 'ENTREGADO', 'WHATSAPP', '2026-11-10 09:30:00', '2026-11-10 10:15:00', '2026-11-20 09:51:47'),
(7, 'PED-0007', 4, 1, 5, 'ENTREGADO', 'ADMIN', '2026-11-14 08:20:00', '2026-11-14 09:00:00', '2026-11-20 09:51:47'),
(8, 'PED-0008', 5, 1, 6, 'REGISTRADO', 'WHATSAPP', '2026-11-20 09:35:00', NULL, '2026-11-20 09:51:47');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `precio_producto`
--

CREATE TABLE `precio_producto` (
  `id_precio` int(10) UNSIGNED NOT NULL,
  `id_producto` int(10) UNSIGNED NOT NULL,
  `tipo_precio` enum('BASE','TEMPORADA') NOT NULL DEFAULT 'BASE',
  `nombre_temporada` varchar(40) DEFAULT NULL,
  `precio_producto` decimal(8,2) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL COMMENT 'NULL = sin fecha de cierre (solo permitido en BASE)',
  `id_adm` int(10) UNSIGNED DEFAULT NULL,
  `fecha_creacion_productos` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Volcado de datos para la tabla `precio_producto`
--

INSERT INTO `precio_producto` (`id_precio`, `id_producto`, `tipo_precio`, `nombre_temporada`, `precio_producto`, `fecha_inicio`, `fecha_fin`, `id_adm`, `fecha_creacion_productos`) VALUES
(1, 1, 'BASE', NULL, 10.50, '2026-10-01', NULL, 1, '2026-11-20 09:51:47'),
(2, 2, 'BASE', NULL, 580.00, '2026-10-01', NULL, 1, '2026-11-20 09:51:47');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prediccion`
--

CREATE TABLE `prediccion` (
  `id_prediccion` int(10) UNSIGNED NOT NULL,
  `id_cliente` int(10) UNSIGNED NOT NULL,
  `id_producto` int(10) UNSIGNED NOT NULL,
  `fecha_calculo` datetime NOT NULL DEFAULT current_timestamp(),
  `cantidad_pedidos_base` tinyint(3) UNSIGNED NOT NULL,
  `promedio_dias_consumo` decimal(6,2) NOT NULL,
  `fecha_ultimo_pedido` date NOT NULL,
  `fecha_estimada_agotamiento` date NOT NULL,
  `fecha_recordatorio` date DEFAULT NULL,
  `cantidad_estimada` decimal(9,2) DEFAULT NULL,
  `probabilidad` decimal(5,2) DEFAULT NULL COMMENT 'Salida del clasificador Naive Bayes (0 a 100)',
  `vigente` tinyint(1) NOT NULL DEFAULT 1,
  `id_pedido_resultado` int(10) UNSIGNED DEFAULT NULL COMMENT 'Pedido real que cerró esta predicción',
  `dias_diferencia` smallint(6) DEFAULT NULL COMMENT 'Días reales - días estimados'
) ;

--
-- Volcado de datos para la tabla `prediccion`
--

INSERT INTO `prediccion` (`id_prediccion`, `id_cliente`, `id_producto`, `fecha_calculo`, `cantidad_pedidos_base`, `promedio_dias_consumo`, `fecha_ultimo_pedido`, `fecha_estimada_agotamiento`, `fecha_recordatorio`, `cantidad_estimada`, `probabilidad`, `vigente`, `id_pedido_resultado`, `dias_diferencia`) VALUES
(1, 1, 1, '2026-11-20 09:51:47', 3, 15.00, '2026-11-05', '2026-11-20', '2026-11-18', 145.00, 91.50, 1, NULL, NULL),
(2, 2, 1, '2026-11-20 09:51:47', 2, 18.00, '2026-11-01', '2026-11-19', '2026-11-17', 190.00, 88.00, 1, NULL, NULL),
(3, 4, 1, '2026-11-20 09:51:47', 4, 7.00, '2026-11-14', '2026-11-21', '2026-11-19', 300.00, 95.20, 1, NULL, NULL),
(4, 3, 1, '2026-11-20 09:51:47', 2, 14.00, '2026-11-10', '2026-11-24', '2026-11-22', 130.00, 84.00, 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id_producto` int(10) UNSIGNED NOT NULL,
  `codigo_producto` varchar(8) NOT NULL,
  `nombre_producto` varchar(50) NOT NULL,
  `tipo_producto` enum('GAS_ESTACIONARIO','CILINDRO_PORTATIL') NOT NULL COMMENT 'GAS_ESTACIONARIO = por litro; CILINDRO_PORTATIL = por pieza',
  `capacidad_kg` decimal(5,2) DEFAULT NULL COMMENT 'Solo para cilindros',
  `activo_producto` tinyint(1) NOT NULL DEFAULT 1
) ;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id_producto`, `codigo_producto`, `nombre_producto`, `tipo_producto`, `capacidad_kg`, `activo_producto`) VALUES
(1, 'GLP-01', 'Gas LP Estacionario', 'GAS_ESTACIONARIO', NULL, 1),
(2, 'CIL-30', 'Cilindro Portátil 30 kg', 'CILINDRO_PORTATIL', 30.00, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursal`
--

CREATE TABLE `sucursal` (
  `id_sucursal` int(10) UNSIGNED NOT NULL,
  `clave_sucursal` char(3) NOT NULL,
  `nombre_sucursal` varchar(80) NOT NULL,
  `id_municipio_sede` int(10) UNSIGNED NOT NULL,
  `telefono_whatsapp` varchar(10) DEFAULT NULL,
  `activa_sucursal` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_creacion_sucursal` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Volcado de datos para la tabla `sucursal`
--

INSERT INTO `sucursal` (`id_sucursal`, `clave_sucursal`, `nombre_sucursal`, `id_municipio_sede`, `telefono_whatsapp`, `activa_sucursal`, `fecha_creacion_sucursal`) VALUES
(1, 'S01', 'Sucursal Matriz Aguascalientes', 1, '4490000000', 1, '2026-11-20 09:51:47');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`id_adm`),
  ADD UNIQUE KEY `uq_adm_numero` (`numero_adm`),
  ADD UNIQUE KEY `uq_adm_usuario` (`nombre_usuario_adm`),
  ADD UNIQUE KEY `uq_adm_correo` (`correo_adm`),
  ADD KEY `fk_adm_sucursal` (`id_sucursal`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `uq_cliente_telefono` (`telefono_whatsapp_cliente`),
  ADD KEY `ix_cliente_sucursal` (`id_sucursal`);

--
-- Indices de la tabla `colonia`
--
ALTER TABLE `colonia`
  ADD PRIMARY KEY (`id_colonia`),
  ADD UNIQUE KEY `uq_colonia_municipio_nombre_cp` (`id_municipio`,`nombre_colonia`,`codigo_postal`);

--
-- Indices de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD PRIMARY KEY (`id_detalle`),
  ADD UNIQUE KEY `uq_detalle_pedido_producto` (`id_pedido`,`id_producto`),
  ADD KEY `ix_detalle_producto` (`id_producto`),
  ADD KEY `fk_detalle_precio_producto` (`id_precio`,`id_producto`);

--
-- Indices de la tabla `direccion`
--
ALTER TABLE `direccion`
  ADD PRIMARY KEY (`id_direccion`),
  ADD KEY `ix_direccion_cliente_vigente` (`id_cliente`,`direccion_recurrente_cliente`),
  ADD KEY `ix_direccion_colonia` (`id_colonia`);

--
-- Indices de la tabla `entidad_federativa`
--
ALTER TABLE `entidad_federativa`
  ADD PRIMARY KEY (`id_entidad_fede`),
  ADD UNIQUE KEY `uq_entidad_clave` (`clave_entidad_fede`),
  ADD UNIQUE KEY `uq_entidad_nombre` (`nombre_entidad_fede`);

--
-- Indices de la tabla `municipio`
--
ALTER TABLE `municipio`
  ADD PRIMARY KEY (`id_municipio`),
  ADD UNIQUE KEY `uq_municipio_entidad_nombre` (`id_entidad_fede`,`nombre_municipio`);

--
-- Indices de la tabla `notificacion`
--
ALTER TABLE `notificacion`
  ADD PRIMARY KEY (`id_notificacion`),
  ADD KEY `ix_notif_cliente` (`id_cliente`),
  ADD KEY `ix_notif_pendientes` (`estado_envio`,`fecha_programada`),
  ADD KEY `fk_notif_prediccion` (`id_prediccion`),
  ADD KEY `fk_notif_pedido` (`id_pedido`),
  ADD KEY `fk_notif_origen` (`id_notificacion_origen`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id_pedido`),
  ADD UNIQUE KEY `uq_pedido_folio` (`folio`),
  ADD KEY `ix_pedido_cliente_fecha` (`id_cliente`,`fecha_registro`),
  ADD KEY `ix_pedido_sucursal_estado` (`id_sucursal`,`estado_pedido`),
  ADD KEY `ix_pedido_direccion` (`id_direccion_entrega`);

--
-- Indices de la tabla `precio_producto`
--
ALTER TABLE `precio_producto`
  ADD PRIMARY KEY (`id_precio`),
  ADD UNIQUE KEY `uq_precio_id_producto` (`id_precio`,`id_producto`),
  ADD UNIQUE KEY `uq_precio_periodo` (`id_producto`,`tipo_precio`,`fecha_inicio`),
  ADD KEY `fk_precio_adm` (`id_adm`);

--
-- Indices de la tabla `prediccion`
--
ALTER TABLE `prediccion`
  ADD PRIMARY KEY (`id_prediccion`),
  ADD KEY `ix_prediccion_vigente` (`vigente`,`id_cliente`,`id_producto`),
  ADD KEY `ix_prediccion_recordatorio` (`fecha_recordatorio`),
  ADD KEY `fk_prediccion_cliente` (`id_cliente`),
  ADD KEY `fk_prediccion_producto` (`id_producto`),
  ADD KEY `fk_prediccion_pedido` (`id_pedido_resultado`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_producto`),
  ADD UNIQUE KEY `uq_producto_codigo` (`codigo_producto`);

--
-- Indices de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  ADD PRIMARY KEY (`id_sucursal`),
  ADD UNIQUE KEY `uq_sucursal_clave` (`clave_sucursal`),
  ADD UNIQUE KEY `uq_sucursal_telefono` (`telefono_whatsapp`),
  ADD KEY `fk_sucursal_municipio` (`id_municipio_sede`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `id_adm` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `colonia`
--
ALTER TABLE `colonia`
  MODIFY `id_colonia` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id_detalle` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `direccion`
--
ALTER TABLE `direccion`
  MODIFY `id_direccion` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `entidad_federativa`
--
ALTER TABLE `entidad_federativa`
  MODIFY `id_entidad_fede` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `municipio`
--
ALTER TABLE `municipio`
  MODIFY `id_municipio` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `notificacion`
--
ALTER TABLE `notificacion`
  MODIFY `id_notificacion` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id_pedido` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `precio_producto`
--
ALTER TABLE `precio_producto`
  MODIFY `id_precio` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `prediccion`
--
ALTER TABLE `prediccion`
  MODIFY `id_prediccion` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_producto` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  MODIFY `id_sucursal` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD CONSTRAINT `fk_adm_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`);

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `fk_cliente_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`);

--
-- Filtros para la tabla `colonia`
--
ALTER TABLE `colonia`
  ADD CONSTRAINT `fk_colonia_municipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`);

--
-- Filtros para la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD CONSTRAINT `fk_detalle_pedido` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`),
  ADD CONSTRAINT `fk_detalle_precio_producto` FOREIGN KEY (`id_precio`,`id_producto`) REFERENCES `precio_producto` (`id_precio`, `id_producto`);

--
-- Filtros para la tabla `direccion`
--
ALTER TABLE `direccion`
  ADD CONSTRAINT `fk_direccion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `fk_direccion_colonia` FOREIGN KEY (`id_colonia`) REFERENCES `colonia` (`id_colonia`);

--
-- Filtros para la tabla `municipio`
--
ALTER TABLE `municipio`
  ADD CONSTRAINT `fk_municipio_entidad` FOREIGN KEY (`id_entidad_fede`) REFERENCES `entidad_federativa` (`id_entidad_fede`);

--
-- Filtros para la tabla `notificacion`
--
ALTER TABLE `notificacion`
  ADD CONSTRAINT `fk_notif_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `fk_notif_origen` FOREIGN KEY (`id_notificacion_origen`) REFERENCES `notificacion` (`id_notificacion`),
  ADD CONSTRAINT `fk_notif_pedido` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`),
  ADD CONSTRAINT `fk_notif_prediccion` FOREIGN KEY (`id_prediccion`) REFERENCES `prediccion` (`id_prediccion`);

--
-- Filtros para la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `fk_pedido_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `fk_pedido_direccion` FOREIGN KEY (`id_direccion_entrega`) REFERENCES `direccion` (`id_direccion`),
  ADD CONSTRAINT `fk_pedido_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`);

--
-- Filtros para la tabla `precio_producto`
--
ALTER TABLE `precio_producto`
  ADD CONSTRAINT `fk_precio_adm` FOREIGN KEY (`id_adm`) REFERENCES `administrador` (`id_adm`),
  ADD CONSTRAINT `fk_precio_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);

--
-- Filtros para la tabla `prediccion`
--
ALTER TABLE `prediccion`
  ADD CONSTRAINT `fk_prediccion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `fk_prediccion_pedido` FOREIGN KEY (`id_pedido_resultado`) REFERENCES `pedido` (`id_pedido`),
  ADD CONSTRAINT `fk_prediccion_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);

--
-- Filtros para la tabla `sucursal`
--
ALTER TABLE `sucursal`
  ADD CONSTRAINT `fk_sucursal_municipio` FOREIGN KEY (`id_municipio_sede`) REFERENCES `municipio` (`id_municipio`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
