# -*- coding: utf-8 -*-
"""
Created on Sun May 26 16:34:16 2019

@author: J
"""

import tkinter as Tk

root = Tk.Tk()
root.geometry('1020x620')
root.config(bg='grey')
root.title('Choose/Create a Database')

label = Tk.Label(root, text='Create a new Database', fg='black', bg='grey')
label.grid(row=0, column=0)

blabel = Tk.Label(root, text = 'Password:  ')
blabel.grid(row=0, column=1)
basis = Tk.Entry(root)
basis.grid(row=0, column =2)
elabel = Tk.Label(root ,text= 'Repeat Password:  ')
elabel.grid(row=1, column =0)
exp = Tk.Entry(root)
exp.grid(row =1, column =1)

ok = Tk.Button(root , text='OK') 
ok.grid(row=2,  columnspan =2)

root.mainloop()



