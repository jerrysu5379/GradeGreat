# main.py
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import plotly.express as px
import webbrowser
import os
from utilities.sqlite_db import SQLiteDB

def get_database_engine(engine, db_path):
    if engine == "sqlite":
        return SQLiteDB(db_path)
    else:
        raise ValueError("Unsupported database engine")

class App:
    def __init__(self, root, db_engine):
        self.root = root
        self.db_engine = db_engine

        self.root.title("Login/Register")

        self.login_frame = tk.Frame(self.root)
        self.register_frame = tk.Frame(self.root)

        self.username_label = tk.Label(self.login_frame, text="Username")
        self.username_entry = tk.Entry(self.login_frame)
        self.password_label = tk.Label(self.login_frame, text="Password")
        self.password_entry = tk.Entry(self.login_frame, show="*")

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.register_button = tk.Button(self.login_frame, text="Register", command=self.show_register)

        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.password_label.grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)
        self.login_button.grid(row=2, column=0)
        self.register_button.grid(row=2, column=1)

        self.login_frame.pack()

        self.db_engine.create_user_table()

    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack()

        self.reg_username_label = tk.Label(self.register_frame, text="Username")
        self.reg_username_entry = tk.Entry(self.register_frame)
        self.reg_password_label = tk.Label(self.register_frame, text="Password")
        self.reg_password_entry = tk.Entry(self.register_frame, show="*")
        self.reg_button = tk.Button(self.register_frame, text="Register", command=self.register)

        self.reg_username_label.grid(row=0, column=0)
        self.reg_username_entry.grid(row=0, column=1)
        self.reg_password_label.grid(row=1, column=0)
        self.reg_password_entry.grid(row=1, column=1)
        self.reg_button.grid(row=2, column=1)

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        success = self.db_engine.register_user(username, password)
        if success:
            messagebox.showinfo("Success", "Registration successful")
            self.register_frame.pack_forget()
            self.login_frame.pack()
        else:
            messagebox.showerror("Error", "Username already exists")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        result = self.db_engine.authenticate_user(username, password)
        if result:
            messagebox.showinfo("Success", "Login successful")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_main_application(self):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.main_frame.pack()

        # Example content for the main application interface
        welcome_label = tk.Label(self.main_frame, text="Welcome to the main application!")
        welcome_label.pack()

        # Additional functionality can be added here
        show_plot_button = tk.Button(self.main_frame, text="Show Plot", command=self.show_plot)
        show_plot_button.pack()

        #Open sqlite file to read

if __name__ == "__main__":
    db_engine_name = os.getenv("DB_ENGINE", "sqlite")
    db_path = os.getenv("DB_PATH", "users.db")
    db_engine = get_database_engine(db_engine_name, db_path)

    root = tk.Tk()
    app = App(root, db_engine)
    root.mainloop()