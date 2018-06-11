# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import logging
import random
import time

import requests
import fake_useragent

from tools.database_tools import insert_proxy_info, update_proxy_info_use_times, update_proxy_info_invalid


class HttpProxyMiddleware(object):

    def __init__(self, proxy_server_url, proxy_verify_url, proxy_retry_times, proxy_extra_delay_seconds, proxy_info_list_max_size, proxy_info_list_min_size):
        self.proxy_server_url = proxy_server_url
        self.proxy_verify_url = proxy_verify_url
        self.proxy_retry_times = proxy_retry_times
        self.proxy_extra_delay_seconds = proxy_extra_delay_seconds
        self.proxy_info_list = []
        self.proxy_info_list_max_size = proxy_info_list_max_size
        self.proxy_info_list_min_size = proxy_info_list_min_size

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_server_url=crawler.settings.get('PROXY_SERVER_URL'),
            proxy_verify_url=crawler.settings.get('PROXY_VERIFY_URL'),
            proxy_retry_times=crawler.settings.get('PROXY_RETRY_TIMES'),
            proxy_extra_delay_seconds=crawler.settings.get('PROXY_EXTRA_DELAY_SECONDS'),
            proxy_info_list_max_size=crawler.settings.get('PROXY_INFO_LIST_MAX_SIZE'),
            proxy_info_list_min_size=crawler.settings.get('PROXY_INFO_LIST_MIN_SIZE')
        )

    def reload_proxy_info_list(self):
        """
        刷新代理信息列表（每批次取3个代理）
        {"code":0,"success":true,"msg":"","data":[{"IP":"0.0.0.0","Port":8080,"ExpireTime":"2018-01-01 08:08:08","IpAddress":"湖南省益阳市 电信","ISP":"电信"},{"IP":"0.0.0.0","Port":8080,"ExpireTime":"2018-01-01 08:08:08","IpAddress":"湖南省益阳市 电信","ISP":"电信"}]}
        :return:
        """
        try:
            if len(self.proxy_info_list) < self.proxy_info_list_max_size:
                response = requests.get(url=self.proxy_server_url, timeout=5)
                time.sleep(self.proxy_extra_delay_seconds)
                response_status_code = response.status_code
                if response_status_code != 200:
                    raise Exception('wrong status code %s' % response_status_code)
                response_text = response.text
                if response_text is None or response_text == '':
                    raise Exception('none response')
                response_json = json.loads(response_text)
                if 'code' not in response_json or 'data' not in response_json:
                    raise Exception('no code or data, response is %s' % response_json)
                if response_json['code'] == 10000:
                    time.sleep(1.5)
                    self.reload_proxy_info_list()
                if response_json['code'] != 0 or len(response_json['data']) <= 0:
                    raise Exception('invalid code or data %s' % response_json)
                proxy_data_list = response_json['data']
                for proxy_data in proxy_data_list:
                    if 'Port' in proxy_data and 'IP' in proxy_data:
                        proxy_info = {'ip': proxy_data["IP"], 'port': proxy_data["Port"]}
                    else:
                        proxy_ip_and_port = proxy_data["IP"].split(':')
                        proxy_info = {'ip': proxy_ip_and_port[0], 'port': proxy_ip_and_port[1]}
                    self.proxy_info_list.append(proxy_info)
                    insert_proxy_info(proxy_info['ip'], proxy_info['port'], proxy_data['ISP'], proxy_data['IpAddress'])
                logging.debug('reload proxy info list, proxy data list is %s' % proxy_data_list)
            else:
                logging.warn('reload proxy info list, already has enough data')
        except Exception as e:
            logging.exception('get proxy ip list from proxy server has an error')

    def set_proxy(self, request, proxy_ip, proxy_port):
        """
        设置代理
        :param request: 原始请求
        :param proxy_ip: 代理IP
        :param proxy_port: 代理端口
        :return:
        """
        request.meta['proxy_ip'] = proxy_ip
        request.meta['proxy_port'] = proxy_port
        request.meta['proxy'] = 'http://%s:%s' % (proxy_ip, proxy_port)
        logging.debug('set proxy: proxy_ip is %s, proxy_port is %s' % (proxy_ip, proxy_port))

    def verify_proxy(self, proxy_ip, proxy_port):
        """
        验证代理
        :return:
        """
        response = requests.get(self.proxy_verify_url, timeout=5, proxies={'http': 'http://%s:%s' % (proxy_ip, proxy_port)})
        if response.status_code == 200:
            logging.debug('verify proxy %s' % response.text)
        else:
            raise Exception('verify proxy fail')

    def use_proxy(self, request):
        """
        使用代理（如果代理不可用则从代理列表中移除）
        :param retry_times: 重试次数
        :param request: 原始请求
        :return:
        """
        time.sleep(1)
        retry_times = request.meta['proxy_retry_times']
        if 'proxy_ip' in request.meta and 'proxy_port' in request.meta:
            proxy_ip = request.meta['proxy_ip']
            proxy_port = request.meta['proxy_port']
            proxy_info = {'ip': proxy_ip, 'port': proxy_port}
        try:
            if retry_times > self.proxy_retry_times:
                logging.error('no enough retry times, url is %s' % request.url)
                if proxy_info and proxy_info in self.proxy_info_list:
                    update_proxy_info_invalid(proxy_ip, proxy_ip, 'retry time is great than %s times' % retry_times)
                    self.proxy_info_list.remove(proxy_info)
                return False
            if len(self.proxy_info_list) <= self.proxy_info_list_min_size:
                self.reload_proxy_info_list()
            if len(self.proxy_info_list) > 0:
                proxy_info = random.choice(self.proxy_info_list)
                proxy_ip = proxy_info['ip']
                proxy_port = proxy_info['port']
                self.set_proxy(request, proxy_ip, proxy_port)
                self.verify_proxy(proxy_ip, proxy_port)
                logging.info('use proxy: request_url is %s, proxy_info is %s, proxy_retry_times is %s' % (request.url, proxy_info, retry_times))
                update_proxy_info_use_times(proxy_ip, proxy_port)
                request.meta['proxy_retry_times'] = retry_times + 1
            else:
                raise Exception('no data in proxy info list')
        except Exception as e:
            logging.error('user proxy error, reason is %s' % e.message)
            request.meta['proxy_retry_times'] = retry_times + 1
            self.use_proxy(request)
        return True

    def process_request(self, request, spider):
        if not request.meta.get('proxy') or not request.meta['proxy_retry_times']:
            request.meta['proxy_retry_times'] = 0
            self.use_proxy(request)

    def process_response(self, request, response, spider):
        index_html = response.body
        index_json = json.loads(index_html)
        if 'data' in index_json:
            data = index_json['data']
            if len(data) == 0:
                need_retry = self.use_proxy(request)
                if need_retry:
                    return request
        return response

    def process_exception(self, request, exception, spider):
        error_proxy = request.meta.get('proxy')
        if not error_proxy:
            return None


class UserAgentMiddleware(object):

    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent_list=crawler.settings.get('USER_AGENT_LIST')
        )

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = fake_useragent.UserAgent().random
