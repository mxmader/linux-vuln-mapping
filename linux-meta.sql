-- MySQL dump 10.14  Distrib 5.5.37-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: linux-meta-dev
-- ------------------------------------------------------
-- Server version	5.5.37-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `distro`
--

DROP TABLE IF EXISTS `distro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distro` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `name` enum('CentOS','Fedora','Oracle Linux','RHEL','Scientific Linux') NOT NULL,
  `family` enum('enterprise','fedora') NOT NULL,
  `major_version` int(8) unsigned NOT NULL,
  `minor_version` int(8) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `major_version` (`major_version`,`minor_version`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distro`
--

LOCK TABLES `distro` WRITE;
/*!40000 ALTER TABLE `distro` DISABLE KEYS */;
/*!40000 ALTER TABLE `distro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mitre_cve`
--

DROP TABLE IF EXISTS `mitre_cve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mitre_cve` (
  `cve` varchar(16) NOT NULL,
  `description` text NOT NULL,
  `published` date DEFAULT NULL,
  `modified` date DEFAULT NULL,
  `title` varchar(16) NOT NULL,
  PRIMARY KEY (`cve`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mitre_cve`
--

LOCK TABLES `mitre_cve` WRITE;
/*!40000 ALTER TABLE `mitre_cve` DISABLE KEYS */;
/*!40000 ALTER TABLE `mitre_cve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mitre_cve_reference`
--

DROP TABLE IF EXISTS `mitre_cve_reference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mitre_cve_reference` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `cve` varchar(16) NOT NULL,
  `url` varchar(1024) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cve` (`cve`),
  CONSTRAINT `mitre_cve_reference_ibfk_2` FOREIGN KEY (`cve`) REFERENCES `mitre_cve` (`cve`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mitre_cve_reference`
--

LOCK TABLES `mitre_cve_reference` WRITE;
/*!40000 ALTER TABLE `mitre_cve_reference` DISABLE KEYS */;
/*!40000 ALTER TABLE `mitre_cve_reference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package`
--

DROP TABLE IF EXISTS `package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `distro_id` int(32) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `distro_id` (`distro_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package`
--

LOCK TABLES `package` WRITE;
/*!40000 ALTER TABLE `package` DISABLE KEYS */;
/*!40000 ALTER TABLE `package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package_group`
--

DROP TABLE IF EXISTS `package_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package_group` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `distro` int(32) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`,`distro`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package_group`
--

LOCK TABLES `package_group` WRITE;
/*!40000 ALTER TABLE `package_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `package_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package_to_group_map`
--

DROP TABLE IF EXISTS `package_to_group_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package_to_group_map` (
  `package_id` int(32) unsigned NOT NULL,
  `package_group_id` int(32) unsigned NOT NULL,
  PRIMARY KEY (`package_id`,`package_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package_to_group_map`
--

LOCK TABLES `package_to_group_map` WRITE;
/*!40000 ALTER TABLE `package_to_group_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `package_to_group_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package_version`
--

DROP TABLE IF EXISTS `package_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package_version` (
  `id` int(32) unsigned NOT NULL,
  `package_id` int(32) unsigned NOT NULL,
  `version` varchar(24) NOT NULL,
  `arch` varchar(24) NOT NULL,
  `release` varchar(32) NOT NULL,
  `epoch` int(32) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `version` (`version`,`arch`),
  KEY `package_id` (`package_id`),
  CONSTRAINT `package_version_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `package` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package_version`
--

LOCK TABLES `package_version` WRITE;
/*!40000 ALTER TABLE `package_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `package_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package_version_bugzilla`
--

DROP TABLE IF EXISTS `package_version_bugzilla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package_version_bugzilla` (
  `package_version_id` int(32) unsigned NOT NULL,
  `bugzilla_id` int(32) unsigned NOT NULL,
  PRIMARY KEY (`package_version_id`,`bugzilla_id`),
  CONSTRAINT `package_version_bugzilla_ibfk_1` FOREIGN KEY (`package_version_id`) REFERENCES `package_version` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package_version_bugzilla`
--

LOCK TABLES `package_version_bugzilla` WRITE;
/*!40000 ALTER TABLE `package_version_bugzilla` DISABLE KEYS */;
/*!40000 ALTER TABLE `package_version_bugzilla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package_version_cve`
--

DROP TABLE IF EXISTS `package_version_cve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package_version_cve` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `package_version_id` int(32) unsigned NOT NULL,
  `cve` varchar(24) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cve` (`cve`),
  KEY `package_version_id` (`package_version_id`),
  CONSTRAINT `package_version_cve_ibfk_1` FOREIGN KEY (`package_version_id`) REFERENCES `package_version` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package_version_cve`
--

LOCK TABLES `package_version_cve` WRITE;
/*!40000 ALTER TABLE `package_version_cve` DISABLE KEYS */;
/*!40000 ALTER TABLE `package_version_cve` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-05-17 10:24:16
