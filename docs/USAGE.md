## Usage

### Getting Help

```
$ surelock -h
usage: surelock [-h]
                {add,view,del,init,show,add_category,delete_category,pwgen}
                ...

positional arguments:
  {add,view,del,init,show,add_category,delete_category,pwgen}
    add                 add a new entry
    view                view a password
    del                 delete an entry
    init                initialize a database
    show                show a category
    add_category        add a category
    delete_category     delete a category
    pwgen               Generate a strong password based on a simple one

optional arguments:
  -h, --help            show this help message and exit
```

## Quickstart Guide

### Initialize a database

First time using Surelock, you will need to create a database for yourself.

Use the `init` command to create a database:
```
./surelock.py init
Type your passphrase:
Retype your passphrase:
```

This will create a database file called `surelock.db` in your current directory, with your
chosen master password (passphrase), you will be able to operate the program using this database.

Some operations as adding/deleting (`add` or `del` commands) entries or viewing them
(`view`) require password authentication, while
others may not such as listing categories (`show`) and entries.

You can have more than one database for different purposes. You can create a new database
with the `init` command and the `-f` or `--file` flag.

```
./surelock.py init -f secret.db
```

will create another database called `work.db`, where you can save your top secret
passwords apart from your regular ones, securing them with a different password.

### Add a category

After creating the database, you can add some categories in it. Let's add a category for
our e-mail accounts.

```
./surelock.py add_category email

```

A possible list of categories you can create now is:
* email
* social
* banking
* work
* ssh-logins
* private
and so on.

### List categories

```
./surelock,py show
Category: root
Category: email
```

Our newly created `email` category is in the list, along with the default `root` category.

### Add an entry

You can add an entry by using the `add` command.

```
usage: surelock add [-h] [-f FILE] [-r] [-l LENGTH] [-s] [-n]
                    [-d [DESCRIPTION [DESCRIPTION ...]]]
                    entry username [category]
```

For example: `./surelock.py add facebook myfacebookusername` will add the entry `facebook`
with username `myfacebookusername` to the table `root`.

`./surelock.py add gmail myuser@gmail.com email` will add the entry `gmail` with
`myuser@gmail.com` as username to the `email` category.

### View an entry
```
./surelock.py view facebook
```
will ask for your master password, and then show the saved password in the database.

### Conclusion

Most other commands from surelock are self-explanatory, such as `add_category`,
`delete_category` or `pwgen` (which is a password generator).

You can always view the help page with `-h` or by running `./surelock.py` without any
arguments.

There is also a GUI made with Tkinter, which can be run with `./surelock-gui.py`.

