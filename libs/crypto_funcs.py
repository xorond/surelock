#!/usr/bin/env python
import re
import base64
import hashlib, binascii, os
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import random

pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

class Algorithm:
    """
    AES-CBC with PBKDF2 derived salted password using 16 bit initialization
    vector
    """
    def __init__(self, password):
        salt = b"we are salty"
        kdf = PBKDF2(password, salt, 64, 1000)
        self.key = kdf[:32]

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode('ascii')))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('ascii')

def pwd_gen(start_pwd="", special_chars=True, numbers=True, upper_case=True, characters=16):
    special=["!", "#", "$", "%", "&", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "{", "}", "~"]
    num=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    capitals=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    lower_case=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    l=lower_case
    a=25
    final_pwd=""
    if special_chars: 
        l=l+special
        a=a+26
    if numbers: 
        l=l+num
        a=a+10
    if upper_case: 
        l=l+capitals
        a=a+26
    if start_pwd=="":
        for i in range(characters):
            final_pwd+=str(l[random.randint(0, a)])
    else:
        n=[ord(x) for x in start_pwd]
        e=0
        while len(n)<=characters:
            n.append(n[e]+characters+len(n))
            e=e+1
        b=characters
        for i in range(characters):
            b=((b+characters)*n[i]*n[i-1]+i)%a
            final_pwd+=str(l[b])
    if special_chars and len(set([x for x in final_pwd]).intersection(set(special))) == 0:
        final_pwd = final_pwd[:2] + special[len(start_pwd)*characters%26] + final_pwd[3:]
    if numbers and len(set([x for x in final_pwd]).intersection(set(num))) == 0:
        final_pwd = final_pwd[:4] + num[len(start_pwd)*characters%10] + final_pwd[5:]
    return final_pwd


# hash_password and verify_password taken from https://www.vitoshacademy.com/hashing-passwords-in-python/

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

class Password:
    """
    a password object, to be generated from an optionally given passphrase and
    other options such as length and specials

    for example:
    entry = Password(passphrase="potato", length=32, specials=True)

    password generator code inspired/adapted from: github.com/xorond/passtrust
    note: it is a slightly different algorithm than passtrust, so the results
    are not the same
    """
    def __init__(self, passphrase="", length=32, specials=False):
        # use random passphrase if none is given
        if passphrase == "":
            passphrase = str(Random.new().read(16))
        self.passphrase = passphrase
        self.length = length
        self.specials = specials
    def generate(self):

        # take bytes
        original = bytes(self.passphrase, encoding='ascii')
        self.passphrase = bytes(self.passphrase, encoding='ascii')

        # run through hashing
        self.passphrase = bytes(sha256(original).hexdigest(), 'ascii')
        self.passphrase = bytes(sha384(self.passphrase).hexdigest(), 'ascii')
        self.passphrase = bytes(sha512(self.passphrase).hexdigest(), 'ascii')

        # other way around
        self.passphrase += bytes(sha512(original).hexdigest(), 'ascii')
        self.passphrase += bytes(sha384(self.passphrase).hexdigest(), 'ascii')

        # do hexdigest in the end (important)
        self.passphrase = bytes(sha256(self.passphrase).hexdigest(), 'ascii')

        # encode with b64
        self.passphrase = base64.b64encode(self.passphrase)
        # turn to string
        self.passphrase = self.passphrase.decode('ascii')
        # remove equal signs
        self.passphrase = re.sub('=', '', self.passphrase)

        # 16 < length < 64
        if self.length < 16:
            self.length = 16
        if self.length > 64:
            self.length = 64
        # cut to length
        part_one = self.passphrase[:int((self.length/2)) - 1]
        part_two = self.passphrase[self.length:int(self.length/2):-1]
        self.passphrase = part_one + part_two

        return self.passphrase

# For testing purposes
"""
if __name__ == '__main__':
    text = input("text: ")
   given_len = input("length: ")

"""
'''

    enc = Algorithm(pwd).encrypt(text)
    print("Ciphertext: {}".format(enc))

    #enc = text
    try:
        print("Decrypted: {}".format(Algorithm(pwd).decrypt(enc)))
    except Exception as e:
        print(f"Error: {e}")
'''
"""
    password = Password(passphrase=text, length=int(given_len))
    generated = password.generate()
    print(f"password: {generated}")
"""

