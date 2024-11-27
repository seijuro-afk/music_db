import mysql.connector
from tkinter import messagebox
from datetime import datetime

# ================================
# Database Connection Management
# ================================
def create_connection():
    """
    Establish and return a connection to the database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='pissword',  # Replace with your MySQL password
            database='musiclibrarydb'  # Replace with your database name
        )
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None


# ================================
# Utility Functions
# ================================
def execute_query(db, query, params=(), fetchone=False, fetchall=False):
    """
    General-purpose query execution utility.
    """
    cursor = db.cursor()
    try:
        print("Executing Query:", query)
        print("With Parameters:", params)

        cursor.execute(query, params)  # Parameters are passed here
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        db.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        db.rollback()
        raise err
    finally:
        cursor.close()


def fetch_or_create(db, table, select_query, insert_query, params):
    """
    Fetch an entity by a query or create a new entry.
    """
    result = execute_query(db, select_query, params, fetchone=True)
    if result:
        return result[0]
    return execute_query(db, insert_query, params)


def fetch_entities(db, table, columns="*", condition=None, params=(), group_by=None):
    """
    Generalized fetch function for any table with optional conditions.
    """
    query = f"SELECT {columns} FROM {table}"
    if condition:
        query += f" WHERE {condition}"
    if group_by:
        query += f" GROUP BY {group_by}"
    return execute_query(db, query, params=params, fetchall=True)


# ================================
# CRUD Operations
# ================================
def get_or_create_artist(db, artist_name):
    """
    Fetch or create an artist and return their ID.
    """
    # Check if the artist exists
    artist_id = execute_query(
        db,
        "SELECT artist_id FROM artists WHERE name = %s",
        params=(artist_name,),
        fetchone=True
    )

    if artist_id:
        return artist_id[0]

    # If the artist doesn't exist, raise a ValueError for account creation
    raise ValueError("Account for this artist was not found.")



def get_or_create_album(db, album_title, artist_id=None, album_type=None, created_at=None):
    """
    Fetch or create an album and optionally link to an artist.
    """
    if not album_type:
        raise ValueError("Album type must be provided.")

    # Fetch album ID if it already exists
    album_id = execute_query(
        db,
        "SELECT album_id FROM albums WHERE title = %s AND album_type = %s",
        (album_title, album_type),  # Match title and album type
        fetchone=True
    )

    if album_id:
        return album_id[0]  # Return the existing album ID

    # Create new album if it doesn't exist
    album_id = execute_query(
        db,
        "INSERT INTO albums (title, album_type, created_at) VALUES (%s, %s, %s)",
        (album_title, album_type, created_at or datetime.now())
    )

    # Link album to artist if artist ID is provided
    if artist_id:
        execute_query(
            db,
            "INSERT IGNORE INTO albumartist (album_id, artist_id) VALUES (%s, %s)",
            (album_id, artist_id)
        )

    return album_id

def update_album_songs(db, album_id, updated_songs):
    """
    Update songs in an album and recalculate album duration.
    """
    # Step 1: Remove existing songs from the album
    execute_query(db, "DELETE FROM albumssongs WHERE album_id = %s", params=(album_id,))

    total_duration = 0  # Track the total duration of the album

    # Step 2: Add updated songs back to the album
    for song_id, title, duration, genre_name in updated_songs:
        # Fetch genre alias from the database
        genre_alias = execute_query(db, "SELECT genre_alias FROM genres WHERE genre_name = %s", params=(genre_name,), fetchone=True)

        if not genre_alias:
            raise ValueError(f"Genre '{genre_name}' does not exist for song '{title}'.")

        # Update the song details
        execute_query(db, "UPDATE songs SET title = %s, song_duration = %s, genre = %s WHERE song_id = %s",
                      params=(title, duration, genre_alias[0], song_id))

        # Re-link the song to the album
        execute_query(db, "INSERT INTO albumssongs (song_id, album_id) VALUES (%s, %s)", params=(song_id, album_id))

        # Convert the song duration to seconds for total calculation
        time_parts = list(map(int, duration.split(":")))
        total_duration += time_parts[0] * 3600 + time_parts[1] * 60 + time_parts[2]

    # Step 3: Update album duration
    if total_duration > 0:
        # Convert total duration back to HH:MM:SS format
        duration_time = f"{total_duration // 3600:02}:{(total_duration % 3600) // 60:02}:{total_duration % 60:02}"
    else:
        # If no songs remain, set the duration to "00:00:00"
        duration_time = "00:00:00"

    execute_query(db, "UPDATE albums SET album_duration = %s WHERE album_id = %s", params=(duration_time, album_id))



def create_account(db, username, email, password):
    """
    Create a new account in the database and return the account ID.
    """
    try:
        print(f"Creating account: username={username}, email={email}")
        account_id = execute_query(
            db,
            "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)",
            params=(username, email, password)
        )
        print(f"Account created with ID: {account_id}")
        return account_id
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            raise ValueError(f"Account with email '{email}' or username '{username}' already exists.")
        raise

def get_genre_alias(db, genre_name):
    """
    Get the genre alias corresponding to a given genre name.
    """
    query = "SELECT genre_alias FROM genres WHERE genre_name = %s"
    result = execute_query(db, query, params=(genre_name,), fetchone=True)

    if not result:
        raise ValueError(f"Genre '{genre_name}' does not exist.")
    return result[0]


def add_song(db, title, genre_name, duration, created_at, artist_id=None, album_id=None):
    """
    Add a new song and link it to an artist and album if provided.
    """
    # Validate genre name and get the alias
    genre_alias = validate_genre(db, genre_name)

    # Insert the song into the database
    song_id = execute_query(
        db,
        """
        INSERT INTO songs (title, genre, song_duration, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        (title, genre_alias, duration, created_at)
    )

    # Link the song to the artist, if provided
    if artist_id:
        execute_query(
            db,
            "INSERT INTO songsartists (song_id, artist_id) VALUES (%s, %s)",
            (song_id, artist_id)
        )

    # Link the song to the album, if provided
    if album_id:
        execute_query(
            db,
            "INSERT INTO albumssongs (song_id, album_id) VALUES (%s, %s)",
            (song_id, album_id)
        )

    return song_id


