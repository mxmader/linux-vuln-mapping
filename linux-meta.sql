-- phpMyAdmin SQL Dump
-- version 3.5.8.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 18, 2014 at 07:33 PM
-- Server version: 5.5.34-MariaDB
-- PHP Version: 5.5.9

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `linux-meta`
--

-- --------------------------------------------------------

--
-- Table structure for table `distro`
--

CREATE TABLE IF NOT EXISTS `distro` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `name` enum('CentOS','Fedora','Oracle Linux','RHEL','Scientific Linux') NOT NULL,
  `family` enum('enterprise','fedora') NOT NULL,
  `major_version` int(8) unsigned NOT NULL,
  `minor_version` int(8) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `major_version` (`major_version`,`minor_version`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `package`
--

CREATE TABLE IF NOT EXISTS `package` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `distro_id` int(32) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `distro_id` (`distro_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `package_group`
--

CREATE TABLE IF NOT EXISTS `package_group` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `distro` int(32) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`,`distro`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `package_version`
--

CREATE TABLE IF NOT EXISTS `package_version` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `version` varchar(24) NOT NULL,
  `arch` varchar(24) NOT NULL,
  `release_number` int(8) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `version` (`version`,`arch`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `package_version_bugzilla`
--

CREATE TABLE IF NOT EXISTS `package_version_bugzilla` (
  `package_version_id` int(32) unsigned NOT NULL,
  `bugzilla_id` int(32) unsigned NOT NULL,
  PRIMARY KEY (`package_version_id`,`bugzilla_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `package_version_cve`
--

CREATE TABLE IF NOT EXISTS `package_version_cve` (
  `package_version_id` int(32) unsigned NOT NULL,
  `cve` varchar(24) NOT NULL,
  KEY `cve` (`cve`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
