# -*-coding:utf8;-*-
from cryptography.fernet import Fernet

"""
this file is contain script to generate secret key
"""

key = Fernet.generate_key()
with open(".env.example", "r+") as f:
    data = f.read()
    data = data.replace('insert your encryption key here', key.decode("utf-8"))
    f.seek(0)
    f.write(data)
    f.truncate()
