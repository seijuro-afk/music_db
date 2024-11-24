import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

def connect_to_db():
    """Connect to the database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Adobo5093",
            database="musiclibrarydb"
        )
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to the database:\n{e}")
        return None

def open_playlist_control_gui(email):
    """Opens the Playlist Control GUI."""
    playlist_window = Tk()
    playlist_window.title(f"Playlist Control - Email: {email}")
    playlist_window.geometry("700x500")
    playlist_window.configure(bg="#2b2b2b")

    # Create playlist table
    columns = ("Playlist ID", "Playlist Name", "Created At")
    playlist_table = ttk.Treeview(playlist_window, columns=columns, show="headings", height=10)
    playlist_table.heading("Playlist ID", text="Playlist ID")
    playlist_table.heading("Playlist Name", text="Playlist Name")
    playlist_table.heading("Created At", text="Created At")
    playlist_table.column("Playlist ID", width=100)
    playlist_table.column("Playlist Name", width=200)
    playlist_table.column("Created At", width=200)
    playlist_table.pack(pady=10)

    def fetch_playlists():
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                # Ensure email is passed correctly
                cursor.execute(
                    "SELECT playlist_id, name, created_at FROM playlist WHERE email = %s", 
                    (email,)
                )
                rows = cursor.fetchall()

                # Clear the table
                for item in playlist_table.get_children():
                    playlist_table.delete(item)

                # Insert playlists into the table with proper type conversion
                for row in rows:
                    # Convert datetime to string format
                    playlist_id, name, created_at = row
                    created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else ""
                    # Insert formatted values
                    playlist_table.insert("", "end", values=(playlist_id, name, created_at_str))

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching playlists:\n{e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def create_playlist():
        """Create a new playlist for the specified account."""
        playlist_name = simpledialog.askstring("Create Playlist", "Enter playlist name:")
        if not playlist_name:
            messagebox.showwarning("Input Error", "Playlist name cannot be empty.")
            return

        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Pass parameters correctly
                cursor.execute(
                    "INSERT INTO playlist (name, created_at, email) VALUES (%s, %s, %s)",
                    (playlist_name, created_at, email)
                )
                connection.commit()
                messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully.")
                fetch_playlists()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error creating playlist:\n{e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def delete_playlist():
        """Delete the selected playlist."""
        selected_item = playlist_table.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a playlist to delete.")
            return

        # Get the playlist ID from the selected item
        playlist_id = playlist_table.item(selected_item)["values"][0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete playlist ID {playlist_id}?")
        if not confirm:
            return

        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                # Use lists instead of tuples for parameters
                cursor.execute("DELETE FROM playlistssongs WHERE playlist_id = %s", (playlist_id,))
                cursor.execute("DELETE FROM playlist WHERE playlist_id = %s", (playlist_id,))
                connection.commit()
                messagebox.showinfo("Success", f"Playlist ID {playlist_id} deleted successfully.")
                fetch_playlists()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error deleting playlist:\n{e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def add_song_to_playlist():
        """Add a song to the playlist."""
        song_id = song_id_entry.get().strip()
        playlist_id = playlist_id_entry.get().strip()

        if not song_id or not playlist_id:
            messagebox.showwarning("Input Error", "Both Song ID and Playlist ID are required.")
            return

        try:
            # Convert inputs to integers to ensure valid IDs
            song_id = int(song_id)
            playlist_id = int(playlist_id)
        except ValueError:
            messagebox.showerror("Input Error", "Song ID and Playlist ID must be valid numbers.")
            return

        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                # Use list instead of tuple for parameters
                cursor.execute("INSERT INTO playlistssongs (playlist_id, song_id) VALUES (%s, %s)", (playlist_id, song_id))
                connection.commit()
                messagebox.showinfo("Success", f"Song ID {song_id} added to Playlist ID {playlist_id}.")
                song_id_entry.delete(0, END)
                playlist_id_entry.delete(0, END)
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error adding song to playlist:\n{e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    # Title Label
    title_label = Label(
        playlist_window, text=f"Playlist Control for Email: {email}",
        font=("Helvetica", 16), fg="white", bg="#2b2b2b"
    )
    title_label.pack(pady=10)

    # Buttons
    add_playlist_button = Button(
        playlist_window, text="Create Playlist", command=create_playlist,
        bg="#444", fg="white", relief=FLAT
    )
    add_playlist_button.pack(pady=5)

    delete_playlist_button = Button(
        playlist_window, text="Delete Playlist", command=delete_playlist,
        bg="#444", fg="white", relief=FLAT
    )
    delete_playlist_button.pack(pady=5)

    # Song Selection Section
    song_label = Label(playlist_window, text="Add Songs to Playlist", 
                      font=("Helvetica", 12), fg="white", bg="#2b2b2b")
    song_label.pack(pady=10)

    song_frame = Frame(playlist_window, bg="#2b2b2b")
    song_frame.pack(pady=10)

    song_id_label = Label(song_frame, text="Song ID:", 
                         font=("Helvetica", 10), fg="white", bg="#2b2b2b")
    song_id_label.grid(row=0, column=0, padx=5, pady=5)
    song_id_entry = Entry(song_frame, font=("Helvetica", 10), 
                         bg="#444", fg="white", insertbackground="white")
    song_id_entry.grid(row=0, column=1, padx=5, pady=5)

    playlist_id_label = Label(song_frame, text="Playlist ID:", 
                            font=("Helvetica", 10), fg="white", bg="#2b2b2b")
    playlist_id_label.grid(row=1, column=0, padx=5, pady=5)
    playlist_id_entry = Entry(song_frame, font=("Helvetica", 10), 
                            bg="#444", fg="white", insertbackground="white")
    playlist_id_entry.grid(row=1, column=1, padx=5, pady=5)

    add_song_button = Button(
        song_frame, text="Add Song to Playlist", command=add_song_to_playlist,
        bg="#444", fg="white", relief=FLAT
    )
    add_song_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Initial fetch of playlists
    fetch_playlists()

    playlist_window.mainloop()

# Run GUI
if __name__ == "__main__":
    email = simpledialog.askstring("Email", "Enter your email:")
    if email:
        open_playlist_control_gui(email)
