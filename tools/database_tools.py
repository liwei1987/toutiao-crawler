# -*- coding: utf-8 -*-

import logging

import MySQLdb


def get_spider_conn():
    db_host = '127.0.0.1'
    db_port = 3306
    db_user = 'spider'
    db_passwd = 'spider0928'
    db = 'spider'
    conn = MySQLdb.Connect(host=db_host, user=db_user, passwd=db_passwd, db=db, port=db_port, charset='utf8mb4', use_unicode=True)
    return conn


def set_utf8mb4_encoding(spider_conn, spider_cursor):
    spider_cursor.execute('SET NAMES utf8mb4')
    spider_cursor.execute("SET CHARACTER SET utf8mb4")
    spider_cursor.execute("SET character_set_connection=utf8mb4")
    spider_conn.commit()


def insert_proxy_info(ip, port, isp_name, location_name):
    """
    插入代理信息到数据库
    :param ip: ip地址
    :param port: 端口
    :param isp_name: 服务提供商名称
    :param location_name: 地理位置名称
    :return:
    """
    spider_conn = get_spider_conn()
    spider_cursor = spider_conn.cursor()
    set_utf8mb4_encoding(spider_conn, spider_cursor)
    insert = 'insert into spider_proxy_info(ip, port, isp_name, location_name, provider) values ("%s", "%s", "%s", "%s", "%s")' % (ip, port, isp_name, location_name, 'et')
    result = spider_cursor.execute(insert)
    spider_conn.commit()
    spider_cursor.close()
    spider_conn.close()
    logging.debug(insert + ', result is %s' % result)


def update_proxy_info_use_times(ip, port):
    """
    更新代理信息使用次数到数据库
    :param ip: ip地址
    :param port: 端口
    :return:
    """
    spider_conn = get_spider_conn()
    spider_cursor = spider_conn.cursor()
    set_utf8mb4_encoding(spider_conn, spider_cursor)
    update = 'update spider_proxy_info set total_use_times = total_use_times + 1 where ip = "%s" and port = "%s"' % (ip, port)
    result = spider_cursor.execute(update)
    spider_conn.commit()
    spider_cursor.close()
    spider_conn.close()
    logging.debug(update + ', result is %s' % result)


def update_proxy_info_invalid(ip, port, invalid_reason):
    """
    更新代理信息为失效到数据库
    :param ip: ip地址
    :param port: 端口
    :return:
    """
    spider_conn = get_spider_conn()
    spider_cursor = spider_conn.cursor()
    set_utf8mb4_encoding(spider_conn, spider_cursor)
    update = 'update spider_proxy_info set status = -1, invalid_reason = "%s" where ip = "%s" and port = "%s"' % (invalid_reason, ip, port)
    result = spider_cursor.execute(update)
    spider_conn.commit()
    spider_cursor.close()
    spider_conn.close()
    logging.debug(update + ', result is %s' % result)


def insert_toutiao_article(item):
    """
    插入头条文章到数据库
    :param item:
    :return:
    """
    spider_conn = get_spider_conn()
    spider_cursor = spider_conn.cursor()
    set_utf8mb4_encoding(spider_conn, spider_cursor)
    insert = """
    INSERT INTO spider_toutiao_article 
    (item_id,user_id,media_id,article_url,title,read_count,share_count,content_type,publish_time) 
    VALUES ("%s","%s","%s","%s","%s",%s,%s,%s,"%s")
    ON DUPLICATE KEY UPDATE read_count=VALUES(read_count),share_count=VALUES(share_count)
    """ % (item['item_id'], item['user_id'], item['media_id'], item['article_url'], item['title'], item['read_count'], item['share_count'], item['content_type'], item['datetime'])
    result = spider_cursor.execute(insert)
    spider_conn.commit()
    spider_cursor.close()
    spider_conn.close()
    logging.debug(insert + ', result is %s' % result)
