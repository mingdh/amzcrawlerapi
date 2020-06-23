# coding=utf-8
from .orm import *

"""
CREATE TABLE `proxys` (
  `id` int(10) UNSIGNED NOT NULL,
  `ip` varchar(60) NOT NULL COMMENT 'ip addr',
  `port` varchar(16) NOT NULL COMMENT 'port number',
  `name` varchar(30) NOT NULL COMMENT 'proxy name',
  `enable` varchar(15) NOT NULL COMMENT 'enable, disable,del',
  `lastused` varchar(30) NOT NULL COMMENT 'Y-m-d hh:mm:ss'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
class proxys(Model):
    __table__ = 'proxys'
    
    # 定义类的属性到列的映射：
    id = IntegerField('id',primary_key = True)
    ip = StringField('ip',ddl='varchar(60)')
    port = StringField('port',ddl='varchar(16)')
    name = StringField('name',ddl='varchar(30)')
    enable = StringField('enable',ddl='varchar(15)')
    lastused = StringField('lastused',ddl='varchar(30)')

"""
CREATE TABLE `headers` (
  `id` int(10) UNSIGNED NOT NULL,
  `header` varchar(500) NOT NULL COMMENT 'browser header',
  `comment` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
class headers(Model):
    __table__ = 'headers'
    
    # 定义类的属性到列的映射：
    id = IntegerField('id',primary_key = True)
    header = StringField('header',ddl='varchar(500)')
    comment = StringField('comment',ddl='varchar(100)')
    