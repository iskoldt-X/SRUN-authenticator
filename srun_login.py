#!/usr/bin/python3
import hashlib
import hmac
import json
import math
import os
import re
import time

import requests

username = ''
password = ''
get_ip_api = ''
get_challenge_api = ''
srun_portal_api = ''
sleep_time = 300
max_retries = 10  # 最大重连次数

if username == '':
    username = os.getenv('USERNAME').strip()
if password == '':
    password = os.getenv('PASSWORD').strip()
if get_challenge_api == '':
    get_challenge_api = os.getenv('get_challenge_api').strip()
if srun_portal_api == '':
    srun_portal_api = os.getenv('srun_portal_api').strip()
if get_ip_api == '':
    get_ip_api = os.getenv('get_ip_api').strip()

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0'
                  'Safari/537.36 Edg/120.0.0.0'
}

n = '200'
type = '1'  # 常量，作用未知
ac_id = '1'  # 常量，作用未知
enc = "srun_bx1"  # 常量，作用未知

_ALPHA = "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA"


def get_base64(s):
    s: str
    r = []
    x = len(s) % 3
    if x:
        s = s + '\0' * (3 - x)
    for i in range(0, len(s), 3):
        d = s[i:i + 3]
        a = ord(d[0]) << 16 | ord(d[1]) << 8 | ord(d[2])
        r.append(_ALPHA[a >> 18])
        r.append(_ALPHA[a >> 12 & 63])
        r.append(_ALPHA[a >> 6 & 63])
        r.append(_ALPHA[a & 63])
    if x == 1:
        r[-1] = '='
        r[-2] = '='
    if x == 2:
        r[-1] = '='
    return ''.join(r)


def get_hmd5():
    global password, token
    return hmac.new(token.encode(), password.encode(), hashlib.md5).hexdigest()


def ordat(msg, idx):
    if len(msg) > idx:
        return ord(msg[idx])
    return 0


def sencode(msg, key):
    l = len(msg)
    pwd = []
    for i in range(0, l, 4):
        pwd.append(
            ordat(msg, i) | ordat(msg, i + 1) << 8 | ordat(msg, i + 2) << 16
            | ordat(msg, i + 3) << 24)
    if key:
        pwd.append(l)
    return pwd


def lencode(msg, key):
    l = len(msg)
    ll = (l - 1) << 2
    if key:
        m = msg[l - 1]
        if m < ll - 3 or m > ll:
            return
        ll = m
    for i in range(0, l):
        msg[i] = chr(msg[i] & 0xff) + chr(msg[i] >> 8 & 0xff) + chr(
            msg[i] >> 16 & 0xff) + chr(msg[i] >> 24 & 0xff)
    if key:
        return "".join(msg)[0:ll]
    return "".join(msg)


def get_xencode(msg, key):
    if msg == "":
        return ""
    pwd = sencode(msg, True)
    pwdk = sencode(key, False)
    if len(pwdk) < 4:
        pwdk = pwdk + [0] * (4 - len(pwdk))
    n = len(pwd) - 1
    z = pwd[n]
    y = pwd[0]
    c = 0x86014019 | 0x183639A0
    m = 0
    e = 0
    p = 0
    q = math.floor(6 + 52 / (n + 1))
    d = 0
    while 0 < q:
        d = d + c & (0x8CE0D9BF | 0x731F2640)
        e = d >> 2 & 3
        p = 0
        while p < n:
            y = pwd[p + 1]
            m = z >> 5 ^ y << 2
            m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
            m = m + (pwdk[(p & 3) ^ e] ^ z)
            pwd[p] = pwd[p] + m & (0xEFB8D130 | 0x10472ECF)
            z = pwd[p]
            p = p + 1
        y = pwd[0]
        m = z >> 5 ^ y << 2
        m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
        m = m + (pwdk[(p & 3) ^ e] ^ z)
        pwd[n] = pwd[n] + m & (0xBB390742 | 0x44C6F8BD)
        z = pwd[n]
        q = q - 1
    return lencode(pwd, False)


def get_sha1(value):
    return hashlib.sha1(value.encode()).hexdigest()


def get_chksum():
    parts = [
        token + username,
        token + hmd5,
        token + ac_id,
        token + ip,
        token + n,
        token + type,
        token + i
    ]
    return get_sha1(''.join(parts))


def get_info():
    info_temp = {
        "username": username,
        "password": password,
        "ip": ip,
        "acid": ac_id,
        "enc_ver": enc
    }
    i = re.sub("'", '"', str(info_temp))
    i = re.sub(" ", '', i)
    return i


def get_ip():
    """
    获取ip并返回ip字符串
    """
    res = requests.get(get_ip_api)
    # [7:-1]是为了去掉前面的 jQuery( 和后面的 )
    data = json.loads(res.text[7:-1])
    return data.get('client_ip') or data.get('online_ip')


def get_token():
    get_challenge_params = {
        "callback": "jQuery112404953340710317169_" + str(int(time.time() * 1000)),
        "username": username,
        "ip": ip,
        "_": int(time.time() * 1000),
    }
    get_challenge_res_text = requests.Session().get(get_challenge_api, params=get_challenge_params, headers=header).text
    return re.search('"challenge":"(.*?)"', get_challenge_res_text).group(1)


def get_i():
    return "{SRBX1}" + get_base64(get_xencode(get_info(), token))


def login():
    srun_portal_params = {
        'callback': 'jQuery11240645308969735664_' + str(int(time.time() * 1000)),
        'action': 'login',
        'username': username,
        'password': '{MD5}' + hmd5,
        'ac_id': ac_id,
        'ip': ip,
        'chksum': chksum,  # chk也许是check的缩写
        'info': i,
        'n': n,
        'type': type,
        'os': 'windows+10',
        'name': 'windows',
        'double_stack': '0',
        '_': int(time.time() * 1000)
    }
    # print(srun_portal_params)
    srun_portal_res = requests.Session().get(srun_portal_api, params=srun_portal_params, headers=header)

    print(get_current_time(), flush=True, end=" ")
    print(srun_portal_res.text, flush=True)


def check_network(url="https://www.baidu.com", timeout=2):
    try:
        with requests.Session() as session:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()  # 如果响应状态码不是200，将引发HTTPError异常
        return True
    except requests.exceptions.RequestException:
        return False


def get_current_time():
    """
    获取当前时间并以 'YYYY-MM-DD HH:MM:SS' 的格式返回。
    """
    current_time = time.localtime(time.time())  # 获取当前时间的时间元组
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)  # 将时间元组格式化为字符串
    return formatted_time


if __name__ == '__main__':
    while True:
        retry_count = 0  # 重置重连计数器
        while not check_network():
            # 如果网络未连接，增加重连计数
            retry_count += 1

            ip = get_ip()
            print(get_current_time() + "ip:" + ip, flush=True)

            token = get_token()
            print(get_current_time() + "token为:" + token, flush=True)

            i = get_i()
            hmd5 = get_hmd5()
            chksum = get_chksum()

            login()

            # 检查是否达到了最大重连次数
            # 如果达到最大重连次数，等待一段时间后再次尝试
            if retry_count >= max_retries:
                print("已达到最大重连次数，暂停连接稍后再试")
                retry_count = 0
                time.sleep(sleep_time)
        print(get_current_time(), flush=True, end=" ")
        print('已通过认证，无需再次认证')

        # 等待一段时间
        time.sleep(sleep_time)
