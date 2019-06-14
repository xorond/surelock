#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import os
try:
    from libs import crypto_funcs
    from libs import sql
    import pandas as pd
except Exception as e:
    print("Error: {}".format(e))
    sys.exit()

is_posix = False
if os.name == 'posix':
    is_posix = True

class FirstWindow:

    def __init__(self, master):
        self.background = "light sea green"
        self.foreground = "light yellow"
        self.master = master
        self.master.title("Choose/Create a Database")
        self.master.geometry('830x470+0+0')
        self.master.config(bg = self.background)
        self.frame = tk.Frame(self.master)
        self.frame.config(bg = self.background)
        self.frame.pack()

        self.file_open = tk.StringVar()
        self.password_open_1 = tk.StringVar()
        self.file_create = tk.StringVar()
        self.password_create_1 = tk.StringVar()
        self.password_create_2 = tk.StringVar()
        
        self.open_frame = tk.LabelFrame(self.frame, width = 650, height = 100, bg = self.background, bd = 10)
        self.open_frame.grid(row=2, column= 0, columnspan=2, ipadx = 10, ipady = 3)
        self.create_frame = tk.LabelFrame(self.frame, width = 650, height = 100, bg = self.background, bd = 10)
        self.create_frame.grid(row=4, column= 0, columnspan=2, ipadx = 10, ipady = 3)
        
        self.label = tk.Label(self.frame, text = "Open an existing Database", font = ("arial", 20, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row=0, column= 0, columnspan=2, pady=(15,0))
        
        self.label = tk.Label(self.open_frame, text = "File: ", bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.label.grid(row=1, column= 0, sticky = tk.E, pady=(8,0))
        self.open_file=tk.Entry(self.open_frame, textvariable=self.file_open, font = ("arial", 13), width = 45)
        self.open_file.grid(row=1, column= 1, pady=(8,0), columnspan=2)
        if is_posix == False:
            self.open_file.insert(tk.END, os.getcwd() + '\surelock.db')
        else:
            self.open_file.insert(tk.END, os.getcwd() + '/surelock.db')
        self.open_file_browse = tk.Button(self.open_frame, text="Browse...", command=self.open_database, bg = self.background, fg = self.foreground, font = ("arial", 8, "bold"))
        self.open_file_browse.grid(row=1, column= 3, pady=(8,0))
        self.label = tk.Label(self.open_frame, text = "Password: ", bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.label.grid(row=2, column= 0, sticky = tk.E, padx=(73,0))
        self.open_file_pwd1=tk.Entry(self.open_frame, show="*", textvariable=self.password_open_1, font = ("arial", 13), width = 45)
        self.open_file_pwd1.insert(tk.END, "1")        #This line temporarily exists to speed up testing with the default database
        self.open_file_pwd1.grid(row=2, column= 1, columnspan=2)
        
        self.open_button = tk.Button(self.open_frame, text = 'Open', command = self.next_window_open, bg = self.background, fg = self.foreground, font = ("arial", 11, "bold"), width = 10)
        self.open_button.grid(row=3, column=2, pady=2)
        self.reset_button = tk.Button(self.open_frame, text = 'Reset', command = self.reset_open, bg = self.background, fg = self.foreground, font = ("arial", 11, "bold"), width = 10)
        self.reset_button.grid(row=3, column=1, pady=2)

        self.label = tk.Label(self.frame, text = "Create a new Database", font = ("arial", 20, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row=3, column= 0, columnspan=2, pady=(15,0))
        
        self.label = tk.Label(self.create_frame, text = "File: ", bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.label.grid(row=0, column= 0, sticky = tk.E, pady=(8,0))
        self.create_file=tk.Entry(self.create_frame, textvariable=self.file_create, font = ("arial", 13), width = 45)
        self.create_file.grid(row=0, column= 1, columnspan=2, pady=(8,0))
        self.create_file_browse = tk.Button(self.create_frame, text="Browse...", command=self.create_database, bg = self.background, fg = self.foreground, font = ("arial", 8, "bold"))
        self.create_file_browse.grid(row=0, column= 3, pady=(8,0))
        self.label = tk.Label(self.create_frame, text = "Password: ", bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.label.grid(row=1, column= 0, sticky = tk.E)
        self.create_file_pwd1=tk.Entry(self.create_frame, show="*", textvariable=self.password_create_1, font = ("arial", 13), width = 45)
        self.create_file_pwd1.grid(row=1, column= 1, columnspan=2)
        self.label = tk.Label(self.create_frame, text = "  Repeat Password: ", bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.label.grid(row=2, column= 0, sticky = tk.E)
        self.create_file_pwd2=tk.Entry(self.create_frame, show="*", textvariable=self.password_create_2, font = ("arial", 13), width = 45)
        self.create_file_pwd2.grid(row=2, column= 1, columnspan=2)
        
        self.label1 = tk.Label(self.create_frame, text = "Passwords do not match! ", bg = self.background, fg = self.background, font = ("arial", 13, "bold"))
        self.label1.grid(row=3, column= 1, columnspan=2)
        
        self.create = tk.Button(self.create_frame, text = 'Create', command = self.next_window_create, bg = self.background, fg = self.foreground, font = ("arial", 11, "bold"), width = 10)
        self.create.grid(row=8, column=2, pady=2)
        self.reset = tk.Button(self.create_frame, text = 'Reset', command = self.reset_create, bg = self.background, fg = self.foreground, font = ("arial", 11, "bold"), width = 10)
        self.reset.grid(row=8, column=1, pady=2)

        self.exit = tk.Button(self.frame, text = 'Exit', command = self.exit_surelock, bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"), width = 10)
        self.exit.grid(row=9, column=1, pady=20)

        self.pw_gen = tk.Button(self.frame, text='Password Generator', command=self.start_password_generator, bg=self.background, fg=self.foreground, font=("arial", 13, "bold"), width=20)
        self.pw_gen.grid(row=9, column=0, pady=20)

        self.password_create_1.trace("w", lambda x,y,z: self.check_passwords())
        self.password_create_2.trace("w", lambda x,y,z: self.check_passwords())

        self.master.protocol("WM_DELETE_WINDOW", self.exit_surelock)

    def open_database(self):
        filename = filedialog.askopenfilename(filetypes=(("Database files", "*.db"),("All files", "*.*") ))
        self.open_file.delete(0,tk.END)
        self.open_file.insert(0,filename)

    def create_database(self):
        filename = filedialog.asksaveasfilename(filetypes=(("Database files", "*.db"), ("All files", "*.*")))
        self.create_file.delete(0, tk.END)
        self.create_file.insert(0, filename)

    def next_window_open(self):
        file = self.file_open.get()
        if file[-3:] != ".db":
            messagebox.showinfo("Error", "Please choose a Surelock Database File (*.db)!")
        elif os.path.isfile(file):
            FirstWindow.file= self.file_open.get()
            FirstWindow.masterpass = self.password_open_1.get()
            self.master.destroy()
        else: 
            messagebox.showinfo("Error", "File does not exist!")
        
    def reset_open(self):
        self.open_file.delete(0, tk.END)
        if is_posix == False:
            self.open_file.insert(tk.END, os.getcwd() + '\surelock.db')
        else:
            self.open_file.insert(tk.END, os.getcwd() + '/surelock.db')
        self.open_file_pwd1.delete(0, tk.END)

    def reset_create(self):
        self.create_file.delete(0, tk.END)
        self.create_file_pwd1.delete(0, tk.END)
        self.create_file_pwd2.delete(0, tk.END)

    def next_window_create(self):
        file = self.file_create.get()
        directory = os.path.split(file)
        if os.path.isfile(file):
            messagebox.showinfo("Error", "This File already exists!")
        elif os.path.isdir(directory[0]) and directory[1] != "":
            if file[-3:] != ".db":
                file = file + ".db"
            FirstWindow.file = file
            FirstWindow.masterpass = self.password_create_1.get()
            self.master.destroy()
        elif not os.path.isdir(directory[0]):
            messagebox.showinfo("Error", "This Directory does not exist!")
        else:
            messagebox.showinfo("Error", "Filename is empty!")
            
    def start_password_generator(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = PwgenWindow(self.newWindow)
        self.newWindow.transient(self.master)
        
    def exit_surelock(self):
        self.master.master.destroy()

    def check_passwords(self):
        if self.password_create_1.get() == self.password_create_2.get():
            self.label1.config(fg = self.background)
            self.create.config(state = tk.NORMAL)
        else:
            self.label1.config(fg = "orange")
            self.create.config(state = tk.DISABLED)
            

class MainWindow:

    def __init__(self, master):
        
        self.background = "light sea green"
        self.foreground = "light yellow"
        
        self.master = master
        self.master.title("Surelock Password Manager")
        self.master.geometry('1250x480+0+0')
        self.master.config(bg = self.background)
        self.frame = tk.Frame(self.master)
        self.frame.config(bg = self.background)
        self.frame.pack()
        
        self.newWindow = tk.Toplevel(self.master)
        self.app = FirstWindow(self.newWindow)
        self.newWindow.transient(self.master)
        self.master.wait_window(self.newWindow)

        self.menubar=tk.Menu(self.frame)
        self.filemenu=tk.Menu(self.menubar ,tearoff =0)
        self.filemenu.add_command(label="Open/Create Database", command=self.ask_to_open_or_create_database)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit_surelock)
        self.menubar.add_cascade(label="File",menu=self.filemenu)
        self.helpmenu=tk.Menu(self.menubar ,tearoff =0)
        self.helpmenu.add_command(label="About", command=self.open_about)
        self.helpmenu.add_command(label="Dokumentation", command=self.open_documentation)
        self.menubar.add_cascade(label="Help",menu=self.helpmenu)
        self.master.config(menu=self.menubar) 

        self.label = tk.Label(self.frame, text ="Categories:", font = ("arial", 15, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row=0, column =0, sticky = tk.W, pady=(15,0))
        self.label = tk.Label(self.frame, text ="Entries:", font = ("arial", 15, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row=0, column =2, sticky = tk.W, pady=(15,0))

        self.category_list = tk.Listbox(self.frame, height = 12, width = 30, font = ("arial", 12))
        self.category_list.grid(row=1, column =0, columnspan =2)
        self.category_list.bind("<<ListboxSelect>>", self.change_selected_table)
        
        self.category_scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.category_scrollbar.config(command=self.category_list.yview)

        self.add_category_button= tk.Button(self.frame, text="Add Category", command=self.add_category, bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.add_category_button.grid(row=2, column =0, pady=3)

        self.delete_category_button= tk.Button(self.frame , text="Delete Category", command=self.delete_category, bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.delete_category_button.grid(row=2, column =1, pady=3, padx=3)

        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Arial', 12), rowheight=25)
        self.style.configure("Treeview.Heading", font=('Arial', 13,'bold'))
        self.entry_list = ttk.Treeview(self.frame, style = "Treeview", columns=("Username", "Password", "Description"), height = 5)
        self.entry_list.heading('Username', text='Username')
        self.entry_list.heading('Password', text='Password')
        self.entry_list.heading('Description', text='Description')
        self.entry_list.heading('#0', text='Site')
        self.entry_scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.entry_scrollbar.config(command=self.entry_list.yview)

        self.entry_list.grid(row=1, column =2, columnspan =13, sticky = "sn")
        self.entry_list.bind("<<TreeviewSelect>>", self.change_button_activation)

        self.add_entry_button= tk.Button(self.frame, text="Add Entry", width = 14, command=self.add_entry, bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.add_entry_button.grid(row=2, column =12, pady=3, padx=3)

        self.delete_entry_button= tk.Button(self.frame, text="Delete Entry", width = 14, command=self.delete_entry, bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.delete_entry_button.grid(row=2, column =11, pady=3, padx=3)

        self.get_password_button= tk.Button(self.frame, text="Show Password", width = 14, command=self.show_password, bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.get_password_button.grid(row=2, column =14, pady=3, padx=3)

        self.copy_password_button= tk.Button(self.frame, width = 24, text="Copy Password to Clipboard", command=self.copy_password, bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.copy_password_button.grid(row=2, column =13, pady=3, padx=3)

        self.clear_clipboard = tk.Button(self.frame, width = 24, text="Clear Clipboard", command=self.clear_clipboard, bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.clear_clipboard.grid(row = 3, column = 13, pady=3, padx=3)

        self.exit = tk.Button(self.frame, text="Exit", width = 14, command=self.exit_surelock, bg = self.background, fg = self.foreground, font = ("arial", 13, "bold"))
        self.exit.grid(row = 4, column = 14, pady=3, padx=3)
 
        self.delete_entry_button.config(state = tk.DISABLED)
        self.copy_password_button.config(state = tk.DISABLED)
        self.get_password_button.config(state = tk.DISABLED)
        
        self.open_or_create_database()
        
    def change_selected_table(self, event):
        if len(self.category_list.curselection()) == 1:
            self.entry_list.selection_remove(self.entry_list.selection())
            selectionnumber=self.category_list.curselection()[0]
            table=sql.list_tables(MainWindow.db_main)[selectionnumber][0]
            self.entry_list.delete(*self.entry_list.get_children())
            for  entry  in sql.retrieve_table(MainWindow.db_main, table): self.entry_list.insert("", "end", text=entry[0], values=(entry[2], "*********", entry[1]))
            if len(sql.retrieve_table(MainWindow.db_main, table))>8:
                self.entry_scrollbar.grid(row=1, column =14, sticky ="nse")
            else:
                self.entry_scrollbar.grid_forget()
                
    def update_categories(self, selection=0):
        tables = sql.list_tables_with_number_of_entries(MainWindow.db_main)
        self.category_list.delete(0,tk.END)
        for  entry  in tables: 
            self.category_list.insert(tk.END, entry)
        self.category_list.selection_set(selection)
        self.change_selected_table(True)
        if len(tables)>12:
            self.category_scrollbar.grid(row=1, column =1, sticky ="nse")
        else:
            self.category_scrollbar.grid_forget()
        if len(tables) == 0:
            self.delete_category_button.config(state = tk.DISABLED)
        else:
            self.delete_category_button.config(state = tk.NORMAL)
            
    def add_category(self):
        answer = simpledialog.askstring("Add category", "Category name: ",parent=self.frame)
        if answer == None:
            return
        elif (answer,) in sql.list_tables(MainWindow.db_main):
            messagebox.showinfo("Error", "This category already exists!")
        elif answer != "":
            sql.create_table(MainWindow.db_main, answer)
            self.update_categories(tk.END)
        else:
            messagebox.showinfo("Error", "Category name too short!")

    def delete_category(self):
        answer=self.category_list.curselection()[0]
        tables=sql.list_tables(MainWindow.db_main)
        if messagebox.askokcancel("Question", "Do you want to delete the category " + tables[answer][0] + "?"):
            sql.delete_table(MainWindow.db_main, tables[answer][0])
            self.update_categories()
                
    def add_entry(self):
        MainWindow.table_num = self.category_list.curselection()
        self.newWindow = tk.Toplevel(self.master)
        self.app = AddWindow(self.newWindow)
        self.master.wait_window(self.newWindow)
        self.category_list.selection_set(MainWindow.table_num)
        self.change_selected_table(True)
        self.update_categories()

    def delete_entry(self):
        entry = self.entry_list.focus()
        itemname = self.entry_list.item(entry)["text"]
        if messagebox.askokcancel("Question", "Do you want to delete the entry " + itemname + "?"):
            table = sql.list_tables(MainWindow.db_main)[self.category_list.curselection()[0]][0]
            sql.delete_entry(MainWindow.db_main, itemname, table)
            self.change_selected_table(True)
            self.update_categories()
        
    def show_password(self):
        entry = self.entry_list.focus()
        itemname = self.entry_list.item(entry)["text"]
        table = sql.list_tables(MainWindow.db_main)[self.category_list.curselection()[0]][0]
        password = sql.retrieve_entry(MainWindow.db_main, MainWindow.masterpass_main, itemname, table)
        messagebox.showinfo("Password", "The password for {} is {}".format(itemname, password))

    def copy_password(self):
        entry = self.entry_list.focus()
        itemname = self.entry_list.item(entry)["text"]
        table = sql.list_tables(MainWindow.db_main)[self.category_list.curselection()[0]][0]
        password = sql.retrieve_entry(MainWindow.db_main, MainWindow.masterpass_main, itemname, table)
        try:
            df=pd.DataFrame([str(password)])
            df.to_clipboard(index=False,header=False)
        except Exception as e:
            print("Error: {}".format(e))

    def ask_to_open_or_create_database(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = FirstWindow(self.newWindow)
        self.newWindow.transient(self.master)
        self.master.wait_window(self.newWindow)
        self.open_or_create_database()

    def open_or_create_database(self):
        MainWindow.db_main=sql.Database(filename=FirstWindow.file)
        if len(sql.list_tables(MainWindow.db_main)) == 0:
            sql.init_database(MainWindow.db_main)
        MainWindow.masterpass_main = FirstWindow.masterpass
        self.update_categories()
        
    def change_button_activation(self,event):
        if self.entry_list.focus() == "":
            self.delete_entry_button.config(state = tk.DISABLED)
            self.copy_password_button.config(state = tk.DISABLED)
            self.get_password_button.config(state = tk.DISABLED)
        else:
            self.delete_entry_button.config(state = tk.NORMAL)
            self.copy_password_button.config(state = tk.NORMAL)
            self.get_password_button.config(state = tk.NORMAL)

    def clear_clipboard(self):
        try:
            df=pd.DataFrame([])
            df.to_clipboard(index=False,header=False)
        except Exception as e:
            print("Error: {}".format(e))
            
    def exit_surelock(self):
        self.master.destroy()

    def open_about(self):
        return
        
    def open_documentation(self):
        return

class AddWindow:

    def __init__(self, master):
        self.background = "light sea green"
        self.foreground = "light yellow"
        
        self.master = master
        self.master.title("Add an entry")
        self.master.geometry('1150x350+0+0')
        self.master.config(bg = self.background)
        self.frame = tk.Frame(self.master)
        self.frame.config(bg = self.background)
        self.frame.pack()
        
        self.site = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.description = tk.StringVar()
        self.category = tk.StringVar()
        self.characters = tk.IntVar()
        self.special_characters = tk.BooleanVar()
        self.numbers = tk.BooleanVar()
        self.selected_table = tk.StringVar()
        
        self.add_frame = tk.LabelFrame(self.frame, width = 650, height = 100, bg = self.background, bd = 10)
        self.add_frame.grid(row=1, column= 0, ipadx = 10, ipady = 3)
        self.pw_gen_frame = tk.LabelFrame(self.frame, width = 650, height = 100, bg = self.background, bd = 10)
        self.pw_gen_frame.grid(row=1, column= 1, ipadx = 10, ipady = 3, sticky = tk.N)
        
        self.label = tk.Label(self.frame, text = "Add an entry: ", font = ("arial", 15, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 0, column = 0, pady=(15,0))
        self.label = tk.Label(self.add_frame, text = "Site: ", font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 0, column = 0, sticky = tk.E, pady=(8,0))
        self.site = tk.Entry(self.add_frame, width = 50, textvariable=self.site, font = ("arial", 13))
        self.site.grid(row = 0, column = 1, pady=(8,0), columnspan = 2)
        self.label = tk.Label(self.add_frame, text = "Username: ", font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 1, column = 0, sticky = tk.E)
        self.username = tk.Entry(self.add_frame, width = 50, textvariable=self.username, font = ("arial", 13))
        self.username.grid(row = 1, column = 1, columnspan = 2)
        self.label = tk.Label(self.add_frame, text = "Password: ", font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 2, column = 0, sticky = tk.E)
        self.password = tk.Entry(self.add_frame, show="*", width = 50, textvariable=self.password, font = ("arial", 13))
        self.password.grid(row = 2, column = 1, columnspan = 2)
        self.label = tk.Label(self.add_frame, text = "Category: ", font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 3, column = 0, sticky = tk.E)
        self.selected_table.set(sql.list_tables(MainWindow.db_main)[MainWindow.table_num[0]][0])
        self.table_select = tk.OptionMenu(self.add_frame, self.selected_table, *[a[0] for a in sql.list_tables(MainWindow.db_main)])
        self.table_select.config(width = 10, font = ("arial", 11, "bold"), bg = self.background, fg = self.foreground, activebackground = self.background, activeforeground = self.foreground)
        self.table_select["menu"].config(bg = self.background, fg = self.foreground, font = ("arial", 11, "bold"))
        self.table_select.grid(row = 3, column = 1, sticky = tk.W)
        self.label = tk.Label(self.add_frame, text = "Description: ", font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 4, column = 0, sticky = tk.E, padx=(10,0))
        self.description = tk.Entry(self.add_frame, width = 50, textvariable=self.description, font = ("arial", 13))
        self.description.grid(row = 4, column = 1, columnspan = 2)
        self.reset_button = tk.Button(self.add_frame, text = 'Reset', command = self.reset, bg = self.background, fg = self.foreground, font = ("arial", 11, "bold"), width = 10)
        self.reset_button.grid(row=5, column=1, pady=2)
        self.ok_button = tk.Button(self.add_frame, text="Add this entry", command=self.add_entry, font = ("arial", 11, "bold"), bg = self.background, fg = self.foreground)
        self.ok_button.grid(row = 5, column = 2, pady=2)

        self.label = tk.Label(self.frame, text = "Generate a random password for the new entry: ", font = ("arial", 15, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 0, column = 1, padx=(10,0), pady=(15,2))
        self.label = tk.Label(self.pw_gen_frame, text = "Number of characters:   ", font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 0, column = 0, padx=(10,0), pady=(8,2))
        self.chars = tk.Scale(self.pw_gen_frame, from_=8,to=40, length = 150, orient=tk.HORIZONTAL, variable=self.characters, font = ("arial", 13, "bold"))
        self.chars.config(font = ("arial", 10), bg = self.background, fg = self.foreground)
        self.chars.grid(row = 0, column = 1, pady=(8,0))
        self.chars.set(16)
        self.sp_chars=tk.Checkbutton(self.pw_gen_frame,text="Include special chracters", variable=self.special_characters, font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground, selectcolor = self.background, activebackground = self.background, activeforeground = self.foreground)
        self.sp_chars.grid(row = 1, column = 0, columnspan = 2, sticky = tk.W, pady=2, padx=(90,0))
        self.ask_numbers=tk.Checkbutton(self.pw_gen_frame,text="Include numbers", variable=self.numbers, font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground, selectcolor = self.background, activebackground = self.background, activeforeground = self.foreground)
        self.ask_numbers.grid(row = 2, column = 0, columnspan = 2, sticky = tk.W, pady=2, padx=(90,0))
        self.password_button = tk.Button(self.pw_gen_frame, text="Generate random password", command=self.generate, font = ("arial", 11, "bold"), bg = self.background, fg = self.foreground)
        self.password_button.grid(row = 3, column = 0, columnspan = 2, pady=2)
        
        self.esc_button = tk.Button(self.frame, text="Exit", width = 14, command=self.esc, font = ("arial", 11, "bold"), bg = self.background, fg = self.foreground)
        self.esc_button.grid(row = 5, column = 1)

    def add_entry(self):
        site = self.site.get()
        username = self.username.get()
        password = self.password.get()
        description = self.description.get()
        table = self.selected_table.get()
        if site == "" or username == "" or password == "":
            messagebox.showinfo("Error", "You must enter a Site, a Password and an Username!")
        elif (site,) in sql.retrieve_entries(MainWindow.db_main, table):
            answer = messagebox.askyesno("Question","The entry " + site + " already exists in the table " + table + "!\nDo you want to replace it?")
            if answer:
                sql.insert_entry_gui(MainWindow.db_main, MainWindow.masterpass_main, site, password, description, table, username=username)
                self.master.destroy()
        else:
            sql.insert_entry_gui(MainWindow.db_main, MainWindow.masterpass_main, site, password, description, table, username=username)
            self.master.destroy()
        
    def generate(self):
        pw = crypto_funcs.pwd_gen(special_chars = self.special_characters.get(), numbers = self.numbers.get(), characters = self.characters.get())
        self.password.delete(0, tk.END)
        self.password.insert(tk.END, pw)
        
    def reset(self):
        self.site.delete(0, tk.END)
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.description.delete(0, tk.END)

    def esc(self):
        self.master.destroy()

class PwgenWindow:
    def __init__(self, master):

        self.background = "light sea green"
        self.foreground = "light yellow"

        self.master = master
        self.master.title("Password Generator")
        self.master.geometry('830x470+0+0')
        self.master.config(bg = self.background)
        self.frame = tk.Frame(self.master)
        self.frame.config(bg = self.background)
        self.frame.pack()

        self.start_pwd = tk.StringVar()
        self.new_pwd = tk.StringVar()
        self.characters = tk.IntVar()
        self.special_characters = tk.BooleanVar()
        self.numbers = tk.BooleanVar()

        self.label = tk.Label(self.frame, text = "Generate a strong password based on a simple one", font = ("arial", 15, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 0, column = 0, columnspan = 3, pady=(15,10))
        self.label = tk.Label(self.frame, text = "Simple Password: ", font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 1, column = 0, sticky = tk.E, pady=3)
        self.base_pwd = tk.Entry(self.frame, width = 50, textvariable=self.start_pwd, show = "*", font = ("arial", 13))
        self.base_pwd.grid(row = 1, column = 1, columnspan = 2, pady=3)
        self.label = tk.Label(self.frame, text = "Number of characters: ", font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 2, column = 0, sticky = tk.E, pady=3)
        self.chars = tk.Scale(self.frame, from_=8,to=40, length = 230, orient=tk.HORIZONTAL, variable=self.characters, bg = self.background, fg = self.foreground)
        self.chars.grid(row = 2, column = 1, sticky = tk.W, columnspan = 2, pady=3)
        self.chars.set(16)
        self.ask_sp_chars=tk.Checkbutton(self.frame,text="Include special chracters", variable=self.special_characters, font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground, selectcolor = self.background, activebackground = self.background, activeforeground = self.foreground)
        self.ask_sp_chars.grid(row = 3, column = 1, sticky = tk.W, columnspan = 2, pady=3)
        self.ask_numbers=tk.Checkbutton(self.frame,text="Include numbers", variable=self.numbers, font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground, selectcolor = self.background, activebackground = self.background, activeforeground = self.foreground)
        self.ask_numbers.grid(row = 4, column = 1, sticky = tk.W, columnspan = 2, pady=3)
        self.label = tk.Label(self.frame, text = "Generated Password: ", font = ("arial", 13, "bold"), bg = self.background, fg = self.foreground)
        self.label.grid(row = 6, column = 0, sticky = tk.E, pady=(30,3))
        self.new_pwd = tk.Entry(self.frame, width = 50, textvariable=self.new_pwd, font = ("arial", 13))
        self.new_pwd.grid(row = 6, column = 1, columnspan = 2, pady=(30,3))
        self.ok_button = tk.Button(self.frame, text="Generate Password", width = 17, command=self.generate, font = ("arial", 11, "bold"), bg = self.background, fg = self.foreground)
        self.ok_button.grid(row = 5, column = 2, sticky = tk.E, pady=3)
        self.esc_button = tk.Button(self.frame, text="Exit", command=self.esc, width = 17, font = ("arial", 11, "bold"), bg = self.background, fg = self.foreground)
        self.esc_button.grid(row = 8, column = 2, sticky = tk.E, pady=10)
        self.copy_to_clipboard = tk.Button(self.frame, text="Copy to Clipboard", width = 17, command=self.copy, font = ("arial", 11, "bold"), bg = self.background, fg = self.foreground)
        self.copy_to_clipboard.grid(row = 7, column = 2, sticky = tk.E, pady=3)
        self.clear_clipboard = tk.Button(self.frame, text="Clear Clipboard", width = 17, command=self.clear, font = ("arial", 11, "bold"), bg = self.background, fg = self.foreground)
        self.clear_clipboard.grid(row = 7, column = 1, sticky = tk.E, pady=3, padx=15)

    def generate(self):
        if self.start_pwd.get() == "":
            messagebox.showinfo("Error", "You must enter a Password")
        else:
            pw = crypto_funcs.pwd_gen(self.start_pwd.get(), self.special_characters.get(), self.numbers.get(),characters = self.characters.get())
            self.new_pwd.delete(0, tk.END)
            self.new_pwd.config(show = "")
            self.new_pwd.insert(tk.END, pw)
            return pw

    def copy(self):
        try:
            df=pd.DataFrame([str(self.new_pwd.get())])
            self.new_pwd.config(show = "*")
            df.to_clipboard(index=False,header=False)
        except Exception as e:
            print("Error: {}".format(e))

    def clear(self):
        try:
            df=pd.DataFrame([])
            df.to_clipboard(index=False,header=False)
        except Exception as e:
            print("Error: {}".format(e))

    def esc(self):
        self.master.destroy()
        
def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
