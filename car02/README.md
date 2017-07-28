
 ###### 2017年7月28日

- **sql**

  ```
  CREATE TABLE `home_brand` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `firstletter` varchar(3) DEFAULT NULL COMMENT '品牌索引',
    `brand_id` int(5) DEFAULT NULL COMMENT '品牌ID',
    `brand_name` varchar(40) DEFAULT NULL COMMENT '品牌名称',
    PRIMARY KEY (`id`),
    KEY `brand_id` (`brand_id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=1063 DEFAULT CHARSET=utf8;


  CREATE TABLE `home_series` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `brand_id` int(10) DEFAULT NULL COMMENT '品牌ID',
    `series_id` int(10) DEFAULT NULL,
    `series_name` varchar(255) DEFAULT NULL,
    `series_order` int(10) DEFAULT NULL,
    `factory_id` int(10) DEFAULT NULL,
    `factory_name` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `brand_id` (`brand_id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=1679 DEFAULT CHARSET=utf8;



    CREATE TABLE `home_detail` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `type_id` int(10) DEFAULT NULL,
      `type_name` varchar(255) DEFAULT NULL,
      `maxprice` varchar(255) DEFAULT NULL,
      `minprice` varchar(255) DEFAULT NULL,
      `state` varchar(255) DEFAULT NULL,
      `years_id` int(10) DEFAULT NULL,
      `years_name` varchar(255) DEFAULT NULL,
      `series_id` int(10) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=52457 DEFAULT CHARSET=utf8;


  ```
  
 - **百度云**
 
 > 链接：http://pan.baidu.com/s/1jIxHz6I 密码：vg6d