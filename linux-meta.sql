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
  UNIQUE KEY `major_version_2` (`major_version`,`minor_version`),
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
-- Table structure for table `distro_package_group`
--

DROP TABLE IF EXISTS `distro_package_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distro_package_group` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `description` text,
  `distro_id` int(32) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`,`distro_id`),
  KEY `distro_id` (`distro_id`),
  CONSTRAINT `distro_package_group_ibfk_1` FOREIGN KEY (`distro_id`) REFERENCES `distro` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distro_package_group`
--

LOCK TABLES `distro_package_group` WRITE;
/*!40000 ALTER TABLE `distro_package_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `distro_package_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distro_package_version`
--

DROP TABLE IF EXISTS `distro_package_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distro_package_version` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `distro_id` int(32) unsigned NOT NULL,
  `package_id` int(32) unsigned DEFAULT NULL,
  `arch` varchar(24) NOT NULL,
  `checksum` varchar(255) NOT NULL,
  `epoch` int(32) unsigned NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `release` varchar(32) NOT NULL,
  `version` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `version` (`version`,`arch`),
  KEY `package_id` (`package_id`),
  KEY `full_name` (`full_name`),
  KEY `name` (`name`),
  KEY `checksum` (`checksum`),
  CONSTRAINT `distro_package_version_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `package` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distro_package_version`
--

LOCK TABLES `distro_package_version` WRITE;
/*!40000 ALTER TABLE `distro_package_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `distro_package_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distro_package_version_bugzilla`
--

DROP TABLE IF EXISTS `distro_package_version_bugzilla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distro_package_version_bugzilla` (
  `package_version_id` int(32) unsigned NOT NULL,
  `bugzilla_id` int(32) unsigned NOT NULL,
  PRIMARY KEY (`package_version_id`,`bugzilla_id`),
  CONSTRAINT `distro_package_version_bugzilla_ibfk_1` FOREIGN KEY (`package_version_id`) REFERENCES `distro_package_version` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distro_package_version_bugzilla`
--

LOCK TABLES `distro_package_version_bugzilla` WRITE;
/*!40000 ALTER TABLE `distro_package_version_bugzilla` DISABLE KEYS */;
/*!40000 ALTER TABLE `distro_package_version_bugzilla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distro_package_version_cve`
--

DROP TABLE IF EXISTS `distro_package_version_cve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distro_package_version_cve` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `distro_package_version_id` int(32) unsigned NOT NULL,
  `cve` varchar(24) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `distro_package_version_id` (`distro_package_version_id`,`cve`),
  KEY `cve` (`cve`),
  CONSTRAINT `distro_package_version_cve_ibfk_2` FOREIGN KEY (`cve`) REFERENCES `mitre_cve` (`cve`),
  CONSTRAINT `distro_package_version_cve_ibfk_1` FOREIGN KEY (`distro_package_version_id`) REFERENCES `distro_package_version` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distro_package_version_cve`
--

LOCK TABLES `distro_package_version_cve` WRITE;
/*!40000 ALTER TABLE `distro_package_version_cve` DISABLE KEYS */;
/*!40000 ALTER TABLE `distro_package_version_cve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distro_package_version_cve_no_match`
--

DROP TABLE IF EXISTS `distro_package_version_cve_no_match`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distro_package_version_cve_no_match` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `distro_package_version_id` int(32) unsigned NOT NULL,
  `cve` varchar(24) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cve` (`cve`),
  KEY `package_version_id` (`distro_package_version_id`),
  CONSTRAINT `distro_package_version_cve_no_match_ibfk_1` FOREIGN KEY (`distro_package_version_id`) REFERENCES `distro_package_version` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distro_package_version_cve_no_match`
--

LOCK TABLES `distro_package_version_cve_no_match` WRITE;
/*!40000 ALTER TABLE `distro_package_version_cve_no_match` DISABLE KEYS */;
/*!40000 ALTER TABLE `distro_package_version_cve_no_match` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distro_package_version_file`
--

DROP TABLE IF EXISTS `distro_package_version_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distro_package_version_file` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `distro_package_version_id` int(32) unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `distro_package_version_id` (`distro_package_version_id`),
  CONSTRAINT `distro_package_version_file_ibfk_1` FOREIGN KEY (`distro_package_version_id`) REFERENCES `distro_package_version` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distro_package_version_file`
--

LOCK TABLES `distro_package_version_file` WRITE;
/*!40000 ALTER TABLE `distro_package_version_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `distro_package_version_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distro_package_version_provides`
--

DROP TABLE IF EXISTS `distro_package_version_provides`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distro_package_version_provides` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `distro_package_version_id` int(32) unsigned NOT NULL,
  `flags` varchar(16) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(16) NOT NULL,
  `version` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `distro_package_version_id` (`distro_package_version_id`),
  KEY `distro_package_version_id_2` (`distro_package_version_id`),
  KEY `name` (`name`),
  CONSTRAINT `distro_package_version_provides_ibfk_1` FOREIGN KEY (`distro_package_version_id`) REFERENCES `distro_package_version` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distro_package_version_provides`
--

LOCK TABLES `distro_package_version_provides` WRITE;
/*!40000 ALTER TABLE `distro_package_version_provides` DISABLE KEYS */;
/*!40000 ALTER TABLE `distro_package_version_provides` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distro_package_version_requires`
--

DROP TABLE IF EXISTS `distro_package_version_requires`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distro_package_version_requires` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `distro_package_version_id` int(32) unsigned NOT NULL,
  `flags` varchar(16) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(16) NOT NULL,
  `version` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type` (`type`(1)),
  KEY `package_version_id` (`distro_package_version_id`),
  KEY `name` (`name`),
  CONSTRAINT `distro_package_version_requires_ibfk_1` FOREIGN KEY (`distro_package_version_id`) REFERENCES `distro_package_version` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distro_package_version_requires`
--

LOCK TABLES `distro_package_version_requires` WRITE;
/*!40000 ALTER TABLE `distro_package_version_requires` DISABLE KEYS */;
/*!40000 ALTER TABLE `distro_package_version_requires` ENABLE KEYS */;
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
-- Table structure for table `nist_cve`
--

