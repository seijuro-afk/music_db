import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import query
from datetime import datetime
import mysql.connector

def open_add_album_window(db, root, refresh_gui):
    """
    Opens a new window for adding an album along with its songs and collaborators.
    """
    add_album_window = tk.Toplevel(root)
    add_album_window.title("Add Album")
    add_album_window.geometry("900x700")
    add_album_window.config(bg="#1c1c1c")

    # Left frame for the song details table
    left_frame = tk.Frame(add_album_window, bg="#1c1c1c", width=500)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Right frame for album details
    right_frame = tk.Frame(add_album_window, bg="#333333", width=300)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Song details table
    columns = ("Title", "Duration", "Genre", "Collaborators")
    treeview = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
    treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Configure treeview style
    style = ttk.Style()
    style.configure("Treeview", background="#1c1c1c", foreground="white", fieldbackground="#1c1c1c")
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

    # Define column headings
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor=tk.CENTER, width=150)

    # Add song entry inputs below the table
    song_title_entry = tk.Entry(left_frame, bg="#333333", fg="white", font=("Helvetica", 12), width=30)
    song_title_entry.insert(0, "Enter Song Title")
    song_title_entry.pack(pady=5)

    song_duration_entry = tk.Entry(left_frame, bg="#333333", fg="white", font=("Helvetica", 12), width=30)
    song_duration_entry.insert(0, "00:00:00")
    song_duration_entry.pack(pady=5)

    song_genre_entry = tk.Entry(left_frame, bg="#333333", fg="white", font=("Helvetica", 12), width=30)
    song_genre_entry.insert(0, "Enter Genre")
    song_genre_entry.pack(pady=5)

    collaborator_entries = []

    def add_collaborator_field():
        """
        Dynamically add a new field for specifying collaborators, up to 10 fields.
        """
        if len(collaborator_entries) >= 10:
            messagebox.showerror("Limit Reached", "You can only add up to 10 collaborators per song.")
            return

        entry = tk.Entry(left_frame, bg="#333333", fg="white", font=("Helvetica", 12), width=30)
        entry.insert(0, "Enter Collaborator Name")
        entry.pack(pady=2)
        collaborator_entries.append(entry)

    add_collaborator_button = tk.Button(left_frame, text="Add Collaborator", command=add_collaborator_field, bg="#555555", fg="white", font=("Helvetica", 12))
    add_collaborator_button.pack(pady=5)

    def add_song_to_table():
        """
        Add the entered song details and collaborators to the treeview.
        """
        title = song_title_entry.get().strip()
        duration = song_duration_entry.get().strip()
        genre = song_genre_entry.get().strip()
        collaborators = [entry.get().strip() for entry in collaborator_entries if entry.get().strip()]

        if not title or not duration or not genre:
            messagebox.showerror("Input Error", "All song fields must be filled!")
            return

        collaborator_names = ", ".join(collaborators)
        treeview.insert("", tk.END, values=(title, duration, genre, collaborator_names))

        # Clear inputs
        song_title_entry.delete(0, tk.END)
        song_duration_entry.delete(0, tk.END)
        song_genre_entry.delete(0, tk.END)
        for entry in collaborator_entries:
            entry.destroy()
        collaborator_entries.clear()

    add_song_button = tk.Button(left_frame, text="Add Song", command=add_song_to_table, bg="#555555", fg="white", font=("Helvetica", 12))
    add_song_button.pack(pady=5)

    # Album and artist account details
    album_name_entry = tk.Entry(right_frame, bg="#1c1c1c", fg="white", font=("Helvetica", 12), width=30)
    album_name_entry.insert(0, "Enter Album Name")
    album_name_entry.pack(pady=5)

    artist_name_entry = tk.Entry(right_frame, bg="#1c1c1c", fg="white", font=("Helvetica", 12), width=30)
    artist_name_entry.insert(0, "Enter Artist Name")
    artist_name_entry.pack(pady=5)

    album_type_entry = tk.Entry(right_frame, bg="#1c1c1c", fg="white", font=("Helvetica", 12), width=30)
    album_type_entry.insert(0, "Enter Album Type")
    album_type_entry.pack(pady=5)

    artist_email_entry = tk.Entry(right_frame, bg="#1c1c1c", fg="white", font=("Helvetica", 12), width=30)
    artist_email_entry.insert(0, "Enter Artist Email")
    artist_email_entry.pack(pady=5)

    artist_password_entry = tk.Entry(right_frame, bg="#1c1c1c", fg="white", font=("Helvetica", 12), width=30, show="*")
    artist_password_entry.insert(0, "password")
    artist_password_entry.pack(pady=5)

    def save_album_and_songs():
        """
        Save album and associated songs with collaborators to the database, then refresh the main GUI.
        """
        album_name = album_name_entry.get().strip()
        artist_name = artist_name_entry.get().strip()
        album_type = album_type_entry.get().strip()
        artist_email = artist_email_entry.get().strip()
        artist_password = artist_password_entry.get().strip()

        if not album_name or not artist_name or not album_type or not artist_email or not artist_password:
            messagebox.showerror("Input Error", "All album and artist account details must be filled!")
            return

        # Collect all song details from the treeview
        songs = []
        for child in treeview.get_children():
            songs.append(treeview.item(child)["values"])

        if not songs:
            messagebox.showerror("Input Error", "At least one song must be added!")
            return

        try:
            # Step 1: Verify or create the account
            account_query = "SELECT email FROM accounts WHERE email = %s"
            account_exists = query.execute_query(db, account_query, params=(artist_email,), fetchone=True)

            if not account_exists:
                create_account = messagebox.askyesno(
                    "Account Not Found",
                    f"No account found for email {artist_email}. Create a new account?"
                )
                if create_account:
                    query.execute_query(
                        db,
                        """
                        INSERT INTO accounts (username, email, password)
                        VALUES (%s, %s, %s)
                        """,
                        params=(artist_name, artist_email, artist_password)
                    )

            # Step 2: Fetch or create the artist
            artist_query = "SELECT artist_id FROM artists WHERE name = %s"
            artist = query.execute_query(db, artist_query, params=(artist_name,), fetchone=True)

            if not artist:
                query.execute_query(
                    db,
                    """
                    INSERT INTO artists (name, email)
                    VALUES (%s, %s)
                    """,
                    params=(artist_name, artist_email)
                )
                artist = query.execute_query(db, artist_query, params=(artist_name,), fetchone=True)

            if not artist:
                raise ValueError("Failed to find or create artist.")

            artist_id = artist[0]

            # Step 3: Create the album
            query.execute_query(
                db,
                """
                INSERT INTO albums (title, album_type)
                VALUES (%s, %s)
                """,
                params=(album_name, album_type)
            )
            album_id_query = "SELECT LAST_INSERT_ID()"
            album_id = query.execute_query(db, album_id_query, fetchone=True)[0]

            # Step 4: Link the album to the artist in albumsartistss
            query.execute_query(
                db,
                """
                INSERT INTO albumsartists (album_id, artist_id)
                VALUES (%s, %s)
                """,
                params=(album_id, artist_id)
            )

            # Step 5: Add songs and collaborators
            for title, duration, genre_name, collaborators in songs:
                # Insert song
                genre_alias = query.validate_genre(db, genre_name)
                query.execute_query(
                    db,
                    """
                    INSERT INTO songs (title, genre, song_duration)
                    VALUES (%s, %s, %s)
                    """,
                    params=(title, genre_alias, duration)
                )
                song_id_query = "SELECT LAST_INSERT_ID()"
                song_id = query.execute_query(db, song_id_query, fetchone=True)[0]

                # Link song to the album in albumssongs
                query.execute_query(
                    db,
                    """
                    INSERT INTO albumssongs (album_id, song_id)
                    VALUES (%s, %s)
                    """,
                    params=(album_id, song_id)
                )

                # Link song to the artist in songsartists
                query.execute_query(
                    db,
                    """
                    INSERT INTO songsartists (song_id, artist_id)
                    VALUES (%s, %s)
                    """,
                    params=(song_id, artist_id)
                )


                # Link collaborators to the song in songsartists
                for collaborator in collaborators.split(", "):
                    collaborator_query = "SELECT artist_id FROM artists WHERE name = %s"
                    collaborator_artist = query.execute_query(db, collaborator_query, params=(collaborator,), fetchone=True)

                    if collaborator_artist:
                        query.execute_query(
                            db,
                            """
                            INSERT INTO songsartists (song_id, artist_id)
                            VALUES (%s, %s)
                            """,
                            params=(song_id, collaborator_artist[0])
                        )

            # Refresh the main GUI
            refresh_gui()

            messagebox.showinfo("Success", "Album and songs added successfully!")
            add_album_window.destroy()

        except ValueError as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        except Exception as e:
            messagebox.showerror("Database Error", f"An unexpected error occurred: {type(e).__name__}: {e}")



    save_button = tk.Button(right_frame, text="Save Album", command=save_album_and_songs, bg="#555555", fg="white", font=("Helvetica", 12))
    save_button.pack(pady=20)

    cancel_button = tk.Button(right_frame, text="Cancel", command=add_album_window.destroy, bg="#555555", fg="white", font=("Helvetica", 12))
    cancel_button.pack(pady=10)



