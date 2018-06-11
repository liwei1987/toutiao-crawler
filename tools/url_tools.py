# -*- coding: utf-8 -*-

import hashlib
import time


def get_sign():
    """
    获取签名
    :return: 签名
    """
    t = int(time.time())
    e = hex(t)[2:].upper()
    m2 = hashlib.md5()
    m2.update(str(t))
    n = str(m2.hexdigest()).upper()
    if (8 != len(e)):
        return {'as': "479BB4B7254C150", 'cp': "7E0AC8874BB0985"}
    o = n[0:5]
    i = n[-5:]
    a = ""
    for r in range(5):
        a += o[r] + e[r]
    l = ""
    for s in range(5):
        l += e[s + 3] + i[s];
    return {'as': "A1" + a + e[-3:], 'cp': e[0:3] + l + "E1"}


def get_index_url(user_id, media_id):
    """
    获取index域名
    :return:
    """
    sign = get_sign()
    sign_as = sign['as']
    sign_cp = sign['cp']
    url = 'https://toutiao.com/pgc/ma/?page_type=1&max_behot_time=0&uid={}&media_id={}&output=json&is_json=1&count=50&version=2&as={}&cp={}'.format(user_id, media_id, sign_as, sign_cp)
    return url
