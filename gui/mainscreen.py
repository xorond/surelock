# -*- coding: utf-8 -*-
"""
Created on Sun May 26 20:09:20 2019

author(s): @juliakoko, @xorond
"""

import tkinter as Tk

root = Tk.Tk()
root.geometry('1020x620')
root.config(bg='white')
root.title('Choose/Create a Database')

label = Tk.Label(root, text='Create a new Database', fg='black', bg='white')
label.grid(row=0, column=0)

blabel = Tk.Label(root, text='Password: ')
blabel.grid(row=1, column=0)
basis = Tk.Entry(root)
basis.grid(row=1, column=1)
elabel = Tk.Label(root, text='Repeat Password: ')
elabel.grid(row=2, column=0)
exp = Tk.Entry(root)
exp.grid(row=2, column=1)

ok = Tk.Button(root, text='OK')
ok.grid(row=3, column=1)


label = Tk.Label(root, text='Using an existing Database', fg='black', bg='white')
label.grid(row=4, column=0)

blabel = Tk.Label(root, text='Browse...')
blabel.grid(row=5, column=0)
basis = Tk.Entry(root)
basis.grid(row=5, column=1)
elabel = Tk.Label(root, text='Password: ')
elabel.grid(row=6, column=0)
exp = Tk.Entry(root)
exp.grid(row=6, column=1)

ok = Tk.Button(root, text='OK')
ok.grid(row=8, column=1)

root.mainloop()