def open_update_album_window(db, root, refresh_gui):
    """
    Opens a window to update an existing album.
    """
    update_album_window = tk.Toplevel(root)
    update_album_window.title("Update Album")
    update_album_window.geometry("900x700")
    update_album_window.config(bg="#1c1c1c")

    # Left frame for album selection and song table
    left_frame = tk.Frame(update_album_window, bg="#1c1c1c", width=500)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Right frame for artist/account verification
    right_frame = tk.Frame(update_album_window, bg="#333333", width=300)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Artist verification UI
    tk.Label(right_frame, text="Verify Artist/Account", font=("Helvetica", 14), bg="#333333", fg="white").pack(pady=10)
    artist_email_entry = tk.Entry(right_frame, bg="#1c1c1c", fg="white", font=("Helvetica", 12), width=30)
    artist_email_entry.insert(0, "Enter Artist Email")
    artist_email_entry.pack(pady=5)
    artist_name_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="#333333", fg="white")
    artist_name_label.pack(pady=5)

    # Album dropdown
    album_dropdown = ttk.Combobox(left_frame, state="readonly", font=("Helvetica", 12))
    album_dropdown.pack(pady=10, padx=10, fill=tk.X)

    # Song details table
    columns = ("Song ID", "Title", "Duration", "Genre")
    treeview = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
    treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Configure column headers
    for col in columns:
        treeview.heading(col, text=col)
    treeview.column("Song ID", anchor=tk.CENTER, width=70)  # Shortened for better display
    treeview.column("Title", anchor=tk.CENTER, width=200)
    treeview.column("Duration", anchor=tk.CENTER, width=100)
    treeview.column("Genre", anchor=tk.CENTER, width=100)

    # Make table editable (except Song ID)
    def edit_cell(event):
        selected_item = treeview.selection()
        if not selected_item:
            return

        column = treeview.identify_column(event.x)  # Column clicked
        column_index = int(column.replace("#", "")) - 1  # Convert to zero-based index
        if column_index == 0:  # Song ID is not editable
            return

        # Create an Entry widget for editing
        def save_edit(e):
            new_value = edit_box.get()
            treeview.set(selected_item, column=columns[column_index], value=new_value)
            edit_box.destroy()

        x, y, width, height = treeview.bbox(selected_item, column)
        edit_box = tk.Entry(treeview)
        edit_box.place(x=x, y=y, width=width, height=height)
        edit_box.insert(0, treeview.set(selected_item, column=columns[column_index]))
        edit_box.bind("<Return>", save_edit)
        edit_box.focus()

    treeview.bind("<Double-1>", edit_cell)

    # Helper: Verify artist and load albums
    def verify_artist():
        artist_email = artist_email_entry.get().strip()
        if not artist_email:
            messagebox.showerror("Error", "Please enter the artist's email.")
            return

        try:
            artist = query.fetch_entities(db, "artists", "artist_id, name", condition="email = %s", params=(artist_email,))
            if not artist:
                messagebox.showerror("Error", "No artist found for the given email.")
                return
            artist_id, artist_name = artist[0]
            artist_name_label.config(text=f"Artist: {artist_name}")

            albums = query.fetch_entities(
                db,
                "albums al JOIN albumsartists aa ON al.album_id = aa.album_id",
                "al.album_id, al.title",
                condition="aa.artist_id = %s",
                params=(artist_id,)
            )
            if not albums:
                messagebox.showinfo("Info", "No albums found for this artist.")
                return
            album_dropdown['values'] = [f"{album[1]} (ID: {album[0]})" for album in albums]
            album_dropdown.album_map = {album[1]: album[0] for album in albums}
            album_dropdown.current(0)
            load_album_songs()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Helper: Load songs for selected album
    def load_album_songs():
        try:
            selected_album = album_dropdown.get()
            if not selected_album:
                messagebox.showerror("Error", "No album selected.")
                return
            album_title = selected_album.split(" (ID: ")[0]
            album_id = album_dropdown.album_map[album_title]

            songs = query.fetch_entities(
                db,
                "songs s JOIN albumssongs als ON s.song_id = als.song_id JOIN genres g ON s.genre = g.genre_alias",
                "s.song_id, s.title, s.song_duration, g.genre_name",
                condition="als.album_id = %s",
                params=(album_id,)
            )
            treeview.delete(*treeview.get_children())
            for song in songs:
                treeview.insert("", tk.END, values=song)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Helper: Add a new song row
    def add_song():
        treeview.insert("", tk.END, values=("New", "New Song", "00:00:00", "Genre"))

    # Helper: Remove a selected song row
    def remove_song():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a song to remove.")
            return
        treeview.delete(selected_item)

    # Helper: Save changes
    def save_changes():
        """
        Save updated songs and album data to the database.
        """
        try:
            selected_album = album_dropdown.get()
            album_title = selected_album.split(" (ID: ")[0]
            album_id = album_dropdown.album_map[album_title]

            # Get updated songs from the table
            updated_songs = [treeview.item(child)["values"] for child in treeview.get_children()]
            if not updated_songs:
                messagebox.showerror("Error", "An album must have at least one song.")
                return

            # Verify artist
            artist_email = artist_email_entry.get().strip()
            artist = query.fetch_entities(db, "artists", "artist_id", condition="email = %s", params=(artist_email,))
            if not artist:
                messagebox.showerror("Error", "Artist verification failed. Please re-verify.")
                return
            artist_id = artist[0][0]  # Fetch the artist ID

            # Fetch current songs linked to the album
            existing_songs = query.fetch_entities(
                db,
                "songs s JOIN albumssongs als ON s.song_id = als.song_id",
                "s.song_id",
                condition="als.album_id = %s",
                params=(album_id,)
            )
            existing_song_ids = {row[0] for row in existing_songs}

            # Track new, updated, and removed songs
            current_song_ids = set()
            for song_id, title, duration, genre_name in updated_songs:
                if not title or not duration or not genre_name:
                    messagebox.showerror("Error", "All song details must be provided.")
                    return

                # Validate genre
                genre = query.fetch_entities(db, "genres", "genre_alias", condition="genre_name = %s", params=(genre_name,))
                if not genre:
                    messagebox.showerror("Error", f"Genre '{genre_name}' does not exist.")
                    return
                genre_alias = genre[0][0]

                if song_id == "New":
                    # Insert the new song
                    query.execute_query(
                        db,
                        "INSERT INTO songs (title, song_duration, genre) VALUES (%s, %s, %s)",
                        params=(title, duration, genre_alias)
                    )
                    new_song_id = query.execute_query(db, "SELECT LAST_INSERT_ID()", fetchone=True)[0]

                    # Associate the new song with the album and artist
                    query.execute_query(
                        db,
                        "INSERT INTO albumssongs (song_id, album_id) VALUES (%s, %s)",
                        params=(new_song_id, album_id)
                    )
                    query.execute_query(
                        db,
                        "INSERT INTO songsartists (song_id, artist_id) VALUES (%s, %s)",
                        params=(new_song_id, artist_id)
                    )
                    current_song_ids.add(new_song_id)
                else:
                    # Update existing song details
                    query.execute_query(
                        db,
                        "UPDATE songs SET title = %s, song_duration = %s, genre = %s WHERE song_id = %s",
                        params=(title, duration, genre_alias, song_id)
                    )
                    current_song_ids.add(int(song_id))

            # Remove songs no longer present in the table
            removed_song_ids = existing_song_ids - current_song_ids
            for song_id in removed_song_ids:
                # Remove the song's association with the album
                query.execute_query(
                    db,
                    "DELETE FROM albumssongs WHERE song_id = %s AND album_id = %s",
                    params=(song_id, album_id)
                )

                # Check if the song is linked to other albums or artists
                song_linked = query.fetch_entities(
                    db,
                    "albumssongs",
                    "song_id",
                    condition="song_id = %s",
                    params=(song_id,)
                )
                if not song_linked:
                    # Remove the song entirely if it's no longer linked
                    query.execute_query(
                        db,
                        "DELETE FROM songs WHERE song_id = %s",
                        params=(song_id,)
                    )
                    query.execute_query(
                        db,
                        "DELETE FROM songsartists WHERE song_id = %s",
                        params=(song_id,)
                    )

            # Refresh the GUI and close the update window
            refresh_gui()
            messagebox.showinfo("Success", "Album and songs updated successfully.")
            update_album_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {e}")
    
    album_dropdown.bind("<<ComboboxSelected>>", lambda e: load_album_songs())

    # Buttons
    tk.Button(left_frame, text="Add Song", command=add_song, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=5)
    tk.Button(left_frame, text="Remove Song", command=remove_song, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=5)
    tk.Button(left_frame, text="Save Changes", command=save_changes, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=20)
    tk.Button(left_frame, text="Cancel", command=update_album_window.destroy, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=10)

    tk.Button(right_frame, text="Verify Artist", command=verify_artist, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=10)

