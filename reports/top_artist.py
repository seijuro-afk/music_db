import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

def fetch_most_listened_artists():
    """Fetch the most listened artists based on song play history."""
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your username
            password="your_password",  # Replace with your password
            database="musiclibrarydb"  # Replace with your database name
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Query to get most listened artists
            query = """
            SELECT 
                a.name AS Artist_Name,
                COUNT(sh.song_id) AS Play_Count
            FROM 
                songhistory sh
            JOIN 
                songs s ON sh.song_id = s.song_id
            JOIN 
                songsartists sa ON s.song_id = sa.song_id
            JOIN 
                artists a ON sa.artist_id = a.artist_id
            GROUP BY 
                a.artist_id
            ORDER BY 
                Play_Count DESC
            LIMIT 10;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def display_most_listened_artists():
    """Display the most listened artists in a Tkinter GUI."""
    # Fetch data
    data = fetch_most_listened_artists()

    # Create the main window
    root = tk.Tk()
    root.title("Most Listened Artists")
    root.geometry("600x400")
    root.configure(bg="#2b2b2b")  # Dark background

    # Title Label
    title_label = tk.Label(
        root,
        text="Most Listened Artists",
        bg="#2b2b2b",
        fg="white",
        font=("Arial", 16, "bold")
    )
    title_label.pack(pady=10)

    # Treeview for artist data
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#444",
        foreground="white",
        rowheight=25,
        fieldbackground="#444",
        font=("Arial", 10)
    )
    style.configure(
        "Treeview.Heading",
        background="#333",
        foreground="white",
        font=("Arial", 11, "bold")
    )
    style.map(
        "Treeview",
        background=[("selected", "#555")],
        foreground=[("selected", "white")]
    )

    # Add Treeview widget
    tree = ttk.Treeview(root, columns=("Artist Name", "Play Count"), show="headings")
    tree.heading("Artist Name", text="Artist Name")
    tree.heading("Play Count", text="Play Count")
    tree.column("Artist Name", width=300)
    tree.column("Play Count", width=150, anchor="center")
    
    # Insert data into Treeview
    for row in data:
        tree.insert("", tk.END, values=row)

    tree.pack(pady=20, fill=tk.BOTH, expand=True)

    # Close Button
    close_button = tk.Button(
        root,
        text="Close",
        command=root.destroy,
        bg="#444",
        fg="white",
        font=("Arial", 10),
        relief="flat",
        activebackground="#555",
        activeforeground="white"
    )
    close_button.pack(pady=10)

    # Run the application
    root.mainloop()

# Call the display function
display_most_listened_artists()
