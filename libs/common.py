#!/usr/bin/env python
import getpass

def get_master_pass(text="Type your passphrase: "):
    # text: The default text to show the user while asking for password

    secret = getpass.getpass("{}".format(text))
    secret_validate = getpass.getpass("Retype your passphrase: ")
    if secret != secret_validate:
        print("Passphrases do not match!")
        get_master_pass() # Ask again
    return secret

def get_pass(text="Type your passphrase: "):
    secret = getpass.getpass("{}".format(text))
    return secret
