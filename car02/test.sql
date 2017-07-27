CREATE TABLE `home_brand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstletter` varchar(3) DEFAULT NULL COMMENT '品牌索引',
  `brand_id` int(5) DEFAULT NULL COMMENT '品牌ID',
  `brand_name` varchar(40) DEFAULT NULL COMMENT '品牌名称',
  PRIMARY KEY (`id`),
  KEY `brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `home_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `series_id` int(10) DEFAULT NULL,
  `series_name` varchar(255) DEFAULT NULL,
  `maxprice` varchar(255) DEFAULT NULL,
  `minprice` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `home_series` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brand_id` int(10) DEFAULT NULL COMMENT '品牌ID',
  `firstletter` varchar(255) DEFAULT NULL,
  `series_id` int(10) DEFAULT NULL,
  `series_name` varchar(255) DEFAULT NULL,
  `factory` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