def open_remove_album_window(db, root, refresh_gui):
    """
    Opens a window to remove an existing album.
    """
    remove_album_window = tk.Toplevel(root)
    remove_album_window.title("Remove Album")
    remove_album_window.geometry("900x600")
    remove_album_window.config(bg="#1c1c1c")

    # Left frame for album selection and song table
    left_frame = tk.Frame(remove_album_window, bg="#1c1c1c", width=500)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Right frame for artist/account verification
    right_frame = tk.Frame(remove_album_window, bg="#333333", width=300)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Artist verification UI
    tk.Label(right_frame, text="Verify Artist/Account", font=("Helvetica", 14), bg="#333333", fg="white").pack(pady=10)
    artist_email_entry = tk.Entry(right_frame, bg="#1c1c1c", fg="white", font=("Helvetica", 12), width=30)
    artist_email_entry.insert(0, "Enter Artist Email")
    artist_email_entry.pack(pady=5)
    artist_name_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="#333333", fg="white")
    artist_name_label.pack(pady=5)

    # Album dropdown
    album_dropdown = ttk.Combobox(left_frame, state="readonly", font=("Helvetica", 12))
    album_dropdown.pack(pady=10, padx=10, fill=tk.X)

    # Song details table
    columns = ("Song ID", "Title", "Duration", "Genre")
    treeview = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
    treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Configure column headers
    for col in columns:
        treeview.heading(col, text=col)
    treeview.column("Song ID", anchor=tk.CENTER, width=70)  # Adjust for better layout
    treeview.column("Title", anchor=tk.CENTER, width=200)
    treeview.column("Duration", anchor=tk.CENTER, width=100)
    treeview.column("Genre", anchor=tk.CENTER, width=100)

    # Helper: Verify artist and load albums
    def verify_artist():
        artist_email = artist_email_entry.get().strip()
        if not artist_email:
            messagebox.showerror("Error", "Please enter the artist's email.")
            return

        try:
            artist = query.fetch_entities(db, "artists", "artist_id, name", condition="email = %s", params=(artist_email,))
            if not artist:
                messagebox.showerror("Error", "No artist found for the given email.")
                return
            artist_id, artist_name = artist[0]
            artist_name_label.config(text=f"Artist: {artist_name}")

            albums = query.fetch_entities(
                db,
                "albums al JOIN albumsartists aa ON al.album_id = aa.album_id",
                "al.album_id, al.title",
                condition="aa.artist_id = %s",
                params=(artist_id,)
            )
            if not albums:
                messagebox.showinfo("Info", "No albums found for this artist.")
                return
            album_dropdown['values'] = [f"{album[1]} (ID: {album[0]})" for album in albums]
            album_dropdown.album_map = {album[1]: album[0] for album in albums}
            album_dropdown.current(0)
            load_album_songs()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Helper: Load songs for selected album
    def load_album_songs():
        try:
            selected_album = album_dropdown.get()
            if not selected_album:
                messagebox.showerror("Error", "No album selected.")
                return
            album_title = selected_album.split(" (ID: ")[0]
            album_id = album_dropdown.album_map[album_title]

            songs = query.fetch_entities(
                db,
                "songs s JOIN albumssongs als ON s.song_id = als.song_id JOIN genres g ON s.genre = g.genre_alias",
                "s.song_id, s.title, s.song_duration, g.genre_name",
                condition="als.album_id = %s",
                params=(album_id,)
            )
            treeview.delete(*treeview.get_children())
            for song in songs:
                treeview.insert("", tk.END, values=song)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Helper: Remove album and all related data
    def remove_album():
        """
        Remove the selected album and all related data after confirmation.
        """
        try:
            # Fetch selected album details
            selected_album = album_dropdown.get()
            if not selected_album:
                messagebox.showerror("Error", "No album selected.")
                return

            album_title = selected_album.split(" (ID: ")[0]
            album_id = album_dropdown.album_map[album_title]

            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Removal",
                f"Are you sure you want to remove the album '{album_title}' and all its songs?"
            )
            if not confirm:
                return

            # Log album details for debugging
            print(f"Deleting album: {album_title} (ID: {album_id})")

            # Step 1: Delete the album
            query.execute_query(db, "DELETE FROM albums WHERE album_id = %s", params=(album_id,))

            # Step 2: Clean up unlinked songs
            unlinked_songs = query.fetch_entities(
                db,
                "songs s LEFT JOIN albumssongs als ON s.song_id = als.song_id",
                "s.song_id",
                condition="als.song_id IS NULL"
            )
            for song in unlinked_songs:
                song_id = song[0]
                # Remove song-artist associations
                query.execute_query(db, "DELETE FROM songsartists WHERE song_id = %s", params=(song_id,))
                # Remove song-playlist associations
                query.execute_query(db, "DELETE FROM playlistssongs WHERE song_id = %s", params=(song_id,))
                # Delete the song itself
                query.execute_query(db, "DELETE FROM songs WHERE song_id = %s", params=(song_id,))

            # Log successful deletion
            print(f"Album '{album_title}' and all related data have been deleted.")

            # Refresh GUI
            refresh_gui()
            messagebox.showinfo("Success", f"Album '{album_title}' and all related data have been removed.")
            remove_album_window.destroy()

        except Exception as e:
            # Log the error for debugging
            print(f"Error during album deletion: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Buttons
    tk.Button(right_frame, text="Verify Artist", command=verify_artist, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=10)
    tk.Button(left_frame, text="Remove Album", command=remove_album, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=20)
    tk.Button(left_frame, text="Cancel", command=remove_album_window.destroy, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=10)

    album_dropdown.bind("<<ComboboxSelected>>", lambda e: load_album_songs())

def open_manage_genre_window(db, root):
    """
    Opens a window for managing genres in the database.
    """
    manage_genre_window = tk.Toplevel(root)
    manage_genre_window.title("Manage Genres")
    manage_genre_window.geometry("600x600")
    manage_genre_window.config(bg="#1c1c1c")

    # Genre table setup
    columns = ("Genre Alias", "Genre Name")
    treeview = ttk.Treeview(manage_genre_window, columns=columns, show="headings", height=20)
    treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Configure column headers
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor=tk.CENTER, width=200)

    # Load genres from the database
    def load_genres():
        """
        Load genres from the database into the table.
        """
        try:
            treeview.delete(*treeview.get_children())
            genres = query.fetch_entities(db, "genres", "genre_alias, genre_name")
            for genre in genres:
                treeview.insert("", tk.END, values=genre)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load genres: {e}")

    # Add new genre row
    def add_genre():
        """
        Add a blank row for a new genre.
        """
        treeview.insert("", tk.END, values=("New Alias", "New Genre"))

    # Remove selected genre
    def remove_genre():
        """
        Remove the selected genre from the database.
        """
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a genre to remove.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Removal",
            "Are you sure you want to remove the selected genre? This cannot be undone."
        )
        if not confirm:
            return

        try:
            for item in selected_item:
                genre_alias = treeview.item(item)["values"][0]
                query.execute_query(db, "DELETE FROM genres WHERE genre_alias = %s", params=(genre_alias,))
                treeview.delete(item)

            messagebox.showinfo("Success", "Selected genre(s) removed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove genre(s): {e}")

    # Save changes to the database
    def save_changes():
        """
        Save changes (new genres or updates) to the database.
        """
        try:
            for item in treeview.get_children():
                genre_alias, genre_name = treeview.item(item)["values"]

                # Skip incomplete rows
                if not genre_alias or not genre_name or genre_alias == "New Alias" or genre_name == "New Genre":
                    continue

                # Check if the genre already exists
                existing_genre = query.fetch_entities(
                    db,
                    "genres",
                    "genre_alias",
                    condition="genre_alias = %s",
                    params=(genre_alias,)
                )

                if existing_genre:
                    # Update existing genre
                    print(f"Updating genre: {genre_alias} -> {genre_name}")
                    query.execute_query(
                        db,
                        "UPDATE genres SET genre_name = %s WHERE genre_alias = %s",
                        params=(genre_name, genre_alias)
                    )
                else:
                    # Insert new genre
                    print(f"Inserting new genre: {genre_alias} -> {genre_name}")
                    query.execute_query(
                        db,
                        "INSERT INTO genres (genre_alias, genre_name) VALUES (%s, %s)",
                        params=(genre_alias, genre_name)
                    )

            # Reload genres after saving changes
            load_genres()
            messagebox.showinfo("Success", "Genres saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {e}")

    # Edit cell in Treeview
    def edit_cell(event):
        """
        Edit the selected cell in the Treeview.
        """
        item = treeview.selection()
        if not item:
            return

        column = treeview.identify_column(event.x)
        column_index = int(column.replace("#", "")) - 1

        def save_edit(e):
            new_value = edit_box.get()
            treeview.set(item, column=column_index, value=new_value)
            edit_box.destroy()

        x, y, width, height = treeview.bbox(item, column)
        edit_box = tk.Entry(treeview, font=("Helvetica", 12))
        edit_box.place(x=x, y=y, width=width, height=height)
        edit_box.bind("<Return>", save_edit)

    treeview.bind("<Double-1>", edit_cell)

    # Buttons
    button_frame = tk.Frame(manage_genre_window, bg="#1c1c1c")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add Genre", command=add_genre, bg="#555555", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Remove Genre", command=remove_genre, bg="#555555", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Save Changes", command=save_changes, bg="#555555", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", command=manage_genre_window.destroy, bg="#555555", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

    # Load genres initially
    load_genres()

