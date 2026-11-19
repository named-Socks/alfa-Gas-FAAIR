-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: faair_alfa_gas
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administrador`
--

DROP TABLE IF EXISTS `administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administrador` (
  `id_adm` int(11) NOT NULL AUTO_INCREMENT,
  `id_sucursal` int(11) DEFAULT NULL COMMENT 'NULL = acceso a todas las sucursales',
  `nombre_adm` varchar(150) NOT NULL,
  `correo_adm` varchar(120) DEFAULT NULL,
  `numero_adm` varchar(16) NOT NULL,
  `nombre_usuario_adm` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `activo_adm` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_adm`),
  UNIQUE KEY `uk_adm_numero` (`numero_adm`),
  UNIQUE KEY `uk_adm_usuario` (`nombre_usuario_adm`),
  UNIQUE KEY `uk_adm_correo` (`correo_adm`),
  KEY `fk_administrador_sucursal` (`id_sucursal`),
  CONSTRAINT `fk_administrador_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador`
--

LOCK TABLES `administrador` WRITE;
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
INSERT INTO `administrador` VALUES (1,NULL,'Administrador General','admin@alfagas.com','4491234567','admin','1236',1);
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cliente` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `id_sucursal` int(11) NOT NULL,
  `nombre_cliente` varchar(150) NOT NULL,
  `telefono_whatsapp_cliente` varchar(10) NOT NULL,
  `estado_cliente` enum('PENDIENTE_REGISTRO','ACTIVO','INACTIVO','BAJA') NOT NULL DEFAULT 'PENDIENTE_REGISTRO',
  `acepta_notificaciones` tinyint(1) NOT NULL DEFAULT 0,
  `fecha_registro_cliente` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `uk_cliente_whatsapp` (`telefono_whatsapp_cliente`),
  KEY `fk_cliente_sucursal` (`id_sucursal`),
  CONSTRAINT `fk_cliente_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,1,'Juan Pérez López','4491112233','ACTIVO',0,'2026-11-18 21:19:22'),(2,1,'María Fernanda Ruiz','4494445566','ACTIVO',0,'2026-11-18 21:19:22'),(3,1,'Carlos Ramírez','4493334455','ACTIVO',1,'2026-11-19 09:53:58'),(4,1,'Tortillería El Sol','4492223344','ACTIVO',1,'2026-11-19 10:07:21');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colonia`
--

DROP TABLE IF EXISTS `colonia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colonia` (
  `id_colonia` int(11) NOT NULL AUTO_INCREMENT,
  `id_municipio` int(11) NOT NULL,
  `nombre_colonia` varchar(100) NOT NULL,
  `codigo_postal` char(5) NOT NULL,
  PRIMARY KEY (`id_colonia`),
  KEY `fk_colonia_municipio` (`id_municipio`),
  CONSTRAINT `fk_colonia_municipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colonia`
--

LOCK TABLES `colonia` WRITE;
/*!40000 ALTER TABLE `colonia` DISABLE KEYS */;
INSERT INTO `colonia` VALUES (1,1,'Casa Blanca','20190'),(2,1,'Zona Centro','20000'),(3,1,'Jardines de la Asunción','20270'),(4,1,'Bosques del Prado Norte','20130');
/*!40000 ALTER TABLE `colonia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direccion`
--

DROP TABLE IF EXISTS `direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `direccion` (
  `id_direccion` int(11) NOT NULL AUTO_INCREMENT,
  `id_colonia` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `direccion_recurrente_cliente` tinyint(1) NOT NULL DEFAULT 0,
  `id_cliente_activo` int(11) GENERATED ALWAYS AS (if(`direccion_recurrente_cliente` = 1,`id_cliente`,NULL)) VIRTUAL,
  `calle` varchar(100) NOT NULL,
  `num_exterior` varchar(10) NOT NULL,
  `num_interior` varchar(10) DEFAULT NULL,
  `referencias` varchar(255) DEFAULT NULL,
  `fecha_creacion_direccion` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_direccion`),
  UNIQUE KEY `uk_cliente_direccion_activa` (`id_cliente_activo`),
  KEY `idx_direccion_cliente_recurrente` (`id_cliente`,`direccion_recurrente_cliente`),
  KEY `fk_direccion_colonia` (`id_colonia`),
  CONSTRAINT `fk_direccion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_direccion_colonia` FOREIGN KEY (`id_colonia`) REFERENCES `colonia` (`id_colonia`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direccion`
--

LOCK TABLES `direccion` WRITE;
/*!40000 ALTER TABLE `direccion` DISABLE KEYS */;
INSERT INTO `direccion` VALUES (1,1,1,1,1,'Av. Aguascalientes','104',NULL,NULL,'2026-11-18 21:19:22'),(2,2,2,1,2,'Calle Madero','318',NULL,NULL,'2026-11-18 21:19:22'),(4,2,2,0,NULL,'Calle General Ignacio Zaragoza','304',NULL,'Fachada amarilla','2026-11-19 09:53:58'),(5,3,3,1,3,'Boulevard José María Chávez','1520',NULL,'Esquina con segundo anillo','2026-11-19 09:53:58'),(6,4,4,1,4,'Avenida Universidad','810',NULL,'Frente al parque','2026-11-19 10:07:21');
/*!40000 ALTER TABLE `direccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entidad_federativa`
--

DROP TABLE IF EXISTS `entidad_federativa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entidad_federativa` (
  `id_entidad_fede` int(11) NOT NULL AUTO_INCREMENT,
  `clave_entidad_fede` char(3) NOT NULL,
  `nombre_entidad_fede` varchar(60) NOT NULL,
  PRIMARY KEY (`id_entidad_fede`),
  UNIQUE KEY `uk_entidad_clave` (`clave_entidad_fede`),
  UNIQUE KEY `uk_entidad_nombre` (`nombre_entidad_fede`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entidad_federativa`
--

LOCK TABLES `entidad_federativa` WRITE;
/*!40000 ALTER TABLE `entidad_federativa` DISABLE KEYS */;
INSERT INTO `entidad_federativa` VALUES (1,'AGS','Aguascalientes');
/*!40000 ALTER TABLE `entidad_federativa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `municipio`
--

DROP TABLE IF EXISTS `municipio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `municipio` (
  `id_municipio` int(11) NOT NULL AUTO_INCREMENT,
  `id_entidad_fede` int(11) NOT NULL,
  `nombre_municipio` varchar(80) NOT NULL,
  PRIMARY KEY (`id_municipio`),
  KEY `fk_municipio_entidad` (`id_entidad_fede`),
  CONSTRAINT `fk_municipio_entidad` FOREIGN KEY (`id_entidad_fede`) REFERENCES `entidad_federativa` (`id_entidad_fede`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `municipio`
--

LOCK TABLES `municipio` WRITE;
/*!40000 ALTER TABLE `municipio` DISABLE KEYS */;
INSERT INTO `municipio` VALUES (1,1,'Aguascalientes');
/*!40000 ALTER TABLE `municipio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notificacion`
--

DROP TABLE IF EXISTS `notificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notificacion` (
  `id_notificacion` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) NOT NULL,
  `id_prediccion` int(11) DEFAULT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `tipo_notificacion` enum('RECORDATORIO','CONFIRMACION_PEDIDO') NOT NULL,
  `id_notificacion_origen` bigint(20) DEFAULT NULL COMMENT 'Primer envío, en caso de reintento',
  `numero_intento` tinyint(4) NOT NULL DEFAULT 1,
  `estado_envio` enum('PENDIENTE','ENVIADO','ENTREGADO','LEIDO','FALLIDO') NOT NULL DEFAULT 'PENDIENTE',
  `resultado_notificacion` enum('SIN_RESPUESTA','ACEPTO','RECHAZO') NOT NULL DEFAULT 'SIN_RESPUESTA',
  `fecha_creacion` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_notificacion`),
  KEY `fk_notificacion_cliente` (`id_cliente`),
  KEY `fk_notificacion_prediccion` (`id_prediccion`),
  KEY `fk_notificacion_pedido` (`id_pedido`),
  KEY `fk_notificacion_origen` (`id_notificacion_origen`),
  CONSTRAINT `fk_notificacion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_notificacion_origen` FOREIGN KEY (`id_notificacion_origen`) REFERENCES `notificacion` (`id_notificacion`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_notificacion_pedido` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_notificacion_prediccion` FOREIGN KEY (`id_prediccion`) REFERENCES `prediccion` (`id_prediccion`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificacion`
--

LOCK TABLES `notificacion` WRITE;
/*!40000 ALTER TABLE `notificacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `notificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pedido` (
  `id_pedido` int(11) NOT NULL AUTO_INCREMENT,
  `folio` varchar(20) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_sucursal` int(11) NOT NULL,
  `id_direccion_entrega` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `id_precio` int(11) NOT NULL,
  `cantidad_litros` decimal(9,2) NOT NULL,
  `total_pedido` decimal(11,2) NOT NULL DEFAULT 0.00,
  `metodo_pago` enum('EFECTIVO','TARJETA') NOT NULL DEFAULT 'EFECTIVO',
  `estado_pedido` enum('REGISTRADO','ENTREGADO','CANCELADO','FALLIDO') NOT NULL DEFAULT 'REGISTRADO',
  `origen_pedido` enum('WHATSAPP','ADMIN') NOT NULL DEFAULT 'WHATSAPP',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp(),
  `fecha_entrega_real` datetime DEFAULT NULL,
  `fecha_actualizacion` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id_pedido`),
  UNIQUE KEY `uk_pedido_folio` (`folio`),
  KEY `fk_pedido_cliente` (`id_cliente`),
  KEY `fk_pedido_sucursal` (`id_sucursal`),
  KEY `fk_pedido_direccion` (`id_direccion_entrega`),
  KEY `fk_pedido_producto` (`id_producto`),
  KEY `fk_pedido_precio` (`id_precio`),
  CONSTRAINT `fk_pedido_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON UPDATE CASCADE,
  CONSTRAINT `fk_pedido_direccion` FOREIGN KEY (`id_direccion_entrega`) REFERENCES `direccion` (`id_direccion`) ON UPDATE CASCADE,
  CONSTRAINT `fk_pedido_precio` FOREIGN KEY (`id_precio`) REFERENCES `precio_producto` (`id_precio`) ON UPDATE CASCADE,
  CONSTRAINT `fk_pedido_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON UPDATE CASCADE,
  CONSTRAINT `fk_pedido_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`) ON UPDATE CASCADE,
  CONSTRAINT `chk_pedido_cantidad_positiva` CHECK (`cantidad_litros` > 0)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,'PED-0001',1,1,1,1,1,120.00,1260.00,'EFECTIVO','REGISTRADO','WHATSAPP','2026-11-18 21:19:22',NULL,'2026-11-18 21:19:22'),(2,'PED-0002',2,1,2,1,1,85.00,892.50,'TARJETA','CANCELADO','ADMIN','2026-11-18 21:19:22','2026-11-18 21:20:39','2026-11-19 09:45:42'),(4,'PED-004',3,1,5,1,1,120.00,1260.00,'EFECTIVO','ENTREGADO','WHATSAPP','2026-11-17 09:53:58','2026-11-17 09:53:58','2026-11-19 09:53:58'),(5,'PED-0005',1,1,1,1,1,150.00,1575.00,'EFECTIVO','ENTREGADO','WHATSAPP','2026-11-18 10:30:00','2026-11-18 11:15:00','2026-11-19 10:07:21'),(6,'PED-0006',2,1,2,1,1,200.00,2100.00,'TARJETA','ENTREGADO','ADMIN','2026-11-18 14:00:00','2026-11-18 14:40:00','2026-11-19 10:07:21'),(7,'PED-0007',2,1,4,1,1,100.00,1050.00,'EFECTIVO','ENTREGADO','WHATSAPP','2026-11-19 08:20:00','2026-11-19 09:00:00','2026-11-19 10:07:21'),(8,'PED-0008',4,1,6,1,1,300.00,3150.00,'TARJETA','ENTREGADO','ADMIN','2026-11-19 09:10:00','2026-11-19 09:50:00','2026-11-19 10:07:21');
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_pedido_bi_total
BEFORE INSERT ON pedido
FOR EACH ROW
BEGIN
  DECLARE v_precio DECIMAL(8,2);

  SELECT precio_producto INTO v_precio
  FROM precio_producto
  WHERE id_precio = NEW.id_precio;

  SET NEW.total_pedido = NEW.cantidad_litros * v_precio;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_pedido_bu_total
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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `precio_producto`
--

DROP TABLE IF EXISTS `precio_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `precio_producto` (
  `id_precio` int(11) NOT NULL AUTO_INCREMENT,
  `id_producto` int(11) NOT NULL,
  `precio_producto` decimal(8,2) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL COMMENT 'NULL = precio vigente',
  `id_adm` int(11) DEFAULT NULL,
  `fecha_creacion_productos` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_precio`),
  KEY `fk_precio_producto` (`id_producto`),
  KEY `fk_precio_adm` (`id_adm`),
  CONSTRAINT `fk_precio_adm` FOREIGN KEY (`id_adm`) REFERENCES `administrador` (`id_adm`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_precio_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `precio_producto`
--

LOCK TABLES `precio_producto` WRITE;
/*!40000 ALTER TABLE `precio_producto` DISABLE KEYS */;
INSERT INTO `precio_producto` VALUES (1,1,10.50,'2026-11-18','2026-11-19',1,'2026-11-18 21:19:22'),(2,1,11.67,'2026-11-19',NULL,1,'2026-11-19 10:37:01');
/*!40000 ALTER TABLE `precio_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prediccion`
--

DROP TABLE IF EXISTS `prediccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prediccion` (
  `id_prediccion` int(11) NOT NULL AUTO_INCREMENT,
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
  `dias_diferecia` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id_prediccion`),
  KEY `idx_prediccion_vigente_cliente` (`vigente`,`id_cliente`),
  KEY `fk_prediccion_cliente` (`id_cliente`),
  KEY `fk_prediccion_producto` (`id_producto`),
  KEY `fk_prediccion_pedido_resultado` (`id_pedido_resultado`),
  CONSTRAINT `fk_prediccion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_prediccion_pedido_resultado` FOREIGN KEY (`id_pedido_resultado`) REFERENCES `pedido` (`id_pedido`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_prediccion_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prediccion`
--

LOCK TABLES `prediccion` WRITE;
/*!40000 ALTER TABLE `prediccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `prediccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `producto` (
  `id_producto` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_producto` varchar(8) NOT NULL,
  `nombre_producto` varchar(50) NOT NULL,
  `tipo_producto` enum('GAS_ESTACIONARIO','CILINDRO_PORTATIL') NOT NULL COMMENT 'GAS_ESTACIONARIO = se vende por litro; CILINDRO_PORTATIL = por pieza',
  `capacidad_kg` decimal(5,2) DEFAULT NULL COMMENT 'Solo para cilindros',
  `activo_producto` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_producto`),
  UNIQUE KEY `uk_producto_codigo` (`codigo_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'GLP-01','Gas LP Estacionario','GAS_ESTACIONARIO',NULL,1);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sucursal`
--

DROP TABLE IF EXISTS `sucursal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sucursal` (
  `id_sucursal` int(11) NOT NULL AUTO_INCREMENT,
  `clave_sucursal` char(3) NOT NULL,
  `nombre_sucursal` varchar(80) NOT NULL,
  `id_municipio_sede` int(11) NOT NULL,
  `telefono_whatsapp` varchar(10) DEFAULT NULL,
  `activa_sucursal` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_creacion_sucursal` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_sucursal`),
  UNIQUE KEY `uk_sucursal_clave` (`clave_sucursal`),
  UNIQUE KEY `uk_sucursal_whatsapp` (`telefono_whatsapp`),
  KEY `fk_sucursal_municipio` (`id_municipio_sede`),
  CONSTRAINT `fk_sucursal_municipio` FOREIGN KEY (`id_municipio_sede`) REFERENCES `municipio` (`id_municipio`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sucursal`
--

LOCK TABLES `sucursal` WRITE;
/*!40000 ALTER TABLE `sucursal` DISABLE KEYS */;
INSERT INTO `sucursal` VALUES (1,'S01','Sucursal Matriz Aguascalientes',1,'4490000000',1,'2026-11-18 21:19:22');
/*!40000 ALTER TABLE `sucursal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'faair_alfa_gas'
--
