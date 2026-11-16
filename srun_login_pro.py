#!/usr/bin/env python3
"""
SRUN Authenticator - High-performance Campus Network Auth Script
Copyright (c) 2026 ClawKing (and the ghosts of the Linux Kernel mailing list)

This script is built for efficiency and correctness. No unnecessary abstractions.
"Talk is cheap. Show me the code." - Linus Torvalds
"""

import os
import sys
import json
import time
import math
import hmac
import signal
import re
import hashlib
import logging
import requests
from dataclasses import dataclass, field
from typing import Optional, List, Dict

# --- Logging Configuration ---
# Keep it standard, keep it clean.
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s: %(message)s',
    datefmt='%H:%M:%S',
    stream=sys.stdout
)
logger = logging.getLogger("SRUN")

@dataclass
class SrunConfig:
    """Repository for all configuration parameters. No globals here."""
    username: str = os.getenv('USERNAME', '').strip()
    password: str = os.getenv('PASSWORD', '').strip()
    init_url: str = os.getenv('INIT_URL', 'https://portal.ucas.ac.cn').strip()
    challenge_api: str = os.getenv('GET_CHALLENGE_API', 'https://portal.ucas.ac.cn/cgi-bin/get_challenge').strip()
    portal_api: str = os.getenv('SRUN_PORTAL_API', 'https://portal.ucas.ac.cn/cgi-bin/srun_portal').strip()
    get_ip_api: str = os.getenv('GET_IP_API', 'http://124.16.81.61/cgi-bin/rad_user_info?callback=JQuery').strip()
    health_url: str = os.getenv('HEALTH_CHECK_URL', 'https://www.baidu.com').strip()
    sleep_time: int = int(os.getenv('SLEEP_TIME', '300'))
    max_retries: int = 3
    retry_delay: int = 5
    user_agent: str = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    def validate(self):
        if not self.username or not self.password:
            logger.error("Error: USERNAME and PASSWORD must be set in the environment.")
            sys.exit(1)

@dataclass
class SrunAuthContext:
    """Internal state for a single authentication attempt."""
    ip: str = ""
    token: str = ""
    hmd5: str = ""
    chksum: str = ""
    info: str = ""
    
    # SRUN protocol constants
    ALPHA: str = "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA"
    ENC_VER: str = "srun_bx1"
    AC_ID: str = "1"
    N: str = "200"
    TYPE: str = "1"

