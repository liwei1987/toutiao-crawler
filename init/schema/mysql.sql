-- mysql -u root -p

CREATE DATABASE spider;

CREATE USER `spider`@`localhost` IDENTIFIED BY 'spider0928';

GRANT ALL ON `spider`.* TO `spider`@`%`;

USE spider;

CREATE TABLE `spider_proxy_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ip` varchar(64) NOT NULL DEFAULT '' COMMENT '代理IP',
  `port` varchar(16) NOT NULL DEFAULT '' COMMENT '代理端口',
  `isp_name` varchar(128) NOT NULL DEFAULT '' COMMENT '服务提供商名称',
  `location_name` varchar(256) NOT NULL DEFAULT '' COMMENT '地理位置描述名称',
  `provider` varchar(64) NOT NULL DEFAULT '' COMMENT '代理提供商',
  `total_use_times` int(11) NOT NULL DEFAULT 0 COMMENT '总使用次数',
  `status` tinyint NOT NULL DEFAULT 0 COMMENT '0表示正常，-1表示下线',
  `invalid_reason` varchar(2000) NOT NULL DEFAULT '' COMMENT '失效原因',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY idx_ip_port (`ip`, `port`),
  KEY idx_status (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='抓取代理表';

CREATE TABLE `spider_toutiao_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(64) NOT NULL DEFAULT '' COMMENT '用户ID',
  `media_id` varchar(64) NOT NULL DEFAULT '' COMMENT '媒体ID',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '用户名称',
  `status` tinyint NOT NULL DEFAULT 0 COMMENT '0表示正常，-1表示下线',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY idx_user_media_id (`user_id`, `media_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='抓取头条用户表';

CREATE TABLE `spider_toutiao_article` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `item_id` varchar(256) NOT NULL DEFAULT '' COMMENT '文章ID',
  `user_id` varchar(64) NOT NULL DEFAULT '' COMMENT '用户ID',
  `media_id` varchar(64) NOT NULL DEFAULT '' COMMENT '媒体ID',
  `article_url` varchar(512) NOT NULL DEFAULT '' COMMENT '文章URL',
  `title` varchar(256) NOT NULL DEFAULT '' COMMENT '文章标题',
  `read_count` int(11) NOT NULL DEFAULT '0' COMMENT '阅读数',
  `share_count` int(11) NOT NULL DEFAULT '0' COMMENT '分享数',
  `content_type` smallint(6) DEFAULT '0' COMMENT '0：普通帖子 1：音频帖子 2：视频帖子',
  `publish_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '原贴发布时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='抓取头条文章表';

CREATE TABLE `spider_toutiao_article_content` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `content` varchar(8192) NOT NULL DEFAULT '' COMMENT '文章内容',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='抓取头条文章内容表';