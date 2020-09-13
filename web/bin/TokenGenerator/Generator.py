# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/13 18:44
import hmac
import base64
import random
import time
from hashlib import sha256
import string


class TokenGenerator:
    """
    Generate a token for authorized
    The token will be like JWT(JSON Web Token) but much simpler.
    The token will contain two part: Payload and Sign.
    Payload is all the info about token, pakage in JSON dict like:
        Exp: 
            {
                "name": "username",
                "uid": "uid"
            }
    Sign is a secret key that generate and encrypt by time, random number and user_info.
    """
    def __init__(self, username, uid):
        self.payload = """{"username": "%s", "uid": "%s"}""" % (username, uid)

    def new(self):
        """
        Usage: use this method to generate new token
        :Return: return a string of token
        """
        payload_base64 = self._payload_base64_generate()
        payload = str(payload_base64, "utf-8").replace("=", "")
        
        salt = self._get_salt()
        secret_key = self._encrypt(salt, payload_base64)
        sign = str(secret_key, "utf-8").replace("=", "")

        return "{}.{}".format(payload, sign)

    def _payload_base64_generate(self):
        payload_base64 = base64.b64encode(self.payload.encode("utf-8"))
        return payload_base64

    def _get_salt(self):
        combine_text = string.ascii_letters + self._get_time_stamp()
        salt = "".join(random.sample(combine_text, 16))
        return salt

    @staticmethod
    def _encrypt(salt, payload):
        secret = hmac.new(salt.encode("utf-8"), payload, sha256)
        secret_digest = secret.hexdigest()
        return base64.b64encode(secret_digest.encode("utf-8"))

    @staticmethod
    def _get_time_stamp():
        return str(round(time.time()))

if __name__ == '__main__':
    t = TokenGenerator("test", "123")
    print(t.new())
