# -*- coding: utf-8 -*-

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as filedialog
from tkinter import messagebox as messagebox
from tkinter import simpledialog as simpledialog
import os
try:
    from libs import crypto_funcs
    from libs import sql
    import pandas as pd
except Exception as e:
    print("Error: {}".format(e))
    sys.exit()

class first_window:
    file=""
    masterpass=""
    def __init__(self, master):
        self.master = master
        self.master.title("Choose/Create a Database")
        self.master.geometry('800x400+0+0')
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.file_open = tk.StringVar()
        self.password_open_1 = tk.StringVar()
        self.file_create = tk.StringVar()
        self.password_create_1 = tk.StringVar()
        self.password_create_2 = tk.StringVar()
        
        self.label = tk.Label(self.frame, text = "Open Database")
        self.label.grid(row=0, column= 0, columnspan=4)
        
        self.label = tk.Label(self.frame, text = "File: ")
        self.label.grid(row=1, column= 0)
        self.open_file=tk.Entry(self.frame, textvariable=self.file_open)
        self.open_file.grid(row=1, column= 1)
        self.open_file.insert(tk.END, os.getcwd() + '\surelock.db')
        self.open_file_browse = tk.Button(self.frame, text="Browse...", command=self.open_database)
        self.open_file_browse.grid(row=1, column= 2)
        self.label = tk.Label(self.frame, text = "Password: ")
        self.label.grid(row=2, column= 0)
        self.open_file_pwd1=tk.Entry(self.frame, show="*", textvariable=self.password_open_1)
        self.open_file_pwd1.insert(tk.END, "1")        #This line temporarily exists to speed up testing with the default database
        self.open_file_pwd1.grid(row=2, column= 1)
        
        self.open = tk.Button(self.frame, text = 'Open', command = self.next_window_open)
        self.open.grid(row=3, column=4, padx=10)

        self.label = tk.Label(self.frame, text = "Create Database")
        self.label.grid(row=4, column= 0, columnspan=4)
        
        self.label = tk.Label(self.frame, text = "File: ")
        self.label.grid(row=5, column= 0)
        self.create_file=tk.Entry(self.frame, textvariable=self.file_create)
        self.create_file.grid(row=5, column= 1)
        self.open_file_browse = tk.Button(self.frame, text="Browse...", command=self.create_database)
        self.open_file_browse.grid(row=5, column= 2)
        self.label = tk.Label(self.frame, text = "Password: ")
        self.label.grid(row=6, column= 0)
        self.create_file_pwd1=tk.Entry(self.frame, show="*", textvariable=self.password_create_1)
        self.create_file_pwd1.grid(row=6, column= 1)
        self.label = tk.Label(self.frame, text = "Repeat Password: ")
        self.label.grid(row=7, column= 0)
        self.create_file_pwd2=tk.Entry(self.frame, show="*", textvariable=self.password_create_2)
        self.create_file_pwd2.grid(row=7, column= 1)
        
        self.create = tk.Button(self.frame, text = 'Create', command = self.next_window_create)
        self.create.grid(row=7, column=4, padx=10)

        self.exit = tk.Button(self.frame, text = 'Exit', command = self.exit_surelock)
        self.exit.grid(row=9, column=4, pady=10, padx=10)
        
        self.pw_gen = tk.Button(self.frame, text = 'Password Generator', command = self.start_password_generator)
        self.pw_gen.grid(row=10, column=0, pady=10, padx=10, columnspan=5)
        
    def open_database(self):
        filename = filedialog.askopenfilename(filetypes=(("Database files", "*.db"),("All files", "*.*") ))
        self.open_file.delete(0,tk.END)
        self.open_file.insert(0,filename)
    
    def create_database(self):
        filename = filedialog.asksaveasfilename(filetypes=(("Database files", "*.db"),("All files", "*.*") ))
        self.create_file.delete(0,tk.END)
        self.create_file.insert(0,filename)
        
    def next_window_open(self):
        first_window.file= self.file_open.get()
        first_window.masterpass = self.password_open_1.get()
        self.master.destroy()

    def next_window_create(self):
        file= self.file_create.get()
        pwd1 = self.password_create_1.get()
        pwd2 = self.password_create_2.get()
        
        if pwd1==pwd2:
            first_window.file=file
            first_window.masterpass=pwd1
            self.master.destroy()
            
    def start_password_generator(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = pw_gen_window(self.newWindow)
        self.newWindow.transient(self.master)
        
    def exit_surelock(self):
        self.master.destroy()
    
class main_window:
    db_main=""
    masterpass_main=""
    def __init__(self, master):

        self.master = master
        self.master.title("Surelock Password Manager")
        self.master.geometry('1250x650+0+0')
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.newWindow = tk.Toplevel(self.master)
        self.app = first_window(self.newWindow)
        self.newWindow.transient(self.master)
        self.master.wait_window(self.newWindow)

        main_window.db_main=sql.Database(filename=first_window.file)
        main_window.masterpass_main = first_window.masterpass

        self.menubar=tk.Menu(self.frame)
        self.filemenu=tk.Menu(self.menubar ,tearoff =0)
        self.filemenu.add_command(label="Open/Create Database", command=self.open_or_create_database)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.frame.quit)
        self.menubar.add_cascade(label="File",menu=self.filemenu)
        self.helpmenu=tk.Menu(self.menubar ,tearoff =0)
        self.helpmenu.add_command(label="About", command=self.open_about)
        self.menubar.add_cascade(label="Help",menu=self.helpmenu)
        self.master.config(menu=self.menubar) 

        self.categorylabel = tk.Label(self.frame, text ="Categories:")
        self.categorylabel.grid(row=0, column =0, columnspan =2)
        
        self.category_list = tk.Listbox(self.frame)
        if (first_window.masterpass != "" and first_window.file != ""):
            self.tables = sql.list_tables(main_window.db_main)
            for  entry  in self.tables: self.category_list.insert(tk.END ,entry[0])
            self.category_list.selection_set(0)
        self.category_list.grid(row=1, column =0, columnspan =2)
        self.category_list.bind("<<ListboxSelect>>", self.change_selected_table)
        
        self.add_category_button= tk.Button(self.frame, text="Add Category", command=self.add_category)
        self.add_category_button.grid(row=2, column =0)
        
        self.delete_category_button= tk.Button(self.frame , text="Delete Category", command=self.delete_category)
        self.delete_category_button.grid(row=2, column =1)
        
        self.entry_list = ttk.Treeview(self.frame, columns=("Username", "Password", "Description"))
        self.entry_list.heading('Username', text='Username')
        self.entry_list.heading('Password', text='Password')
        self.entry_list.heading('Description', text='Description')
        if (first_window.masterpass != "" and first_window.file != "" and len(sql.list_tables(main_window.db_main)) != 0):
            for entry in sql.retrieve_table(main_window.db_main, sql.list_tables(main_window.db_main)[self.category_list.curselection()[0]][0]):
                self.entry_list.insert("", "end", text=entry[0], values=(entry[2], "*********", entry[1]))
        self.entry_list.grid(row=1, column =2, columnspan =13)
        self.entry_list.bind("<<TreeviewSelect>>", self.change_button_activation)
        
        self.add_entry_button= tk.Button(self.frame, text="Add Entry", command=self.add_entry)
        self.add_entry_button.grid(row=2, column =12)
        
        self.delete_entry_button= tk.Button(self.frame, text="Delete Entry", command=self.delete_entry)
        self.delete_entry_button.grid(row=2, column =11)
        
        self.get_password_button= tk.Button(self.frame, text="Show Password", command=self.show_password)
        self.get_password_button.grid(row=2, column =14)

        self.copy_password_button= tk.Button(self.frame, text="Copy Password to Clipboard", command=self.copy_password)
        self.copy_password_button.grid(row=2, column =13)
        
        self.clear_clipboard = tk.Button(self.frame, text="Clear clipboard", command=self.clear_clipboard)
        self.clear_clipboard.grid(row = 3, column = 13)
        
        self.delete_entry_button.config(state = tk.DISABLED)
        self.copy_password_button.config(state = tk.DISABLED)
        self.get_password_button.config(state = tk.DISABLED)
        
    def change_selected_table(self, event):
        if len(self.category_list.curselection()) == 1:
            self.entry_list.selection_remove(self.entry_list.selection())
            selectionnumber=self.category_list.curselection()[0]
            table=sql.list_tables(main_window.db_main)[selectionnumber][0]
            self.entry_list.delete(*self.entry_list.get_children())
            for  entry  in sql.retrieve_table(main_window.db_main, table): self.entry_list.insert("", "end", text=entry[0], values=(entry[2], "*********", entry[1]))
    
    def add_category(self):
        answer = simpledialog.askstring("Add category", "Category name: ",parent=self.frame)
        if answer != "":
            self.category_list.insert(tk.END ,answer)
            sql.create_table(main_window.db_main, answer)

    def delete_category(self):
        answer=self.category_list.curselection()[0]
        tables=sql.list_tables(main_window.db_main)
        if messagebox.askokcancel("Question", "Do you want to delete the category " + tables[answer][0] + "?"):
            self.category_list.delete(answer)
            self.entry_list.delete(*self.entry_list.get_children())
            sql.delete_table(main_window.db_main, tables[answer][0])
            self.category_list.selection_set(0)
            self.entry_list.delete(*self.entry_list.get_children())
            if len(sql.list_tables(main_window.db_main)) != 0:
                table=sql.list_tables(main_window.db_main)[0][0]
                for  entry  in sql.retrieve_table(main_window.db_main, table): self.entry_list.insert("", "end", text=entry[0], values=(entry[2], "*********", entry[1]))
    
    def add_entry(self):
        a = self.category_list.curselection()
        self.newWindow = tk.Toplevel(self.master)
        self.app = add_window(self.newWindow)
        self.master.wait_window(self.newWindow)
        self.category_list.selection_set(a)

    def delete_entry(self):
        entry = self.entry_list.focus()
        itemname = self.entry_list.item(entry)["text"]
        if messagebox.askokcancel("Question", "Do you want to delete the entry " + itemname + "?"):
            table = sql.list_tables(main_window.db_main)[self.category_list.curselection()[0]][0]
            sql.delete_entry(main_window.db_main, itemname, table)
            self.entry_list.delete(*self.entry_list.get_children())
            for  entry  in sql.retrieve_table(main_window.db_main, table): self.entry_list.insert("", "end", text=entry[0], values=(entry[2], "*********", entry[1]))
        
    def show_password(self):
        entry = self.entry_list.focus()
        itemname = self.entry_list.item(entry)["text"]
        table = sql.list_tables(main_window.db_main)[self.category_list.curselection()[0]][0]
        password = sql.retrieve_entry(main_window.db_main, main_window.masterpass_main, itemname, table)
        messagebox.showinfo("Password", "The password for {} is {}".format(itemname, password))

    def copy_password(self):
        entry = self.entry_list.focus()
        itemname = self.entry_list.item(entry)["text"]
        table = sql.list_tables(main_window.db_main)[self.category_list.curselection()[0]][0]
        password = sql.retrieve_entry(main_window.db_main, main_window.masterpass_main, itemname, table)
        try:
            df=pd.DataFrame([str(password)])
            df.to_clipboard(index=False,header=False)
        except Exception as e:
            print("Error: {}".format(e))

    def open_or_create_database(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = first_window(self.newWindow)
        self.newWindow.transient(self.master)
        self.master.wait_window(self.newWindow)
        main_window.db_main=sql.Database(filename=first_window.file)
        main_window.masterpass_main = first_window.masterpass
        tables = sql.list_tables(main_window.db_main)
        self.category_list.delete(0,tk.END)
        if len(tables) != 0:
            for  entry  in tables: self.category_list.insert(tk.END ,entry[0])
        self.category_list.selection_set(0)
        self.entry_list.delete(*self.entry_list.get_children())
        if len(tables) != 0:
            table=sql.list_tables(main_window.db_main)[0][0]
            for  entry  in sql.retrieve_table(main_window.db_main, table): self.entry_list.insert("", "end", text=entry[0], values=(entry[2], "*********", entry[1]))
        
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

    def open_about(self):
            return

class add_window:
    db_main=""
    masterpass_main=""
    def __init__(self, master):
        add_window.db_main = main_window.db_main
        add_window.masterpass_main = main_window.masterpass_main
        
        self.master = master
        self.master.title("Add an entry")
        self.master.geometry('1250x650+0+0')
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.site = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.description = tk.StringVar()
        self.category = tk.StringVar()
        self.characters = tk.IntVar()
        self.special_characters = tk.BooleanVar()
        
        self.label = tk.Label(self.frame, text = "Site: ")
        self.label.grid(row = 0, column = 0)
        self.site = tk.Entry(self.frame, textvariable=self.site)
        self.site.grid(row = 0, column = 1)
        self.label = tk.Label(self.frame, text = "Username: ")
        self.label.grid(row = 1, column = 0)
        self.username = tk.Entry(self.frame, textvariable=self.username)
        self.username.grid(row = 1, column = 1)
        self.label = tk.Label(self.frame, text = "Password: ")
        self.label.grid(row = 2, column = 0)
        self.password = tk.Entry(self.frame, show="*", width = 50, textvariable=self.password)
        self.password.grid(row = 2, column = 1)
        
        self.label = tk.Label(self.frame, text = "Generate a random password for this entry: ")
        self.label.grid(row = 0, column = 3)
        self.label = tk.Label(self.frame, text = "Number of characters: ")
        self.label.grid(row = 1, column = 3)
        self.chars = tk.Scale(self.frame, from_=8,to=40, orient=tk.HORIZONTAL, variable=self.characters)
        self.chars.grid(row = 1, column = 4)
        self.chars.set(16)
        self.sp_chars=tk.Checkbutton(self.frame,text="Generate with special chracters", variable=self.special_characters)
        self.sp_chars.grid(row = 2, column = 3, columnspan = 2)
        self.password_button = tk.Button(self.frame, text="Generate a random password", command=self.generate)
        self.password_button.grid(row = 3, column = 3)
        
        self.label = tk.Label(self.frame, text = "Category: ")
        self.label.grid(row = 3, column = 0)
        self.category = tk.Entry(self.frame, textvariable=self.category)
        self.category.grid(row = 3, column = 1)
        self.label = tk.Label(self.frame, text = "Description: ")
        self.label.grid(row = 4, column = 0)
        self.description = tk.Entry(self.frame, textvariable=self.description)
        self.description.grid(row = 4, column = 1)
        
        self.ok_button = tk.Button(self.frame, text="OK", command=self.add_entry)
        self.ok_button.grid(row = 5, column = 0, columnspan = 2)
        
    def add_entry(self):
        site = self.site.get()
        username = self.username.get()
        password = self.password.get()
        description = self.description.get()
        table = self.category.get()
        sql.insert_entry(add_window.db_main, add_window.masterpass_main, site, password, description, table, username=username)
        self.master.destroy()
        
    def generate(self):
        pw = crypto_funcs.pwd_gen(special_chars = self.special_characters.get(), characters = self.characters.get())
        self.password.delete(0, tk.END)
        self.password.insert(tk.END, pw)
        
class pw_gen_window:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")
        self.master.geometry('1250x650+0+0')
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.start_pwd = tk.StringVar()
        self.characters = tk.IntVar()
        self.special_characters = tk.BooleanVar()
        
        self.label = tk.Label(self.frame, text = "Generate a strong password based on a simple one")
        self.label.grid(row = 0, column = 0)
        self.label = tk.Label(self.frame, text = "Simple Password: ")
        self.label.grid(row = 1, column = 0)
        self.base_pwd = tk.Entry(self.frame, textvariable=self.start_pwd)
        self.base_pwd.grid(row = 1, column = 1)
        self.label = tk.Label(self.frame, text = "Number of characters: ")
        self.label.grid(row = 2, column = 0)
        self.chars = tk.Scale(self.frame, from_=8,to=40, orient=tk.HORIZONTAL, variable=self.characters)
        self.chars.grid(row = 2, column = 1)
        self.chars.set(16)
        self.sp_chars=tk.Checkbutton(self.frame,text="Generate with special chracters", variable=self.special_characters)
        self.sp_chars.grid(row = 3, column = 0, columnspan = 2)
        self.label = tk.Label(self.frame, text = "Generated Password: ")
        self.label.grid(row = 4, column = 0)
        self.new_pwd = tk.Entry(self.frame, width = 50)
        self.new_pwd.grid(row = 4, column = 1)
        self.ok_button = tk.Button(self.frame, text="OK", command=self.generate)
        self.ok_button.grid(row = 5, column = 0)
        self.esc_button = tk.Button(self.frame, text="Exit", command=self.esc)
        self.esc_button.grid(row = 6, column = 0)
        self.copy_to_clipboard = tk.Button(self.frame, text="Copy to clipboard", command=self.copy)
        self.copy_to_clipboard.grid(row = 5, column = 1)
        self.clear_clipboard = tk.Button(self.frame, text="Clear clipboard", command=self.clear)
        self.clear_clipboard.grid(row = 5, column = 2)
        

    def generate(self):
        pw = crypto_funcs.pwd_gen(self.start_pwd.get(), self.special_characters.get(), characters = self.characters.get())
        self.new_pwd.delete(0, tk.END)
        self.new_pwd.insert(tk.END, pw)
        return pw
    
    def copy(self):
        try:
            df=pd.DataFrame([str(self.generate())])
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
        exit()
        
def main():
    root = tk.Tk()
    app = main_window(root)
    root.mainloop()

if __name__ == '__main__':
    main()
