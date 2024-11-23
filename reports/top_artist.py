import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

def fetch_most_listened_artists():
    """Fetch the most listened artists based on song streams from the database."""
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
                    a.name AS Artist_Name,
                    SUM(s.song_streams) AS Total_Streams
                FROM 
                    artists a
                JOIN 
                    songsartists sa ON a.artist_id = sa.artist_id
                JOIN 
                    songs s ON sa.song_id = s.song_id
                GROUP BY 
                    a.artist_id
                ORDER BY 
                    Total_Streams DESC
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

def display_most_listened_artists():
    """Display the most listened artists in a Tkinter GUI."""
    # Fetch data
    data = fetch_most_listened_artists()

    # Create the main window
    root = tk.Tk()
    root.title("Most Listened Artists")
    root.geometry("500x400")
    root.configure(bg="#121212")  # Dark background

    # Title Label
    title_label = tk.Label(
        root, 
        text="Most Listened Artists", 
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

    # Add Treeview to display artist data
    tree = ttk.Treeview(root, columns=("Artist Name", "Total Streams"), show="headings")
    tree.heading("Artist Name", text="Artist Name")
    tree.heading("Total Streams", text="Total Streams")
    tree.column("Artist Name", width=250)
    tree.column("Total Streams", width=150, anchor="center")

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
display_most_listened_artists()
