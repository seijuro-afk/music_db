import tkinter as tk
from login import login_screen
from initialize import initialize
from query import create_connection

db = create_connection()

# Initialize main application after login
def start_main_app(username, email):
    root = tk.Tk()
    root.title("Music Player")
    root.geometry("1200x900")
    root.config(bg="#1c1c1c")
    
    # Call the initialize function and pass db, root, and username for further use in the app
    initialize(db, root, username, email)
    root.mainloop()

# Show the login screen first
login_screen(db, start_main_app)