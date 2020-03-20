# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: patt-db (MySQL 5.7.13-log)
# Database: pathogen_software
# Generation Time: 2020-03-20 16:21:17 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table container
# ------------------------------------------------------------

DROP TABLE IF EXISTS `container`;

CREATE TABLE `container` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `image` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table executable
# ------------------------------------------------------------

DROP TABLE IF EXISTS `executable`;

CREATE TABLE `executable` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `container_id` int(10) unsigned NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `container_id` (`container_id`),
  CONSTRAINT `executable_ibfk_1` FOREIGN KEY (`container_id`) REFERENCES `container` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table module_usage
# ------------------------------------------------------------

DROP TABLE IF EXISTS `module_usage`;

CREATE TABLE `module_usage` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(16) NOT NULL DEFAULT '',
  `timestamp` varchar(16) NOT NULL DEFAULT '',
  `executable_id` int(11) unsigned NOT NULL,
  `path` int(11) unsigned DEFAULT NULL COMMENT 'in table text',
  `parameters` int(10) unsigned DEFAULT NULL COMMENT 'in table text',
  PRIMARY KEY (`id`),
  KEY `executable_id` (`executable_id`),
  KEY `path` (`path`),
  KEY `parameters` (`parameters`),
  KEY `user` (`user`),
  KEY `timestamp` (`timestamp`),
  CONSTRAINT `module_usage_ibfk_1` FOREIGN KEY (`executable_id`) REFERENCES `executable` (`id`),
  CONSTRAINT `module_usage_ibfk_2` FOREIGN KEY (`path`) REFERENCES `text` (`id`),
  CONSTRAINT `module_usage_ibfk_3` FOREIGN KEY (`parameters`) REFERENCES `text` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table text
# ------------------------------------------------------------

DROP TABLE IF EXISTS `text`;

CREATE TABLE `text` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `text` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `text` (`text`(200))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table vw_rows
# ------------------------------------------------------------

DROP VIEW IF EXISTS `vw_rows`;

CREATE TABLE `vw_rows` (
   `user` VARCHAR(16) NOT NULL DEFAULT '',
   `timestamp` VARCHAR(16) NOT NULL DEFAULT '',
   `image` VARCHAR(255) NOT NULL DEFAULT '',
   `executable` VARCHAR(255) NULL DEFAULT NULL,
   `path` LONGTEXT NULL DEFAULT NULL,
   `parameters` LONGTEXT NULL DEFAULT NULL
) ENGINE=MyISAM;





# Replace placeholder table for vw_rows with correct view syntax
# ------------------------------------------------------------

DROP TABLE `vw_rows`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pathpipe_admin`@`%` SQL SECURITY DEFINER VIEW `vw_rows`
AS SELECT
   `module_usage`.`user` AS `user`,
   `module_usage`.`timestamp` AS `timestamp`,
   `container`.`image` AS `image`,
   `executable`.`name` AS `executable`,(select `text`.`text`
FROM `text` where (`text`.`id` = `module_usage`.`path`)) AS `path`,(select `text`.`text` from `text` where (`text`.`id` = `module_usage`.`parameters`)) AS `parameters` from ((`module_usage` join `executable`) join `container`) where ((`module_usage`.`executable_id` = `executable`.`id`) and (`executable`.`container_id` = `container`.`id`));

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
