DROP TABLE IF EXISTS `logging_event`;

CREATE TABLE `logging_event` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uuid` char(36) NOT NULL DEFAULT '',
  `user` varchar(16) NOT NULL DEFAULT '',
  `timestamp` datetime NOT NULL,
  `image` varchar(255) NOT NULL DEFAULT '',
  `executable` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `parameters` mediumtext,
  `origin` set('api','logfile') NOT NULL DEFAULT 'api',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `user` (`user`),
  KEY `image` (`image`),
  KEY `timestamp` (`timestamp`),
  KEY `user_2` (`user`,`image`,`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;