# coding: utf8
"""
helper for decrypt encrypt sensitive information
"""

__all__ = ["AESCipher"]

import base64
from Crypto.Cipher import AES


# AES CBC PKCS5, IV '\x00' * 16
class AESCipher:
    def __init__(self, key):
        self.bs = 16
        self.key = key

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, "\x00" * 16)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, "\x00" * 16)
        return self._unpad(cipher.decrypt(enc)).decode("utf-8")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]


if __name__ == "__main__":
    import os

    a = AESCipher(os.getenv("CRYPKEY"))
    c = a.encrypt("123456")
    print(c)
