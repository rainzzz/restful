import time
import hashlib
from urllib.parse import urlencode
import json

import requests


class RBACLogin:
    RBAC_SITE_ID = 53
    RBAC_SECRET_KEY = "1a695db3-20a6-4f03-bcf8-09a1bd91f230"
    RBAC_USER_SALT_URL = 'http://rbac.api.xq5.com/auth/salt'
    RBAC_USER_DATA_URL = "http://rbac.api.xq5.com/auth/login"

    def __init__(self, login_name, password):
        self.login_name = login_name
        self.password = password
        self.t = int(time.time())

    def hexdigest_password(self, algorithm, salt, raw_password):
        """
        Returns a string of the hexdigest of the given plaintext password and salt
        using the given algorithm ('md5', 'sha1' or 'crypt').
        """
        raw_password, salt = raw_password, salt
        if algorithm == 'crypt':
            try:
                import crypt
            except ImportError:
                raise ValueError('"crypt" password algorithm not \
                    supported in this environment')
            return crypt.crypt(raw_password, salt)

        if algorithm == 'md5':
            return hashlib.md5((salt + raw_password).encode(encoding='utf-8')).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(salt + raw_password).hexdigest()
        raise ValueError("Got unknown password algorithm type in password.")

    def sort_hash_urlencode(self, d, pop_keys=None):
        """对字典进行排序, 按照key的顺序从小到大进行排列"""
        d2 = d.copy()

        # 剔除不参与排序的key
        if pop_keys is not None:
            for k in pop_keys:
                if k in d2:
                    d2.pop(k)

        d3 = sorted(d2.items(), key=lambda m: m[0])
        return "&".join(['%s=%s' % i for i in d3])

    def hexdigest_hash(self, pop_keys=None, **kwargs):
        """对请求参数进行签名"""
        if 'secret_key' not in kwargs:
            raise Exception("secret_key is required.")
        secert_key = kwargs.pop('secret_key')

        request_str = self.sort_hash_urlencode(kwargs, pop_keys=pop_keys)
        unsigned_str = "%s%s" % (request_str, secert_key)
        return hashlib.md5(unsigned_str.encode(encoding='utf-8')).hexdigest()

    def validate(self):
        salt = self.get_user_salt()
        if salt:
            user = self.get_user(salt)
            return user
        return None

    def get_user(self, salt):
        password = self.hexdigest_password("md5", salt, self.password)
        sign = self.hexdigest_hash(secret_key=self.RBAC_SECRET_KEY, login_name=self.login_name,
                                   login_password=password, t=self.t, site_id=self.RBAC_SITE_ID)
        request_args = dict(login_name=self.login_name, login_password=password, t=self.t,
                            site_id=self.RBAC_SITE_ID, sign=sign)
        request_url = "%s?%s" % (self.RBAC_USER_DATA_URL, urlencode(request_args))
        r = requests.get(request_url)
        if r.status_code == 200:
            rr = json.loads(r.text)
            if rr['status'] == 200:
                return rr['user']
        else:
            raise Exception('账号或密码错误')

    def get_user_salt(self):
        sign = self.hexdigest_hash(secret_key=self.RBAC_SECRET_KEY, login_name=self.login_name, t=self.t,
                                   site_id=self.RBAC_SITE_ID)
        request_args = dict(login_name=self.login_name, t=self.t, sign=sign, site_id=self.RBAC_SITE_ID)
        request_url = "%s?%s" % (self.RBAC_USER_SALT_URL, urlencode(request_args))
        r = requests.get(request_url)
        if r.status_code == 200:
            rr = json.loads(r.text)
            if rr['status'] == 200:
                return rr['salt']
        else:
            raise Exception('RBAC 接口异常')


if __name__ == '__main__':
    rbac = RBACLogin('zhangyuwei', '123456')
    print(rbac.validate())
