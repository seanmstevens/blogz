import hashlib
import string
import random

def make_pw_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    hashed = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0}.{1}'.format(hash, salt)

def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])

def check_pw_hash(password, salt):
    salt = hashed.split('.')[1]
    if make_pw_hash(password, salt) == hash:
        return True

    return False
