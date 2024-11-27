import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

def fetch_top_songs(account_id):
    """Fetch the top songs played by a specific account."""
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your username
            password="Adobo5093",  # Replace with your password
            database="musiclibrarydb"  # Replace with your database name
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Check if account exists
            check_query = "SELECT COUNT(*) FROM accounts WHERE account_id = %s"
            cursor.execute(check_query, (account_id,))
            account_exists = cursor.fetchone()[0]

            if account_exists == 0:
                messagebox.showinfo("Notification", "Account not found in the database.")
                return []

            # Query to fetch top songs played by account
            query = """
            SELECT 
                s.title AS Song_Title,
                COUNT(sh.song_id) AS Play_Count
            FROM 
                songhistory sh
            JOIN 
                songs s ON sh.song_id = s.song_id
            WHERE 
                sh.account_id = %s
            GROUP BY 
                s.song_id
            ORDER BY 
                Play_Count DESC;
            """
            cursor.execute(query, (account_id,))
            rows = cursor.fetchall()
            return rows

    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def display_top_songs():
    """Display top songs played by a specific account in a Tkinter GUI."""
    # Fetch the Account ID from the input field
    account_id = account_id_entry.get().strip()

    if not account_id:
        messagebox.showerror("Input Error", "Please enter an Account ID.")
        return

    # Fetch data
    data = fetch_top_songs(account_id)

    # Clear existing data from the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Populate the Treeview with new data
    if data:
        for row in data:
            tree.insert("", tk.END, values=row)
    else:
        messagebox.showinfo("Notification", "No songs found for this account.")

# Create the main GUI window
root = tk.Tk()
root.title("Top Songs Played by Account")
root.geometry("600x400")
root.configure(bg="#2b2b2b")  # Dark theme background

# Title label
title_label = tk.Label(
    root,
    text="Top Songs Played by Account",
    bg="#2b2b2b",
    fg="white",
    font=("Arial", 16, "bold")
)
title_label.pack(pady=10)

# Account ID input
input_frame = tk.Frame(root, bg="#2b2b2b")
input_frame.pack(pady=10)

account_id_label = tk.Label(
    input_frame, 
    text="Enter Account ID:", 
    bg="#2b2b2b", 
    fg="white", 
    font=("Arial", 12)
)
account_id_label.grid(row=0, column=0, padx=5, pady=5)

account_id_entry = tk.Entry(input_frame, bg="#444444", fg="white", font=("Arial", 12), relief="flat")
account_id_entry.grid(row=0, column=1, padx=5, pady=5)

fetch_button = tk.Button(
    input_frame, 
    text="Fetch Songs", 
    command=display_top_songs, 
    bg="#444444", 
    fg="white", 
    font=("Arial", 12), 
    relief="flat", 
    activebackground="#555555", 
    activeforeground="white"
)
fetch_button.grid(row=0, column=2, padx=5, pady=5)

# Treeview for song data
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background="#333333",
    foreground="white",
    fieldbackground="#333333",
    rowheight=25,
    font=("Arial", 10)
)
style.configure(
    "Treeview.Heading",
    background="#444444",
    foreground="white",
    font=("Arial", 11, "bold")
)
style.map(
    "Treeview",
    background=[("selected", "#555555")],
    foreground=[("selected", "white")]
)

tree_frame = tk.Frame(root, bg="#2b2b2b")
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("Song Title", "Play Count")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
tree.heading("Song Title", text="Song Title")
tree.heading("Play Count", text="Play Count")
tree.column("Song Title", width=300)
tree.column("Play Count", width=100, anchor="center")
tree.pack(fill=tk.BOTH, expand=True)

# Scrollbar for the Treeview
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Close button
close_button = tk.Button(
    root,
    text="Close",
    command=root.destroy,
    bg="#444444",
    fg="white",
    font=("Arial", 12),
    relief="flat",
    activebackground="#555555",
    activeforeground="white"
)
close_button.pack(pady=10)

# Start the GUI application
root.mainloop()