def open_manage_artists_window(db, root):
    """
    Opens a window to manage accounts and their linked artists. Updates are done through a dedicated window.
    """
    manage_artists_window = tk.Toplevel(root)
    manage_artists_window.title("Manage Accounts and Artists")
    manage_artists_window.geometry("900x600")
    manage_artists_window.config(bg="#1c1c1c")

    # Account-Artist table setup
    columns = ("Account ID", "Username", "Email", "Artist Name")
    treeview = ttk.Treeview(manage_artists_window, columns=columns, show="headings", height=20)
    treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Configure column headers
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor=tk.CENTER, width=200)

    # Helper: Load accounts with artist information
    def load_accounts():
        """
        Load accounts and their linked artists into the table.
        """
        try:
            treeview.delete(*treeview.get_children())
            query_str = """
                SELECT a.account_id, a.username, a.email, ar.name AS artist_name
                FROM accounts a
                LEFT JOIN artists ar ON a.email = ar.email
                ORDER BY artist_name DESC
            """
            accounts = query.execute_query(db, query_str, fetchall=True)
            for account in accounts:
                treeview.insert("", tk.END, values=account)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accounts: {e}")

    # Helper: Open the update account window
    def update_account():
        """
        Open a new window to update account details and link artist name.
        """
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an account to update.")
            return

        account_id, username, email, artist_name = treeview.item(selected_item[0])["values"]

        # Create a pop-up window for updating account details
        update_window = tk.Toplevel(manage_artists_window)
        update_window.title("Update Account")
        update_window.geometry("400x400")
        update_window.config(bg="#1c1c1c")

        tk.Label(update_window, text="Update Account and Artist", font=("Helvetica", 14), bg="#1c1c1c", fg="white").pack(pady=10)

        username_entry = tk.Entry(update_window, bg="#333333", fg="white", font=("Helvetica", 12), width=30)
        username_entry.pack(pady=5)
        username_entry.insert(0, username)

        email_entry = tk.Entry(update_window, bg="#333333", fg="white", font=("Helvetica", 12), width=30)
        email_entry.pack(pady=5)
        email_entry.insert(0, email)

        artist_name_entry = tk.Entry(update_window, bg="#333333", fg="white", font=("Helvetica", 12), width=30)
        artist_name_entry.pack(pady=5)
        artist_name_entry.insert(0, artist_name if artist_name else "New Artist")

        def save_update():
            """
            Save the updated account and artist details to the database.
            """
            new_username = username_entry.get().strip()
            new_email = email_entry.get().strip()
            new_artist_name = artist_name_entry.get().strip()

            if not new_username or not new_email or not new_artist_name:
                messagebox.showerror("Error", "All fields must be filled.")
                return

            try:
                # Update account details
                query.execute_query(
                    db,
                    "UPDATE accounts SET username = %s, email = %s WHERE account_id = %s",
                    params=(new_username, new_email, account_id)
                )

                # Link or create the artist
                existing_artist = query.fetch_entities(
                    db,
                    "artists",
                    "artist_id",
                    condition="email = %s",
                    params=(new_email,)
                )

                if existing_artist:
                    # Update artist name if already linked
                    query.execute_query(
                        db,
                        "UPDATE artists SET name = %s WHERE email = %s",
                        params=(new_artist_name, new_email)
                    )
                else:
                    # Create a new artist if not linked
                    query.execute_query(
                        db,
                        "INSERT INTO artists (name, email) VALUES (%s, %s)",
                        params=(new_artist_name, new_email)
                    )

                load_accounts()
                messagebox.showinfo("Success", "Account and artist updated successfully.")
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update account: {e}")

        tk.Button(update_window, text="Save Changes", command=save_update, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=10)
        tk.Button(update_window, text="Cancel", command=update_window.destroy, bg="#555555", fg="white", font=("Helvetica", 12)).pack(pady=5)

    # Helper: Remove selected account
    def remove_account():
        """
        Remove the selected account and its linked artist.
        """
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an account to remove.")
            return

        account_id, username, email, artist_name = treeview.item(selected_item[0])["values"]

        confirm = messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove the account '{username}' and its linked artist (if any)?"
        )
        if not confirm:
            return

        try:
            # Remove linked artist if exists
            if artist_name:
                query.execute_query(db, "DELETE FROM artists WHERE email = %s", params=(email,))

            # Remove the account
            query.execute_query(db, "DELETE FROM accounts WHERE account_id = %s", params=(account_id,))
            load_accounts()
            messagebox.showinfo("Success", f"Account '{username}' removed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove account: {e}")

    # Buttons
    button_frame = tk.Frame(manage_artists_window, bg="#1c1c1c")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Update Account", command=update_account, bg="#555555", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Remove Account", command=remove_account, bg="#555555", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Close", command=manage_artists_window.destroy, bg="#555555", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

    # Load accounts initially
    load_accounts()


