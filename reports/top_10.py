import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

def fetch_top_10_songs():
    """Fetch the top 10 songs with the highest view count from the database."""
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your username
            password='Adobo5093',  # Replace with your password
            database='musiclibrarydb'  # Replace with your database name
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = """
                SELECT 
                    s.title AS Song_Title,
                    s.song_streams AS View_Count,
                    GROUP_CONCAT(a.name SEPARATOR ', ') AS Artists
                FROM 
                    songs s
                JOIN 
                    songsartists sa ON s.song_id = sa.song_id
                JOIN 
                    artists a ON sa.artist_id = a.artist_id
                GROUP BY 
                    s.song_id
                ORDER BY 
                    s.song_streams DESC
                LIMIT 10;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def display_top_10_songs():
    """Display the top 10 songs in a Tkinter GUI."""
    # Fetch data
    data = fetch_top_10_songs()

    # Create the main window
    root = tk.Tk()
    root.title("Top 10 Songs of All Time")
    root.geometry("600x400")
    root.configure(bg="#121212")  # Dark background

    # Title Label
    title_label = tk.Label(
        root, 
        text="Top 10 Songs of All Time", 
        bg="#121212", 
        fg="white", 
        font=("Arial", 16, "bold")
    )
    title_label.pack(pady=10)

    # Create a Treeview widget with dark theme styling
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#1e1e1e",
        foreground="white",
        rowheight=25,
        fieldbackground="#1e1e1e",
        font=("Arial", 10)
    )
    style.configure(
        "Treeview.Heading",
        background="#2c2c2c",
        foreground="white",
        font=("Arial", 11, "bold")
    )
    style.map(
        "Treeview",
        background=[("selected", "#333333")],
        foreground=[("selected", "white")]
    )

    # Add Treeview to display song data
    tree = ttk.Treeview(root, columns=("Title", "Streams", "Artists"), show="headings")
    tree.heading("Title", text="Title")
    tree.heading("Streams", text="View Count")
    tree.heading("Artists", text="Artists")
    tree.column("Title", width=200)
    tree.column("Streams", width=100, anchor="center")
    tree.column("Artists", width=250)

    # Add data to the Treeview
    for row in data:
        tree.insert("", tk.END, values=row)

    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Add a muted close button
    close_button = tk.Button(
        root, 
        text="Close", 
        command=root.destroy, 
        bg="#2c2c2c", 
        fg="white", 
        font=("Arial", 10),
        relief="flat",  # No colorful borders
        activebackground="#333333",  # Darker hover background
        activeforeground="white"
    )
    close_button.pack(pady=10)

    # Run the application
    root.mainloop()

# Call the display function
display_top_10_songs()
