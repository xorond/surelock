# surelock

A password manager written in python.

This is a project that was written for the Programming course for Bachelor of Mathematics at University of Vienna. See the [README in German](https://github.com/xorond/surelock/blob/master/docs/README-de.md) for more information on this.

## Usage:

See [USAGE.md](https://github.com/xorond/surelock/blob/master/docs/USAGE.md).

## Features:
- [x] Usable with CLI
- [x] or GUI (Tkinter)
- [x] Uses cryptographic libraries (AES and salted sha512) to ensure security of data.
- [x] Uses a local database (encrypted sqlite3 with a master password) to store user data.
- [x] Generate secure passwords (length and availability of special characters is configurable during the generation) with or without a "seed password" using an irreversible algorithm

## TODO:
- [ ] A keyfile feature, as found commonly in other password managers such as KeepassX.

### Members:
  * Oguz Bektas           [@xorond](https://github.com/xorond)
  * Alexander Panzenböck  [@Alex6312](https://github.com/Alex6312)
