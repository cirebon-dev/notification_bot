# -*-coding:utf8;-*-
from cryptography.fernet import Fernet
"""
this file is contain script to generate secret key
"""

key = Fernet.generate_key()
with open(".secret_key", "wb") as f:
    f.write(key)
