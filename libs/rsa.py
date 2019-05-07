#!/usr/bin/env python
import getpass
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

def get_pass_input(text="Type your passphrase: "):
    # text: The default text to show the user while asking for password

    secret = getpass.getpass("{}".format(text))
    secret_validate = getpass.getpass("Retype your passphrase: ")
    if secret != secret_validate:
        print("Passphrases do not match!")
        get_pass_input() # Ask again
    else:
        return secret

def generate_rsa_key(filename="privkey.rsa"):
    # filename: Default name of the private key file

    secret = get_pass_input("Choose your master passphrase: ")
    key = RSA.generate(2048)
    encrypted_key = key.export_key(passphrase=secret)
    outfile = open(filename, "wb")
    outfile.write(encrypted_key)
    outfile.close()

    # Print the RSA public key in ASCII format
    #print(key.publickey().exportKey('PEM'))

def read_rsa_key(filename):
    # filename: Name of the RSA keyfile.
    secret = get_pass_input()
    encrypted_key = open(filename, "rb").read()
    key = RSA.import_key(encrypted_key, passphrase=secret)

    print(key.publickey().exportKey('PEM'))

def encrypt_file(ifilename, ofilename, keyfile, _bytes=16):
    # ifilename: Name of input file (unencrypted)
    # ofilename: Name of output file (encrypted)
    # keyfile: Name of the RSA private key file
    # _bytes: The default number of bytes used in the session (16)

    secret = get_pass_input()

    data = open(ifilename, "rb").read()
    outfile = open(ofilename, "wb")

    recipient_key = RSA.importKey(open(keyfile).read(), passphrase=secret)
    session_key = get_random_bytes(_bytes)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [ outfile.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
    outfile.close()

def decrypt_file(ifilename, ofilename, keyfile, _bytes=16):
    # ifilename: Name of input file (encrypted)
    # ofilename: Name of output file (unencrypted)
    # keyfile: Name of the RSA private key file
    # _bytes: The default number of bytes used in the session (16)

    secret = get_pass_input()

    infile = open(ifilename, "rb")

    private_key = RSA.import_key(open(keyfile).read(), passphrase=secret)

    enc_session_key, nonce, tag, ciphertext = \
            [ infile.read(x) for x in (private_key.size_in_bytes(), _bytes, _bytes, -1) ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    outfile = open(ofilename, "wb")
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    outfile.write(data)
