from tkinter import *
from tkinter import Tk
import tkinter.ttk as ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Spinbox
from tkinter import StringVar
from tkcalendar import Calendar
import datetime
import random
from tkinter import messagebox
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sqlite3
import io
from io import BytesIO
from questions import QUESTIONS
from tkinterhtml import HtmlFrame
import webbrowser
from tkintermapview import TkinterMapView
from tkinter import Label
import hashlib
import json


class TravelKioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Penang Travel Kiosk")
        self.conn = sqlite3.connect('TRAVEL KIOSK.db')
        self.cursor = self.conn.cursor()
        self.signup_window = None  # Initialize signup_window as None
        self.open_login_page()

    def get_image_data(self, image_id):
        self.cursor.execute("SELECT IMAGE_DATA FROM IMAGES WHERE IMAGE_ID = ?", (image_id,))
        data = self.cursor.fetchone()

        if data is not None:
            return BytesIO(data[0])
        else:
            return None

    def insert_user(self, username, email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("INSERT INTO USER (USER_NAME, USER_EMAIL, USER_PASSWORD) VALUES (?, ?, ?)",
                            (username, email, hashed_password))
        self.conn.commit()

    def get_user(self, username_email):
        self.cursor.execute("SELECT * FROM USER WHERE USER_NAME = ? OR USER_EMAIL = ?",
                            (username_email, username_email))
        return self.cursor.fetchone()

    def open_signup_page(self):
        def validate_signup():
            # Retrieve input values
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()

            # Perform sign-up validation logic
            if not username or not email or not password or not confirm_password:
                messagebox.showerror("Sign Up Failed", "Please fill in all the fields.")
            # Perform sign-up validation logic
            elif not username:
                messagebox.showerror("Sign Up Failed", "Username is required.")
            elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@_#$%])[a-zA-Z\d!@_#$%]{5,}$", username):
                messagebox.showerror("Sign Up Failed",
                                     "Username must contain at least 1 uppercase letter, 1 lowercase letter, numbers, "
                                     "and symbols (e.g., !@_#$%), and be at least 5 characters long.")
            elif not email:
                messagebox.showerror("Sign Up Failed", "Email is required.")
            elif not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
                messagebox.showerror("Sign Up Failed", "Invalid email format.")
            elif not password:
                messagebox.showerror("Sign Up Failed", "Password is required.")
            elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
                messagebox.showerror("Sign Up Failed",
                                     "Password must contain at least 1 uppercase letter, 1 lowercase letter, numbers, "
                                     "and be at least 8 characters long.")
            elif password != confirm_password:
                messagebox.showerror("Sign Up Failed", "Passwords do not match.")
            else:
                # Check if the username already exists in the database
                user = self.get_user(username)
                if user:
                    messagebox.showerror("Sign Up Failed", "Username already exists.")
                else:
                    # Registration successful
                    self.insert_user(username, email, password)
                    messagebox.showinfo("Sign Up Successful", "You have successfully registered.")
                    switch_to_login()  # Redirect to the login page

        def switch_to_login():
            self.signup_window.destroy()
            self.open_login_page()

        self.signup_window = Toplevel(self.root)  # Use Toplevel for signup window
        self.signup_window.title("Sign Up")
        self.signup_window.geometry("920x500+300+200")
        self.signup_window.configure(bg="#fff")
        self.signup_window.resizable(False, False)

        back_image = self.get_image_data(28)
        if back_image is not None:
            back_image = Image.open(back_image)
            back_image = back_image.resize((920, 500))  # Resize to the window size with antialiasing
            back_image = ImageTk.PhotoImage(back_image)  # Convert to Tkinter PhotoImage

            # Create a label to display the background image
            background_label = Label(self.signup_window, image=back_image, border=0)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

        heading = Label(self.signup_window, text="SignUp", fg="#57a1f8", bg="#f8f8f8",
                        font=("Microsoft Yahei UI Light", 23, "bold"))
        heading.place(x=610, y=80)

        # Username entry
        def on_enter_username(e):
            if username_entry.get() == 'Username':
                username_entry.delete(0, 'end')

        def on_leave_username(e):
            if username_entry.get() == '':
                username_entry.insert(0, 'Username')

        username_entry = Entry(self.signup_window, width=25, fg='black', border=0, bg='white',
                               font=('Microsoft Yahei UI Light', 11))
        username_entry.place(x=500, y=150)
        username_entry.insert(0, 'Username')
        username_entry.bind("<FocusIn>", on_enter_username)
        username_entry.bind("<FocusOut>", on_leave_username)

        Frame(self.signup_window, width=295, height=2, bg='black').place(x=500, y=170)

        # Email entry
        def on_enter_email(e):
            if email_entry.get() == 'Email':
                email_entry.delete(0, 'end')

        def on_leave_email(e):
            if email_entry.get() == '':
                email_entry.insert(0, 'Email')

        email_entry = Entry(self.signup_window, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        email_entry.place(x=500, y=190)
        email_entry.insert(0, 'Email')
        email_entry.bind("<FocusIn>", on_enter_email)
        email_entry.bind("<FocusOut>", on_leave_email)

        Frame(self.signup_window, width=295, height=2, bg='black').place(x=500, y=210)

        # Password entry
        def on_enter_password(e):
            if password_entry.get() == 'Password':
                password_entry.delete(0, 'end')

        def on_leave_password(e):
            if password_entry.get() == '':
                password_entry.insert(0, 'Password')

        password_entry = Entry(self.signup_window, width=25, fg='black', border=0, bg='white',
                               font=('Microsoft Yahei UI Light', 11))
        password_entry.place(x=500, y=230)
        password_entry.insert(0, 'Password')
        password_entry.bind("<FocusIn>", on_enter_password)
        password_entry.bind("<FocusOut>", on_leave_password)

        Frame(self.signup_window, width=295, height=2, bg='black').place(x=500, y=248)

        # Confirm Password entry
        def on_enter_confirm_password(e):
            if confirm_password_entry.get() == 'Confirm Password':
                confirm_password_entry.delete(0, 'end')

        def on_leave_confirm_password(e):
            if confirm_password_entry.get() == '':
                confirm_password_entry.insert(0, 'Confirm Password')

        confirm_password_entry = Entry(self.signup_window, width=25, fg='black', border=0, bg='white',
                                       font=('Microsoft Yahei UI Light', 11))
        confirm_password_entry.place(x=500, y=270)
        confirm_password_entry.insert(0, 'Confirm Password')
        confirm_password_entry.bind("<FocusIn>", on_enter_confirm_password)
        confirm_password_entry.bind("<FocusOut>", on_leave_confirm_password)

        Frame(self.signup_window, width=295, height=2, bg='black').place(x=500, y=288)

        Button(self.signup_window, width=20, pady=5, text='Sign Up', bg='#57a1f8', fg='black', border=0,
               command=validate_signup).place(
            x=560, y=310)
        login_button = Button(self.signup_window, width=30, pady=5, text='Already a Member? Login', border=0, bg='white',
                              cursor='hand2',
                              fg='#57a1f8', command=switch_to_login)
        login_button.place(x=530, y=350)
        self.signup_window.mainloop()

    def open_login_page(self):
        def validate_login(self):
            # Retrieve input values
            username_email = username_email_entry.get()
            password = password_entry.get()

            # Perform login validation logic
            user = self.get_user(username_email)
            if user:
                stored_password = user[3]  # Assuming user[3] contains the hashed password in the database
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if stored_password == hashed_password:
                    user_id = user[0]  # Assuming user[0] is the user ID in the database

                    # Login is successful
                    messagebox.showinfo("Login Successful", "You have successfully logged in.")

                    # Close the current login window
                    self.root.destroy()

                    # Open a new root window for the TravelKiosk
                    new_root = Tk()

                    # Create an instance of TravelKiosk with the new root
                    TravelKiosk(new_root, user_id)

                    # Start the Tkinter event loop for the new window
                    new_root.mainloop()
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
            if self.root.winfo_exists():
                self.open_signup_page()

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

        login_window = self.root
        login_window.title("Login")
        login_window.geometry("920x500+300+200")
        login_window.configure(bg="#fff")
        login_window.resizable(False, False)

        back_image = self.get_image_data(28)
        if back_image is not None:
            back_image = Image.open(back_image)
            back_image = back_image.resize((920, 500))  # Resize to the window size with antialiasing
            back_image = ImageTk.PhotoImage(back_image)  # Convert to Tkinter PhotoImage

            # Create a label to display the background image
            background_label = Label(login_window, image=back_image, border=0)
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
               command=lambda:validate_login(self)).place(x=500, y=225)
        signup = Button(login_window, width=10, pady=5, text='Sign Up', border=1, bg='white', cursor='hand2',
                        fg='#57a1f8',command=switch_to_signup)
        signup.place(x=660, y=225)

        show_password_var = IntVar()
        show_password_checkbox = Checkbutton(login_window, text="Show Password", variable=show_password_var,
                                             command=toggle_password_visibility, bg="white")
        show_password_checkbox.place(x=738, y=190)

        login_window.mainloop()

    def __del__(self):
        self.conn.close()

def get_image_data(image_id):
    conn = sqlite3.connect('TRAVEL KIOSK.db')
    cursor = conn.cursor()

    cursor.execute("SELECT IMAGE_DATA FROM IMAGES WHERE IMAGE_ID = ?", (image_id,))
    data = cursor.fetchone()

    conn.close()

    if data is not None:
        image_data = io.BytesIO(data[0])
        return image_data
    else:
        return None

class TravelKiosk:
    def __init__(self, root, user_id):
        self.style = ttk.Style()
        self.root = root
        self.root.title("Penang Travel Kiosk")
        self.root.geometry("1420x700")
        self.user_id = user_id

        self.image_references = []  # Initialize an empty list

        # Create a custom style for buttons and entry boxes
        self.create_styles()

        # Create top bar
        self.create_top_bar()

        # Create second bar with page links
        # self.create_second_bar()

        # Create a frame to display content
        self.canvas = tk.Canvas(root, bg="white")
        self.content_frame = ttk.Frame(self.canvas)

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add this line to pack the content frame inside the canvas
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Add this line to bind the canvas configuration to the canvas_configure function
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Create the home page
        self.open_home_page()

    def create_styles(self):
        # Set the background color to white for buttons and entry boxes
        self.style.configure('TButton', background='white')
        self.style.configure('TEntry', background='white')

    def create_top_bar(self):
        top_bar = ttk.Frame(self.root)
        top_bar.pack(fill='x')

        # Create a label with a specified background color
        top_bar_label = tk.Frame(top_bar, bg='white', height=1, bd=1, relief="raised")
        top_bar_label.pack(fill='both', )
        top_bar_label2 = tk.Label(top_bar_label, bg='white', )
        top_bar_label2.pack(fill='x', side='left')
        top_bar_label1 = tk.Label(top_bar_label, bg='white')
        top_bar_label1.pack(fill='x', side='right')

        logo_image = get_image_data(24)
        logo_image = Image.open(logo_image)
        logo_image = logo_image.resize((65, 50))
        logo_image = ImageTk.PhotoImage(logo_image)

        # Create the Logo label with the image (no border)
        logo_label = tk.Label(top_bar_label2, image=logo_image, cursor="hand2", bd=0, highlightthickness=0)
        logo_label.image = logo_image
        logo_label.pack(side='left', padx=20, pady=10)

        # Bind the callback function to the click event of the logo label
        logo_label.bind("<Button-1>", lambda event: self.open_home_page())
        # Create page links
        pages = ["Explore Destination", "Ticket", "Transport", "Food", "Mall", "Market", "Map", "Game"]
        page_buttons = []
        for page in pages:
            if page == "Explore Destination":
                button = ttk.Button(top_bar_label2, text=page, command=self.explore_north, style='TButton')
            elif page == "Ticket":
                button = ttk.Button(top_bar_label2, text=page, command=self.ticket_page, style='TButton')
            elif page == "Game":
                button = ttk.Button(top_bar_label2, text=page, command=self.game_page, style='TButton')
            elif page == "Food":
                button = ttk.Button(top_bar_label2, text=page, command=self.food_page, style='TButton')
            elif page == "Mall":
                button = ttk.Button(top_bar_label2, text=page, command=self.shopping_page, style='TButton')
            elif page == "Market":
                button = ttk.Button(top_bar_label2, text=page, command=self.market_page, style='TButton')
            elif page == "Transport":
                button = ttk.Button(top_bar_label2, text=page, command=self.transport_page, style='TButton')
            elif page == "Map":
                button = ttk.Button(top_bar_label2, text=page, command=self.map_page, style='TButton')
            button.pack(side='left', padx=10, pady=3)
            page_buttons.append(button)

        # Search Bar
        search_entry = ttk.Entry(top_bar_label1, width=25, style='TEntry')  # Adjust the width and use the custom style
        search_entry.pack(side='left', padx=10, pady=5, fill='x', expand=True)

        search_button = ttk.Button(top_bar_label1, text="Search", style='TButton',
                                   command=lambda: self.search_activities(search_entry.get()))
        search_button.pack(side='left', padx=10)

        account_image = get_image_data(29)
        account_image = Image.open(account_image)
        account_image = account_image.resize((50, 50))
        account_image = ImageTk.PhotoImage(account_image)

        # Create the Account label with the image (no border)
        account_label = tk.Label(top_bar_label1, image=account_image, cursor="hand2", bd=0, highlightthickness=0)
        account_label.image = account_image
        account_label.pack(side='right', padx=10, pady=10)
        account_label.bind("<Button-1>", lambda event: self.open_account())  # Bind a click event

        # Help Center Link (customize the command)
        help_button = ttk.Button(top_bar_label1, text="Help", command=self.open_help_center,
                                 style='TButton')  # Use the custom style
        help_button.pack(side='right', padx=5)

    def open_home_page(self):
        # Reset the hole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the banner background
        banner_label = tk.Frame(self.content_frame, bg='white', height=4, )
        banner_label.pack(fill='both')

        # Load and resize the banner image
        banner_image = get_image_data(25)
        banner_image = Image.open(banner_image)
        banner_image = banner_image.resize((1200, 380))  # Adjust the size as needed
        banner_image = ImageTk.PhotoImage(banner_image)

        # Create the banner image label
        banner_image_label = tk.Label(banner_label, image=banner_image)
        banner_image_label.image = banner_image
        banner_image_label.pack(padx=100, side='left')

        # Create a title label for Popular Activities
        popular_activities_label = tk.Label(self.content_frame, text="Popular Activities", font=("Lato", 20),
                                            fg='Black', padx=100, bg='white',
                                            anchor='w')  # Use 'w' (west) for left alignment
        popular_activities_label.pack(fill='x')

        # Create a label for the banner background
        activity_label2 = tk.Frame(self.content_frame, bg='white')
        activity_label2.pack(fill='x')
        activity_label1 = tk.Frame(activity_label2, bg='white', padx=10)
        activity_label1.pack(fill='x', padx=50, )
        activity_label = tk.Frame(activity_label1, bg='white', padx=10)
        activity_label.pack(fill='x')
        # 0124374916

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        selected_attraction_ids = (2, 3, 4, 5)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT a.ATTRACTION_NAME, a.TICKET_PRICE, i.IMAGE_DATA
        FROM ATTRACTION a
        JOIN IMAGES i ON a.ATTRACTION_ID = i.IMAGE_RELATED_ID
        WHERE a.ATTRACTION_ID IN {selected_attraction_ids} and i.IMAGE_TYPE = "Attraction" and i.IMAGE_NAME like "%1"
        """
        cursor.execute(query)

        # Fetch the query result
        activities = [
            {"name": row[0], "money": "RM" + f"  {row[1]}", "image_data": row[2]}
            for row in cursor.fetchall()
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Create a BytesIO object from the binary image data
            image_data_io = BytesIO(activity["image_data"])

            # Load the image from the BytesIO object
            activity_image = Image.open(image_data_io)

            # Resize the activity image
            activity_image = activity_image.resize((240, 170))  # Adjust the size as needed

            # Convert the image to a format that Tkinter can use
            activity_image = ImageTk.PhotoImage(activity_image)

            # Create a frame to hold both the image and information labels with an outline
            activity_frame = tk.Frame(activity_label, bg='white', bd=1, relief="solid")  # Add the border
            activity_frame.grid(row=0, column=i, padx=35, )
            # Create the activity image label inside the frame
            activity_image_label = tk.Label(activity_frame, image=activity_image)
            activity_image_label.image = activity_image
            activity_image_label.pack()

            # Create a frame to hold both labels
            activity_info_frame = tk.Frame(activity_frame, bg='white')  # No need for a border here
            activity_info_frame.pack(fill='x', expand=True)

            # Create activity_info1 and activity_info2 inside the info frame
            activity_info1 = tk.Label(activity_info_frame, text=activity["name"], font=("Lato", 12), fg='Black',
                                      bg='white', anchor='w', width=23)
            activity_info2 = tk.Label(activity_info_frame, text=activity["money"], font=("Lato", 12), fg='Black',
                                      bg='white', anchor='e', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            activity_info1.pack(fill='x', expand=True)
            activity_info2.pack(fill='x', expand=True)

            # Create the activity button inside the frame and open the destination page on click
            activity_button = ttk.Button(activity_frame, text="Details",
                                         command=lambda a=activity,
                                                        path=activity["image_data"]: self.open_activity_ticket_page(a,
                                                                                                                    path),
                                         style='TButton')
            activity_button.pack(fill='x', expand=True)
            self.buttons.append(activity_button)

        blank_label = tk.Label(self.content_frame, bg='white')
        blank_label.pack(fill='x')

        # Create a new box with a map image below the activity boxes
        map_box_label1 = tk.Frame(self.content_frame, bg='white', padx=98)
        map_box_label1.pack(fill='x')
        map_box_label = tk.Frame(map_box_label1, bg='white', bd=1, relief="solid")
        map_box_label.pack(fill='x')

        # Load and resize the map image
        map_image = get_image_data(23)
        map_image = Image.open(map_image)
        map_image = map_image.resize((260, 170))  # Adjust the size as needed
        map_image = ImageTk.PhotoImage(map_image)

        # Create the map image label
        map_image_frame = tk.Label(map_box_label, image=map_image)
        map_image_frame.image = map_image
        map_image_frame.pack(side='right')
        # Make the map image clickable
        map_image_frame.bind("<Button-1>", self.show_large_image)

        # Create a frame to hold information below the map
        map_info_label = ttk.Frame(map_box_label)
        map_info_label.pack(side='left', padx=10)

        # Add information label below the map
        map_info = tk.Label(
            map_info_label,
            text="Penang is a vibrant State with its capital, George Town, having the rare distinction of being a "
                 "UNESCO World Heritage Site. It is a true melting pot of cultures with its blend of Eastern and "
                 "Western influences. Retaining many of the values adopted during its era of British rule, Penang bears"
                 " a charm that is unique to itself.", font=("Lato", 15), fg='Black', bg='white', anchor='w',
            justify='left', wraplength=900)
        map_info.pack(fill='x', expand=True)

        blank_label = tk.Label(self.content_frame, bg='white')
        blank_label.pack(fill='x')

    def ticket_page(self):
        # Reset the hole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a title label for Popular Activities
        popular_activities_label = tk.Label(self.content_frame, text="     Popular Activities", font=("Lato", 20),
                                            fg='Black', bg='white', anchor='w',
                                            padx=100)  # Use 'w' (west) for left alignment
        popular_activities_label.pack(fill='x')

        activity_label = tk.Frame(self.content_frame, bg='white', padx=100)
        activity_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        selected_attraction_ids = (2, 3, 4, 5)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT a.ATTRACTION_NAME, a.TICKET_PRICE, i.IMAGE_DATA
        FROM ATTRACTION a
        JOIN IMAGES i ON a.ATTRACTION_ID = i.IMAGE_RELATED_ID
        WHERE a.ATTRACTION_ID IN {selected_attraction_ids} and i.IMAGE_TYPE = "Attraction" and i.IMAGE_NAME like "%1"
        """
        cursor.execute(query)

        # Fetch the query result
        activities = [
            {"name": row[0], "money": "RM" + f"  {row[1]}", "image_data": row[2]}
            for row in cursor.fetchall()
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Create a BytesIO object from the binary image data
            image_data_io = BytesIO(activity["image_data"])

            # Load the image from the BytesIO object
            activity_image = Image.open(image_data_io)

            # Resize the activity image
            activity_image = activity_image.resize((240, 170))  # Adjust the size as needed

            # Convert the image to a format that Tkinter can use
            activity_image = ImageTk.PhotoImage(activity_image)

            # Create a frame to hold both the image and information labels with an outline
            activity_frame = tk.Frame(activity_label, bg='white', bd=1, relief="solid")  # Add the border
            activity_frame.grid(row=0, column=i, padx=25)

            # Create the activity image label inside the frame
            activity_image_label = tk.Label(activity_frame, image=activity_image)
            activity_image_label.image = activity_image
            activity_image_label.pack()

            # Create a frame to hold both labels
            activity_info_frame = tk.Frame(activity_frame, bg='white')  # No need for a border here
            activity_info_frame.pack(fill='x', expand=True)

            # Create activity_info1 and activity_info2 inside the info frame
            activity_info1 = tk.Label(activity_info_frame, text=activity["name"], font=("Lato", 12), fg='Black',
                                      bg='white', anchor='w', width=23)
            activity_info2 = tk.Label(activity_info_frame, text=activity["money"], font=("Lato", 12), fg='Black',
                                      bg='white', anchor='e', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            activity_info1.pack(fill='x', expand=True)
            activity_info2.pack(fill='x', expand=True)

            # Create the activity button inside the frame and open the destination page on click
            activity_button = ttk.Button(activity_frame, text="Details",
                                         command=lambda a=activity,
                                                        path=activity["image_data"]: self.open_activity_ticket_page(a,
                                                                                                                    path),
                                         style='TButton')
            activity_button.pack(fill='x', expand=True)
            self.buttons.append(activity_button)

    def open_activity_ticket_page(self, activity, image_path):
        # Reset the hole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"     Details for {activity['name']}", font=("Lato", 20),
                                 fg='Black', bg='white', anchor='w', padx=215)
        details_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')
        cursor = conn.cursor()

        # Execute a query to retrieve details for the specific attraction and its images
        query = """
            SELECT a.ATTRACTION_ID, a.ATTRACTION_NAME, a.ATTRACTION_DETAILS, a.ATTRACTION_LOCATION, a.OPERATING_HOURS, a.TICKET_PRICE, 
            i.IMAGE_DATA
            FROM ATTRACTION a
            JOIN IMAGES i ON a.ATTRACTION_ID = i.IMAGE_RELATED_ID
            WHERE a.ATTRACTION_NAME = ? and i.IMAGE_TYPE = "Attraction" and i.IMAGE_NAME like "%2"
            """
        cursor.execute(query, (activity['name'],))  # Provide the attraction name as a tuple

        # Extract details for the attraction
        result = cursor.fetchone()
        if result:
            attraction_id = result[0]
            id, name, details, location, operating_hours, price, image_data = result

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            # Create a frame to display details and additional information
            details_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
            details_frame.pack(fill='x')

            # Load and resize the activity image for the details page
            image_data_io = BytesIO(image_data)
            activity_image = Image.open(image_data_io)
            activity_image = activity_image.resize((950, 240))
            activity_image = ImageTk.PhotoImage(activity_image)

            # Create the activity image label on the details page
            activity_image_label = tk.Label(details_frame, image=activity_image)
            activity_image_label.image = activity_image
            activity_image_label.pack(side='top', padx=250)

            blank_label = tk.Label(details_frame, bg='white')
            blank_label.pack(fill='x')

            # Replace the if-else block with a direct assignment
            name_text = f"About {name}"

            # Create a frame for information
            info_frame = tk.Frame(details_frame, bg='white', bd=1, relief="solid", width=700, height=200)
            info_frame.pack(side='top', padx=20)

            # Set the text for the labels
            info_text = f"{details}\n\n\u27A4 {location}\n\nOperating Hours: {operating_hours}"
            name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            name_label.pack(fill='both', expand=True, padx=25, pady=10)
            info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            info_label.pack(fill='both', expand=True, padx=25, pady=10)

            blank_label = tk.Label(details_frame, bg='white')
            blank_label.pack(fill='x')

            # Create a frame for information
            buy_tic_frame1 = tk.Frame(details_frame, bg='white', bd=1, relief="solid", width=300, height=200)
            buy_tic_frame1.pack(fill='x', padx=257)
            buy_tic_frame2 = tk.Frame(buy_tic_frame1, bg='white')
            buy_tic_frame2.pack(side="right")
            buy_tic_frame3 = tk.Frame(buy_tic_frame1, bg='white')
            buy_tic_frame3.pack(side="left")
            buy_tic_frame4 = tk.Frame(buy_tic_frame1, bg='white')
            buy_tic_frame4.pack(anchor="center")

            # Add a section for buying tickets and selecting a date
            buy_ticket_label = tk.Label(buy_tic_frame3, text="    Buy Tickets", font=("Lato", 20), fg='black',
                                        bg='white',
                                        anchor='w')
            buy_ticket_label.pack(fill='x', padx=10)

            price_text = f"RM {price}"
            price_label = tk.Label(buy_tic_frame2, text=f"One Person : {price_text}", font=("Lato", 12), fg='black',
                                   bg='white', anchor='w')
            price_label.pack(fill='x', pady=5, padx=10)
            # Create a Spinbox to select the number of tickets
            ticket_count_label = tk.Label(buy_tic_frame2, text="Number of Tickets:", font=("Lato", 12), fg='black',
                                          bg='white', anchor='w')
            ticket_count_label.pack(fill='x', padx=10)
            ticket_count = StringVar()
            ticket_count.set("1")  # Default value
            ticket_spinbox = Spinbox(buy_tic_frame2, from_=1, to=20, textvariable=ticket_count)
            ticket_spinbox.pack(fill='x', padx=10)

            # blank space
            blank_label = tk.Label(buy_tic_frame2, bg='white')
            blank_label.pack(fill='x')

            # Load an image
            ppl_image = get_image_data(30)
            ppl_image = Image.open(ppl_image)
            ppl_image = ppl_image.resize((150, 180))
            ppl_image = ImageTk.PhotoImage(ppl_image)

            # Create a label to display the resized image
            ppl_image_label = tk.Label(buy_tic_frame3, image=ppl_image, bg='white')
            ppl_image_label.image = ppl_image
            ppl_image_label.pack()

            # blank space
            blank_label = tk.Label(buy_tic_frame4, bg='white')
            blank_label.pack(fill='x')

            # Create a "Select Date" label
            date_label = tk.Label(buy_tic_frame4, text="Select Date:", font=("Lato", 12), fg='black', bg='white',
                                  anchor='w')
            date_label.pack(fill='x', padx=25, pady=10)

            # Create the Calendar widget with a custom date format
            self.date_calendar = Calendar(buy_tic_frame4, locale='en_US', font="Arial 7", date_pattern='dd/MM/yyyy',
                                          selectmode='day', mindate=datetime.date.today(),)
            self.date_calendar.pack(fill='x', padx=25)

            #attraction_id = 123  # Replace 123 with the actual attraction ID

            # Create a button to book tickets
            book_button = ttk.Button(buy_tic_frame2, text="Book Tickets", style='TButton',
                                     command=lambda: self.show_payment_page(activity, image_path, ticket_count, attraction_id,))
            book_button.pack(padx=20, pady=5)

            # blank space
            blank_label = tk.Label(buy_tic_frame3, bg='white')
            blank_label.pack(fill='x')

            # Create a button to go back to the ticket_page
            back_button = ttk.Button(details_frame, text="Back", command=self.ticket_page, style='TButton')
            back_button.pack(pady=10)

    def show_payment_page(self, activity, image_path, ticket_count, attraction_id, ):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        details_frame = tk.Frame(self.content_frame, bg='white', padx=320)
        details_frame.pack(fill='x', anchor='center')

        blank_label = tk.Label(details_frame, bg='white')
        blank_label.pack(fill='x')

        # Create an X box (upper center of the page)
        x_box = tk.Frame(details_frame, bg='white', padx=20, bd=1, relief="solid")
        x_box.pack(fill='x', anchor='center')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        selected_attraction_ids = (2, 3, 4, 5)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT ATTRACTION_NAME, TICKET_PRICE
        FROM ATTRACTION
        WHERE ATTRACTION_ID IN {selected_attraction_ids}
        """

        # Fetch the query result
        attraction_details = cursor.execute(query).fetchall()
        # Initialize total_amount to 0
        total_amount = 0

        # Iterate through the attractions and find the corresponding ticket price
        for attraction in attraction_details:
            attraction_name, ticket_price = attraction

            # Check if the current attraction is the one selected
            if activity['name'] == attraction_name:
                total_amount += ticket_price * int(ticket_count.get())
                break

        # Create labels for X box
        payment_label = tk.Label(x_box, text="Payment", font=("Lato", 20), fg='black', bg='white', anchor='w')
        payment_label.grid(row=0, column=0, sticky='w', padx=213)

        total_amount_label1 = tk.Label(x_box, text="Total Amount:", font=("Lato", 14), fg='black', bg='white',
                                       anchor='w')
        total_amount_label1.grid(row=1, column=0, sticky='w', padx=10)

        total_amount_label2 = tk.Label(x_box, text=f"RM{total_amount}", font=("Lato", 14), fg='black', bg='white')
        total_amount_label2.grid(row=1, column=1, sticky='w', padx=10)

        selected_date_label1 = tk.Label(x_box, text="Date:", font=("Lato", 14), fg='black', bg='white', anchor='w')
        selected_date_label1.grid(row=2, column=0, sticky='w', padx=10)

        selected_date = self.date_calendar.get_date()  # Get the selected date as a string

        selected_date_label2 = tk.Label(x_box, text=self.date_calendar.get_date(), font=("Lato", 14), fg='black', bg='white')
        selected_date_label2.grid(row=2, column=1, sticky='w', padx=10)

        total_people_label1 = tk.Label(x_box, text="Total People:", font=("Lato", 14), fg='black', bg='white',
                                       anchor='w')
        total_people_label1.grid(row=3, column=0, sticky='w', padx=10)

        total_people_label2 = tk.Label(x_box, text=ticket_count.get(), font=("Lato", 14), fg='black', bg='white')
        total_people_label2.grid(row=3, column=1, sticky='w', padx=10)

        blank_label = tk.Label(details_frame, bg='white')
        blank_label.pack(fill='x')

        # Create a Y box (image on the left and input boxes on the right)
        y_box = tk.Frame(details_frame, bg='white', padx=20, bd=1, relief="solid")
        y_box.pack(fill='x', anchor='center')
        y_info_box2 = tk.Frame(y_box, bg='white')
        y_info_box2.pack(side="left")
        y_info_box3 = tk.Frame(y_box, bg='white', pady=20)
        y_info_box3.pack(side="right")

        # Create a label for the image
        card_image = get_image_data(5)
        card_image = Image.open(card_image)
        card_image = card_image.resize((290, 190))
        card_image = ImageTk.PhotoImage(card_image)

        card_image_label = tk.Label(y_info_box2, image=card_image, bg='white')
        card_image_label.image = card_image
        card_image_label.grid(row=0, column=0, sticky='w', padx=10)

        # Create labels and entry widgets for user input
        input_labels = ["Name:", "Email:", "Phone Number:", "Card Number:", "Cardholder Name:", "Date (MM/YY)", "CCV"]
        entry_widgets = []

        for i, label_text in enumerate(input_labels):
            label = tk.Label(y_info_box3, text=label_text, font=("Lato", 14), fg='black', bg='white', anchor='w')
            label.grid(row=i, column=1, sticky='w', padx=10)
            entry = tk.Entry(y_info_box3, font=("Lato", 14))
            entry.grid(row=i, column=2, sticky='w', padx=10)
            entry_widgets.append(entry)

        # Create a "Confirm Payment" button (initially disabled)
        confirm_button = ttk.Button(y_info_box3, text="Confirm Payment", style='TButton',
                                    command=lambda: self.confirm_payment(entry_widgets, attraction_id, ticket_count, total_amount,selected_date))
        confirm_button.grid(row=len(input_labels), columnspan=3, pady=10)
        confirm_button.config(state="disabled")  # Disable the button initially

        for entry in entry_widgets:
            entry.bind("<KeyRelease>", lambda event, confirm_button=confirm_button: self.validate_entries(entry_widgets,
                                                                                                          confirm_button))

        # Create a button to go back to the open_activity_ticket_page
        back_button = ttk.Button(details_frame, text="Back",
                                 command=lambda: self.open_activity_ticket_page(activity, image_path), style='TButton')
        back_button.pack(pady=10)

    def validate_entries(self, entry_widgets, confirm_button):
        # Check if all required fields are filled
        # Validate user input
        name = entry_widgets[0].get().strip().upper()  # Convert to uppercase
        email = entry_widgets[1].get().strip()
        phone_number = entry_widgets[2].get().strip()
        card_number = entry_widgets[3].get().strip()
        cardholder_name = entry_widgets[4].get().strip().upper()  # Convert to uppercase
        date = entry_widgets[5].get().strip()
        ccv = entry_widgets[6].get().strip()

        if all([name, email, phone_number, card_number, cardholder_name, date, ccv]):
            confirm_button.config(state="active")  # Enable the button
        else:
            confirm_button.config(state="disabled")  # Disable the button

    def confirm_payment(self, entry_widgets, attraction_id, ticket_count, total_amount,selected_date):
        name = entry_widgets[0].get()
        email = entry_widgets[1].get()

        # Use the formatted phone number and card number
        phone_number = ''.join(filter(str.isdigit, entry_widgets[2].get()))
        card_number = ''.join(filter(str.isdigit, entry_widgets[3].get()))

        cardholder_name = entry_widgets[4].get()
        date = entry_widgets[5].get()
        ccv = entry_widgets[6].get().strip()

        # Define regular expressions for validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
        phone_pattern = r'^\d{10}$'  # Adjusted for formatted phone number (e.g., 123-456-7890)
        card_number_pattern = r'^\d{16}$'
        date_pattern = r'^\d{2}/\d{2}$'
        ccv_pattern = r'^\d{3}$'

        # Ensure that required fields are not empty and that date is in MM/YY format
        if not name:
            self.show_error_message("Error", "Please provide a name.")
        elif not re.match("^[A-Za-z]+( [A-Za-z]+)*$", name):
            self.show_error_message("Error", "Name must contain only alphabetic characters.")
        elif not email or not re.match(email_pattern, email):
            self.show_error_message("Error", "Please provide a valid email address.")
        elif not phone_number or not re.match(phone_pattern, phone_number):
            self.show_error_message("Error", "Please provide a valid phone number in the format: 123-456-7890.")
        elif not card_number or not re.match(card_number_pattern, card_number):
            self.show_error_message("Error", "Please provide a valid 16-digit card number.")
        elif not cardholder_name:
            self.show_error_message("Error", "Please provide the cardholder's name.")
        elif not re.match("^[A-Za-z]+( [A-Za-z]+)*$", cardholder_name):
            self.show_error_message("Error", "Cardholder name must contain only alphabetic characters.")
        elif not date or not re.match(date_pattern, date):
            self.show_error_message("Error", "Invalid date format. Please use MM/YY.")
        elif not ccv or not re.match(ccv_pattern, ccv):
            self.show_error_message("Error", "Please provide a valid CCV (3 digits).")
        else:
            # Send email
            print("Before send_payment_confirmation_email:", [entry.get() for entry in entry_widgets])
            self.send_payment_confirmation_email(entry_widgets, attraction_id, ticket_count, total_amount, selected_date)
            print("After send_payment_confirmation_email:", [entry.get() for entry in entry_widgets])

            # Reset the whole page
            self.clear_content_frame()
            # Reset the vertical scrollbar to the top
            self.canvas.yview_moveto(0)

            details_frame = tk.Frame(self.content_frame, bg='white', padx=570, pady=200)
            details_frame.pack(fill='x', anchor='center')

            # Create a centered box (Frame) with a shadow effect
            center_box = tk.Frame(details_frame, bg='white', padx=20, pady=20, )
            center_box.pack(fill='x')

            success_image = get_image_data(88)
            success_image = Image.open(success_image)
            success_image = success_image.resize((140, 100))
            success_image = ImageTk.PhotoImage(success_image)

            # Create a label to display the resized image
            success_image_label = tk.Label(center_box, image=success_image, bg='white')
            success_image_label.image = success_image
            success_image_label.pack()

            # Text under the image
            text_label = tk.Label(center_box, text="Payment Successful!", font=("Lato", 20), fg='Black', bg='white')
            text_label.pack()

    def send_payment_confirmation_email(self, entry_widgets, attraction_id, ticket_count, total_amount,selected_date):
        name = entry_widgets[0].get()
        email = entry_widgets[1].get()
        phone_number = ''.join(filter(str.isdigit, entry_widgets[2].get()))
        card_number = ''.join(filter(str.isdigit, entry_widgets[3].get()))
        cardholder_name = entry_widgets[4].get()
        date = entry_widgets[5].get()
        ccv = entry_widgets[6].get().strip()

        # Generate a random order ID (ensure it's unique)
        while True:
            order_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            with sqlite3.connect('TRAVEL KIOSK.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM TICKET WHERE TICKET_ID = ?", (order_id,))
                if cursor.fetchone()[0] == 0:
                    break

        smtp_port = 587  # Standard secure SMTP port
        smtp_server = "smtp.gmail.com"  # Google SMTP Server
        email_from = "zixin2040@gmail.com"
        pswd = "kwqj qfeo aniu yzzk"  # Replace with a secure way to store your password
        subject = "Payment Confirmation"

        try:
            # Attempt to parse the selected date with the expected format 'dd/mm/yyyy'
            selected_date_formatted = datetime.datetime.strptime(selected_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError as e:
            print(f"Error parsing selected_date: {e}")
            # Handle the case when the date format doesn't match the expected format

        try:
            # Connect to the SQLite database using a context manager
            with sqlite3.connect('TRAVEL KIOSK.db') as conn:
                cursor = conn.cursor()

                # Insert payment information into the 'Payments' table
                insert_payment_query = """
                    INSERT INTO Payments (user_id, payment_name, email, phone_number, card_number, cardholder_name, expiry_date, ccv)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """

                # Execute the query with user_id and payment_info values
                cursor.execute(insert_payment_query, (self.user_id, name, email, phone_number, card_number,
                                                      cardholder_name, date, ccv))

                # Save the order ID to the TICKET entity
                ticket_insert_query = """
                    INSERT INTO TICKET (TICKET_ID, USER_ID, ATTRACTION_ID, QUANTITY, PURCHASE_DATE, TOTAL_PRICE, VALID_DATE)
                    VALUES (?, ?, ?, ?, CURRENT_DATE, ?, ?)
                """

                # Assuming you have the attraction_id and ticket_count values available
                cursor.execute(ticket_insert_query,
                               (order_id, self.user_id, attraction_id, int(ticket_count.get()), total_amount, selected_date_formatted))

                # Commit the changes to the database
                conn.commit()

            body = f"Thank you for your payment! Your order ID is: {order_id}"

            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = email
            msg['Subject'] = subject

            # Attach the body of the message
            msg.attach(MIMEText(body, 'plain'))

            filename = get_image_data(87)  # Assuming get_image_data returns a BytesIO object
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload(filename.read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', f"attachment; filename=image_filename.jpg")
            msg.attach(attachment_package)

            # Cast as string
            text = msg.as_string()

            TIE_server = smtplib.SMTP(smtp_server, smtp_port)
            TIE_server.starttls()
            TIE_server.login(email_from, pswd)

            print(f"Sending email to: {email}...")
            TIE_server.sendmail(email_from, email, text)
            print(f"Email sent to: {email}")

            TIE_server.quit()
        except Exception as e:
            print(f"Error sending email: {e}")

    def show_error_message(self, title, message):
        # You can implement a message box to show the error message
        # Here's a simple example using the tkinter messagebox:
        messagebox.showerror(title, message)

    def show_large_image(self, event):
        # Create a pop-up window to display the large image
        large_image_window = tk.Toplevel(self.root)
        large_image_window.title("Map Penang")

        # Resize the original image for the pop-up window
        large_image = get_image_data(23)
        large_image = Image.open(large_image)
        large_image = large_image.resize((950, 700))  # Adjust the size as needed
        large_image = ImageTk.PhotoImage(large_image)

        # Display the resized image in the pop-up window
        large_image_label = tk.Label(large_image_window, image=large_image)
        large_image_label.image = large_image
        large_image_label.pack()

    def explore_north(self):
        # Reset the whole page
        self.clear_content_frame()

        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the destination page content
        destination_label = tk.Label(self.content_frame, text="Explore Destination Page", font=("Lato", 20),
                                     fg='Black', bg='white', padx=340)
        destination_label.pack(fill='x')

        blank_label = tk.Label(self.content_frame, bg='white')
        blank_label.pack(fill='x')

        explore_bar = tk.Frame(self.content_frame, bg='white', padx=340)
        explore_bar.pack(fill='x')

        # Create a label with a specified background color
        explore_bar_label1 = tk.Frame(explore_bar, bg='white', height=1, bd=1, relief="solid")
        explore_bar_label1.pack(fill='x', side='left')

        # Create a label with a specified background color
        explore_bar_label2 = tk.Frame(explore_bar, bg='white', height=1, bd=1, relief="solid")
        explore_bar_label2.pack(fill='x', side='right')

        # Create "North" button (same as in open_explore_page)
        north_button = ttk.Button(explore_bar_label1, text="North", command=self.explore_north, style='TButton')
        north_button.pack(padx=160, pady=5)

        # Create "South" button (same as in open_explore_page)
        south_button = ttk.Button(explore_bar_label2, text="South", command=self.explore_south, style='TButton')
        south_button.pack(padx=160, pady=5)

        blank_label = tk.Label(self.content_frame, bg='white')
        blank_label.pack(fill='x')

        # Function to handle the "North" button click
        # Create a title label for "North"
        north_name_label = tk.Label(self.content_frame, text="   Northeast Penang Island", font=("Lato", 20),
                                    fg='Black', bg='white', padx=340)
        north_name_label.pack(fill='x')

        north_label2 = tk.Frame(self.content_frame, bg='white')
        north_label2.pack(fill='x')
        north_label = tk.Frame(north_label2, bg='white')
        north_label.pack(fill='x', padx=230)
        north_label1 = tk.Frame(north_label, bg='white')
        north_label1.pack(fill='x')

        # Create a new frame for attractions
        north_attractions_frame = tk.Frame(self.content_frame, bg='white')
        north_attractions_frame.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        selected_attraction_ids = (1, 6, 7, 8, 9, 10)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT a.ATTRACTION_NAME, i.IMAGE_DATA
        FROM ATTRACTION a
        JOIN IMAGES i ON a.ATTRACTION_ID = i.IMAGE_RELATED_ID
        WHERE a.ATTRACTION_ID IN {selected_attraction_ids} and i.IMAGE_TYPE = "Attraction" and i.IMAGE_NAME like "%1"
        """
        cursor.execute(query)

        # Fetch the query result
        activities = [
            {"name": row[0], "image_data": row[1]}
            for row in cursor.fetchall()
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Create a BytesIO object from the binary image data
            image_data_io = BytesIO(activity["image_data"])

            # Load the image from the BytesIO object
            north_image1 = Image.open(image_data_io)

            # Resize the image
            north_image1 = north_image1.resize((240, 170))

            # If you want to display the image in Tkinter, you should convert it to PhotoImage
            north_image1 = ImageTk.PhotoImage(north_image1)

            # Create a frame for each item
            north_frame1 = tk.Frame(north_label1, bg='white', bd=1, relief="solid")
            north_frame1.grid(row=i // 3, column=i % 3, padx=40, pady=20)

            # Create the north image label inside the frame
            north_image_label1 = tk.Label(north_frame1, image=north_image1)
            north_image_label1.image = north_image1
            north_image_label1.pack()

            # Create a frame to hold both labels and the button vertically
            north_info_frame1 = tk.Frame(north_frame1, bg='white')  # No need for a border here
            north_info_frame1.pack(fill='x', expand=True)

            # Create north_info1 inside the info frame
            north_info1 = tk.Label(north_info_frame1, text=f"    {activity['name']}", font=("Lato", 12), fg='Black',
                                   bg='white', anchor='w', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            north_info1.pack(fill='x', expand=True)

            # Create the north button inside the frame and open the destination page on click
            north_info_button1 = ttk.Button(north_frame1, text="Details",
                                            command=lambda a=activity: self.open_north_details_page(a), style='TButton')
            north_info_button1.pack(fill='x', expand=True)
            self.buttons.append(north_info_button1)

    def open_north_details_page(self, activity):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"Details for {activity['name']}", font=("Lato", 20),
                                 fg='Black', bg='white', anchor='w', padx=215)
        details_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')
        cursor = conn.cursor()

        # Execute a query to retrieve details for the specific attraction and its images
        query = """
            SELECT a.ATTRACTION_NAME, a.ATTRACTION_DETAILS, a.ATTRACTION_LOCATION, a.OPERATING_HOURS, i.IMAGE_DATA
            FROM ATTRACTION a
            JOIN IMAGES i ON a.ATTRACTION_ID = i.IMAGE_RELATED_ID
            WHERE a.ATTRACTION_NAME = ? and i.IMAGE_TYPE = "Attraction" and i.IMAGE_NAME like "%2"
            """
        cursor.execute(query, (activity['name'],))  # Provide the attraction name as a tuple

        # Extract details for the attraction
        result = cursor.fetchone()
        if result:
            name, details, location, operating_hours, image_data = result

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            # Create a new frame for the attraction's details
            details_frame = tk.Frame(self.content_frame, bg='white')
            details_frame.pack(fill='x')

            image_data_io = BytesIO(image_data)
            activity_image = Image.open(image_data_io)
            activity_image = activity_image.resize((950, 240))
            activity_image = ImageTk.PhotoImage(activity_image)

            # Create the activity image label on the details page
            activity_image_label = tk.Label(details_frame, image=activity_image)
            activity_image_label.image = activity_image
            activity_image_label.pack(side='top', padx=250)

            blank_label = tk.Label(details_frame, bg='white')
            blank_label.pack(fill='x')

            # Create a frame for information
            info_frame = tk.Frame(details_frame, bg='white', bd=1, relief="solid", width=600, height=200)
            info_frame.pack(padx=20)
            info_frame1 = tk.Frame(info_frame, bg='white', )
            info_frame1.pack(padx=20, side='left')
            info_frame2 = tk.Frame(info_frame1, bg='white', )
            info_frame2.pack(padx=20, side='bottom')

            # Replace the if-else block with a direct assignment
            name_text = f"About {name}"

            # Set the text for the labels
            info_text = f"{details}\n\n\u27A4 {location}\n\nOperating Hours: {operating_hours}"
            name_label = tk.Label(info_frame1, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            name_label.pack(fill='both', expand=True, padx=25, pady=10)
            info_label = tk.Label(info_frame2, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            info_label.pack(fill='both', expand=True, padx=25, pady=10)

            back_button = ttk.Button(details_frame, text="Back", command=self.explore_north, style='TButton')
            back_button.pack(side='top', anchor='nw', padx=740, pady=20)
        else:
            # Handle the case where the attraction with the specified ID is not found
            cursor.close()
            conn.close()

    def explore_south(self):
        # Reset the hole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the destination page content
        destination_label = tk.Label(self.content_frame, text="Explore Destination Page", font=("Lato", 20),
                                     fg='Black', bg='white', padx=340)
        destination_label.pack(fill='x')

        blank_label = tk.Label(self.content_frame, bg='white')
        blank_label.pack(fill='x')

        explore_bar = tk.Frame(self.content_frame, bg='white', padx=340)
        explore_bar.pack(fill='x')

        # Create a label with a specified background color
        explore_bar_label1 = tk.Frame(explore_bar, bg='white', height=1, bd=1, relief="solid")
        explore_bar_label1.pack(fill='x', side='left')

        # Create a label with a specified background color
        explore_bar_label2 = tk.Frame(explore_bar, bg='white', height=1, bd=1, relief="solid")
        explore_bar_label2.pack(fill='x', side='right')

        # Create "North" button (same as in open_explore_page)
        north_button = ttk.Button(explore_bar_label1, text="North", command=self.explore_north, style='TButton')
        north_button.pack(padx=160, pady=5)

        # Create "South" button (same as in open_explore_page)
        south_button = ttk.Button(explore_bar_label2, text="South", command=self.explore_south, style='TButton')
        south_button.pack(padx=160, pady=5)

        blank_label = tk.Label(self.content_frame, bg='white')
        blank_label.pack(fill='x')

        # Function to handle the "South" button click
        # Create a title label for "South"
        south_name_label = tk.Label(self.content_frame, text="   Southeast Penang Island", font=("Lato", 20),
                                    fg='Black', bg='white')  # Use 'w' (west) for left alignment
        south_name_label.pack(fill='x')

        south_label2 = tk.Frame(self.content_frame, bg='white')
        south_label2.pack(fill='x')
        south_label = tk.Frame(south_label2, bg='white')
        south_label.pack(fill='x', padx=230)
        south_label1 = tk.Frame(south_label, bg='white')
        south_label1.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        selected_attraction_ids = (2, 4, 11, 12, 13, 14)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT a.ATTRACTION_NAME, i.IMAGE_DATA
        FROM ATTRACTION a
        JOIN IMAGES i ON a.ATTRACTION_ID = i.IMAGE_RELATED_ID
        WHERE a.ATTRACTION_ID IN {selected_attraction_ids} and i.IMAGE_TYPE = "Attraction" and i.IMAGE_NAME like "%1"
        """
        cursor.execute(query)

        # Fetch the query result
        activities = [
            {"name": row[0], "image_data": row[1]}
            for row in cursor.fetchall()
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Create a BytesIO object from the binary image data
            image_data_io = BytesIO(activity["image_data"])

            # Load the image from the BytesIO object
            south_image1 = Image.open(image_data_io)

            # Resize the image
            south_image1 = south_image1.resize((240, 170))

            # If you want to display the image in Tkinter, you should convert it to PhotoImage
            south_image1 = ImageTk.PhotoImage(south_image1)

            # Create a frame for each item
            south_frame1 = tk.Frame(south_label1, bg='white', bd=1, relief="solid")  # Frame of the south boxes
            south_frame1.grid(row=i // 3, column=i % 3, padx=40, pady=20)  # Use grid to organize in rows and columns

            # Create the south image label inside the frame
            south_image_label1 = tk.Label(south_frame1, image=south_image1)
            south_image_label1.image = south_image1
            south_image_label1.pack()

            # Create a frame to hold both labels and the button vertically
            south_info_frame1 = tk.Frame(south_frame1, bg='white')  # No need for a border here
            south_info_frame1.pack(fill='x', expand=True)

            # Create south_info1 inside the info frame
            south_info1 = tk.Label(south_info_frame1, text=f"    {activity['name']}", font=("Lato", 12), fg='Black',
                                   bg='white', anchor='w', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            south_info1.pack(fill='x', expand=True)

            # Create the south button inside the frame and open the destination page on click
            south_info_button1 = ttk.Button(south_frame1, text="Details",
                                            command=lambda a=activity: self.open_south_details_page(a), style='TButton')
            south_info_button1.pack(fill='x', expand=True)
            self.buttons.append(south_info_button1)

    def open_south_details_page(self, activity):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"     Details for {activity['name']}", font=("Lato", 20),
                                 fg='Black', bg='white', anchor='w', padx=213)
        details_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')
        cursor = conn.cursor()

        # Execute a query to retrieve details for the specific attraction and its images
        query = """
            SELECT a.ATTRACTION_NAME, a.ATTRACTION_DETAILS, a.ATTRACTION_LOCATION, a.OPERATING_HOURS, i.IMAGE_DATA
            FROM ATTRACTION a
            JOIN IMAGES i ON a.ATTRACTION_ID = i.IMAGE_RELATED_ID
            WHERE a.ATTRACTION_NAME = ? and i.IMAGE_TYPE = "Attraction" and i.IMAGE_NAME like "%2"
            """
        cursor.execute(query, (activity['name'],))  # Provide the attraction name as a tuple

        # Extract details for the attraction
        result = cursor.fetchone()
        if result:
            name, details, location, operating_hours, image_data = result

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            # Create a new frame for the attraction's details
            details_frame = tk.Frame(self.content_frame, bg='white')
            details_frame.pack(fill='x')

            image_data_io = BytesIO(image_data)
            activity_image = Image.open(image_data_io)
            activity_image = activity_image.resize((950, 240))
            activity_image = ImageTk.PhotoImage(activity_image)

            # Create the activity image label on the details page
            activity_image_label = tk.Label(details_frame, image=activity_image)
            activity_image_label.image = activity_image
            activity_image_label.pack(side='top', padx=250)

            blank_label = tk.Label(details_frame, bg='white')
            blank_label.pack(fill='x')

            info_frame = tk.Frame(details_frame, bg='white', bd=1, relief="solid", width=600, height=200)
            info_frame.pack(padx=20)

            # Replace the if-else block with a direct assignment
            name_text = f"About {name}"

            # Set the text for the labels
            info_text = f"{details}\n\n\u27A4 {location}\n\nOperating Hours: {operating_hours}"
            name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            name_label.pack(fill='both', expand=True, padx=25, pady=10)
            info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            info_label.pack(fill='both', expand=True, padx=25, pady=10)

            # Create a button to go back to the explore_south page
            back_button = ttk.Button(details_frame, text="Back", command=self.explore_south, style='TButton')
            back_button.pack(pady=20)
        else:
            # Handle the case where the attraction with the specified ID is not found
            cursor.close()
            conn.close()

    def food_page(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a title label for Shopping Malls
        food_name_label = tk.Label(self.content_frame, text="   Food", font=("Lato", 18),
                                   fg='Black', bg='white', anchor='w', padx=240, pady=20)
        food_name_label.pack(fill='x')

        food_label2 = tk.Frame(self.content_frame, bg='white')
        food_label2.pack(fill='x')
        food_label = tk.Frame(food_label2, bg='white')
        food_label.pack(fill='x', padx=230)
        food_label1 = tk.Frame(food_label, bg='white')
        food_label1.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        selected_food_ids = (2, 3, 4, 5, 1, 6)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT a.SAD_NAME, i.IMAGE_DATA
        FROM ShoppingAndDining a
        JOIN IMAGES i ON a.SAD_ID = i.IMAGE_RELATED_ID
        WHERE a.SAD_ID IN {selected_food_ids} and i.IMAGE_TYPE = "SAD-Food" and i.IMAGE_NAME like "%1"
        """
        cursor.execute(query)

        # Fetch the query result
        activities = [
            {"name": row[0], "image_data": row[1]}
            for row in cursor.fetchall()
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Create a BytesIO object from the binary image data
            image_data_io = BytesIO(activity["image_data"])

            # Load the image from the BytesIO object
            food_image = Image.open(image_data_io)
            food_image = food_image.resize((240, 170))  # Adjust the size as needed
            food_image = ImageTk.PhotoImage(food_image)

            # Create a frame to hold both the image and information labels with an outline
            food_frame = tk.Frame(food_label1, bg='white', bd=1, relief="solid")
            food_frame.grid(row=i // 3, column=i % 3, padx=40, pady=20)

            # Create the food image label inside the frame
            food_image_label = tk.Label(food_frame, image=food_image)
            food_image_label.image = food_image
            food_image_label.pack()

            # Create a frame to hold both labels and the button vertically
            food_info_frame1 = tk.Frame(food_frame, bg='white')  # No need for a border here
            food_info_frame1.pack(fill='x', expand=True)

            # Create north_info1 inside the info frame
            food_info1 = tk.Label(food_info_frame1, text=f" {activity['name']}", font=("Lato", 12), fg='Black',
                                  bg='white', anchor='w', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            food_info1.pack(fill='x', expand=True)

            # Create the shopping button inside the frame and open the destination page on click
            food_button = ttk.Button(food_frame, text="Details",
                                     command=lambda a=activity: self.open_food_page(a),
                                     style='TButton')
            food_button.pack(fill='x', expand=True)

    def open_food_page(self, activity):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"Details for {activity['name']}", font=("Lato", 20),
                                 fg='Black', bg='white', anchor='w', padx=215)
        details_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')
        cursor = conn.cursor()

        # Execute a query to retrieve details for the specific attraction and its images
        query = """
            SELECT a.SAD_NAME, a.SAD_DETAILS, a.SAD_LOCATION, a.SAD_OPERATINGHOURS, i.IMAGE_DATA
            FROM ShoppingAndDining a
            JOIN IMAGES i ON a.SAD_ID = i.IMAGE_RELATED_ID
            WHERE a.SAD_NAME = ? and i.IMAGE_TYPE = "SAD-Food" and i.IMAGE_NAME like "%2"
            """
        cursor.execute(query, (activity['name'],))  # Provide the attraction name as a tuple

        # Extract details for the attraction
        result = cursor.fetchone()
        activities = [
            {"name": row[0], "image_data": row[4]}
            for row in cursor.fetchall()
        ]

        if result:
            name, details, location, operating_hours, image_data = result

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            # Create a new frame for each attraction's details
            details_frame = tk.Frame(self.content_frame, bg='white')
            details_frame.pack(fill='x')

            image_data_io = BytesIO(image_data)
            food_image = Image.open(image_data_io)
            food_image = food_image.resize((950, 240))
            food_image = ImageTk.PhotoImage(food_image)

            # Create the activity image label on the details page
            food_image_label = tk.Label(details_frame, image=food_image)
            food_image_label.image = food_image
            food_image_label.pack(side='top', padx=250)

            blank_label = tk.Label(details_frame, bg='white')
            blank_label.pack(fill='x')

            # Create a frame for information
            info_frame = tk.Frame(details_frame, bg='white', bd=1, relief="solid", width=600, height=200)
            info_frame.pack(padx=20)
            info_frame1 = tk.Frame(info_frame, bg='white', )
            info_frame1.pack(padx=20, side='left')
            info_frame2 = tk.Frame(info_frame1, bg='white', )
            info_frame2.pack(padx=20, side='bottom')

            # Replace the if-else block with a direct assignment
            name_text = f"About {name}"

            # Set the text for the labels
            info_text = f"{details}\n\n\u27A4 {location}\n\nOperating Hours: {operating_hours}"
            name_label = tk.Label(info_frame1, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            name_label.pack(fill='both', expand=True, padx=25, pady=10)
            info_label = tk.Label(info_frame2, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            info_label.pack(fill='both', expand=True, padx=25, pady=10)

            back_button = ttk.Button(details_frame, text="Back", command=self.food_page, style='TButton')
            back_button.pack(pady=20)
        else:
            # Handle the case where the attraction with the specified name is not found
            cursor.close()
            conn.close()

            back_button = ttk.Button(self.content_frame, text="Back", command=self.food_page, style='TButton')
            back_button.pack(side='top', anchor='nw', padx=740, pady=20)

    def shopping_page(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a title label for Shopping Malls
        shopping_label = tk.Label(self.content_frame, text="   Shopping Malls", font=("Lato", 18),
                                  fg='Black', bg='white', anchor='w', padx=240, pady=20)
        shopping_label.pack(fill='x')

        shopping_label2 = tk.Frame(self.content_frame, bg='white')
        shopping_label2.pack(fill='x')
        shopping_label = tk.Frame(shopping_label2, bg='white')
        shopping_label.pack(fill='x', padx=230)
        shopping_label1 = tk.Frame(shopping_label, bg='white')
        shopping_label1.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        selected_mall_ids = (12, 13, 14, 15, 16, 17)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT a.SAD_NAME, i.IMAGE_DATA
        FROM ShoppingAndDining a
        JOIN IMAGES i ON a.SAD_ID = i.IMAGE_RELATED_ID
        WHERE a.SAD_ID IN {selected_mall_ids} and i.IMAGE_TYPE = "SAD-Mall" and i.IMAGE_NAME like "%1"
        """
        cursor.execute(query)

        # Fetch the query result
        activities = [
            {"name": row[0], "image_data": row[1]}
            for row in cursor.fetchall()
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the shopping image
            # Create a BytesIO object from the binary image data
            image_data_io = BytesIO(activity["image_data"])

            # Load the image from the BytesIO object
            shopping_image = Image.open(image_data_io)
            shopping_image = shopping_image.resize((240, 170))  # Adjust the size as needed
            shopping_image = ImageTk.PhotoImage(shopping_image)

            # Create a frame to hold both the image and information labels with an outline
            shopping_frame = tk.Frame(shopping_label1, bg='white', bd=1, relief="solid")
            shopping_frame.grid(row=i // 3, column=i % 3, padx=40, pady=20)

            # Create the shopping image label inside the frame
            shopping_image_label = tk.Label(shopping_frame, image=shopping_image)
            shopping_image_label.image = shopping_image
            shopping_image_label.pack()

            # Create a frame to hold both labels and the button vertically
            shop_info_frame1 = tk.Frame(shopping_frame, bg='white')  # No need for a border here
            shop_info_frame1.pack(fill='x', expand=True)

            # Create south_info1 inside the info frame
            shop_info1 = tk.Label(shop_info_frame1, text=f"    {activity['name']}", font=("Lato", 12), fg='Black',
                                  bg='white', anchor='w', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            shop_info1.pack(fill='x', expand=True)

            # Create the shopping button inside the frame and open the destination page on click
            shopping_button = ttk.Button(shopping_frame, text="Details",
                                         command=lambda a=activity: self.open_shopping_details_page(a),
                                         style='TButton')
            shopping_button.pack(fill='x', expand=True)
            self.buttons.append(shopping_button)
    def open_shopping_details_page(self, activity):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"Details for {activity['name']}", font=("Lato", 20),
                                 fg='Black', bg='white', anchor='w', padx=215)
        details_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')
        cursor = conn.cursor()

        # Execute a query to retrieve details for the specific attraction and its images
        query = """
            SELECT a.SAD_NAME, a.SAD_DETAILS, a.SAD_LOCATION, a.SAD_OPERATINGHOURS, i.IMAGE_DATA
            FROM ShoppingAndDining a
            JOIN IMAGES i ON a.SAD_ID = i.IMAGE_RELATED_ID
            WHERE a.SAD_NAME = ? and i.IMAGE_TYPE = "SAD-Mall" and i.IMAGE_NAME like "%2"
            """
        cursor.execute(query, (activity['name'],))  # Provide the attraction name as a tuple

        # Extract details for the attraction
        result = cursor.fetchone()
        activities = [
            {"name": row[0], "image_data": row[4]}
            for row in cursor.fetchall()
        ]

        if result:
            name, details, location, operating_hours, image_data = result

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            # Create a new frame for each attraction's details
            details_frame = tk.Frame(self.content_frame, bg='white')
            details_frame.pack(fill='x')

            image_data_io = BytesIO(image_data)
            shopping_image = Image.open(image_data_io)
            shopping_image = shopping_image.resize((950, 240))
            shopping_image = ImageTk.PhotoImage(shopping_image)

            # Create the activity image label on the details page
            shopping_image_label = tk.Label(details_frame, image=shopping_image)
            shopping_image_label.image = shopping_image
            shopping_image_label.pack(side='top', padx=250)

            blank_label = tk.Label(details_frame, bg='white')
            blank_label.pack(fill='x')

            # Create a frame for information
            info_frame = tk.Frame(details_frame, bg='white', bd=1, relief="solid", width=600, height=200)
            info_frame.pack(padx=20)
            info_frame1 = tk.Frame(info_frame, bg='white', )
            info_frame1.pack(padx=20, side='left')
            info_frame2 = tk.Frame(info_frame1, bg='white', )
            info_frame2.pack(padx=20, side='bottom')

            # Replace the if-else block with a direct assignment
            name_text = f"About {name}"

            # Set the text for the labels
            info_text = f"{details}\n\n\u27A4 {location}\n\nOperating Hours: {operating_hours}"
            name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            name_label.pack(fill='both', expand=True, padx=25, pady=10)
            info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            info_label.pack(fill='both', expand=True, padx=25, pady=10)

            back_button = ttk.Button(details_frame, text="Back", command=self.shopping_page, style='TButton')
            back_button.pack(pady=20)
        else:
            # Handle the case where the attraction with the specified name is not found
            cursor.close()
            conn.close()

    def market_page(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a title label for "Market Everyday"
        market_label = tk.Label(self.content_frame, text="Market Everyday", font=("Lato", 18), fg='Black', bg='white',
                                anchor='w', padx=240, pady=20)
        market_label.pack(fill='x')

        market_label = tk.Label(self.content_frame, bg='white')
        market_label.pack(fill='x')

        market_label = tk.Frame(market_label, bg='white')
        market_label.pack(fill='x', padx=200)
        market_label = tk.Frame(market_label, bg='white')
        market_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        selected_market_ids1 = (7, 8, 9)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT a.SAD_NAME, i.IMAGE_DATA
        FROM ShoppingAndDining a
        JOIN IMAGES i ON a.SAD_ID = i.IMAGE_RELATED_ID
        WHERE a.SAD_ID IN {selected_market_ids1} and i.IMAGE_TYPE = "SAD-Market" and i.IMAGE_NAME like "%1"
        """
        cursor.execute(query)

        # Fetch the query result
        activities = [
            {"name": row[0], "image_data": row[1]}
            for row in cursor.fetchall()
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the shopping image
            # Create a BytesIO object from the binary image data
            image_data_io = BytesIO(activity["image_data"])

            # Load the image from the BytesIO object
            market_image = Image.open(image_data_io)
            market_image = market_image.resize((240, 170))  # Adjust the size as needed
            market_image = ImageTk.PhotoImage(market_image)

            # Create a frame to hold both the image and information labels with an outline
            market_frame = tk.Frame(market_label, bg='white', bd=1, relief="solid")
            market_frame.grid(row=i // 3, column=i % 3, padx=40, pady=20)

            # Create the shopping image label inside the frame
            market_image_label = tk.Label(market_frame, image=market_image)
            market_image_label.image = market_image
            market_image_label.pack()

            # Create a frame to hold both labels and the button vertically
            market_info_frame1 = tk.Frame(market_frame, bg='white')  # No need for a border here
            market_info_frame1.pack(fill='x', expand=True)

            # Create south_info1 inside the info frame
            market_info1 = tk.Label(market_info_frame1, text=f"    {activity['name']}", font=("Lato", 12), fg='Black',
                                    bg='white', anchor='w', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            market_info1.pack(fill='x', expand=True)

            # Create the market button inside the frame and open the destination page on click
            market_button = ttk.Button(market_frame, text="Details",
                                       command=lambda a=activity: self.open_market_details_page(a, market2),
                                       style='TButton')
            market_button.pack(fill='x', expand=True)
            self.buttons.append(market_button)

        # Create a title label for "Market on Specific Day"
        specific_day_label = tk.Label(self.content_frame, text="Market on Specific Day", font=("Lato", 18),
                                      fg='Black', bg='white', anchor='w', padx=240, pady=20)
        specific_day_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        selected_market_ids2 = (10, 11)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT a.SAD_NAME, i.IMAGE_DATA
        FROM ShoppingAndDining a
        JOIN IMAGES i ON a.SAD_ID = i.IMAGE_RELATED_ID
        WHERE a.SAD_ID IN {selected_market_ids2} and i.IMAGE_TYPE = "SAD-Market" and i.IMAGE_NAME like "%1"
        """
        cursor.execute(query)

        # Fetch the query result
        activities = [
            {"name": row[0], "image": row[1]}
            for row in cursor.fetchall()
        ]

        # Create a frame to hold the second set of markets
        second_market_frame = tk.Label(self.content_frame, bg='white')
        second_market_frame.pack(fill='x')

        second_market_frame = tk.Frame(second_market_frame, bg='white')
        second_market_frame.pack(fill='x', padx=200)
        second_market_frame = tk.Frame(second_market_frame, bg='white')
        second_market_frame.pack(fill='x')

        for i, market2 in enumerate(activities):
            # Load and resize the shopping image
            # Create a BytesIO object from the binary image data
            image_data_io = BytesIO(market2["image"])

            # Load the image from the BytesIO object
            market_image = Image.open(image_data_io)
            market_image = market_image.resize((240, 170))  # Adjust the size as needed
            market_image = ImageTk.PhotoImage(market_image)

            # Create a frame to hold both the image and information labels with an outline
            market_frame = tk.Frame(second_market_frame, bg='white', bd=1, relief="solid")
            market_frame.grid(row=i // 3, column=i % 3, padx=40, pady=20)

            # Create the market image label inside the frame
            market_image_label = tk.Label(market_frame, image=market_image)
            market_image_label.image = market_image
            market_image_label.pack()

            # Create a frame to hold both labels and the button vertically
            market_info_frame2 = tk.Frame(market_frame, bg='white')  # No need for a border here
            market_info_frame2.pack(fill='x', expand=True)

            # Create south_info1 inside the info frame
            market_info2 = tk.Label(market_info_frame2, text=f"    {market2['name']}", font=("Lato", 12), fg='Black',
                                    bg='white', anchor='w', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            market_info2.pack(fill='x', expand=True)

            # Create the market button inside the frame and open the destination page on click
            market_button = ttk.Button(market_frame, text="Details",
                                       command=lambda b=market2: self.open_market_details_page(b, market2),
                                       style='TButton')
            market_button.pack(fill='x', expand=True)
            self.buttons.append(market_button)

    def open_market_details_page(self, activity, market2):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"Details for {activity['name']}", font=("Lato", 20),
                                 fg='Black', bg='white', anchor='w', padx=215)
        details_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')
        cursor = conn.cursor()

        # Execute a query to retrieve details for the specific attraction and its images
        query = """
            SELECT a.SAD_NAME, a.SAD_DETAILS, a.SAD_LOCATION, a.SAD_OPERATINGHOURS, i.IMAGE_DATA
            FROM ShoppingAndDining a
            JOIN IMAGES i ON a.SAD_ID = i.IMAGE_RELATED_ID
            WHERE a.SAD_NAME = ? and i.IMAGE_TYPE = "SAD-Market" and i.IMAGE_NAME like "%2"
            """
        cursor.execute(query, (activity['name'],))  # Provide the attraction name as a tuple

        # Extract details for the attraction
        result = cursor.fetchone()
        activities = [
            {"name": row[0], "image_data": row[4]}
            for row in cursor.fetchall()
        ]

        if result:
            name, details, location, operating_hours, image_data = result

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            # Create a new frame for each attraction's details
            details_frame = tk.Frame(self.content_frame, bg='white')
            details_frame.pack(fill='x')

            image_data_io = BytesIO(image_data)
            market_image = Image.open(image_data_io)
            market_image = market_image.resize((950, 240))
            market_image = ImageTk.PhotoImage(market_image)

            # Create the activity image label on the details page
            market_image_label = tk.Label(details_frame, image=market_image)
            market_image_label.image = market_image
            market_image_label.pack(side='top', padx=250)

            blank_label = tk.Label(details_frame, bg='white')
            blank_label.pack(fill='x')

            # Create a frame for information
            info_frame = tk.Frame(details_frame, bg='white', bd=1, relief="solid", width=600, height=200)
            info_frame.pack(padx=20)
            info_frame1 = tk.Frame(info_frame, bg='white', )
            info_frame1.pack(padx=20, side='left')
            info_frame2 = tk.Frame(info_frame1, bg='white', )
            info_frame2.pack(padx=20, side='bottom')

            # Replace the if-else block with a direct assignment
            name_text = f"About {name}"

            # Set the text for the labels
            info_text = f"{details}\n\n\u27A4 {location}\n\nOperating Hours: {operating_hours}"
            name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            name_label.pack(fill='both', expand=True, padx=25, pady=10)
            info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            info_label.pack(fill='both', expand=True, padx=25, pady=10)

            back_button = ttk.Button(details_frame, text="Back", command=self.market_page, style='TButton')
            back_button.pack(pady=20)
        else:
            # Handle the case where the attraction with the specified name is not found
            cursor.close()
            conn.close()

    def transport_page(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a title label for Shopping Malls
        transport_label = tk.Label(self.content_frame, text="   Transport", font=("Lato", 18),
                                   fg='Black', bg='white', anchor='w', padx=240, pady=20)
        transport_label.pack(fill='x')
        transport_label = tk.Label(self.content_frame, bg='white')
        transport_label.pack(fill='x')

        transport_label2 = tk.Frame(self.content_frame, bg='white')
        transport_label2.pack(fill='x')
        transport_label = tk.Frame(transport_label, bg='white')
        transport_label.pack(fill='x', padx=230)
        transport_label1 = tk.Frame(transport_label, bg='white')
        transport_label1.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Define a tuple with the IDs of the attractions you want to select
        transport_id = (1, 2, 3, 4, 5)  # Replace with the actual IDs of the attractions you want

        # Execute a query to retrieve details for the specific attractions and their images
        query = f"""
        SELECT a.TRANSPORT_NAME, i.IMAGE_DATA
        FROM TRANSPORTATION a
        JOIN IMAGES i ON a.TRANSPORT_ID = i.IMAGE_RELATED_ID
        WHERE a.TRANSPORT_ID IN {transport_id} and i.IMAGE_TYPE = "Transport" and i.IMAGE_NAME like "%1"
        """
        cursor.execute(query)

        # Fetch the query result
        activities = [
            {"name": row[0], "image_data": row[1]}
            for row in cursor.fetchall()
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the shopping image
            # Create a BytesIO object from the binary image data
            image_data_io = BytesIO(activity["image_data"])

            # Load the image from the BytesIO object
            transport_image = Image.open(image_data_io)
            transport_image = transport_image.resize((240, 170))  # Adjust the size as needed
            transport_image = ImageTk.PhotoImage(transport_image)

            # Create a frame to hold both the image and information labels with an outline
            transport_frame = tk.Frame(transport_label1, bg='white', bd=1, relief="solid")
            transport_frame.grid(row=i // 3, column=i % 3, padx=40, pady=20)

            # Create the shopping image label inside the frame
            transport_image_label = tk.Label(transport_frame, image=transport_image)
            transport_image_label.image = transport_image
            transport_image_label.pack()

            # Create a frame to hold both labels and the button vertically
            transport_info_frame1 = tk.Frame(transport_frame, bg='white')  # No need for a border here
            transport_info_frame1.pack(fill='x', expand=True)

            # Create south_info1 inside the info frame
            transport_info1 = tk.Label(transport_info_frame1, text=f"    {activity['name']}", font=("Lato", 12),
                                       fg='Black',
                                       bg='white', anchor='w', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            transport_info1.pack(fill='x', expand=True)

            # Create the shopping button inside the frame and open the destination page on click
            transport_button = ttk.Button(transport_frame, text="Details",
                                          command=lambda a=activity: self.open_transport_details_page(a),
                                          style='TButton')
            transport_button.pack(fill='x', expand=True)
            self.buttons.append(transport_button)

    def open_transport_details_page(self, activity):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"Details for {activity['name']}", font=("Lato", 18),
                                 fg='Black', bg='white', anchor='w', padx=215, pady=10)
        details_label.pack(fill='x')

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVEL KIOSK.db')
        cursor = conn.cursor()

        # Execute a query to retrieve details for the specific attraction and its images
        query = """
            SELECT a.TRANSPORT_NAME, a.TRANSPORT_DETAILS, a.TRANSPORT_LOCATION, a.TRANSPORT_PRICE, i.IMAGE_DATA
            FROM TRANSPORTATION a
            JOIN IMAGES i ON a.TRANSPORT_ID = i.IMAGE_RELATED_ID
            WHERE a.TRANSPORT_NAME = ? and i.IMAGE_TYPE = "Transport" and i.IMAGE_NAME like "%2"
            """
        cursor.execute(query, (activity['name'],))  # Provide the attraction name as a tuple

        # Extract details for the attraction
        result = cursor.fetchone()
        activities = [
            {"name": row[0], "image_data": row[4]}
            for row in cursor.fetchall()
        ]

        if result:
            name, details, location, price, image_data = result

            # Close the cursor and the connection
            cursor.close()
            conn.close()

            # Create a new frame for each attraction's details
            details_frame = tk.Frame(self.content_frame, bg='white')
            details_frame.pack(fill='x')

            image_data_io = BytesIO(image_data)
            transport_image = Image.open(image_data_io)
            transport_image = transport_image.resize((950, 240))
            transport_image = ImageTk.PhotoImage(transport_image)

            # Create the activity image label on the details page
            transport_image_label = tk.Label(details_frame, image=transport_image)
            transport_image_label.image = transport_image
            transport_image_label.pack(side='top', padx=250)

            blank_label = tk.Label(details_frame, bg='white')
            blank_label.pack(fill='x')

            # Create a frame for information
            info_frame = tk.Frame(details_frame, bg='white', bd=1, relief="solid", width=600, height=200)
            info_frame.pack(padx=20)

            # Replace the if-else block with a direct assignment
            name_text = f"About {name}"

            # Set the text for the labels
            info_text = f"{details}\n\n\u27A4 Location: {location}\n\n\u27A4 Pricing:   {price}"
            name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            name_label.pack(fill='both', expand=True, padx=25, pady=10)
            info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                                  justify='left', wraplength=900)
            info_label.pack(fill='both', expand=True, padx=25, pady=10)

            # Create a button to go back to the shopping malls page
            back_button = ttk.Button(details_frame, text="Back", command=self.transport_page, style='TButton')
            back_button.pack(pady=20)

    def open_account(self):
        self.clear_content_frame()
        self.canvas.yview_moveto(0)

        # Create a label or other widgets to display profile information
        account_label = tk.Label(self.content_frame, text="Account", font=("Lato", 18), fg='Black', bg='white',
                                 anchor='w', padx=240, pady=20)
        account_label.pack(fill='x')
        account_label = tk.Label(self.content_frame, bg='white')
        account_label.pack(fill='x')

        profile_label = tk.Label(self.content_frame, text="Profile", font=("Lato", 25), fg='black', bg='white',
                                 anchor='w', padx=240, pady=10)
        profile_label.pack(fill='x')
        profile_label = tk.Label(self.content_frame, bg='white')
        profile_label.pack(fill='x')

        profile_details_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
        profile_details_frame.pack(fill='x')

        # Load and resize the activity image for the details page
        profile_image = get_image_data(92)
        profile_image = Image.open(profile_image)
        profile_image = profile_image.resize((300, 300))
        profile_image = ImageTk.PhotoImage(profile_image)

        # Create the activity image label on the details page
        profile_image_label = tk.Label(profile_details_frame, image=profile_image)
        profile_image_label.image = profile_image
        profile_image_label.grid(row=0, column=2, padx=240, pady=20, rowspan=2)  # Adjust padx, pady as needed

        # Connect to the SQLite database
        with sqlite3.connect('TRAVEL KIOSK.db') as conn:
            cursor = conn.cursor()

            # Get user information from the USER table based on the user_id
            query = "SELECT USER_NAME, USER_EMAIL FROM USER WHERE USER_ID = ?"
            cursor.execute(query, (self.user_id,))
            user_data = cursor.fetchone()

            # Check if user_data is not None
            if user_data:
                user_name, user_email = user_data

                # Example user information (replace with actual user data)
                user_name_label = tk.Label(profile_details_frame, text=f"Username: {user_name}", font=("Lato", 18),
                                           fg='Black', bg='white', anchor='w')
                user_name_label.grid(row=0, column=3, sticky='w', padx=20, pady=5)

                email_label = tk.Label(profile_details_frame, text=f"Email Address: {user_email}", font=("Lato", 18),
                                       fg='Black', bg='white', anchor='w')
                email_label.grid(row=1, column=3, sticky='w', padx=20, pady=5)

        # Button to manage the account
        manage_account_button = ttk.Button(profile_details_frame, text="Manage your account",
                                           command=self.manage_account_page,
                                           style='TButton')
        manage_account_button.grid(row=2, column=1, columnspan=2, padx=20, pady=20)

        # Button to view payment history
        view_payment_history_button = ttk.Button(profile_details_frame, text="View Payment History",
                                                 command=self.view_payment_history,
                                                 style='TButton')
        view_payment_history_button.grid(row=3, column=1, columnspan=2, pady=20)

        # Load and resize the logout image
        logout_image = get_image_data(89)
        logout_image = Image.open(logout_image)
        logout_image = logout_image.resize((100, 100))
        logout_image = ImageTk.PhotoImage(logout_image)

        # Create a label for the logout image
        logout_label = tk.Label(profile_details_frame, image=logout_image)
        logout_label.image = logout_image
        logout_label.grid(row=3, column=8, padx=10, pady=10)

        # Bind a callback function to the click event of the logout label
        logout_label.bind("<Button-1>", lambda event: self.close_window())

    def close_window(self):
        self.root.destroy()

    def view_payment_history(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        payment_history_label = tk.Label(self.content_frame, text="Payment History", font=("Lato", 18), fg='Black',
                                         bg='white', anchor='w', padx=250, pady=20)
        payment_history_label.pack(fill='x')
        payment_history_label = tk.Label(self.content_frame, bg='white')
        payment_history_label.pack(fill='x')

        # Create a frame to display payment history using Treeview
        payment_history_frame1 = tk.Frame(self.content_frame, bg='white', padx=250)
        payment_history_frame1.pack(fill='both', expand=True)
        payment_history_frame = tk.Frame(payment_history_frame1, bg='white', width=900, height=600)
        payment_history_frame.pack(fill='both', expand=True)

        # Create a Treeview widget
        tree = ttk.Treeview(payment_history_frame, columns=(
        "Ticket ID", "Attraction", "Purchase Date", "Quantity", "Valid Date", "Total Price"),
                            show="headings", selectmode="none")

        # Define column headings
        tree.heading("Ticket ID", text="Ticket ID")
        tree.heading("Attraction", text="Attraction")
        tree.heading("Purchase Date", text="Purchase Date")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Valid Date", text="Valid Date")
        tree.heading("Total Price", text="Total Price")

        # Set the width of each column (adjust the values as needed)
        tree.column("Ticket ID", width=200)
        tree.column("Attraction", width=250)
        tree.column("Purchase Date", width=100)
        tree.column("Quantity", width=300)
        tree.column("Valid Date", width=100)
        tree.column("Total Price", width=100)

        # Connect to the database and fetch payment history data
        with sqlite3.connect('TRAVEL KIOSK.db') as conn:
            cursor = conn.cursor()

            payment_query= "SELECT USER_ID,TICKET_ID, ATTRACTION_ID, PURCHASE_DATE, QUANTITY,Valid_DATE,TOTAL_PRICE FROM TICKET where USER_ID=?"
            cursor.execute(payment_query, (self.user_id,))

            payment_history_data = cursor.fetchall()

        # Add data to the Treeview
        for record in payment_history_data:
            tree.insert("", "end", values=record)

        # Add the Treeview to the frame
        tree.pack(fill='both', expand=True)

        # Create a button to go back to the ticket_page
        back_button = ttk.Button(payment_history_frame, text="Back", command=self.open_account, style='TButton')
        back_button.pack(pady=20)
    def manage_account_page(self):
        self.clear_content_frame()
        self.canvas.yview_moveto(0)


        # Create a label for the Manage Account page
        manage_account_label = tk.Label(self.content_frame, text="Manage Your Account", font=("Lato", 18),
                                        fg='Black', bg='white', anchor='w', padx=240, pady=20)
        manage_account_label.pack(fill='x')

        # Create a frame for account management
        manage_account_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
        manage_account_frame.pack(fill='both', expand=True)

        # Example labels and entry widgets for username, email, and password
        username_label = tk.Label(manage_account_frame, text="New Username:", font=("Lato", 14),
                                  fg='Black', bg='white', anchor='w', padx=240, pady=10)
        username_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)

        username_entry = ttk.Entry(manage_account_frame, font=("Lato", 14))
        username_entry.grid(row=0, column=1, sticky='w', padx=20, pady=10)

        email_label = tk.Label(manage_account_frame, text="New Email Address:", font=("Lato", 14),
                               fg='Black', bg='white', anchor='w', padx=240, pady=10)
        email_label.grid(row=1, column=0, sticky='w', padx=20, pady=10)

        email_entry = ttk.Entry(manage_account_frame, font=("Lato", 14))
        email_entry.grid(row=1, column=1, sticky='w', padx=20, pady=10)

        password_label = tk.Label(manage_account_frame, text="New Password:", font=("Lato", 14),
                                  fg='Black', bg='white', anchor='w', padx=240, pady=10)
        password_label.grid(row=2, column=0, sticky='w', padx=20, pady=10)

        password_entry = ttk.Entry(manage_account_frame, show='*', font=("Lato", 14))  # Show '*' for password
        password_entry.grid(row=2, column=1, sticky='w', padx=20, pady=10)

        confirm_password_label = tk.Label(manage_account_frame, text="Confirm New Password:", font=("Lato", 14),
                                          fg='Black', bg='white', anchor='w', padx=240, pady=10)
        confirm_password_label.grid(row=3, column=0, sticky='w', padx=20, pady=10)

        confirm_password_entry = ttk.Entry(manage_account_frame, show='*', font=("Lato", 14))  # Show '*' for password
        confirm_password_entry.grid(row=3, column=1, sticky='w', padx=20, pady=10)

        # Button to apply changes
        # Button to apply changes
        save_changes_button = ttk.Button(
            manage_account_frame,
            text="Save Changes",
            command=lambda: [self.validate_changes_and_apply(
                username_entry.get(),
                email_entry.get(),
                password_entry.get(),
                confirm_password_entry.get(),
            ), self.manage_account_page()],
            style='TButton'
        )
        save_changes_button.grid(row=4, column=1, columnspan=2, pady=20)

        # Create a button to go back to the ticket_page
        back_button = ttk.Button(manage_account_frame, text="Back", command=self.open_account,
                                 style='TButton')
        back_button.grid(row=4, column=0, columnspan=2, pady=20)

    def validate_changes_and_apply(self, new_username, new_email, new_password, confirm_password):
        # Perform validation logic for changes
        if not new_username or not new_email or not new_password or not confirm_password:
            messagebox.showerror("Validation Failed", "Please fill in all the fields.")
        elif not new_username:
            messagebox.showerror("Validation Failed", "Username is required.")
        elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%])[a-zA-Z\d!@#$%]{5,}$", new_username):
            messagebox.showerror("Validation Failed",
                                 "Username must contain at least 1 uppercase letter, 1 lowercase letter, numbers, "
                                 "and symbols (e.g., !@_#$%), and be at least 5 characters long.")
        elif not new_email:
            messagebox.showerror("Validation Failed", "Email is required.")
        elif not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", new_email):
            messagebox.showerror("Validation Failed", "Invalid email format.")
        elif not new_password:
            messagebox.showerror("Validation Failed", "Password is required.")
        elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", new_password):
            messagebox.showerror("Validation Failed",
                                 "Password must contain at least 1 uppercase letter, 1 lowercase letter, numbers, "
                                 "and be at least 8 characters long.")

        elif new_password != confirm_password:
            messagebox.showerror("Validation Failed", "Passwords do not match.")
        else:
            # Connect to the database
            with sqlite3.connect('TRAVEL KIOSK.db') as conn:
                cursor = conn.cursor()

                # Get user information from the USER table based on the user_id
                query = "SELECT USER_NAME, USER_EMAIL FROM USER WHERE USER_ID = ?"
                cursor.execute(query, (self.user_id,))
                user_data = cursor.fetchone()

                if not user_data:
                    messagebox.showerror("User Not Found", "User with the provided ID not found.")
                    return

                # Extract the existing username and email from the database
                existing_username, existing_email = user_data

                # Check if the new username is different from the existing one
                if new_username != existing_username:
                    # Check if the new username already exists in the database
                    cursor.execute("SELECT * FROM USER WHERE USER_NAME = ?", (new_username,))
                    existing_user = cursor.fetchone()

                    if existing_user:
                        messagebox.showerror("Validation Failed", "Username already exists.")
                        return

                    # Hash the new password before updating it in the database
                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

                    # Now you can update the user information in the database
                    cursor.execute(
                            "UPDATE USER SET USER_NAME = ?, USER_EMAIL = ?, USER_PASSWORD = ? WHERE USER_ID = ?",
                            (new_username, new_email, hashed_password, self.user_id))

                    conn.commit()

                messagebox.showinfo("Changes Applied", "Your changes have been applied successfully.")

    def search_activities(self, keyword):
        # Perform a search based on the keyword
        self.search_results = []  # Clear previous search results

        # Connect to the SQLite database
        conn = sqlite3.connect('TRAVeL KIOSK.db')  # Replace with your database file path
        cursor = conn.cursor()

        # Execute the SQL query to search for attractions, shopping, and transportation (one statement at a time)
        # Fetch attractions
        query_attractions = f"""
        SELECT A.ATTRACTION_NAME, I.IMAGE_DATA, 'attraction' AS category
        FROM ATTRACTION A
        JOIN IMAGES I ON A.ATTRACTION_ID = I.IMAGE_RELATED_ID
        WHERE LOWER(A.ATTRACTION_NAME) LIKE LOWER('%{keyword}%')
          AND I.IMAGE_TYPE IN ('Attraction') AND I.IMAGE_NAME like "%1";
        """
        search_results_attractions = cursor.execute(query_attractions).fetchall()

        query_shopping = f"""
        SELECT S.SAD_NAME, I.IMAGE_DATA, 'shopping' AS category
        FROM ShoppingAndDining S
        JOIN IMAGES I ON S.SAD_ID = I.IMAGE_RELATED_ID
        WHERE LOWER(S.SAD_NAME) LIKE LOWER('%{keyword}%')
          AND I.IMAGE_TYPE IN ('SAD-Mall')AND I.IMAGE_NAME like "%1";
        """

        search_results_shopping = cursor.execute(query_shopping).fetchall()

        query_market = f"""
                SELECT S.SAD_NAME, I.IMAGE_DATA, 'market' AS category
                FROM ShoppingAndDining S
                JOIN IMAGES I ON S.SAD_ID = I.IMAGE_RELATED_ID
                WHERE LOWER(S.SAD_NAME) LIKE LOWER('%{keyword}%')
                  AND I.IMAGE_TYPE IN ('SAD-Market')AND I.IMAGE_NAME like "%1";
                """

        search_results_market= cursor.execute(query_market).fetchall()

        query_food = f"""
                SELECT S.SAD_NAME, I.IMAGE_DATA, 'food' AS category
                FROM ShoppingAndDining S
                JOIN IMAGES I ON S.SAD_ID = I.IMAGE_RELATED_ID
                WHERE LOWER(S.SAD_NAME) LIKE LOWER('%{keyword}%')
                  AND I.IMAGE_TYPE IN ('SAD-Food')AND I.IMAGE_NAME like "%1";
                """

        search_results_food = cursor.execute(query_food).fetchall()

        # Fetch transportation
        query_transportation = f"""
        SELECT T.TRANSPORT_NAME, I.IMAGE_DATA, 'transportation' AS category
        FROM TRANSPORTATION T
        JOIN IMAGES I ON T.TRANSPORT_ID = I.IMAGE_RELATED_ID
        WHERE LOWER(T.TRANSPORT_NAME) LIKE LOWER('%{keyword}%')
          AND I.IMAGE_TYPE IN ('Transport-Taxi', 'Transport-Grab Car', 'Transport-Rapid Bus', 'Transport-Ferry', 
          'Transport-Car Rental')AND I.IMAGE_NAME like "%1";
        """
        search_results_transportation = cursor.execute(query_transportation).fetchall()

        # Combine the results
        search_results = (search_results_attractions + search_results_shopping + search_results_market
                          +search_results_food+search_results_transportation)

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Populate self.search_results with the fetched data
        for result in search_results:
            self.search_results.append({
                "name": result[0],
                "image_data": result[1],
                "category": result[2]
            })

        # Display search results on the content frame
        self.display_search_results()

    def display_search_results(self):
        # Clear the content frame
        self.clear_content_frame()

        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        activity_label2 = tk.Frame(self.content_frame, bg='white')
        activity_label2.pack(fill='x')
        activity_label1 = tk.Frame(activity_label2, bg='white', padx=10)
        activity_label1.pack(fill='x', padx=50, )
        activity_label = tk.Frame(activity_label1, bg='white', padx=10)
        activity_label.pack(fill='x')

        # Display search results, similar to how you displayed activities in open_home_page
        for i, result in enumerate(self.search_results):
            # Load and resize the image
            image_data = result["image_data"]
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((240, 170))  # Adjust the size as needed
            image = ImageTk.PhotoImage(image)
            self.image_references.append(image)

            # Create a frame to hold both the image and information labels with an outline
            activity_frame = tk.Frame(activity_label, bg='white', bd=1, relief="solid")  # Add the border
            activity_frame.grid(row=i // 4, column=i % 4, padx=40, pady=20)
            # Create the image label inside the frame
            image_label = tk.Label(activity_frame, image=image)
            image_label.image = image
            image_label.pack()

            # Create a frame to hold both labels
            activity_info_frame = tk.Frame(activity_frame, bg='white')  # No need for a border here
            activity_info_frame.pack(fill='x', expand=True)

            # Create activity_info1 and activity_info2 inside the info frame
            activity_info1 = tk.Label(activity_info_frame, text=result["name"], font=("Lato", 12), fg='Black',
                                      bg='white', anchor='w', width=23)

            # Place activity_info1 and activity_info2 inside the info frame
            activity_info1.pack(fill='x', expand=True)

            # Add category-specific details (button, etc.) based on the result's category
            if result["category"] == "attraction":
                activity_button = ttk.Button(activity_frame, text="Details",
                                             command=lambda r=result: self.open_south_details_page(r),
                                             style='TButton')
                activity_button.pack(fill='x', expand=True)
                self.buttons.append(activity_button)
            elif result["category"] == "shopping":
                shopping_button = ttk.Button(activity_frame, text="Details",
                                             command=lambda r=result: self.open_shopping_details_page(r),
                                             style='TButton')
                shopping_button.pack(fill='x', expand=True)
                self.buttons.append(shopping_button)
            elif result["category"] == "market":
                market_button = ttk.Button(activity_frame, text="Details",
                                             command=lambda r=result: self.open_market_details_page(r,market2=0),
                                             style='TButton')
                market_button.pack(fill='x', expand=True)
                self.buttons.append(market_button)
            elif result["category"] == "food":
                food_button = ttk.Button(activity_frame, text="Details",
                                             command=lambda r=result: self.open_food_page(r),
                                             style='TButton')
                food_button.pack(fill='x', expand=True)
                self.buttons.append(food_button)
            elif result["category"] == "transportation":
                transport_button = ttk.Button(activity_frame, text="Details",
                                              command=lambda r=result: self.open_transport_details_page(r),
                                              style='TButton')
                transport_button.pack(fill='x', expand=True)
                self.buttons.append(transport_button)

    def open_help_center(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a title label for "Contact Us" and center it horizontally
        help_center_label = tk.Label(self.content_frame, text="   Contact Us", font=("Lato", 60),
                                     fg='Black', bg='white', anchor='w', padx=500, pady=20)
        help_center_label.pack(fill='x')

        help_center_label = tk.Frame(self.content_frame, bg='white')
        help_center_label.pack(fill='x')

        help_center_label = tk.Frame(help_center_label, bg='white')
        help_center_label.pack(fill='x')
        help_center_label = tk.Frame(help_center_label, bg='white')
        help_center_label.pack(fill='x')

        # Define the activity names and corresponding image identifiers
        contactus = [
            {"name": "Email Us: penang123@gmail.com", "time": "Monday to Friday (9am to 4pm)", "image_id": 11},
            {"name": "Give Feedback", "time": "", "image_id": 91},  # Removed the feedback option
            {"name": "Ask any information with our chatbot", "time": "", "image_id": 6},
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, contactus_item in enumerate(contactus):
            # Load and resize the activity image
            image_data = get_image_data(contactus_item["image_id"])
            contactus_image = Image.open(image_data)
            contactus_image = contactus_image.resize((400, 370))  # Adjust the size as needed
            contactus_image = ImageTk.PhotoImage(contactus_image)

            # Create a frame to hold both the image and information labels with no border (relief='flat')
            contactus_frame = tk.Frame(help_center_label, bg='white', relief="flat")  # Remove the border
            contactus_frame.grid(row=0, column=i, padx=16, pady=58)

            # Create the activity image label inside the frame and center it vertically and horizontally
            contactus_image_label = tk.Label(contactus_frame, image=contactus_image, bg='white')
            contactus_image_label.image = contactus_image
            contactus_image_label.grid(row=0, column=0, sticky='nsew')  # Use grid manager to position and resize

            # Create a frame to hold both labels and center the text
            contactus_info_frame = tk.Frame(contactus_frame, bg='white')  # No need for a border here
            contactus_info_frame.grid(row=1, column=0, sticky='nsew')

            # Create contactus_info1 and contactus_info2 inside the info frame
            contactus_info1 = tk.Label(contactus_info_frame, text=contactus_item["name"], font=("Lato", 20), fg='Black',
                                       bg='white', anchor='center', width=30)
            contactus_info2 = tk.Label(contactus_info_frame, text=contactus_item["time"], font=("Lato", 20), fg='Black',
                                       bg='white', anchor='center', width=30)
            contactus_info1.grid(row=0, column=0)
            contactus_info2.grid(row=1, column=0)

            if "Give Feedback" in contactus_item["name"]:
                # Create a label for the feedback
                contactus_feedback_label = Label(contactus_info_frame, text=contactus_item["name"], font=("Lato", 20),
                                                 fg='Blue', bg='white', anchor='center', cursor="hand2")
                contactus_feedback_label.grid(row=0, column=0)

                # Bind a click event to the feedback label
                def open_feedback_link(event):
                    import webbrowser
                    webbrowser.open("https://forms.gle/5WusWzoAZ1qYto928")  # Open the specified feedback link

                contactus_feedback_label.bind("<Button-1>", open_feedback_link)

            if "penang123@gmail.com" in contactus_item["name"]:
                # Create a label for the email
                contactus_email_label = Label(contactus_info_frame, text=contactus_item["name"], font=("Lato", 20),
                                              fg='Blue', bg='white', anchor='center', cursor="hand2")
                contactus_email_label.grid(row=0, column=0)

                # Bind a click event to the email label
                def open_email_link(event):
                    import webbrowser
                    webbrowser.open("https://mail.google.com/")

                contactus_email_label.bind("<Button-1>", open_email_link)
            if "Ask any information with our chatbot" in contactus_item["name"]:
                # Create a label for the chatbot
                contactus_chatbot_label = Label(contactus_info_frame, text=contactus_item["name"], font=("Lato", 20),
                                                fg='Blue', bg='white', anchor='center', cursor="hand2")
                contactus_chatbot_label.grid(row=0, column=0)

                # Bind a click event to the chatbot label
                contactus_chatbot_label.bind("<Button-1>", self.open_chatbot_window)  # Bind it to a new method

            self.buttons.append(contactus_frame)  # Add the frame to the list instead of a button

    def open_chatbot_window(self, event):
        # Destroy the current frame to clear the content
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create an instance of the ChatBotApplication class
        ChatBotApplication(self.content_frame)

    def game_page(self):
        # Reset the content frame
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create an instance of the Quiz class
        Quiz(self.content_frame)

    # Inside your App class, where you create an instance of the Map class:
    def map_page(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create an instance of the Map class
        map_instance = Map(self.content_frame)
        map_instance.button()

    def on_canvas_configure(self, event):
        # Update the canvas scroll region when the content frame size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()  # Add this line to update idletasks

    def clear_content_frame(self):
        # Destroy all widgets inside the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

class Map:
    def __init__(self, parent):
        self.parent = parent
        self.marker_info = {}
        self.marker_list = []

    def button(self):
        frame1 = tk.Frame(self.parent, bg='white', padx=270, pady=10)
        frame1.pack(fill='both')

        frame_left = tk.Frame(frame1, bg='white')
        frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        frame_right = tk.Frame(frame1, bg='white', width=800, height=600)
        frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============
        frame_left.grid_rowconfigure(2, weight=1)

        button_1 = tk.Button(frame_left, text="Set Marker", bg='white', command=self.set_marker_event)
        button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        button_2 = tk.Button(frame_left, text="Clear Markers", bg='white', command=self.clear_marker_event)
        button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        map_label = tk.Label(frame_left, text="Tile Server:", anchor="w", bg='white', )
        map_label.grid(row=2, column=0, padx=(20, 0), pady=(10, 5))

        # Combobox for selecting map styles
        maps_style = [
            {"name": "OpenStreetMap"},
            {"name": "Google normal"},
            {"name": "Google satellite"}]
        self.map_option_menu = ttk.Combobox(frame_left, values=[maps['name'] for maps in maps_style])
        self.map_option_menu.grid(row=3, column=0, padx=20)
        self.map_option_menu.bind("<<ComboboxSelected>>", self.change_map)

        button_3 = tk.Button(frame_left, text="Google Map", bg='white', command=self.ggmap)
        button_3.grid(pady=(20, 0), padx=(20, 20), row=4, column=0)

        blank_label = tk.Label(frame_left, bg='white')
        blank_label.grid(pady=250, padx=0, row=5, column=0)

        frame_right.grid_rowconfigure(1, weight=1)
        frame_right.grid_rowconfigure(0, weight=0)
        frame_right.grid_columnconfigure(0, weight=1)
        frame_right.grid_columnconfigure(1, weight=0)
        frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nsew", padx=(0, 0), pady=(0, 0))

        self.entry = tk.Entry(frame_right, width=20)
        self.entry.insert(0, "")
        self.entry.grid(row=0, column=0, sticky="we", padx=12, pady=12)
        self.entry.bind("<Return>", self.search_event)

        button_5 = tk.Button(frame_right, text="Search", width=10, bg='white', command=self.search_event)
        button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        blank_label = tk.Label(frame_right, bg='white')
        blank_label.grid(row=2, column=1, sticky="w", padx=300)

        # Set default values
        self.map_widget.set_address("Penang")
        self.map_option_menu.set("OpenStreetMap")

        # Set the size of the frame_right
        frame_right.config(width=800, height=600)

        # Bind map click event to handle marker clicks
        self.map_widget.bind("<Button-1>", self.on_map_click)

    def ggmap(self):
        map_frame = HtmlFrame(horizontal_scrollbar="auto", vertical_scrollbar="auto")
        map_frame.pack(fill=tk.BOTH, expand=True)

        # Load Google Maps
        map_url = "https://www.google.com/maps"
        map_frame.set_content(webbrowser.get().open(map_url))

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        marker = self.map_widget.set_marker(current_position[0], current_position[1])
        location_info = {
            "name": "Marker Location",  # Example location name
            "latitude": current_position[0],
            "longitude": current_position[1]
        }
        self.marker_info[marker] = location_info
        self.marker_list.append(marker)

    def on_map_click(self, event):
        x, y = event.x, event.y
        for marker, location_info in self.marker_info.items():
            marker_x, marker_y = self.map_widget.get_position_on_map(location_info["latitude"],
                                                                     location_info["longitude"])
            if abs(x - marker_x) < 10 and abs(y - marker_y) < 10:
                # Marker clicked, handle your action here
                self.map_widget.set_center(location_info["latitude"],
                                           location_info["longitude"])  # Move map to the marker's coordinates
                print(
                    f"Clicked on marker at {location_info['name']} ({location_info['latitude']}, {location_info['longitude']})")
                break

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_map(self, event=None):
        new_map = self.map_option_menu.get()
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)
        self.map_widget.set_size(width=800, height=600)

class Quiz:
    def __init__(self, parent):
        self.parent = parent
        self.questions = self.import_questions()
        self.num_questions = 5
        self.current_question = 0
        self.score = 0

        # Create a white canvas to act as a background
        self.canvas_frame = tk.Frame(self.parent, bg="white")
        self.canvas_frame.pack(fill='both', expand=True)

        # Create a frame for quiz content
        self.quiz_frame = tk.Frame(self.canvas_frame, bg='white')
        self.quiz_frame.pack(fill='both', expand=True)

        self.shuffle_questions()
        self.display_question()

    def destroy_children(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def import_questions(self):
        return QUESTIONS

    def shuffle_questions(self):
        random.shuffle(self.questions)
        self.questions = self.questions[:self.num_questions]

    def check_answer(self):
        question_data = self.questions[self.current_question]
        user_answer = self.options_var.get()  # Get the selected answer

        if user_answer == question_data["answer"]:
            self.score += 1

        self.current_question += 1
        self.destroy_children(self.quiz_frame)
        self.display_question()

    def display_question(self):
        # The title to be shown
        title_frame = tk.Frame(self.quiz_frame, bg="#4F795E")  # Create a frame for the title
        title_frame.pack(side='top', fill='x')

        title = tk.Label(title_frame, text="Take a Test", bg="#4F795E", fg="white", font=("Lato", 20, "bold"))
        title.pack(side='left', padx=700, pady=10)

        blank_label = tk.Label(self.quiz_frame, bg='white')
        blank_label.pack(fill='x')

        quiz_frame1 = tk.Frame(self.quiz_frame, bg='white', padx=320, pady=50)
        quiz_frame1.pack(fill='both', expand=True, anchor='center')

        quiz_frame = tk.Frame(quiz_frame1, bg='white', padx=40, pady=20, bd=1, relief="solid")
        quiz_frame.pack(fill='both', expand=False, anchor='center',
                        side='top')  # Set expand to False and anchor to center

        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            question_label = tk.Label(quiz_frame, text=question_data["question"], font=("Lato", 20), fg='Black',
                                      bg='white', anchor='w',
                                      justify='left', wraplength=900)
            question_label.pack()

            self.options_var = StringVar()
            self.options_var.set(None)

            for i, option in enumerate(question_data["options"]):
                ans_frame1 = tk.Frame(quiz_frame, bg='white', padx=60, pady=10)
                ans_frame1.pack(fill='both')
                ans_frame = tk.Frame(ans_frame1, bg='#4F795E', padx=10, pady=10, bd=1, relief="solid")
                common_bg = '#' + ''.join([hex(x)[2:].zfill(2) for x in (79, 121, 94)])  # RGB in dec
                common_fg = '#ffffff'
                option_radio = tk.Radiobutton(ans_frame, text=option, variable=self.options_var, value=option,
                                              fg=common_fg, bg=common_bg,
                                              activebackground=common_bg, activeforeground=common_fg,
                                              selectcolor=common_bg, font=("Lato", 13))  # Specify font size for choices
                option_radio.pack(anchor='w')
                ans_frame.pack(fill='both', expand=True)

            next_button = tk.Button(quiz_frame, text="Next", command=self.check_answer, bg='#505d58', fg='white',
                                    font=("Lato", 14, "bold"), padx=30, pady=5)
            next_button.pack(side='bottom')  # Move the "Next" button to the bottom of the quiz_frame
        else:
            self.display_result(quiz_frame)

    def display_result(self, question_frame):
        result_frame = tk.Frame(question_frame, bg='white')  # Create a white frame for displaying the result
        result_frame.pack(fill='both', expand=True)

        result_label = tk.Label(result_frame, text=f"Your Score: {self.score}/{self.num_questions}", font=("Lato", 14),
                                fg='Black', bg='white', anchor='w',
                                justify='left', wraplength=900)
        result_label.pack()

class ChatBotApplication:
    def __init__(self, parent):
        self.parent = parent
        # Create a white canvas to act as a background
        self.canvas_frame = tk.Frame(self.parent, bg="white")
        self.canvas_frame.pack(fill='both', expand=True)

        # Create a frame for chat content
        self.chat_frame = tk.Frame(self.canvas_frame, bg='white')
        self.chat_frame.pack(fill='both', expand=True)
        self.intents = self.load_intents()

        # Initialize chat interface
        self.chat()

    def chat(self):
        chat_frame2 = tk.Frame(self.chat_frame, bg='white', padx=340, pady=40)
        chat_frame2.pack(fill='both', expand=True)
        chat_frame1 = tk.Frame(chat_frame2, bg='#4F795E',bd=1, relief='solid')
        chat_frame1.pack(fill='both', expand=True)
        self.text_widget = Text(chat_frame1, bg='white',height=30, width=100, fg='black', font=("Lato", 12))
        self.text_widget.pack(padx=10, pady=10, fill='x', anchor='nw')
        self.text_widget.insert(tk.END, "ChatBot: Hello! How can I assist you?\n")
        self.text_widget.configure(state='disabled')

        self.input_entry = Entry(chat_frame1, width=50)
        self.input_entry.pack(anchor='w', padx=100, pady=15, fill='x')  # Align to the left

        send_button = Button(chat_frame1, text="Send", command=self.send_message)
        send_button.pack(anchor='w', padx=100, pady=15, fill='x')  # Align to the left

        blank_label = tk.Label(chat_frame1, bg='#4F795E')
        blank_label.pack(pady=10)

    def load_intents(self):
        with open('intents.json', 'r') as file:
            intents_data = json.load(file)
        return intents_data.get('intents', [])  # Use get to handle missing 'intents' key

    def send_message(self):
        user_input = self.input_entry.get().lower().strip()
        self.display_message(f"You: {user_input}\n")
        self.input_entry.delete(0, 'end')

        response = self.get_response(user_input)
        self.display_message(f"ChatBot: {response}\n")

    def get_response(self, user_input):
        user_input = user_input.lower()
        for intent in self.intents:
            if any(keyword.lower() in user_input for keyword in intent['keywords']):
                return random.choice(intent['responses'])
        return "I'm sorry, I don't understand that."

    def display_message(self, message):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, message)
        self.text_widget.configure(state='disabled')
        self.text_widget.see(tk.END)

def main():
    root = Tk()    # Create the root window

    TravelKioskApp(root)    # Run the application with the root window

    root.mainloop()    # Start the Tkinter event loop


if __name__ == "__main__":
    main()