class SrunClient:
    """The engine. Pure logic, zero fluff."""
    def __init__(self, config: SrunConfig):
        self.cfg = config
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.cfg.user_agent})
        self.running = True

        # Attach signals for clean shutdown (Linux way)
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, self._handle_exit)

    def _handle_exit(self, signum, frame):
        logger.info(f"Signal {signum} caught. Shutting down...")
        self.running = False

    def is_connected(self) -> bool:
        """Verify network reachability with minimal overhead."""
        try:
            r = self.session.get(self.cfg.health_url, timeout=5)
            return r.status_code == 200
        except Exception:
            return False

    def _get_base64(self, s: str, alpha: str) -> str:
        """Standard SRUN base64 implementation."""
        res = []
        pad = len(s) % 3
        if pad: s += '\0' * (3 - pad)
        for i in range(0, len(s), 3):
            a = ord(s[i]) << 16 | ord(s[i+1]) << 8 | ord(s[i+2])
            res.extend([alpha[a >> 18], alpha[a >> 12 & 63], alpha[a >> 6 & 63], alpha[a & 63]])
        if pad == 1: res[-1] = '='
        elif pad == 2: res[-1] = res[-2] = '='
        return "".join(res)

    def _xencode(self, msg: str, key: str) -> str:
        """The core encryption loop. Optimized for clarity and speed."""
        if not msg: return ""
        
        def sencode(m: str, k: bool) -> List[int]:
            l = len(m)
            pwd = []
            for i in range(0, l, 4):
                chunk = 0
                for j in range(4):
                    if i + j < l: chunk |= ord(m[i+j]) << (j * 8)
                pwd.append(chunk)
            if k: pwd.append(l)
            return pwd

        pwd = sencode(msg, True)
        pwdk = sencode(key, False)
        if len(pwdk) < 4: pwdk += [0] * (4 - len(pwdk))
        
        n, z, y, c = len(pwd) - 1, pwd[-1], pwd[0], 0x9E3779B9
        q = math.floor(6 + 52 / (n + 1))
        d = 0
        while q > 0:
            d = (d + c) & 0xFFFFFFFF
            e = d >> 2 & 3
            for p in range(n):
                y = pwd[p + 1]
                m = ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((d ^ y) + (pwdk[(p & 3) ^ e] ^ z))
                pwd[p] = (pwd[p] + m) & 0xFFFFFFFF
                z = pwd[p]
            y = pwd[0]
            m = ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((d ^ y) + (pwdk[(n & 3) ^ e] ^ z))
            pwd[n] = (pwd[n] + m) & 0xFFFFFFFF
            z = pwd[n]
            q -= 1
        
        # Convert back to string
        res = []
        for v in pwd:
            res.extend([chr(v & 0xFF), chr(v >> 8 & 0xFF), chr(v >> 16 & 0xFF), chr(v >> 24 & 0xFF)])
        return "".join(res)

    def authenticate(self) -> bool:
        """The main authentication state machine."""
        ctx = SrunAuthContext()
        
        try:
            # 1. Get client IP
            r = self.session.get(self.cfg.get_ip_api, timeout=10)
            m = re.search(r'jQuery\d+\((.*)\)', r.text)
            if not m: return False
            data = json.loads(m.group(1))
            ctx.ip = data.get('client_ip') or data.get('online_ip')
            logger.info(f"Local IP: {ctx.ip}")

            # 2. Get challenge token
            params = {"callback": f"jQuery{int(time.time()*1000)}", "username": self.cfg.username, "ip": ctx.ip, "_": int(time.time()*1000)}
            r = self.session.get(self.cfg.challenge_api, params=params, timeout=10)
            m = re.search('"challenge":"(.*?)"', r.text)
            if not m: return False
            ctx.token = m.group(1)
            logger.info(f"Acquired Token: {ctx.token[:8]}...")

            # 3. Cryptography
            info_dict = {"username": self.cfg.username, "password": self.cfg.password, "ip": ctx.ip, "acid": ctx.AC_ID, "enc_ver": ctx.ENC_VER}
            ctx.info = "{SRBX1}" + self._get_base64(self._xencode(json.dumps(info_dict, separators=(',', ':')), ctx.token), ctx.ALPHA)
            ctx.hmd5 = hmac.new(ctx.token.encode(), self.cfg.password.encode(), hashlib.md5).hexdigest()
            
            chkstr = ctx.token + self.cfg.username + ctx.token + ctx.hmd5 + ctx.token + ctx.AC_ID + ctx.token + ctx.ip + ctx.token + ctx.N + ctx.token + ctx.TYPE + ctx.token + ctx.info
            ctx.chksum = hashlib.sha1(chkstr.encode()).hexdigest()

            # 4. Final Login
            login_params = {
                'callback': f'jQuery{int(time.time()*1000)}', 'action': 'login', 'username': self.cfg.username,
                'password': '{MD5}' + ctx.hmd5, 'ac_id': ctx.AC_ID, 'ip': ctx.ip, 'chksum': ctx.chksum,
                'info': ctx.info, 'n': ctx.N, 'type': ctx.TYPE, 'os': 'Linux', 'name': 'Linux', 'double_stack': '0', '_': int(time.time()*1000)
            }
            r = self.session.get(self.cfg.portal_api, params=login_params, timeout=10)
            logger.info(f"Response: {r.text[:100]}")
            return "login_ok" in r.text.lower()

        except Exception as e:
            logger.error(f"Auth loop error: {e}")
            return False

    def loop(self):
        """The eternal loop of vigilance."""
        logger.info(f"Authentication starting. Interval: {self.cfg.sleep_time}s")
        while self.running:
            if not self.is_connected():
                logger.warning("Connection lost. Authenticating...")
                for i in range(self.cfg.max_retries):
                    if self.authenticate(): break
                    logger.info(f"Retry {i+1} in {self.cfg.retry_delay}s...")
                    time.sleep(self.cfg.retry_delay)
            else:
                logger.info("Connection stable.")
            
            # Sub-second responsiveness to exit signals
            for _ in range(self.cfg.sleep_time):
                if not self.running: break
                time.sleep(1)

if __name__ == '__main__':
    config = SrunConfig()
    config.validate()
    client = SrunClient(config)
    client.loop()
