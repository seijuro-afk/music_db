import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Function to fetch data
def fetch_top_songs():
    account_id = account_id_entry.get()
    if not account_id:
        messagebox.showerror("Input Error", "Please enter an Account ID.")
        return
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Adobo5093",
            database="musiclibrarydb"
        )
        cursor = connection.cursor()
        
        check_data = "SELECT COUNT(*) FROM account WHERE account_id = %s"
        cursor.execute(check_data, (account_id,))
        result = cursor.fetchone()

        if result[0] == 0:
            messagebox.showinfo("Notification", "Account not found in the database")
            return
        else:
            messagebox.showinfo("Notification", "Account found in the database")

        # Execute the query
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
        
        # Clear the table
        for item in table.get_children():
            table.delete(item)
        
        # Insert fetched data into the table
        for row in rows:
            table.insert("", "end", values=row)
        
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Create the main GUI window
root = tk.Tk()
root.title("Top Songs Played by Account")
root.configure(bg="#2c2c2c")  # Dark theme

# Style configuration
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", borderwidth=0)
style.configure("Treeview.Heading", background="#444444", foreground="white", font=("Arial", 10, "bold"))
style.map("Treeview", background=[("selected", "#666666")])
style.configure("TButton", background="#444444", foreground="white", borderwidth=0)
style.map("TButton", background=[("active", "#555555")])

# Account ID input
account_id_label = tk.Label(root, text="Enter Account ID:", bg="#2c2c2c", fg="white", font=("Arial", 10))
account_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

account_id_entry = tk.Entry(root, bg="#444444", fg="white", font=("Arial", 10), relief="flat")
account_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Fetch button
fetch_button = ttk.Button(root, text="Fetch Top Songs", command=fetch_top_songs)
fetch_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Table to display data
columns = ("Song Title", "Play Count")
table = ttk.Treeview(root, columns=columns, show="headings")
table.heading("Song Title", text="Song Title")
table.heading("Play Count", text="Play Count")
table.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Scrollbar for the table
scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.grid(row=1, column=3, sticky="ns")

# Adjust column weights
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(1, weight=1)

# Start the GUI loop
root.mainloop()
