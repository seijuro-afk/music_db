import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from user_view.user_view import MusicPlayer

# Connect to MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       # Replace with your MySQL username
            password='Adobo5093',    # Replace with your MySQL password
            database='musiclibrarydb'     # Replace with your database name
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

# Function to handle signup
def signup():
    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()
    created_at = datetime.now()
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO account (username, email, password, created_at) VALUES (%s, %s, %s, %s)", 
                           (username, email, password, created_at))
            connection.commit()
            messagebox.showinfo("Signup", "Account created successfully!")
            MusicPlayer(root)
            root.withdraw()
        except Error as e:
            messagebox.showerror("Signup Error", f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to handle login
def login():
    email = entry_email.get()
    password = entry_password.get()

    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM account WHERE email = %s AND password = %s", (email, password))
            account = cursor.fetchone()
            if account:
                messagebox.showinfo("Login", "Login successful!")
                root.withdraw()
                MusicPlayer(root)
            else:
                messagebox.showerror("Login", "Invalid email or password.")
        except Error as e:
            messagebox.showerror("Login Error", f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Tkinter GUI
root = tk.Tk()
root.title("Signup/ Login Frame")
root.geometry("400x300")

# Dark theme colors
bg_color = "#1a1a1a"
fg_color = "#ffffff"
accent_color = "#555555"

root.configure(bg=bg_color)

# Styling labels and entries
label_font = ("Arial", 12)
entry_bg = "#333333"
entry_fg = fg_color

# Username label and entry for signup
tk.Label(root, text="Username", font=label_font, fg=fg_color, bg=bg_color).grid(row=0, column=0, pady=10, padx=10, sticky="w")
entry_username = tk.Entry(root, font=label_font, bg=entry_bg, fg=entry_fg, insertbackground=fg_color)
entry_username.grid(row=0, column=1, padx=10, pady=10)

# Email label and entry for both signup and login
tk.Label(root, text="Email", font=label_font, fg=fg_color, bg=bg_color).grid(row=1, column=0, pady=10, padx=10, sticky="w")
entry_email = tk.Entry(root, font=label_font, bg=entry_bg, fg=entry_fg, insertbackground=fg_color)
entry_email.grid(row=1, column=1, padx=10, pady=10)

# Password label and entry for both signup and login
tk.Label(root, text="Password", font=label_font, fg=fg_color, bg=bg_color).grid(row=2, column=0, pady=10, padx=10, sticky="w")
entry_password = tk.Entry(root, show="*", font=label_font, bg=entry_bg, fg=entry_fg, insertbackground=fg_color)
entry_password.grid(row=2, column=1, padx=10, pady=10)

# Signup and Login buttons with accent color
btn_signup = tk.Button(root, text="Sign Up", command=signup, bg=accent_color, fg=fg_color, font=label_font, relief="flat")
btn_signup.grid(row=3, column=0, pady=20)

btn_login = tk.Button(root, text="Login", command=login, bg=accent_color, fg=fg_color, font=label_font, relief="flat")
btn_login.grid(row=3, column=1, pady=20)

root.mainloop()
