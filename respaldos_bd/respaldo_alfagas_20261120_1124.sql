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
  `id_adm` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_sucursal` int(10) unsigned DEFAULT NULL COMMENT 'NULL = acceso a todas las sucursales',
  `nombre_adm` varchar(150) NOT NULL,
  `correo_adm` varchar(120) DEFAULT NULL,
  `numero_adm` varchar(10) NOT NULL,
  `nombre_usuario_adm` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL COMMENT 'Hash bcrypt/argon2, nunca texto plano',
  `activo_adm` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_adm`),
  UNIQUE KEY `uq_adm_numero` (`numero_adm`),
  UNIQUE KEY `uq_adm_usuario` (`nombre_usuario_adm`),
  UNIQUE KEY `uq_adm_correo` (`correo_adm`),
  KEY `fk_adm_sucursal` (`id_sucursal`),
  CONSTRAINT `fk_adm_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`),
  CONSTRAINT `ck_adm_numero` CHECK (`numero_adm` regexp '^[0-9]{10}$')
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
  `id_cliente` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_sucursal` int(10) unsigned NOT NULL,
  `nombre_cliente` varchar(150) NOT NULL,
  `telefono_whatsapp_cliente` varchar(10) NOT NULL,
  `estado_cliente` enum('PENDIENTE_REGISTRO','ACTIVO','INACTIVO','BAJA') NOT NULL DEFAULT 'PENDIENTE_REGISTRO',
  `acepta_notificaciones` tinyint(1) NOT NULL DEFAULT 0,
  `fecha_registro_cliente` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `uq_cliente_telefono` (`telefono_whatsapp_cliente`),
  KEY `ix_cliente_sucursal` (`id_sucursal`),
  CONSTRAINT `fk_cliente_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`),
  CONSTRAINT `ck_cliente_telefono` CHECK (`telefono_whatsapp_cliente` regexp '^[0-9]{10}$')
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,1,'Juan Pérez López','4491112233','ACTIVO',1,'2026-10-05 10:15:00'),(2,1,'María Fernanda Ruiz','4494445566','ACTIVO',1,'2026-10-10 12:30:00'),(3,1,'Carlos Ramírez','4493334455','ACTIVO',1,'2026-10-12 09:50:00'),(4,1,'Tortillería El Sol','4492223344','ACTIVO',1,'2026-10-15 10:07:00'),(5,1,'Rosa Elena Martínez','4495556677','ACTIVO',1,'2026-10-20 16:40:00');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colonia`
--

