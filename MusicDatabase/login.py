import tkinter as tk
import mysql.connector
from tkinter import messagebox
import query

def signup(db, username, email, password):
    """
    Create a new account in the database.
    """
    try:
        query.execute_query(
            db,
            "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        messagebox.showinfo("Signup", "Account created successfully!")
    except Exception as e:
        messagebox.showerror("Signup Error", f"Error: {e}")

def authenticate(db, email, password):
    """
    Authenticate a user with email and password.
    """
    result = query.execute_query(
        db,
        "SELECT username FROM accounts WHERE email = %s AND password = %s",
        (email, password),
        fetchone=True
    )
    return result[0] if result else None

# Function to show the login screen
def login_screen(db, start_main_app_callback):
    login_root = tk.Tk()
    login_root.title("Signup/ Login Frame")
    login_root.geometry("400x300")
    login_root.configure(bg="#1a1a1a")
    
    # Dark theme setup
    label_font = ("Arial", 12)
    entry_bg = "#333333"
    entry_fg = "#ffffff"

    # Username entry for signup
    tk.Label(login_root, text="Username", font=label_font, fg=entry_fg, bg="#1a1a1a").grid(row=0, column=0, pady=10, padx=10)
    entry_username = tk.Entry(login_root, font=label_font, bg=entry_bg, fg=entry_fg)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    # Email entry for login/signup
    tk.Label(login_root, text="Email", font=label_font, fg=entry_fg, bg="#1a1a1a").grid(row=1, column=0, pady=10, padx=10)
    entry_email = tk.Entry(login_root, font=label_font, bg=entry_bg, fg=entry_fg)
    entry_email.grid(row=1, column=1, padx=10, pady=10)

    # Password entry
    tk.Label(login_root, text="Password", font=label_font, fg=entry_fg, bg="#1a1a1a").grid(row=2, column=0, pady=10, padx=10)
    entry_password = tk.Entry(login_root, show="*", font=label_font, bg=entry_bg, fg=entry_fg)
    entry_password.grid(row=2, column=1, padx=10, pady=10)

    def on_signup():
        signup(db, entry_username.get(), entry_email.get(), entry_password.get())

    def on_login(email, password):
        username = authenticate(db, email, password)
        if username:
            messagebox.showinfo("Login", "Login successful!")
            login_root.destroy()
            # Pass email and username to the main app
            start_main_app_callback(username, email)
        else:
            messagebox.showerror("Login", "Invalid email or password.")

    tk.Button(login_root, text="Sign Up", command=on_signup, bg="#555555", fg=entry_fg, font=label_font).grid(row=3, column=0, pady=10)
    tk.Button(login_root, text="Login", command=lambda: on_login(entry_email.get(), entry_password.get()), bg="#555555", fg=entry_fg, font=label_font).grid(row=3, column=1, pady=10)
    tk.Button(login_root, text="Login as Guest", command=lambda: on_login("guest@gmail.com", "1234"), bg="#555555", fg=entry_fg, font=label_font).grid(row=4, column=1, pady=10)

    login_root.mainloop()
