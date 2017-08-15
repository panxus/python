CREATE TABLE `article_spider` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT '0',
  `create_date` varchar(60) DEFAULT '0',
  `url` varchar(255) DEFAULT '0',
  `url_object_id` varchar(50) DEFAULT NULL,
  `front_image_url` varchar(255) DEFAULT NULL,
  `front_image_path` varchar(255) DEFAULT NULL,
  `praise_nums` int(10) DEFAULT NULL,
  `fav_nums` int(10) DEFAULT NULL,
  `comment_nums` int(10) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

