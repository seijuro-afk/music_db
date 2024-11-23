import tkinter as tk
from tkinter import ttk, Toplevel, Label, Frame, Canvas, Entry, N
from PIL import Image, ImageTk
import os
import mysql.connector
from mysql.connector import Error
from collections import deque

class MusicPlayer:
    def __init__(self, root):
        self.root = root
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

        self.search_button = tk.Button(self.search_frame, text="Search", bg="#2e2e2e", fg="white", relief=tk.FLAT)
        self.search_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Playlist frame
        self.playlist_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.playlist_frame.place(x=0, y=50, width=200, height=500)

        self.playlist_label = tk.Label(self.playlist_frame, text="Playlist", bg="#2e2e2e", fg="white")
        self.playlist_label.pack(pady=10)

        self.playlist_listbox = ttk.Treeview(self.playlist_frame, columns=("TitlePlaylist", "Action"), show="headings")
        self.playlist_listbox.heading("TitlePlaylist", text="Title")
        self.playlist_listbox.column("TitlePlaylist", anchor=tk.W, width=100)
        self.playlist_listbox.heading("Action", text="Add")
        self.playlist_listbox.column("Action", anchor=tk.W, width=30)
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True, pady=20)

        # Account center button (borderless)
        self.account_button = tk.Button(self.main_frame, text="Account Center", bg="#2e2e2e", fg="white", relief=tk.FLAT)
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

        # Fetch and display songs
        self.fetch_and_enqueue_songs()

        # Latest songs and albums frame
        self.latest_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.latest_frame.place(x=200, y=50, width=400, height=450)

        self.latest_label = tk.Label(self.latest_frame, text="Latest Songs and Albums", bg="#2e2e2e", fg="white")
        self.latest_label.pack(pady=10)

        # Add Treeview in the center with album title and a button
        self.album_tree = ttk.Treeview(self.latest_frame, columns=("AlbumTitle", "Button"), show="headings")
        self.album_tree.heading("AlbumTitle", text="Album Title")
        self.album_tree.heading("Button", text="Action")
        self.album_tree.column("AlbumTitle", anchor=tk.W, width=300)
        self.album_tree.column("Button", anchor=tk.CENTER, width=100)
        self.album_tree.pack(fill=tk.BOTH, expand=True)

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
        self.previous_image = Image.open("prev.png")
        self.previous_image = self.previous_image.resize((50, 50), Image.LANCZOS)  # Adjust the size as needed
        self.previous_image = ImageTk.PhotoImage(self.previous_image)

        self.play_pause_image = Image.open("play.png")
        self.play_pause_image = self.play_pause_image.resize((50, 50), Image.LANCZOS)
        self.play_pause_image = ImageTk.PhotoImage(self.play_pause_image)

        self.next_image = Image.open("next.png")
        self.next_image = self.next_image.resize((50, 50), Image.LANCZOS)
        self.next_image = ImageTk.PhotoImage(self.next_image)

        # Adjust the control buttons with icons
        self.previous_button = tk.Button(self.controls_frame, image=self.previous_image, bg="#2e2e2e", relief=tk.FLAT)
        self.previous_button.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

        self.play_button = tk.Button(self.controls_frame, image=self.play_pause_image, bg="#2e2e2e", relief=tk.FLAT)
        self.play_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.next_button = tk.Button(self.controls_frame, image=self.next_image, bg="#2e2e2e", relief=tk.FLAT)
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

    def toggle_like(self):
        if self.like_button.config('text')[-1] == 'Like':
            self.like_button.config(text='Unlike')
        else:
            self.like_button.config(text='Like')

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
            print("connected")
            return connection
        except Error as e:
            tk.messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None

    def fetch_and_enqueue_songs(self):
        connection = self.create_connection()
        if connection is not None:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT title, song_duration FROM songs")
                songs = cursor.fetchall()
                for song in songs:
                    self.enqueue_song(song)
            except Error as e:
                tk.messagebox.showerror("Database Error", f"Error fetching songs: {e}")
            finally:
                cursor.close()

    def enqueue_song(self, song):
        self.song_queue.append(song)
        self.queue_listbox.insert(tk.END, f"{song[0]} ({song[2]}) - {song[1]}")

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
                cursor.execute("SELECT title FROM albums")
                albums = cursor.fetchall()
                for album in albums:
                    title = album[0]
                    item_id = self.album_tree.insert("", "end", values=(title,))
                    self.album_tree.set(item_id, "#1", title)
                    add_button = tk.Button(self.latest_frame, text="+", command=lambda: self.add_to_queue(title))
                    self.album_tree.set(item_id, "Add to Queue", add_button)
                    self.album_tree.insert("", "end", values=(title, ))
            except Error as e:
                tk.messagebox.showerror("Database Error", f"Error fetching songs: {e}")
            finally:
                cursor.close()
                connection.close()

        