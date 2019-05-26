#!/usr/bin/env python
import getpass
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
#from Crypto.Protocol.KDF import PBKDF2

pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size
        - len(s) % AES.block_size)
unpad = lambda s: s[:-ord(s[len(s) - 1:])] # TODO: fix this

def get_pass_input(text="Type your passphrase: "):
    # text: The default text to show the user while asking for password

    secret = getpass.getpass("{}".format(text))
    secret_validate = getpass.getpass("Retype your passphrase: ")
    if secret != secret_validate:
        print("Passphrases do not match!")
        get_pass_input() # Ask again
    else:
        return secret

def generate_key(password):
    key = hashlib.sha256(password.encode("utf-8")).digest()
    return key

def encrypt_text(text, password):
    key = generate_key(password)
    text = pad(text)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(text.encode()))

def decrypt_text(enc, password):
    key = generate_key(password)
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

'''
# DEBUG
password = get_pass_input()
encrypted = encrypt_text("test encryption", password)
print(encrypted)
decrypted = decrypt_text(encrypted, password)
print(bytes.decode(decrypted))
'''