# ================================
# Fetch Operations
# ================================
def fetch_songs(db, album_id=None):
    """
    Fetch songs from the database, optionally filtered by album ID.
    """
    columns = """
        s.title,
        GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS artist,
        GROUP_CONCAT(DISTINCT al.title SEPARATOR ', ') AS album,
        GROUP_CONCAT(DISTINCT g.genre_name SEPARATOR ', ') AS genre,
        s.song_duration
    """
    base_table = """
        songs s
        LEFT JOIN albumssongs als ON s.song_id = als.song_id
        LEFT JOIN albums al ON als.album_id = al.album_id
        LEFT JOIN songsartists sa ON s.song_id = sa.song_id
        LEFT JOIN artists a ON sa.artist_id = a.artist_id
        LEFT JOIN genres g ON s.genre = g.genre_alias
    """
    condition = "al.album_id = %s" if album_id else None
    params = (album_id,) if album_id else ()

    # Ensure params are passed to fetch_entities
    return fetch_entities(
        db,
        table=base_table,
        columns=columns,
        condition=condition,
        params=params,
        group_by="s.song_id"
    )


def fetch_artist_by_email(db, email):
    """
    Fetch artist by email.
    """
    query = "SELECT artist_id, name FROM artists WHERE email = %s"
    return execute_query(db, query, params=(email,), fetchone=True)

def fetch_albums_by_artist(db, artist_id):
    """
    Fetch albums by artist ID.
    """
    query = """
        SELECT al.album_id, al.title
        FROM albumartist aa
        JOIN albums al ON aa.album_id = al.album_id
        WHERE aa.artist_id = %s
    """
    return execute_query(db, query, params=(artist_id,), fetchall=True)

def fetch_songs_by_album(db, album_id):
    """
    Fetch songs by album ID.
    """
    query = """
        SELECT s.song_id, s.title, s.song_duration, g.genre_name
        FROM albumssongs als
        JOIN songs s ON als.song_id = s.song_id
        JOIN genres g ON s.genre = g.genre_alias
        WHERE als.album_id = %s
    """
    return execute_query(db, query, params=(album_id,), fetchall=True)


# ================================
# Validation and Miscellaneous
# ================================
def validate_genre(db, genre_name):
    """
    Validates that the genre name exists in the database and returns its alias.
    """
    query = "SELECT genre_alias FROM genres WHERE genre_name = %s"
    result = execute_query(db, query, params=(genre_name,), fetchone=True)

    if not result:
        raise ValueError(f"Genre '{genre_name}' does not exist.")
    return result[0]  # Return the alias for the genre

def link_account_to_artist(db, email, password, artist_name):
    """
    Link an existing account to an artist or raise an error if it doesn't exist.
    """
    # Check if the account exists
    account_query = "SELECT account_id FROM accounts WHERE email = %s AND password = %s"
    account = execute_query(db, account_query, params=(email, password), fetchone=True)

    if not account:
        raise ValueError("Account not found.")

    account_id = account[0]

    # Check if the artist exists
    artist_query = "SELECT artist_id FROM artists WHERE account_id = %s"
    artist = execute_query(db, artist_query, params=(account_id,), fetchone=True)

    if artist:
        return artist[0]  # Return the existing artist ID

    # Create a new artist
    artist_id = execute_query(
        db,
        "INSERT INTO artists (name, account_id) VALUES (%s, %s)",
        params=(artist_name, account_id)
    )
    return artist_id

