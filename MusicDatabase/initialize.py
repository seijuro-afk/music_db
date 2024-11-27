import tkinter as tk
from tkinter import ttk
import query
import action_windows


def initialize(db, root, username, email):
    """
    Initialize the main GUI with dynamic search and proper filtering logic.
    """

    # Helper Functions
    def fetch_data(query_str, params=()):
        """
        Fetch data from the database using a query and parameters.
        """
        try:
            return query.execute_query(db, query_str, params=params, fetchall=True)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Database Error: {e}")
            return []

    def load_data():
        """
        Load full data into all panels (artists, albums, playlists, songs).
        """
        artists = fetch_data("SELECT artist_id, name FROM artists")
        albums = fetch_data("SELECT album_id, title FROM albums")
        playlists = fetch_data("SELECT playlist_id, name FROM playlists")
        songs = fetch_data(
            """
            SELECT s.title, GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS artists, g.genre_name AS genre, s.song_duration
            FROM songs s
            LEFT JOIN songsartists sa ON s.song_id = sa.song_id
            LEFT JOIN artists a ON sa.artist_id = a.artist_id
            LEFT JOIN genres g ON s.genre = g.genre_alias
            GROUP BY s.song_id
            """
        )

        populate_listbox(artists_listbox, artists, artists_ids)
        populate_listbox(albums_listbox, albums, albums_ids)
        populate_listbox(playlists_listbox, playlists, playlists_ids)
        populate_treeview(treeview, songs)

    def populate_listbox(listbox, data, ids_store):
        """
        Populate a Listbox with data and store corresponding IDs.
        """
        listbox.delete(0, tk.END)
        ids_store.clear()
        for item_id, item_name in data:
            listbox.insert(tk.END, item_name)
            ids_store.append(item_id)

    def populate_treeview(treeview, data):
        """
        Populate the Treeview with song data.
        """
        for row in treeview.get_children():
            treeview.delete(row)
        for item in data:
            treeview.insert("", tk.END, values=item)

    def perform_search(event=None):
        """
        Perform a dynamic search and update all panels based on the search term.
        """
        search_text = search_entry.get().strip().lower()
        if not search_text:
            load_data()
            return

        # Filter all panels based on search text
        artists = fetch_data("SELECT artist_id, name FROM artists WHERE LOWER(name) LIKE %s", (f"%{search_text}%",))
        albums = fetch_data("SELECT album_id, title FROM albums WHERE LOWER(title) LIKE %s", (f"%{search_text}%",))
        playlists = fetch_data("SELECT playlist_id, name FROM playlists WHERE LOWER(name) LIKE %s", (f"%{search_text}%",))
        songs = fetch_data(
            """
            SELECT s.title, GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS artists, g.genre_name AS genre, s.song_duration
            FROM songs s
            LEFT JOIN songsartists sa ON s.song_id = sa.song_id
            LEFT JOIN artists a ON sa.artist_id = a.artist_id
            LEFT JOIN genres g ON s.genre = g.genre_alias
            WHERE LOWER(s.title) LIKE %s
            GROUP BY s.song_id
            """,
            (f"%{search_text}%",),
        )

        populate_listbox(artists_listbox, artists, artists_ids)
        populate_listbox(albums_listbox, albums, albums_ids)
        populate_listbox(playlists_listbox, playlists, playlists_ids)
        populate_treeview(treeview, songs)

    def on_select(event, source):
        """
        Handle selection from Artists, Albums, or Playlists panels.
        """
        selected_index = source.curselection()
        if not selected_index:
            return

        selected_id = None
        if source == artists_listbox:
            selected_id = artists_ids[selected_index[0]]
            # Fetch albums and songs for the selected artist
            albums = fetch_data(
                """
                SELECT al.album_id, al.title
                FROM albums al
                JOIN albumsartists aa ON al.album_id = aa.album_id
                WHERE aa.artist_id = %s
                """,
                (selected_id,),
            )
            songs = fetch_data(
                """
                SELECT s.title, GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS artists, g.genre_name AS genre, s.song_duration
                FROM songs s
                LEFT JOIN songsartists sa ON s.song_id = sa.song_id
                LEFT JOIN artists a ON sa.artist_id = a.artist_id
                LEFT JOIN genres g ON s.genre = g.genre_alias
                WHERE s.song_id IN (
                    SELECT DISTINCT sa.song_id FROM songsartists sa WHERE sa.artist_id = %s
                )
                GROUP BY s.song_id
                """,
                (selected_id,),
            )
            populate_listbox(albums_listbox, albums, albums_ids)
            populate_treeview(treeview, songs)

        elif source == albums_listbox:
            selected_id = albums_ids[selected_index[0]]
            # Fetch songs for the selected album
            songs = fetch_data(
                """
                SELECT s.title, GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS artists, g.genre_name AS genre, s.song_duration
                FROM songs s
                JOIN albumssongs als ON s.song_id = als.song_id
                JOIN albums al ON als.album_id = al.album_id
                LEFT JOIN songsartists sa ON s.song_id = sa.song_id
                LEFT JOIN artists a ON sa.artist_id = a.artist_id
                LEFT JOIN genres g ON s.genre = g.genre_alias
                WHERE al.album_id = %s
                GROUP BY s.song_id
                """,
                (selected_id,),
            )
            populate_treeview(treeview, songs)

        elif source == playlists_listbox:
            selected_id = playlists_ids[selected_index[0]]
            # Fetch songs for the selected playlist
            songs = fetch_data(
                """
                SELECT s.title, GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS artists, g.genre_name AS genre, s.song_duration
                FROM songs s
                JOIN playlistssongs pls ON s.song_id = pls.song_id
                JOIN playlists p ON pls.playlist_id = p.playlist_id
                LEFT JOIN songsartists sa ON s.song_id = sa.song_id
                LEFT JOIN artists a ON sa.artist_id = a.artist_id
                LEFT JOIN genres g ON s.genre = g.genre_alias
                WHERE p.playlist_id = %s
                GROUP BY s.song_id
                """,
                (selected_id,),
            )
            populate_treeview(treeview, songs)
    # GUI Setup
    top_frame = tk.Frame(root, bg="#1c1c1c")
    top_frame.pack(side=tk.TOP, fill=tk.X)

    left_frame = tk.Frame(root, bg="#1c1c1c", width=200)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    middle_frame = tk.Frame(root, bg="#1c1c1c")
    middle_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    right_frame = tk.Frame(root, bg="#1c1c1c", width=200)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    search_label = tk.Label(top_frame, text="Search:", font=("Helvetica", 12), bg="#1c1c1c", fg="white")
    search_label.pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(top_frame, bg="#333333", fg="white", font=("Helvetica", 12), width=40)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_entry.bind("<KeyRelease>", perform_search)

    # Artists Panel
    artists_label = tk.Label(left_frame, text="Artists", font=("Helvetica", 14), bg="#1c1c1c", fg="white")
    artists_label.pack(pady=10)
    artists_listbox = tk.Listbox(left_frame, bg="#333333", fg="white", font=("Helvetica", 12))
    artists_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
    artists_ids = []
    artists_listbox.bind("<<ListboxSelect>>", lambda e: on_select(e, artists_listbox))

    # Albums Panel
    albums_label = tk.Label(left_frame, text="Albums", font=("Helvetica", 14), bg="#1c1c1c", fg="white")
    albums_label.pack(pady=10)
    albums_listbox = tk.Listbox(left_frame, bg="#333333", fg="white", font=("Helvetica", 12))
    albums_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
    albums_ids = []
    albums_listbox.bind("<<ListboxSelect>>", lambda e: on_select(e, albums_listbox))

    # Playlists Panel
    playlists_label = tk.Label(left_frame, text="Playlists", font=("Helvetica", 14), bg="#1c1c1c", fg="white")
    playlists_label.pack(pady=10)
    playlists_listbox = tk.Listbox(left_frame, bg="#333333", fg="white", font=("Helvetica", 12))
    playlists_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
    playlists_ids = []
    playlists_listbox.bind("<<ListboxSelect>>", lambda e: on_select(e, playlists_listbox))

    # Songs Panel
    songs_label = tk.Label(middle_frame, text="Songs", font=("Helvetica", 14), bg="#1c1c1c", fg="white")
    songs_label.pack(pady=10)
    treeview = ttk.Treeview(middle_frame, columns=("Title", "Artists", "Genre", "Duration"), show="headings", height=25)
    treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    for col in ("Title", "Artists", "Genre", "Duration"):
        treeview.heading(col, text=col)

    # Admin Buttons (if logged in as admin)
    if email == "admin@gmail.com":
        def refresh_gui():
            load_data()

        # Right Panel: Action Buttons
        right_label = tk.Label(right_frame, text=f"Welcome, {username}", font=("Helvetica", 12), bg="#1c1c1c", fg="white")
        right_label.pack(pady=10)

        manage_genre_button = tk.Button(right_frame, text="Genres", command=lambda: action_windows.open_manage_genre_window(db, root), bg="#555555", fg="white", font=("Helvetica", 12))
        manage_genre_button.pack(padx=10, pady=10)

        manage_artists_button = tk.Button(right_frame, text="Artists", command=lambda: action_windows.open_manage_artists_window(db, root), bg="#555555", fg="white", font=("Helvetica", 12))
        manage_artists_button.pack(padx=10, pady=10)

        add_album_button = tk.Button(right_frame, text="Add Album", command=lambda: action_windows.open_add_album_window(db, root, refresh_gui), bg="#555555", fg="white", font=("Helvetica", 12))
        add_album_button.pack(padx=10, pady=10)

        update_album_button = tk.Button(right_frame, text="Update Album", command=lambda: action_windows.open_update_album_window(db, root, refresh_gui), bg="#555555", fg="white", font=("Helvetica", 12))
        update_album_button.pack(padx=10, pady=10)

        remove_album_button = tk.Button(right_frame, text="Remove Album", command=lambda: action_windows.open_remove_album_window(db, root, refresh_gui), bg="#555555", fg="white", font=("Helvetica", 12))
        remove_album_button.pack(padx=10, pady=10)

        manage_playlists_button = tk.Button(right_frame, text="Manage Playlists", command=lambda: action_windows.open_manage_playlists_window(db, root, refresh_gui), bg="#555555", fg="white", font=("Helvetica", 12))
        manage_playlists_button.pack(padx=10, pady=10)

        # Load Initial Data
    load_data()
