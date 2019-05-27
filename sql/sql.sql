CREATE TABLE `tb_wh_vegetables_price` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `price_max` double(255,3) DEFAULT NULL,
  `price_min` double(255,3) DEFAULT NULL,
  `price_avg` double(255,3) DEFAULT NULL,
  `date_value` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;