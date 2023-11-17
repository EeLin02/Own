from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import sqlite3
import hashlib

def create_users_table():
    conn = sqlite3.connect("TRAVEL KIOSK.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS USER (
            USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_NAME TEXT NOT NULL,
            USER_EMAIL TEXT NOT NULL,
            USER_PASSWORD TEXT NOT NULL,
            USER_TYPE TEXT NOT NULL DEFAULT 'user'
        )
    ''')

    conn.commit()
    conn.close()

def insert_user(username, email, password):
    conn = sqlite3.connect('TRAVEL KIOSK.db')
    cursor = conn.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("INSERT INTO USER (USER_NAME, USER_EMAIL, USER_PASSWORD) VALUES (?, ?, ?)",
                   (username, email, hashed_password))

    conn.commit()
    conn.close()

def get_user(username_email):
    conn = sqlite3.connect("TRAVEL KIOSK.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER WHERE USER_NAME = ? OR USER_EMAIL = ?",
                   (username_email, username_email))
    user = cursor.fetchone()
    conn.close()
    return user

def open_user_ui():
    # Add code for the regular user interface
    pass

def open_admin_ui():
    # Add code for the admin user interface
    pass

def validate_login():
    username_email = username_email_entry.get()
    password = password_entry.get()

    user = get_user(username_email)
    if user:
        stored_password = user[3]
        user_type = user[4]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if stored_password == hashed_password:
            if user_type == 'user':
                open_user_ui()
            elif user_type == 'admin':
                open_admin_ui()
            login_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid password.")
    else:
        messagebox.showerror("Login Failed", "User not found.")

def toggle_password_visibility():
    if show_password_var.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

def switch_to_signup():
    login_window.destroy()
    open_signup_page()

def on_enter_username_email(e):
    if username_email_entry.get() == 'Username/Email':
        username_email_entry.delete(0, 'end')

def on_leave_username_email(e):
    if username_email_entry.get() == '':
        username_email_entry.insert(0, 'Username/Email')

def on_enter_password(e):
    if password_entry.get() == 'Password':
        password_entry.delete(0, 'end')
        password_entry.config(show='*')

def on_leave_password(e):
    if password_entry.get() == '':
        password_entry.config(show='')
        password_entry.insert(0, 'Password')

def open_signup_page():
    # Your existing sign-up page code
    pass

# Login Page
login_window = Tk()
login_window.title("Login")
login_window.geometry("920x500+300+200")
login_window.configure(bg="#fff")
login_window.resizable(False, False)

background_image = Image.open('png.png')
background_image = background_image.resize((920, 500))
img = ImageTk.PhotoImage(background_image)

background_label = Label(login_window, image=img, border=0)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

heading = Label(login_window, text="Login", fg="#57a1f8", bg="#f8f8f8",
                font=("Microsoft Yahei UI Light", 23, "bold"))
heading.place(x=620, y=80)

username_email_entry = Entry(login_window, width=25, fg='black', border=0, bg='white',
                             font=('Microsoft Yahei UI Light', 11))
username_email_entry.place(x=500, y=150)
username_email_entry.insert(0, 'Username/Email')
username_email_entry.bind("<FocusIn>", on_enter_username_email)
username_email_entry.bind("<FocusOut>", on_leave_username_email)

Frame(login_window, width=295, height=2, bg='black').place(x=495, y=172)
password_entry = Entry(login_window, width=25, fg='black', border=0, bg='white',
                       font=('Microsoft Yahei UI Light', 11))
password_entry.place(x=500, y=190)
password_entry.insert(0, 'Password')
password_entry.bind("<FocusIn>", on_enter_password)
password_entry.bind("<FocusOut>", on_leave_password)

Frame(login_window, width=295, height=2, bg='black').place(x=495, y=212)
Button(login_window, width=20, pady=5, text='Login', bg='#57a1f8', fg='black', border=1,
       command=validate_login).place(x=500, y=225)
signup = Button(login_window, width=10, pady=5, text='Sign Up', border=1, bg='white', cursor='hand2', fg='#57a1f8',
                command=switch_to_signup)
signup.place(x=660, y=225)

show_password_var = IntVar()
show_password_checkbox = Checkbutton(login_window, text="Show Password", variable=show_password_var,
                                     command=toggle_password_visibility, bg="white")
show_password_checkbox.place(x=738, y=190)

login_window.mainloop()
