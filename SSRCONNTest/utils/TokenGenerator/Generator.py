# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/13 18:44
import hmac
import base64
import time
from hashlib import sha256
import string
import secrets


class TokenGenerator:
    """
    Generate a token for authorized
    The token will be like JWT(JSON Web Token) but much simpler.
    The token using a time stamp which generated when using `TokenGenerator.new()` methods,
    and randomize it with `string.ascii` to generate key.
    Use this key to encrypt payload with SHA256 algorithms.
    Payload is all the info about token, pakage in JSON dict like:
        Exp: 
            {
                "name": "username",
                "uid": "uid"
            }
    Sign is a secret key that generate and encrypt by time, random number and user_info.
    """
    def new(self, username, uid):
        """
        Usage: use this method to generate new token
        :Return: return a tuple of encrypt key and token
        """
        self.payload = """{"username": "%s", "uid": "%s"}""" % (username, uid)
        payload_base64 = self._payload_base64_generate()
        
        salt = self.get_salt(16)
        secret_key = self._encrypt(salt, payload_base64)
        sign = self._safe_b64_url_encode(secret_key)

        return (salt, sign.decode("utf-8"))

    def get_salt(self, length):
        """
        :return: This function will return the random combine of string 
        and time stamp.
        """
        combine_text = string.ascii_letters + self._get_time_stamp()
        salt = ""
        while length > 0:
            ref = secrets.choice(combine_text)
            salt += ref
            length -= 1
        return salt
    
    def _payload_base64_generate(self):
        payload_base64 = self._safe_b64_url_encode(self.payload)
        return payload_base64

    @staticmethod
    def _encrypt(salt, payload):
        secret = hmac.new(salt.encode("utf-8"), payload, sha256).digest()
        return secret

    @staticmethod
    def _get_time_stamp():
        return str(round(time.time()))

    @staticmethod
    def _safe_b64_url_encode(val):
        if isinstance(val, str):
            val = val.encode("utf-8")
        elif isinstance(val, bytes):
            pass
        else:
            raise TypeError("Expected Bytes or String Values")
        
        return base64.urlsafe_b64encode(val).replace(b"=", b"")

if __name__ == '__main__':
    t = TokenGenerator()
    print(t.get_salt(16))
