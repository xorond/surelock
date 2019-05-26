#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 12:09:05 2019

author: @juliakoko, @xorond
"""

import tkinter as Tk

# main window
root = Tk.Tk()
root.title('Surelock Password Manager')
root.geometry('1020x620')

def main():
    root = Tk.Tk()
    root.title('Surelock Password Manager')
    root.geometry('1020x620')
    app = Window1(root)
    root.mainloop()

class Window1:
    def __init__(self, master):
        self.master = master
        self.master.title("Choose/Create a Database")
        self.master.geometry('1250x650+0+0')
        self.frame = Tk.Frame(self.master)
        self.frame.pack()

        self.btn_create_db = Tk.Button(self.frame, text="Create a new Database",
                                       command=self.Create_a_new_Database)
        self.btn_create_db.grid(row=0, column=0)

        self.btn_ex_db = Tk.Button(self.frame, text="Use an existing Database",
                                   command=self.Use_an_existing_Database)
        self.btn_ex_db.grid(row=0, column=1)


    def Create_a_new_Database(self):
        self.newWindow = root.Toplevel(self.master)
        self.app = Window2(self.newWindow)

    def Use_an_existing_Database(self):
        self.newWindow = Tk.Toplevel(self.master)
        self.app = Window3(self.newWindow)

class Window2:
    def __init__(self, master):
        self.master = master
        self.master.title("Create a new Database")
        self.master.geometry ('1250x650+0+0')
        self.frame = Tk.Frame(self.master)
        self.frame.pack()

class Window3:
    def __init__(self, master):
        self.master = master
        self.master.title("Use an existing Database")
        self.master.geometry('1250x650+0+0')
        self.frame = Tk.Frame(self.master)
        self.frame.pack()

main()
