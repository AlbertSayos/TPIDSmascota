-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: tp
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `centros`
--

DROP TABLE IF EXISTS `centros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `centros` (
  `centroid` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(75) NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `calle` varchar(50) NOT NULL,
  `altura` int NOT NULL,
  `zona` varchar(75) NOT NULL,
  PRIMARY KEY (`centroid`)
) ENGINE=InnoDB AUTO_INCREMENT=30000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `centros`
--

LOCK TABLES `centros` WRITE;
/*!40000 ALTER TABLE `centros` DISABLE KEYS */;
/*!40000 ALTER TABLE `centros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mascotas`
--

DROP TABLE IF EXISTS `mascotas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mascotas` (
  `mascotaid` int NOT NULL AUTO_INCREMENT,
  `especie` varchar(50) NOT NULL,
  `raza` varchar(50) NOT NULL,
  `sexo` varchar(50) NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `calle` varchar(50) NOT NULL,
  `altura` int NOT NULL,
  `zona` varchar(75) NOT NULL,
  `usuarioid` int NOT NULL,
  `contacto` varchar(75) NOT NULL,
  `estado` varchar(50) NOT NULL,
  PRIMARY KEY (`mascotaid`)
) ENGINE=InnoDB AUTO_INCREMENT=20000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mascotas`
--

LOCK TABLES `mascotas` WRITE;
/*!40000 ALTER TABLE `mascotas` DISABLE KEYS */;
/*!40000 ALTER TABLE `mascotas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preguntas_respuestas`
--

DROP TABLE IF EXISTS `preguntas_respuestas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `preguntas_respuestas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pregunta` text COLLATE utf8mb4_general_ci NOT NULL,
  `respuesta` text COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preguntas_respuestas`
--

LOCK TABLES `preguntas_respuestas` WRITE;
/*!40000 ALTER TABLE `preguntas_respuestas` DISABLE KEYS */;
INSERT INTO `preguntas_respuestas` VALUES (1,'¿Qué es ENMA?','\"Encuentra tu Mascota\" es una plataforma diseñada para ayudar a reunir a las mascotas perdidas con sus dueños. Funciona como una base de datos en línea donde puedes registrar una mascota perdida y buscar mascotas encontradas por otros usuarios'),(2,'¿Cómo puedo encontrar mi mascota?','Desde la página de <a href=\"buscadas\">búsqueda</a>, nuestra plataforma permite ver una lista de todas las mascotas registradas, así como filtrar por sus características.También puedes buscar mascotas perdidas dentro de tu barrio o en zonas donde crees que tu mascota podría estar.'),(3,'¿Dónde puedo hallar refugios de mascotas perdidas?','En nuestra página de <a href=\"buscadas\">búsqueda</a> puedes interactuar con el mapa y encontrar las distintas casas y refugios de mascotas perdidas cercanas a tu barrio o zona.'),(4,'¿Qué debo hacer si encuentro una mascota perdida?','Si encuentras una mascota perdida, puedes <a href=\"registrar\">registrarla</a> en nuestra plataforma.Completa el formulario con la información básica y proporciona detalles para que podamos ayudar a reunirla con su dueño.'),(5,'¿Cómo puedo contribuir a mejorar ENMA?','Puedes ayudar difundiendo la página entre amigos y familiares, compartiendo publicaciones en redes sociales y registrando mascotas que estén perdidas. También puedes enviar tus ideas a nuestro correo electrónico de soporte.'),(6,'¿Cómo puedo evitar que mi mascota se pierda?','Asegúrate de que tu mascota lleve un collar con identificación clara y la información de contacto actualizada. También puedes considerar la posibilidad de un microchip, que proporciona una forma adicional de identificar a tu mascota si se pierde y se encuentra sin su collar.');
/*!40000 ALTER TABLE `preguntas_respuestas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `usuarioid` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `contraseña` varchar(50) NOT NULL,
  `contacto` varchar(75) NOT NULL,
  PRIMARY KEY (`usuarioid`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-27  0:27:04
