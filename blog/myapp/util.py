import random
import hashlib
from myapp.settings import Config

def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def enc_pwd(pwd):
    md5 = hashlib.md5()
    key = Config.SECRET_KEY
    md5.update((pwd+key).encode())
    return md5.hexdigest().upper()