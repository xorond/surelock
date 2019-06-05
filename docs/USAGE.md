## Usage

### Getting Help

```
$ surelock -h
usage: surelock [-h] {add,view,del,list,init} ...

positional arguments:
  {add,view,del,list,init}
    add                 add a new entry
    view                view an entry
    del                 delete an entry
    list                list categories from the database
    init                initialize the database

optional arguments:
  -h, --help            show this help message and exit
```

### Initialize database
```
$ surelock init
```

### List categories
```
$ surelock list
```

### Add a new entry
```
$ surelock add github
```
adds a password for github in the database.

### View an entry
```
$ surelock view github
```
will ask for your master password, and then show the saved password in the database.
