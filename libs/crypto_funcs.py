#!/usr/bin/env python
import re
import base64
import common
from hashlib import sha512, sha384, sha256
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

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
if __name__ == '__main__':
    text = input("text: ")
    given_len = input("length: ")
    '''
    pwd = common.get_master_pass()

    enc = Algorithm(pwd).encrypt(text)
    print("Ciphertext: {}".format(enc))

    #enc = text
    try:
        print("Decrypted: {}".format(Algorithm(pwd).decrypt(enc)))
    except Exception as e:
        print(f"Error: {e}")
    '''

    password = Password(passphrase=text, length=int(given_len))
    generated = password.generate()
    print(f"password: {generated}")
