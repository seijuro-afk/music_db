import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def fetch_all_album_data():
    try:
        # Connect to MySQL database (update with your credentials)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Adobo5093",
            database="musiclibrarydb"
        )
        cursor = conn.cursor(dictionary=True)

        # Updated query to include dynamic completion ratio
        query = """
        SELECT 
            a.album_id,
            a.title AS album_title,
            COALESCE(SUM(s.song_streams), 0) AS total_plays,
            CONCAT(
                COUNT(CASE WHEN s.song_streams > 0 THEN asg.song_id END), 
                ' / ', 
                COUNT(asg.song_id)
            ) AS completion_ratio
        FROM 
            albums a
        LEFT JOIN 
            albumssongs asg ON a.album_id = asg.album_id
        LEFT JOIN 
            songs s ON asg.song_id = s.song_id
        GROUP BY 
            a.album_id, a.title;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Clear previous data in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Populate Treeview with new data
        for row in results:
            tree.insert("", "end", values=(row['album_id'], row['album_title'], row['total_plays'], row['completion_ratio']))

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")


# Create tkinter GUI
root = tk.Tk()
root.title("Album Data Viewer")
root.geometry("600x400")
root.configure(bg="#121212")  # Dark background for the root window

# Apply dark theme styles
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e", rowheight=25)
style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Arial", 10, "bold"))
style.map("Treeview", background=[("selected", "#565656")], foreground=[("selected", "white")])

# Fetch button with dark theme
fetch_button = tk.Button(
    root,
    text="Fetch All Albums",
    command=fetch_all_album_data,
    bg="#333333",
    fg="white",
    activebackground="#565656",
    activeforeground="white",
    font=("Arial", 12, "bold"),
)
fetch_button.pack(pady=10)

# Treeview to display album data
columns = ("Album ID", "Title", "Total Plays", "Completion Ratio")
tree = ttk.Treeview(root, columns=columns, show="headings", style="Treeview")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar for Treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Run the GUI
root.mainloop()
