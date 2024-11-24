import mysql.connector
from tkinter import *
from tkinter import messagebox

def open_delete_account_gui(main_window):
    """Opens the Delete Account GUI."""
    # Create GUI for account deletion
    delete_window = Tk()
    delete_window.title("User Account Deletion")
    delete_window.geometry("400x300")
    delete_window.configure(bg="#2b2b2b")  # Dark theme background

    def delete_account():
        """Delete the account based on username, email, and password."""
        username = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not email or not password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            # Connect to the database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adobo5093",
                database="musiclibrarydb"
            )
            cursor = connection.cursor()

            # Verify the account credentials
            cursor.execute(
                "SELECT email FROM accounts WHERE username = %s AND email = %s AND password = %s",
                (username, email, password)
            )
            result = cursor.fetchone()

            if result is None:
                messagebox.showerror("Account Not Found", "No account matches the provided credentials.")
                return

            mail = result[0]

            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete the account '{username}' and all associated data?"
            )
            if not confirm:
                return

            # Perform deletion of associated data
            delete_queries = [
                ("DELETE FROM albumartist WHERE artist_id IN (SELECT artist_id FROM artists WHERE email = %s)", (mail,)),
                ("DELETE FROM artists WHERE email = %s", (mail,)),
                ("DELETE FROM playlistssongs WHERE playlist_id IN (SELECT playlist_id FROM playlist WHERE email = %s)", (mail,)),
                ("DELETE FROM playlist WHERE email = %s", (mail,)),
                ("DELETE FROM albumssongs WHERE song_id IN (SELECT song_id FROM songsartists WHERE artist_id IN (SELECT artist_id FROM artists WHERE email = %s))", (mail,)),
                ("DELETE FROM songsartists WHERE artist_id IN (SELECT artist_id FROM artists WHERE email = %s)", (mail,)),
                ("DELETE FROM songhistory WHERE account_id IN (SELECT account_id FROM accounts WHERE email = %s)", (mail,)),
                ("DELETE FROM accountlikessong WHERE account_id IN (SELECT account_id FROM accounts WHERE email = %s)", (mail,)),
                ("DELETE FROM accounts WHERE email = %s AND username = %s AND password = %s", (email, username, password))
            ]

            for query, params in delete_queries:
                cursor.execute(query, params)
            
            connection.commit()

            # Success message
            messagebox.showinfo("Success", f"The account '{username}' and all associated data have been deleted.")

            # Close both GUIs
            delete_window.destroy()  # Close deletion GUI
            main_window.destroy()  # Close main application

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error deleting account:\n{e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # Title Label
    title_label = Label(
        delete_window, text="Delete User Account", font=("Helvetica", 16), fg="white", bg="#2b2b2b"
    )
    title_label.pack(pady=10)

    # Username Label and Entry
    username_label = Label(delete_window, text="Username:", font=("Helvetica", 12), fg="white", bg="#2b2b2b")
    username_label.pack(pady=5)
    username_entry = Entry(delete_window, font=("Helvetica", 12), bg="#444", fg="white", insertbackground="white")
    username_entry.pack(pady=5)

    # Email Label and Entry
    email_label = Label(delete_window, text="Email:", font=("Helvetica", 12), fg="white", bg="#2b2b2b")
    email_label.pack(pady=5)
    email_entry = Entry(delete_window, font=("Helvetica", 12), bg="#444", fg="white", insertbackground="white")
    email_entry.pack(pady=5)

    # Password Label and Entry
    password_label = Label(delete_window, text="Password:", font=("Helvetica", 12), fg="white", bg="#2b2b2b")
    password_label.pack(pady=5)
    password_entry = Entry(delete_window, font=("Helvetica", 12), bg="#444", fg="white", insertbackground="white", show="*")
    password_entry.pack(pady=5)

    # Delete Account Button
    delete_button = Button(
        delete_window, text="Delete Account", command=delete_account, bg="#444", fg="white", font=("Helvetica", 12), relief=FLAT
    )
    delete_button.pack(pady=20)

    delete_window.mainloop()