DROP TABLE IF EXISTS `colonia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colonia` (
  `id_colonia` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_municipio` int(10) unsigned NOT NULL,
  `nombre_colonia` varchar(100) NOT NULL,
  `codigo_postal` char(5) NOT NULL,
  PRIMARY KEY (`id_colonia`),
  UNIQUE KEY `uq_colonia_municipio_nombre_cp` (`id_municipio`,`nombre_colonia`,`codigo_postal`),
  CONSTRAINT `fk_colonia_municipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`),
  CONSTRAINT `ck_colonia_cp` CHECK (`codigo_postal` regexp '^[0-9]{5}$')
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colonia`
--

LOCK TABLES `colonia` WRITE;
/*!40000 ALTER TABLE `colonia` DISABLE KEYS */;
INSERT INTO `colonia` VALUES (4,1,'Bosques del Prado Norte','20130'),(1,1,'Casa Blanca','20190'),(3,1,'Jardines de la Asunción','20270'),(2,1,'Zona Centro','20000'),(5,2,'Centro Jesús María','20920');
/*!40000 ALTER TABLE `colonia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalle_pedido` (
  `id_detalle` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_pedido` int(10) unsigned NOT NULL,
  `id_producto` int(10) unsigned NOT NULL,
  `id_precio` int(10) unsigned NOT NULL,
  `cantidad` decimal(9,2) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  UNIQUE KEY `uq_detalle_pedido_producto` (`id_pedido`,`id_producto`),
  KEY `ix_detalle_producto` (`id_producto`),
  KEY `fk_detalle_precio_producto` (`id_precio`,`id_producto`),
  CONSTRAINT `fk_detalle_pedido` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`),
  CONSTRAINT `fk_detalle_precio_producto` FOREIGN KEY (`id_precio`, `id_producto`) REFERENCES `precio_producto` (`id_precio`, `id_producto`),
  CONSTRAINT `ck_detalle_cantidad` CHECK (`cantidad` > 0)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedido`
--

LOCK TABLES `detalle_pedido` WRITE;
/*!40000 ALTER TABLE `detalle_pedido` DISABLE KEYS */;
INSERT INTO `detalle_pedido` VALUES (1,1,1,1,150.00),(2,2,1,1,140.00),(3,3,1,1,120.00),(4,4,1,1,200.00),(5,5,1,1,85.00),(6,6,1,1,130.00),(7,7,1,1,300.00),(8,8,1,1,180.00);
/*!40000 ALTER TABLE `detalle_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direccion`
--

DROP TABLE IF EXISTS `direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `direccion` (
  `id_direccion` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_colonia` int(10) unsigned NOT NULL,
  `id_cliente` int(10) unsigned NOT NULL,
  `direccion_recurrente_cliente` tinyint(1) NOT NULL DEFAULT 1 COMMENT '1 = dirección vigente; 0 = anterior (se conserva para el histórico)',
  `calle` varchar(100) NOT NULL,
  `num_exterior` varchar(10) NOT NULL,
  `num_interior` varchar(10) DEFAULT NULL,
  `referencias` varchar(255) DEFAULT NULL,
  `fecha_creacion_direccion` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_direccion`),
  KEY `ix_direccion_cliente_vigente` (`id_cliente`,`direccion_recurrente_cliente`),
  KEY `ix_direccion_colonia` (`id_colonia`),
  CONSTRAINT `fk_direccion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `fk_direccion_colonia` FOREIGN KEY (`id_colonia`) REFERENCES `colonia` (`id_colonia`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direccion`
--

LOCK TABLES `direccion` WRITE;
/*!40000 ALTER TABLE `direccion` DISABLE KEYS */;
INSERT INTO `direccion` VALUES (1,1,1,1,'Av. Aguascalientes','104',NULL,'Portón blanco','2026-11-20 09:51:47'),(2,2,2,1,'Calle Madero','318',NULL,'Junto a la farmacia','2026-11-20 09:51:47'),(3,2,2,0,'Calle General Ignacio Zaragoza','304',NULL,'Fachada amarilla','2026-11-20 09:51:47'),(4,3,3,1,'Boulevard José María Chávez','1520',NULL,'Esquina con segundo anillo','2026-11-20 09:51:47'),(5,4,4,1,'Avenida Universidad','810',NULL,'Frente al parque','2026-11-20 09:51:47'),(6,5,5,1,'Calle Hidalgo','215','B','Local comercial','2026-11-20 09:51:47');
/*!40000 ALTER TABLE `direccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entidad_federativa`
--

DROP TABLE IF EXISTS `entidad_federativa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entidad_federativa` (
  `id_entidad_fede` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `clave_entidad_fede` char(3) NOT NULL,
  `nombre_entidad_fede` varchar(60) NOT NULL,
  PRIMARY KEY (`id_entidad_fede`),
  UNIQUE KEY `uq_entidad_clave` (`clave_entidad_fede`),
  UNIQUE KEY `uq_entidad_nombre` (`nombre_entidad_fede`)
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
  `id_municipio` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_entidad_fede` int(10) unsigned NOT NULL,
  `nombre_municipio` varchar(80) NOT NULL,
  PRIMARY KEY (`id_municipio`),
  UNIQUE KEY `uq_municipio_entidad_nombre` (`id_entidad_fede`,`nombre_municipio`),
  CONSTRAINT `fk_municipio_entidad` FOREIGN KEY (`id_entidad_fede`) REFERENCES `entidad_federativa` (`id_entidad_fede`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `municipio`
--

LOCK TABLES `municipio` WRITE;
/*!40000 ALTER TABLE `municipio` DISABLE KEYS */;
INSERT INTO `municipio` VALUES (1,1,'Aguascalientes'),(2,1,'Jesús María');
/*!40000 ALTER TABLE `municipio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notificacion`
--

DROP TABLE IF EXISTS `notificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notificacion` (
  `id_notificacion` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `id_cliente` int(10) unsigned NOT NULL,
  `id_prediccion` int(10) unsigned DEFAULT NULL,
  `id_pedido` int(10) unsigned DEFAULT NULL,
  `tipo_notificacion` enum('RECORDATORIO','CONFIRMACION_PEDIDO') NOT NULL,
  `id_notificacion_origen` bigint(20) unsigned DEFAULT NULL COMMENT 'Primer envío, en caso de reintento',
  `numero_intento` tinyint(3) unsigned NOT NULL DEFAULT 1,
  `fecha_programada` datetime NOT NULL,
  `fecha_envio` datetime DEFAULT NULL,
  `estado_envio` enum('PENDIENTE','ENVIADO','ENTREGADO','LEIDO','FALLIDO') NOT NULL DEFAULT 'PENDIENTE',
  `resultado_notificacion` enum('SIN_RESPUESTA','ACEPTO','RECHAZO') NOT NULL DEFAULT 'SIN_RESPUESTA',
  `fecha_creacion` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_notificacion`),
  KEY `ix_notif_cliente` (`id_cliente`),
  KEY `ix_notif_pendientes` (`estado_envio`,`fecha_programada`),
  KEY `fk_notif_prediccion` (`id_prediccion`),
  KEY `fk_notif_pedido` (`id_pedido`),
  KEY `fk_notif_origen` (`id_notificacion_origen`),
  CONSTRAINT `fk_notif_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `fk_notif_origen` FOREIGN KEY (`id_notificacion_origen`) REFERENCES `notificacion` (`id_notificacion`),
  CONSTRAINT `fk_notif_pedido` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`),
  CONSTRAINT `fk_notif_prediccion` FOREIGN KEY (`id_prediccion`) REFERENCES `prediccion` (`id_prediccion`),
  CONSTRAINT `ck_notif_intento` CHECK (`numero_intento` >= 1)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificacion`
--

LOCK TABLES `notificacion` WRITE;
/*!40000 ALTER TABLE `notificacion` DISABLE KEYS */;
INSERT INTO `notificacion` VALUES (1,1,1,NULL,'RECORDATORIO',NULL,1,'2026-11-18 09:00:00','2026-11-18 09:01:00','LEIDO','ACEPTO','2026-11-20 09:51:47'),(2,2,2,NULL,'RECORDATORIO',NULL,1,'2026-11-17 09:00:00','2026-11-17 09:02:00','ENTREGADO','SIN_RESPUESTA','2026-11-20 09:51:47'),(3,4,3,NULL,'RECORDATORIO',NULL,1,'2026-11-19 09:00:00',NULL,'PENDIENTE','SIN_RESPUESTA','2026-11-20 09:51:47'),(4,3,4,NULL,'RECORDATORIO',NULL,1,'2026-11-20 09:57:32','2026-11-20 09:57:32','ENVIADO','SIN_RESPUESTA','2026-11-20 09:57:32'),(5,2,2,NULL,'RECORDATORIO',NULL,1,'2026-11-20 10:09:22','2026-11-20 10:09:22','ENVIADO','SIN_RESPUESTA','2026-11-20 10:09:22'),(6,2,2,NULL,'RECORDATORIO',NULL,1,'2026-11-20 11:12:47','2026-11-20 11:12:47','ENVIADO','SIN_RESPUESTA','2026-11-20 11:12:47');
/*!40000 ALTER TABLE `notificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pedido` (
  `id_pedido` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `folio` varchar(20) NOT NULL,
  `id_cliente` int(10) unsigned NOT NULL,
  `id_sucursal` int(10) unsigned NOT NULL,
  `id_direccion_entrega` int(10) unsigned NOT NULL,
  `estado_pedido` enum('REGISTRADO','ENTREGADO','CANCELADO','FALLIDO') NOT NULL DEFAULT 'REGISTRADO',
  `origen_pedido` enum('WHATSAPP','ADMIN') NOT NULL DEFAULT 'WHATSAPP',
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp(),
  `fecha_entrega_real` datetime DEFAULT NULL,
  `fecha_actualizacion` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id_pedido`),
  UNIQUE KEY `uq_pedido_folio` (`folio`),
  KEY `ix_pedido_cliente_fecha` (`id_cliente`,`fecha_registro`),
  KEY `ix_pedido_sucursal_estado` (`id_sucursal`,`estado_pedido`),
  KEY `ix_pedido_direccion` (`id_direccion_entrega`),
  CONSTRAINT `fk_pedido_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `fk_pedido_direccion` FOREIGN KEY (`id_direccion_entrega`) REFERENCES `direccion` (`id_direccion`),
  CONSTRAINT `fk_pedido_sucursal` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursal` (`id_sucursal`),
  CONSTRAINT `ck_pedido_entrega` CHECK (`fecha_entrega_real` is null or `estado_pedido` = 'ENTREGADO' and `fecha_entrega_real` >= `fecha_registro`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,'PED-0001',1,1,1,'ENTREGADO','WHATSAPP','2026-10-20 10:00:00','2026-10-20 10:45:00','2026-11-20 09:51:47'),(2,'PED-0002',1,1,1,'REGISTRADO','WHATSAPP','2026-11-05 11:10:00',NULL,'2026-11-20 10:14:49'),(3,'PED-0003',1,1,1,'REGISTRADO','WHATSAPP','2026-11-20 09:15:00',NULL,'2026-11-20 09:51:47'),(4,'PED-0004',2,1,2,'FALLIDO','ADMIN','2026-11-01 14:00:00',NULL,'2026-11-20 10:14:27'),(5,'PED-0005',2,1,3,'CANCELADO','ADMIN','2026-11-12 16:00:00',NULL,'2026-11-20 09:51:47'),(6,'PED-0006',3,1,4,'ENTREGADO','WHATSAPP','2026-11-10 09:30:00','2026-11-20 10:14:19','2026-11-20 10:14:19'),(7,'PED-0007',4,1,5,'ENTREGADO','ADMIN','2026-11-14 08:20:00','2026-11-14 09:00:00','2026-11-20 09:51:47'),(8,'PED-0008',5,1,6,'ENTREGADO','WHATSAPP','2026-11-20 09:35:00','2026-11-20 09:56:18','2026-11-20 09:56:18');
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `precio_producto`
--

DROP TABLE IF EXISTS `precio_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `precio_producto` (
  `id_precio` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_producto` int(10) unsigned NOT NULL,
  `tipo_precio` enum('BASE','TEMPORADA') NOT NULL DEFAULT 'BASE',
  `nombre_temporada` varchar(40) DEFAULT NULL,
  `precio_producto` decimal(8,2) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL COMMENT 'NULL = sin fecha de cierre (solo permitido en BASE)',
  `id_adm` int(10) unsigned DEFAULT NULL,
  `fecha_creacion_productos` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_precio`),
  UNIQUE KEY `uq_precio_id_producto` (`id_precio`,`id_producto`),
  UNIQUE KEY `uq_precio_periodo` (`id_producto`,`tipo_precio`,`fecha_inicio`),
  KEY `fk_precio_adm` (`id_adm`),
  CONSTRAINT `fk_precio_adm` FOREIGN KEY (`id_adm`) REFERENCES `administrador` (`id_adm`),
  CONSTRAINT `fk_precio_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`),
  CONSTRAINT `ck_precio_positivo` CHECK (`precio_producto` > 0),
  CONSTRAINT `ck_precio_fechas` CHECK (`fecha_fin` is null or `fecha_fin` >= `fecha_inicio`),
  CONSTRAINT `ck_precio_temporada` CHECK (`tipo_precio` = 'BASE' and `nombre_temporada` is null or `tipo_precio` = 'TEMPORADA' and `nombre_temporada` is not null and `fecha_fin` is not null)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `precio_producto`
--

LOCK TABLES `precio_producto` WRITE;
/*!40000 ALTER TABLE `precio_producto` DISABLE KEYS */;
INSERT INTO `precio_producto` VALUES (1,1,'BASE',NULL,10.50,'2026-10-01','2026-11-19',1,'2026-11-20 09:51:47'),(2,2,'BASE',NULL,580.00,'2026-10-01',NULL,1,'2026-11-20 09:51:47'),(3,1,'BASE',NULL,11.67,'2026-11-20',NULL,1,'2026-11-20 09:58:18');
/*!40000 ALTER TABLE `precio_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prediccion`
--

DROP TABLE IF EXISTS `prediccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prediccion` (
  `id_prediccion` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_cliente` int(10) unsigned NOT NULL,
  `id_producto` int(10) unsigned NOT NULL,
  `fecha_calculo` datetime NOT NULL DEFAULT current_timestamp(),
  `cantidad_pedidos_base` tinyint(3) unsigned NOT NULL,
  `promedio_dias_consumo` decimal(6,2) NOT NULL,
  `fecha_ultimo_pedido` date NOT NULL,
  `fecha_estimada_agotamiento` date NOT NULL,
  `fecha_recordatorio` date DEFAULT NULL,
  `cantidad_estimada` decimal(9,2) DEFAULT NULL,
  `probabilidad` decimal(5,2) DEFAULT NULL COMMENT 'Salida del clasificador Naive Bayes (0 a 100)',
  `vigente` tinyint(1) NOT NULL DEFAULT 1,
  `id_pedido_resultado` int(10) unsigned DEFAULT NULL COMMENT 'Pedido real que cerró esta predicción',
  `dias_diferencia` smallint(6) DEFAULT NULL COMMENT 'Días reales - días estimados',
  PRIMARY KEY (`id_prediccion`),
  KEY `ix_prediccion_vigente` (`vigente`,`id_cliente`,`id_producto`),
  KEY `ix_prediccion_recordatorio` (`fecha_recordatorio`),
  KEY `fk_prediccion_cliente` (`id_cliente`),
  KEY `fk_prediccion_producto` (`id_producto`),
  KEY `fk_prediccion_pedido` (`id_pedido_resultado`),
  CONSTRAINT `fk_prediccion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `fk_prediccion_pedido` FOREIGN KEY (`id_pedido_resultado`) REFERENCES `pedido` (`id_pedido`),
  CONSTRAINT `fk_prediccion_producto` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`),
  CONSTRAINT `ck_prediccion_base` CHECK (`cantidad_pedidos_base` >= 2),
  CONSTRAINT `ck_prediccion_promedio` CHECK (`promedio_dias_consumo` > 0),
  CONSTRAINT `ck_prediccion_cantidad` CHECK (`cantidad_estimada` is null or `cantidad_estimada` > 0),
  CONSTRAINT `ck_prediccion_prob` CHECK (`probabilidad` is null or `probabilidad` between 0 and 100)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prediccion`
--

LOCK TABLES `prediccion` WRITE;
/*!40000 ALTER TABLE `prediccion` DISABLE KEYS */;
INSERT INTO `prediccion` VALUES (1,1,1,'2026-11-20 09:51:47',3,15.00,'2026-11-05','2026-11-20','2026-11-18',145.00,91.50,1,NULL,NULL),(2,2,1,'2026-11-20 09:51:47',2,18.00,'2026-11-01','2026-11-19','2026-11-17',190.00,88.00,1,NULL,NULL),(3,4,1,'2026-11-20 09:51:47',4,7.00,'2026-11-14','2026-11-21','2026-11-19',300.00,95.20,1,NULL,NULL),(4,3,1,'2026-11-20 09:51:47',2,14.00,'2026-11-10','2026-11-24','2026-11-22',130.00,84.00,1,NULL,NULL);
/*!40000 ALTER TABLE `prediccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `producto` (
  `id_producto` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `codigo_producto` varchar(8) NOT NULL,
  `nombre_producto` varchar(50) NOT NULL,
  `tipo_producto` enum('GAS_ESTACIONARIO','CILINDRO_PORTATIL') NOT NULL COMMENT 'GAS_ESTACIONARIO = por litro; CILINDRO_PORTATIL = por pieza',
  `capacidad_kg` decimal(5,2) DEFAULT NULL COMMENT 'Solo para cilindros',
  `activo_producto` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_producto`),
  UNIQUE KEY `uq_producto_codigo` (`codigo_producto`),
  CONSTRAINT `ck_producto_capacidad` CHECK (`tipo_producto` = 'CILINDRO_PORTATIL' and `capacidad_kg` is not null and `capacidad_kg` > 0 or `tipo_producto` = 'GAS_ESTACIONARIO' and `capacidad_kg` is null)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'GLP-01','Gas LP Estacionario','GAS_ESTACIONARIO',NULL,1),(2,'CIL-30','Cilindro Portátil 30 kg','CILINDRO_PORTATIL',30.00,1);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sucursal`
--

DROP TABLE IF EXISTS `sucursal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sucursal` (
  `id_sucursal` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `clave_sucursal` char(3) NOT NULL,
  `nombre_sucursal` varchar(80) NOT NULL,
  `id_municipio_sede` int(10) unsigned NOT NULL,
  `telefono_whatsapp` varchar(10) DEFAULT NULL,
  `activa_sucursal` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_creacion_sucursal` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_sucursal`),
  UNIQUE KEY `uq_sucursal_clave` (`clave_sucursal`),
  UNIQUE KEY `uq_sucursal_telefono` (`telefono_whatsapp`),
  KEY `fk_sucursal_municipio` (`id_municipio_sede`),
  CONSTRAINT `fk_sucursal_municipio` FOREIGN KEY (`id_municipio_sede`) REFERENCES `municipio` (`id_municipio`),
  CONSTRAINT `ck_sucursal_telefono` CHECK (`telefono_whatsapp` is null or `telefono_whatsapp` regexp '^[0-9]{10}$')
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sucursal`
--

LOCK TABLES `sucursal` WRITE;
/*!40000 ALTER TABLE `sucursal` DISABLE KEYS */;
INSERT INTO `sucursal` VALUES (1,'S01','Sucursal Matriz Aguascalientes',1,'4490000000',1,'2026-11-20 09:51:47');
/*!40000 ALTER TABLE `sucursal` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-20 11:24:12
