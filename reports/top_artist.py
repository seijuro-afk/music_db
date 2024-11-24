import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

def fetch_most_listened_artists():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="musiclibrarydb"
        )
        cursor = connection.cursor()

        # Query for most listened artists
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
            Play_Count DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Clear the table
        for item in table.get_children():
            table.delete(item)

        # Insert fetched data into the table
        for row in rows:
            table.insert("", "end", values=row)

        if not rows:
            messagebox.showinfo("No Data", "No artist records found.")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Create GUI
root = Tk()
root.title("Most Listened Artists")
root.geometry("600x400")
root.configure(bg="#2b2b2b")  # Dark theme background

# Label
title_label = Label(
    root, text="Top Artists", font=("Helvetica", 16), fg="white", bg="#2b2b2b"
)
title_label.pack(pady=10)

# Table
columns = ("Artist Name", "Play Count")
table = ttk.Treeview(root, columns=columns, show="headings", height=15)
table.heading("Artist Name", text="Artist Name")
table.heading("Play Count", text="Play Count")
table.column("Artist Name", width=300)
table.column("Play Count", width=100)
table.pack(pady=20)

# Style for dark theme
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background="#444",
    foreground="white",
    fieldbackground="#444",
    rowheight=25,
    font=("Helvetica", 10),
)
style.configure("Treeview.Heading", background="#333", foreground="white", font=("Helvetica", 11))

# Button
fetch_button = Button(
    root, text="Fetch Most Listened Artists", command=fetch_most_listened_artists, bg="#444", fg="white", font=("Helvetica", 11), relief=FLAT
)
fetch_button.pack(pady=10)

# Run the GUI
root.mainloop()
