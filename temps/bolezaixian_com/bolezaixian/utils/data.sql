CREATE TABLE `article_spider` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT '0',
  `create_date` varchar(60) DEFAULT '0',
  `url` varchar(255) DEFAULT '0',
  `url_object_id` varchar(50) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `z_num` int(10) DEFAULT NULL,
  `sc_num` int(10) DEFAULT NULL,
  `pl_num` int(10) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `content` longtext,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=125 DEFAULT CHARSET=utf8;

CREATE TABLE `zh_question` (
  `question_id` int(11) unsigned NOT NULL,
  `question_url` varchar(255) DEFAULT '0',
  `question_title` varchar(200) DEFAULT '0',
  `question_topic` varchar(200) DEFAULT NULL,
  `question_content` longtext,
  `question_pinglun` int(10) DEFAULT NULL,
  `question_huida` int(10) DEFAULT NULL,
  `question_guanzhu` int(10) DEFAULT NULL,
  PRIMARY KEY (`question_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `zh_answer` (
  `answer_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `question_id` varchar(60) DEFAULT '0',
  `created` varchar(60) DEFAULT '0',
  `updated` varchar(60) DEFAULT '0',
  `crawl` varchar(60) DEFAULT '0',
  `answer_content` longtext,
  `answer_excerpt` longtext,
  `answer_author_name` varchar(255) DEFAULT NULL,
  `answer_author_id` varchar(255) DEFAULT NULL,
  `answer_pl` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`answer_id`)
) ENGINE=MyISAM AUTO_INCREMENT=145239316 DEFAULT CHARSET=utf8;
