import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label, Frame, Canvas, Entry, N
from PIL import Image, ImageTk
import os
import mysql.connector
from mysql.connector import Error
from collections import deque
from client_gui.delete_account import open_delete_account_gui
from client_gui.playlist_control import open_playlist_control_gui
class MusicPlayer:
    def __init__(self, root, email):
        self.email = email
        self.root = root
        self.current_song_index = 0
        self.new_window = Toplevel(root)
        self.new_window.title("Music Player")
        self.new_window.configure(bg="black")
        self.new_window.geometry("800x600")


        # Exit Protocol
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Main frame to ensure consistent background
        self.main_frame = Frame(self.new_window, bg="#2e2e2e")
        self.main_frame.place(x=0, y=0, width=800, height=600)

        # Create a canvas for the rounded border
        self.search_canvas = Canvas(self.main_frame, bg="#dddddd", highlightthickness=0)
        self.search_canvas.place(relx=0.5, rely=0, anchor=N, width=410, height=40)

        # Add refresh button at top left
        self.refresh_button = tk.Button(
            self.main_frame,
            text="Refresh",
            bg="#2e2e2e",
            fg="white",
            relief=tk.FLAT,
            command=self.refresh_all_data,
            font=('Arial', 10, 'bold')
        )

        # Place the refresh button in the top left corner
        self.refresh_button.place(x=10, y=10, width=80, height=30)

        # Draw a rounded rectangle
        self.create_rounded_rectangle(self.search_canvas, 5, 5, 405, 35, 10, outline="#2e2e2e", width=2)

        # Search frame on the canvas
        self.search_frame = Frame(self.search_canvas, bg="#2e2e2e")
        self.search_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=30)

        self.search_entry = Entry(self.search_frame, bg="#333333", fg="white", relief=tk.FLAT)
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)

        # Placeholder text
        self.search_placeholder_text = "Search here..."
        self.search_entry.insert(0, self.search_placeholder_text)
        self.search_entry.bind("<FocusIn>", self.on_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_focus_out)

        self.search_button = tk.Button(self.search_frame, text="Search", bg="#2e2e2e", fg="white", relief=tk.FLAT, command=self.search_albums)
        self.search_button.pack(side=tk.RIGHT, padx=10, pady=5)


        # Playlist frame
        self.playlist_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.playlist_frame.place(x=0, y=50, width=200, height=500)

        self.account_button = tk.Button(
            self.main_frame, 
            text="Playlist Controls", 
            bg="#2e2e2e", 
            fg="white", 
            relief=tk.FLAT, 
            command=lambda: open_playlist_control_gui(self.email)  # Extract the ID from tuple
        )
        self.account_button.place(x=0, y=50, width=200, height=50)

        self.playlist_label = tk.Label(self.playlist_frame, text="Playlist", bg="#2e2e2e", fg="white")
        self.playlist_label.pack(pady=10)

        self.playlist_listbox = ttk.Treeview(self.playlist_frame, columns=("TitlePlaylist"), show="headings")
        self.playlist_listbox.heading("TitlePlaylist", text="Title")
        self.playlist_listbox.column("TitlePlaylist", anchor=tk.W, width=100)
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True, pady=20)

        self.playlist_listbox.bind('<Double-1>', self.on_playlist_double_click)

        self.populate_playlist_listbox()

        # Account center button (borderless)
        self.account_button = tk.Button(self.main_frame, text="Delete Accounts", bg="#2e2e2e", fg="white", relief=tk.FLAT, command=lambda: open_delete_account_gui(root))
        self.account_button.place(x=600, y=50, width=200, height=50)

        # Queue frame
        self.queue_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.queue_frame.place(x=600, y=100, width=200, height=500)
        self.queue_label = tk.Label(self.queue_frame, text="Queue", bg="#2e2e2e", fg="white")
        self.queue_label.pack(pady=10)

        self.song_queue = deque()

        # Create a Treeview widget
        self.queue_listbox = ttk.Treeview(self.queue_frame, columns=("TitleArtist", "Duration"), show="headings")
        self.queue_listbox.heading("TitleArtist", text="Title by Artist")
        self.queue_listbox.heading("Duration", text="Duration")
        self.queue_listbox.column("TitleArtist", anchor=tk.W, width=100)  # Adjusted width for Title by Artist
        self.queue_listbox.column("Duration", anchor=tk.E, width=100)     # Adjusted width for Duration
        self.queue_listbox.pack(fill=tk.BOTH, expand=True, pady=20)

        # Create a context menu
        self.context_menu = tk.Menu(self.queue_listbox, tearoff=0)
        self.context_menu.add_command(label="Remove", command=self.dequeue_selected_song)
        
        # Bind right-click to the listbox
        self.queue_listbox.bind("<Button-3>", self.show_context_menu)

        # Latest songs and albums frame
        self.latest_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.latest_frame.place(x=200, y=50, width=400, height=450)

        self.latest_label = tk.Label(self.latest_frame, text="Albums", bg="#2e2e2e", fg="white")
        self.latest_label.pack(pady=10)

        # Add Treeview in the center with album title and a button
        self.album_tree = ttk.Treeview(self.latest_frame, columns=("AlbumTitle", "CreatedAt"), show="headings")
        self.album_tree.heading("AlbumTitle", text="Album Title")
        self.album_tree.heading("CreatedAt", text="Created At")
        self.album_tree.column("AlbumTitle", anchor=tk.W, width=300)
        self.album_tree.column("CreatedAt", anchor=tk.CENTER, width=100)
        self.album_tree.pack(fill=tk.BOTH, expand=True)


        self.album_tree.bind('<Double-1>', self.on_album_double_click)

        self.fetch_and_display_albums()

        # Music player controls frame
        self.controls_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.controls_frame.place(x=200, y=500, width=400, height=100)

        # Custom progress bar
        self.progress_canvas = tk.Canvas(self.controls_frame, bg="#2e2e2e", highlightthickness=0)
        self.progress_canvas.place(relx=0.5, rely=0.2, anchor=tk.CENTER, width=380, height=15)

        self.create_rounded_rectangle(self.progress_canvas, 5, 5, 375, 10, 7, fill="#808080", outline="")

        # Dummy progress for demonstration
        self.progress = self.progress_canvas.create_rectangle(5, 5, 50, 10, fill="#999999", outline="")


        # Load and resize images using PIL
        self.previous_image = Image.open(os.path.join("prev.png"))
        self.previous_image = self.previous_image.resize((50, 50), Image.LANCZOS)  # Adjust the size as needed
        self.previous_image = ImageTk.PhotoImage(self.previous_image)

        self.play_pause_image = Image.open("play.png")
        self.play_pause_image = self.play_pause_image.resize((50, 50), Image.LANCZOS)
        self.play_pause_image = ImageTk.PhotoImage(self.play_pause_image)

        self.next_image = Image.open("next.png")
        self.next_image = self.next_image.resize((50, 50), Image.LANCZOS)
        self.next_image = ImageTk.PhotoImage(self.next_image)

        # Adjust the control buttons with icons
        self.previous_button = tk.Button(self.controls_frame, image=self.previous_image, bg="#2e2e2e", relief=tk.FLAT, command=self.previous_song)
        self.previous_button.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

        self.play_button = tk.Button(self.controls_frame, image=self.play_pause_image, bg="#2e2e2e", relief=tk.FLAT, command=self.play_song)
        self.play_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.next_button = tk.Button(self.controls_frame, image=self.next_image, bg="#2e2e2e", relief=tk.FLAT, command=self.next_song)
        self.next_button.place(relx=0.7, rely=0.7, anchor=tk.CENTER)

        self.like_button = tk.Button(self.controls_frame, text="Like", bg="#2e2e2e", fg="white", relief=tk.FLAT, command=self.toggle_like)
        self.like_button.place(relx=0.9, rely=0.7, anchor=tk.CENTER)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

        return canvas.create_polygon(points, **kwargs, smooth=True)

    def on_entry_click(self, event):
        if self.search_entry.get() == self.search_placeholder_text:
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg="white")

    def on_focus_out(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, self.search_placeholder_text)
            self.search_entry.config(fg="grey")

    def get_song_id(self, song_title):
        """Fetch the song_id from the database based on the song title."""
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                query = "SELECT `song_id` FROM `musiclibrarydb`.`songs` WHERE `title` = %s"
                cursor.execute(query, (song_title,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    messagebox.showerror("Song Not Found", f"Song '{song_title}' not found in the database.")
                    return None
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching song_id: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        else:
            return None


    def toggle_like(self):
        """Toggle like status for the current song."""
        if not self.song_queue:
            messagebox.showinfo("Like", "No songs in the queue.")
            return

        current_song = list(self.song_queue)[self.current_song_index]
        song_id = self.get_song_id(current_song[0])  # Get the song_id using the new method

        if song_id is None:
            return  # Exit if song_id is not found

        account_id = self.get_account_id()  # Get the account_id using the new method

        if account_id is None:
            return  # Exit if account_id is not found

        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                if self.is_song_liked(song_id):
                    # Song is already liked, so unlike it
                    unlike_query = "DELETE FROM `musiclibrarydb`.`accountlikessong` WHERE `account_id` = %s AND `song_id` = %s"
                    cursor.execute(unlike_query, (account_id, song_id))
                
                    decrement_likes_query = "UPDATE `musiclibrarydb`.`songs` SET `song_likes` = `song_likes` - 1 WHERE `song_id` = %s"
                    cursor.execute(decrement_likes_query, (song_id,))
                
                    connection.commit()
                    self.like_button.config(text='Like')
                    messagebox.showinfo("Unlike", f"Unliked '{current_song[0]}'")
                else:
                    # Song is not liked yet, so like it
                    like_query = "INSERT INTO `musiclibrarydb`.`accountlikessong` (`account_id`, `song_id`) VALUES (%s, %s)"
                    cursor.execute(like_query, (account_id, song_id))
                
                    increment_likes_query = "UPDATE `musiclibrarydb`.`songs` SET `song_likes` = `song_likes` + 1 WHERE `song_id` = %s"
                    cursor.execute(increment_likes_query, (song_id,))
                
                    connection.commit()
                    self.like_button.config(text='Unlike')
                    messagebox.showinfo("Like", f"Liked '{current_song[0]}'")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error toggling like status: {e}")
            finally:
                cursor.close()
                connection.close()

        
    def is_song_liked(self, song_id):
        """Check if the current song is liked by the user."""
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                query = "SELECT * FROM `musiclibrarydb`.`accountlikessong` WHERE `account_id` = %s AND `song_id` = %s"
                account_id = self.get_account_id()
                cursor.execute(query, (account_id, song_id))
                result = cursor.fetchone()
                return result is not None
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error checking like status: {e}")
                return False
            finally:
                cursor.close()
                connection.close()
        return False


    def on_closing(self):
        self.new_window.destroy
        self.root.destroy()

    # Connect to MySQL database
    def create_connection(self):
        try:
            connection = mysql.connector.connect(
            host='localhost',
            user='root',       # Replace with your MySQL username
            password='Adobo5093',    # Replace with your MySQL password
            database='musiclibrarydb'     # Replace with your database name
            )
            return connection
        except Error as e:
            tk.messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None

    def fetch_and_enqueue_songs(self):
        """Fetch songs from the database and add them to the queue."""
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT title, song_duration FROM songs")
                songs = cursor.fetchall()

                # Determine if the queue was initially empty
                was_empty = len(self.song_queue) == 0

                for song in songs:
                    self.enqueue_song(song)
                
                # Highlight the first item if the queue was initially empty
                if was_empty:
                    self.highlight_first_item()
                else:
                    # Maintain the current song highlight if the queue was not empty
                    self.highlight_current_song()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching songs: {e}")
            finally:
                cursor.close()
                connection.close()

    def enqueue_song(self, song):
        """Add a song to the queue."""
        self.song_queue.append(song)
        try:
            if len(song) == 2:
                self.queue_listbox.insert('', 'end', values=(song[0], song[1]))
            else:
                print("Song tuple does not have the expected number of elements:", song)
        except Exception as e:
            print(f"Error inserting song into listbox: {e}")


    def highlight_first_item(self):
        """Highlight the first item in the Treeview."""
        if self.queue_listbox.get_children():
            first_item = self.queue_listbox.get_children()[0]
            self.queue_listbox.selection_set(first_item)
            self.queue_listbox.focus(first_item)
            self.queue_listbox.see(first_item)

    def highlight_current_song(self):
        """Highlight the current song in the Treeview."""
        for item in self.queue_listbox.get_children():
            self.queue_listbox.selection_remove(item)
        if self.queue_listbox.get_children():
            current_item = self.queue_listbox.get_children()[self.current_song_index]
            self.queue_listbox.selection_set(current_item)
            self.queue_listbox.focus(current_item)
            self.queue_listbox.see(current_item)

    def dequeue_song(self):
        if self.song_queue:
            song = self.song_queue.popleft()
            self.queue_listbox.delete(0)
            return song
        else:
            tk.messagebox.showinfo("Queue", "No songs in the queue.")
            return None
        
    def fetch_and_display_albums(self):
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                self.album_tree.delete(*self.album_tree.get_children())  # Clear existing entries
                query = "SELECT title, created_at FROM albums ORDER BY created_at DESC"
                cursor.execute(query)
                albums = cursor.fetchall()
                for album in albums:
                    title, created_at = album
                    formatted_date = created_at.strftime("%Y-%m-%d")  # Format the date for display
                    self.album_tree.insert("", "end", values=(title, formatted_date))
            except Error as e:
                tk.messagebox.showerror("Database Error", f"Error fetching albums: {e}")
            finally:
                cursor.close()
                connection.close()

    def fetch_playlists_for_account(self):
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                query = "SELECT name FROM playlist WHERE email = %s"
                cursor.execute(query, (self.email,))
                return cursor.fetchall()
            except Error as e:
                tk.messagebox.showerror("Database Error", f"Error fetching playlists: {e}")
            finally:
                cursor.close()
                connection.close()
        return []

    def populate_playlist_listbox(self):
        playlists = self.fetch_playlists_for_account()
        self.playlist_listbox.delete(*self.playlist_listbox.get_children())  # Clear old entries
        for playlist in playlists:
            self.playlist_listbox.insert("", tk.END, values=(playlist[0],))  # Insert playlist name


    def on_playlist_double_click(self, event):
        selected_item = self.playlist_listbox.selection()
        if not selected_item:
            return
        
        playlist_name = self.playlist_listbox.item(selected_item[0])['values'][0]
        self.add_playlist_songs_to_queue(playlist_name)

    def on_album_double_click(self, event):
        selected_item = self.album_tree.selection()
        if not selected_item:
            return
        
        album_title = self.album_tree.item(selected_item[0])['values'][0]
        self.add_album_songs_to_queue(album_title)

    def add_playlist_songs_to_queue(self, playlist_name):
        """Add songs from a playlist to the queue with empty playlist check."""
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                # First, check if the playlist exists and has songs
                check_query = """
                SELECT COUNT(ps.song_id) 
                FROM playlist p
                LEFT JOIN playlistssongs ps ON p.playlist_id = ps.playlist_id
                WHERE p.name = %s AND p.email = %s
                """
                cursor.execute(check_query, (playlist_name, self.email))
                song_count = cursor.fetchone()[0]

                if song_count == 0:
                    messagebox.showinfo("Empty Playlist", f"The playlist '{playlist_name}' is empty. Add some songs first!")
                    return

                # If playlist has songs, proceed with adding them to queue
                query = """
                SELECT s.title, s.song_duration 
                FROM songs s
                JOIN playlistssongs ps ON s.song_id = ps.song_id
                JOIN playlist p ON ps.playlist_id = p.playlist_id
                WHERE p.name = %s AND p.email = %s
                """
                cursor.execute(query, (playlist_name, self.email))
                songs = cursor.fetchall()

                # Determine if the queue was initially empty
                was_empty = len(self.song_queue) == 0
            
                # Add each song to the queue
                for song in songs:
                    self.enqueue_song(song)
            
                # Highlight the first item if the queue was initially empty
                if was_empty:
                    self.highlight_first_item()
                else:
                    self.highlight_current_song()

                # Update like button text based on the current song's like status
                if len(self.song_queue) > 0:
                    current_song = list(self.song_queue)[self.current_song_index]
                    song_id = self.get_song_id(current_song[0])
                    if song_id and self.is_song_liked(song_id):
                        self.like_button.config(text='Unlike')
                    else:
                        self.like_button.config(text='Like')

                messagebox.showinfo("Queue Updated", f"Added {len(songs)} songs from playlist '{playlist_name}' to queue")

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error adding songs to queue:\n{e}")
            finally:
                cursor.close()
                connection.close()



    def add_album_songs_to_queue(self, album_title):
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                # Get all songs from the selected album
                query = """
                SELECT s.title, s.song_duration 
                FROM songs s
                JOIN albumssongs als ON s.song_id = als.song_id
                JOIN albums a ON als.album_id = a.album_id
                WHERE a.title = %s
                """
                cursor.execute(query, (album_title,))
                songs = cursor.fetchall()

                # Determine if the queue was initially empty
                was_empty = len(self.song_queue) == 0
            
                # Add each song to the queue
                for song in songs:
                    self.enqueue_song(song)
            
                # Highlight the first item if the queue was initially empty
                if was_empty:
                    self.highlight_first_item()
                else:
                    self.highlight_current_song()

                # Update like button text based on the current song's like status
                current_song = list(self.song_queue)[self.current_song_index]
                song_id = self.get_song_id(current_song[0])
                if song_id and self.is_song_liked(song_id):
                    self.like_button.config(text='Unlike')
                else:
                    self.like_button.config(text='Like')
            
                messagebox.showinfo("Queue Updated", f"Added {len(songs)} songs from album '{album_title}' to queue")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching album songs: {e}")
            finally:
                cursor.close()
                connection.close()



    def previous_song(self):
        """Play the previous song in the queue."""
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.highlight_current_song()
        
            current_song = list(self.song_queue)[self.current_song_index]
            song_id = self.get_song_id(current_song[0])

            # Set like button text based on current like status
            if song_id and self.is_song_liked(song_id):
                self.like_button.config(text='Unlike')
            else:
                self.like_button.config(text='Like')

    def next_song(self):
        """Play the next song in the queue."""
        if self.current_song_index < len(self.song_queue) - 1:
            self.current_song_index += 1
            self.highlight_current_song()
        
            current_song = list(self.song_queue)[self.current_song_index]
            song_id = self.get_song_id(current_song[0])

            # Set like button text based on current like status
            if song_id and self.is_song_liked(song_id):
                self.like_button.config(text='Unlike')
            else:
                self.like_button.config(text='Like')


    def show_context_menu(self, event):
        """Show the context menu on right-click."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()


    def dequeue_selected_song(self):
        """Dequeue the selected song from the listbox and queue."""
        selected_item = self.queue_listbox.selection()
        if selected_item:
            # Get the index of the selected item
            index = self.queue_listbox.index(selected_item)
            # Remove the song from the deque
            self.song_queue.remove(self.song_queue[index])
            # Delete the song from the listbox
            self.queue_listbox.delete(selected_item)
            # Adjust current_song_index if necessary
            if index <= self.current_song_index and self.current_song_index > 0:
                self.current_song_index -= 1
            self.highlight_current_song()
    
    def play_song(self):
        """Increment song streams and play the current song."""
        if not self.song_queue:
            messagebox.showinfo("Play", "No songs in the queue.")
            return

        current_song = list(self.song_queue)[self.current_song_index]
        song_id = self.get_song_id(current_song[0])  # Get the song_id using the new method

        if song_id is None:
            return  # Exit if song_id is not found

        # Increment song_streams
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                query = "UPDATE `musiclibrarydb`.`songs` SET `song_streams` = `song_streams` + 1 WHERE `title` = %s"
                cursor.execute(query, (current_song[0],))
                connection.commit()

                # Insert into songhistory
                account_id = self.get_account_id()  # Assuming you have a way to get the current account_id
                insert_query = "INSERT INTO `musiclibrarydb`.`songhistory` (`account_id`, `song_id`, `date_played`) VALUES (%s, %s, NOW())"
                cursor.execute(insert_query, (account_id, song_id))
                connection.commit()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error updating song streams or inserting song history: {e}")
            finally:
                cursor.close()
                connection.close()

        # Set like button text based on current like status
        if self.is_song_liked(song_id):
            self.like_button.config(text='Unlike')
        else:
            self.like_button.config(text='Like')

        messagebox.showinfo("Play", f"Playing '{current_song[0]}'")



    
    def like_song(self):
        """Like the current song."""
        if not self.song_queue:
            messagebox.showinfo("Like", "No songs in the queue.")
            return

        current_song = list(self.song_queue)[self.current_song_index]
        song_id = self.get_song_id(current_song[0])  # Assuming you have a method to get song_id from title

        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                query = "INSERT INTO `musiclibrarydb`.`accountlikessong` (`account_id`, `song_id`) VALUES (%s, %s)"
                cursor.execute(query, (self.account_id, song_id))
                connection.commit()
                messagebox.showinfo("Like", f"Liked '{current_song[0]}'")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error liking song: {e}")
            finally:
                cursor.close()
                connection.close()

    def unlike_song(self):
        """Unlike the current song."""
        if not self.song_queue:
            messagebox.showinfo("Unlike", "No songs in the queue.")
            return

        current_song = list(self.song_queue)[self.current_song_index]
        song_id = self.get_song_id(current_song[0])  # Assuming you have a method to get song_id from title

        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                query = "DELETE FROM `musiclibrarydb`.`accountlikessong` WHERE `account_id` = %s AND `song_id` = %s"
                cursor.execute(query, (self.account_id, song_id))
                connection.commit()
                messagebox.showinfo("Unlike", f"Unliked '{current_song[0]}'")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error unliking song: {e}")
            finally:
                cursor.close()
                connection.close()

    def get_account_id(self):
        """Fetch the account_id from the database based on the user's email."""
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                query = "SELECT `account_id` FROM `musiclibrarydb`.`accounts` WHERE `email` = %s"
                cursor.execute(query, (self.email,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    messagebox.showerror("Account Not Found", f"Account with email '{self.email}' not found.")
                    return None
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching account_id: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        else:
            return None

    def search_albums(self):
        """Function to search for albums based on user input or fetch all albums if no input."""
        search_term = self.search_entry.get().strip()
        if search_term == self.search_placeholder_text or search_term == '':
            self.fetch_and_display_albums()
            return

        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                # Search for albums
                album_query = "SELECT title, album_duration FROM albums WHERE title LIKE %s"
                cursor.execute(album_query, (f"%{search_term}%",))
                album_results = cursor.fetchall()

                if album_results:
                    self.display_album_results(album_results)
                else:
                    messagebox.showinfo("Search", "No albums found.")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error searching for albums: {e}")
            finally:
                cursor.close()
                connection.close()





    def display_album_results(self, album_results):
        """Function to display the album search results in the album tree view."""
        # Clear the current contents of the album_tree
        self.album_tree.delete(*self.album_tree.get_children())

        # Insert search results into the album_tree
        for result in album_results:
            title, duration = result
            self.album_tree.insert("", "end", values=(title, duration))


    def refresh_all_data(self):
        """Refresh all playlists and data"""
        try:
            # Refresh playlists
            self.populate_playlist_listbox()
            
            # Refresh albums
            self.fetch_and_display_albums()
            
            messagebox.showinfo("Refresh", "All data refreshed successfully!")
        except Exception as e:
            messagebox.showerror("Refresh Error", f"Error refreshing data: {e}")

