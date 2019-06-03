#!/usr/bin/env python
import getpass
import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

class Algorithm:
    # AES-CBC with PBKDF2 derived salted password using 16 bit initialization
    # vector
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

def get_pass_input(text="Type your passphrase: "):
    # text: The default text to show the user while asking for password

    secret = getpass.getpass("{}".format(text))
    secret_validate = getpass.getpass("Retype your passphrase: ")
    if secret != secret_validate:
        print("Passphrases do not match!")
        get_pass_input() # Ask again
    else:
        return secret

def get_pass(text="Type your passphrase: "):
    secret = getpass.getpass("{}".format(text))
    return secret

# For testing purposes
if __name__ == '__main__':
    text = input("text: ")
    pwd = get_pass_input()

    enc = Algorithm(pwd).encrypt(text)
    print("Ciphertext: {}".format(enc))

    #enc = text
    try:
        print("Decrypted: {}".format(Algorithm(pwd).decrypt(enc)))
    except Exception as e:
        print(f"Error: {e}")