def open_manage_playlists_window(db, root, refresh_gui):
    """
    Opens a window to manage playlists for a specific account with a compact layout.
    """
    manage_playlists_window = tk.Toplevel(root)
    manage_playlists_window.title("Manage Playlists")
    manage_playlists_window.geometry("700x900")
    manage_playlists_window.config(bg="#1c1c1c")

    # Top frame for account input and buttons
    top_frame = tk.Frame(manage_playlists_window, bg="#333333")
    top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    tk.Label(top_frame, text="Account Email:", font=("Helvetica", 12), bg="#333333", fg="white").pack(side=tk.LEFT, padx=5)
    account_email_entry = tk.Entry(top_frame, bg="#1c1c1c", fg="white", font=("Helvetica", 12), width=25)
    account_email_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(top_frame, text="Load Playlists", command=lambda: load_playlists(), bg="#555555", fg="white",
              font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

    # Main frame for tables
    main_frame = tk.Frame(manage_playlists_window, bg="#1c1c1c")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Playlist table
    tk.Label(main_frame, text="Playlists", font=("Helvetica", 14), bg="#1c1c1c", fg="white").pack(pady=5)
    playlist_columns = ("Playlist ID", "Name", "Created At")
    playlist_tree = ttk.Treeview(main_frame, columns=playlist_columns, show="headings", height=10)
    playlist_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    for col in playlist_columns:
        playlist_tree.heading(col, text=col)
        playlist_tree.column(col, anchor=tk.CENTER)

    # Song table
    tk.Label(main_frame, text="Songs in Playlist", font=("Helvetica", 14), bg="#1c1c1c", fg="white").pack(pady=5)
    song_columns = ("Song ID", "Title", "Duration", "Genre")
    song_tree = ttk.Treeview(main_frame, columns=song_columns, show="headings", height=10)
    song_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    for col in song_columns:
        song_tree.heading(col, text=col)
        song_tree.column(col, anchor=tk.CENTER)

    # Bottom frame for action buttons
    button_frame = tk.Frame(manage_playlists_window, bg="#333333")
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    tk.Button(button_frame, text="Add Playlist", command=lambda: add_playlist(), bg="#555555", fg="white",
              font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Update Playlist", command=lambda: update_playlist(), bg="#555555", fg="white",
              font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete Playlist", command=lambda: delete_playlist(), bg="#555555", fg="white",
              font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Close", command=manage_playlists_window.destroy, bg="#555555", fg="white",
              font=("Helvetica", 12)).pack(side=tk.RIGHT, padx=5)

    for col in song_columns:
        song_tree.heading(col, text=col)
        song_tree.column(col, anchor=tk.CENTER)

    def load_playlists():
        """
        Load playlists for the entered account email.
        """
        account_email = account_email_entry.get().strip()
        if not account_email:
            messagebox.showerror("Input Error", "Please enter an account email.")
            return

        try:
            playlists = query.fetch_entities(
                db,
                table="playlists",
                columns="playlist_id, name, created_at",
                condition="email = %s",
                params=(account_email,)
            )
            playlist_tree.delete(*playlist_tree.get_children())
            for playlist in playlists:
                playlist_tree.insert("", tk.END, values=playlist)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load playlists: {e}")


    def load_songs_in_playlist(event):
        """
        Load songs for the selected playlist.
        """
        selected_item = playlist_tree.selection()
        if not selected_item:
            return

        playlist_id = playlist_tree.item(selected_item[0], "values")[0]
        try:
            songs = query.fetch_entities(
                db, 
                table="playlistssongs ps JOIN songs s ON ps.song_id = s.song_id",
                columns="s.song_id, s.title, s.song_duration, s.genre",
                condition="ps.playlist_id = %s",
                params=(playlist_id,)
            )
            song_tree.delete(*song_tree.get_children())
            for song in songs:
                song_tree.insert("", tk.END, values=song)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load songs: {e}")

    def add_playlist():
        """
        Add a new playlist for the account.
        """
        account_email = account_email_entry.get().strip()
        playlist_name = simpledialog.askstring("New Playlist", "Enter playlist name:")
        if not playlist_name or not account_email:
            messagebox.showerror("Input Error", "Please enter valid details.")
            return

        try:
            query.execute_query(
                db,
                """
                INSERT INTO playlists (name, email, created_at)
                VALUES (%s, %s, NOW())
                """,
                params=(playlist_name, account_email)
            )
            load_playlists()
            messagebox.showinfo("Success", "Playlist added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add playlist: {e}")


    def delete_playlist():
        """
        Delete the selected playlist.
        """
        selected_item = playlist_tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a playlist to delete.")
            return

        playlist_id = playlist_tree.item(selected_item[0], "values")[0]
        try:
            query.execute_query(db, "DELETE FROM playlists WHERE playlist_id = %s", params=(playlist_id,))
            load_playlists()
            song_tree.delete(*song_tree.get_children())
            messagebox.showinfo("Success", "Playlist deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete playlist: {e}")

    def update_playlist():
        """
        Update the name of the selected playlist.
        """
        selected_item = playlist_tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a playlist to update.")
            return

        playlist_id = playlist_tree.item(selected_item[0], "values")[0]
        new_name = simpledialog.askstring("Update Playlist", "Enter new playlist name:")
        if not new_name:
            return

        try:
            query.execute_query(db, "UPDATE playlists SET name = %s WHERE playlist_id = %s", params=(new_name, playlist_id))
            load_playlists()
            messagebox.showinfo("Success", "Playlist updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update playlist: {e}")
        
        refresh_gui()

    playlist_tree.bind("<<TreeviewSelect>>", load_songs_in_playlist)

    button_frame = tk.Frame(manage_playlists_window, bg="#333333")
    button_frame.pack(pady=10)

