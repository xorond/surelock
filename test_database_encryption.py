#!/usr/bin/env python
from libs import sql
from libs import crypto_funcs

db = sql.Database(filename="test.db")
pwd = crypto_funcs.get_pass_input()
sql.init_database(db)
print(sql.list_tables(db))
for i in range(1000):
    sql.insert_entry(db, pwd, "test{}".format(i), "test{}".format(i))
db.close()
