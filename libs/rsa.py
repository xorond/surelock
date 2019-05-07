#!/usr/bin/env python
import getpass
from Crypto.PublicKey import RSA

def get_pass_input(text="Type your passphrase: "):
    secret = getpass.getpass("{}".format(text))
    secret_validate = getpass.getpass("Retype your passphrase: ")
    if secret != secret_validate:
        print("Passphrases do not match!")
        get_pass_input() # Ask again
    else:
        return secret

def generate_rsa_key(filename="privkey.rsa"):
    # Generate a new RSA key pair (with a secret) and save it to a password-protected file.
    secret = get_pass_input("Choose your master passphrase: ")

    key = RSA.generate(2048)
    # Use scrypt key derivation function to thwart dictionary attacks
    encrypted_key = key.export_key(passphrase=secret, pkcs=8,
                    protection="scryptAndAES128-CBC")
    outfile = open(filename, "wb")
    outfile.write(encrypted_key)

    # Print the RSA public key in ASCII format
    print(key.publickey().export_key())

def read_rsa_key(filename):
    secret = get_pass_input()
    encrypted_key = open(filename, "rb").read()
    key = RSA.import_key(encrypted_key, passphrase=secret)

    print(key.publickey().export_key())