DROP TABLE IF EXISTS `nist_cve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nist_cve` (
  `cve` varchar(16) NOT NULL,
  `description` text NOT NULL,
  `published` date DEFAULT NULL,
  `modified` date DEFAULT NULL,
  `title` varchar(16) NOT NULL,
  PRIMARY KEY (`cve`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nist_cve`
--

LOCK TABLES `nist_cve` WRITE;
/*!40000 ALTER TABLE `nist_cve` DISABLE KEYS */;
/*!40000 ALTER TABLE `nist_cve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nist_cve_reference`
--

DROP TABLE IF EXISTS `nist_cve_reference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nist_cve_reference` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `cve` varchar(16) NOT NULL,
  `url` varchar(1024) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cve` (`cve`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nist_cve_reference`
--

LOCK TABLES `nist_cve_reference` WRITE;
/*!40000 ALTER TABLE `nist_cve_reference` DISABLE KEYS */;
/*!40000 ALTER TABLE `nist_cve_reference` ENABLE KEYS */;
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
  PRIMARY KEY (`id`)
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
-- Table structure for table `package_to_distro_group_map`
--

DROP TABLE IF EXISTS `package_to_distro_group_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package_to_distro_group_map` (
  `package_id` int(32) unsigned NOT NULL,
  `distro_package_group_id` int(32) unsigned NOT NULL,
  PRIMARY KEY (`package_id`,`distro_package_group_id`),
  KEY `distro_package_group_id` (`distro_package_group_id`),
  CONSTRAINT `package_to_distro_group_map_ibfk_2` FOREIGN KEY (`distro_package_group_id`) REFERENCES `distro_package_group` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `package_to_distro_group_map_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `package` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package_to_distro_group_map`
--

LOCK TABLES `package_to_distro_group_map` WRITE;
/*!40000 ALTER TABLE `package_to_distro_group_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `package_to_distro_group_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package_to_required_package_map`
--

DROP TABLE IF EXISTS `package_to_required_package_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package_to_required_package_map` (
  `package_id` int(32) unsigned NOT NULL,
  `required_package_id` int(32) unsigned NOT NULL,
  PRIMARY KEY (`package_id`,`required_package_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package_to_required_package_map`
--

LOCK TABLES `package_to_required_package_map` WRITE;
/*!40000 ALTER TABLE `package_to_required_package_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `package_to_required_package_map` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-05-20 17:19:56
