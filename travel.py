import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import Spinbox
from tkinter import StringVar
from tkcalendar import Calendar
from tkinter import Label
import random
#from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer
from tkinter import messagebox
import re
#from tkinterhtml import HtmlFrame
import webbrowser
#from tkintermapview import TkinterMapView
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime

class TravelKiosk:
    def __init__(self, root):
        self.root = root
        self.root.title("Penang Travel Kiosk")

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
        # Create a custom style for buttons and entry boxes
        self.style = ttk.Style()

        # Set the background color to white for buttons and entry boxes
        self.style.configure('TButton', background='white')
        self.style.configure('TEntry', background='white')

    def create_top_bar(self):
        top_bar = ttk.Frame(self.root, )
        top_bar.pack(fill='x',)

        # Create a label with a specified background color
        top_bar_label = tk.Frame(top_bar, bg='white', height=1, bd=1, relief="raised")
        top_bar_label.pack(fill='both',)
        top_bar_label2 = tk.Label(top_bar_label, bg='white',)
        top_bar_label2.pack(fill='x', side='left')
        top_bar_label1 = tk.Label(top_bar_label, bg='white')
        top_bar_label1.pack(fill='x', side='right')

        # Load and resize the logo image
        logo_image = Image.open('palm2.png')  # Replace with the actual path to your logo image
        logo_image = logo_image.resize((65, 50))  # Adjust the size as needed
        logo_image = ImageTk.PhotoImage(logo_image)

        # Create the logo label (with clickable behavior)
        logo_label = tk.Label(top_bar_label2, image=logo_image, cursor="hand2")
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

        # Load the image for the Account button
        account_image = Image.open('ppl.png')  # Replace with the path to your account logo image
        account_image = account_image.resize((50, 51))  # Adjust the size as needed
        account_image = ImageTk.PhotoImage(account_image)

        # Create the Account label with the image (no border)
        account_label = tk.Label(top_bar_label1, image=account_image, cursor="hand2")
        account_label.image = account_image
        account_label.pack(side='right', padx=10, pady=7)
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
        banner_image = Image.open('pngbridge.jpg')  # Replace with the path to your banner image
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

        # Define the activity names and corresponding image paths
        activities = [
            {"name": "Escape Penang", "money": "  155", "image_path": "escape.jpg"},
            {"name": "The Top Penang", "money": "  RM9", "image_path": "thetop.jpg"},
            {"name": "Entopia Penang", "money": "  RM40", "image_path": "entopia.jpg"},
            {"name": "Penang Hill", "money": "  RM10", "image_path": "railway.jpg"},
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the activity image
            activity_image = Image.open(activity["image_path"])
            activity_image = activity_image.resize((240, 170))  # Adjust the size as needed
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
                                                        path=activity["image_path"]: self.open_activity_ticket_page(a,
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
        map_image = Image.open('map.jpg')  # Replace with the path to your map image
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
            text="Penang is a vibrant State with its capital, George Town, having the rare distinction of being a UNESCO World Heritage Site. It is a true melting pot of cultures with its blend of Eastern and Western influences. Retaining many of the values adopted during its era of British rule, Penang bears a charm that is unique to itself.",
            font=("Lato", 10),
            fg='Black',
            bg='white',
            anchor='w',
            justify='left',
            wraplength=500
        )
        map_info.pack(fill='x', expand=True)

        blank_label = tk.Label(self.content_frame, bg='white')
        blank_label.pack(fill='x')

    def show_large_image(self, event):
        # Create a pop-up window to display the large image
        large_image_window = tk.Toplevel(self.root)
        large_image_window.title("Map Penang")

        # Resize the original image for the pop-up window
        large_image = Image.open('map.png')  # Replace with the path to your map image
        large_image = large_image.resize((950, 700))  # Adjust the size as needed
        large_image = ImageTk.PhotoImage(large_image)

        # Display the resized image in the pop-up window
        large_image_label = tk.Label(large_image_window, image=large_image)
        large_image_label.image = large_image
        large_image_label.pack()

    def explore_north(self):
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

        # Define the north names and corresponding image paths
        activities = [
            {"name": "Street Art", "image_path": "StreetArt1.jpg"},
            {"name": "Clan Jetties", "image_path": "clan.jpg"},
            {"name": "Kek Lok Si", "image_path": "KekLokSiTemple.jpg"},
            {"name": "Peranakan Mansion", "image_path": "PeranakanMansion.jpg"},
            {"name": "Upside Down Museum", "image_path": "UpsideDownMuseum.jpg"},
            {"name": "Dark Mansion", "image_path": "darkmansion.jpg"},
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the activity image
            north_image1 = Image.open(activity["image_path"])
            north_image1 = north_image1.resize((240, 170))
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

        # Check the north name and set the appropriate image path
        image_path = ""
        if activity['name'] == "Street Art":
            image_path = "StreetArt2.jpg"
        elif activity['name'] == "Clan Jetties":
            image_path = "clan2.jpg"
        elif activity['name'] == "Kek Lok Si":
            image_path = "kekloksitemple2.jpg"
        elif activity['name'] == "Peranakan Mansion":
            image_path = "peranakanmansion2.jpg"
        elif activity['name'] == "Upside Down Museum":
            image_path = "UpsideDownMuseum.jpg"
        elif activity['name'] == "Dark Mansion":
            image_path = "darkmansion2.jpg"

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"     Details for {activity['name']}", font=("Lato", 20),
                                 fg='Black', bg='white', anchor='w', padx=215)
        details_label.pack(fill='x', )

        # Create a frame to display details and additional information
        details_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
        details_frame.pack(fill='x')

        # Load and resize the activity image for the details page
        activity_image = Image.open(image_path)
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
        info_frame1 = tk.Frame(info_frame, bg='white',)
        info_frame1.pack(padx=20, side='left')
        info_frame2 = tk.Frame(info_frame1, bg='white',)
        info_frame2.pack(padx=20, side='bottom')

        # Create a label to display information for the activity
        if activity['name'] == "Street Art":
            name_text = "About Street Art"
        elif activity['name'] == "Clan Jetties":
            name_text = "About Clan Jetties"
        elif activity['name'] == "Kek Lok Si":
            name_text = "About Kek Lok Si"
        elif activity['name'] == "Peranakan Mansion":
            name_text = "About Peranakan Mansion"
        elif activity['name'] == "Upside Down Museum":
            name_text = "About Upside Down Museum"
        elif activity['name'] == "Dark Mansion":
            name_text = "About Dark Mansion"

        # Create a label to display information for the activity
        info_text = ""
        if activity['name'] == "Street Art":
            info_text = "Penang, a vibrant island state located in Malaysia, has gained international acclaim for its captivating street art scene. The heart of this phenomenon can be found in George Town, Penang's capital city, where narrow alleys and historic streets are adorned with an array of colorful and thought-provoking murals. These street art pieces, many of which are created by talented local and international artists, offer a delightful blend of cultural, historical, and contemporary themes. From larger-than-life caricatures to realistic depictions of daily life, Penang's street art not only serves as a visual treat for tourists but also tells the story of the city's rich heritage and diverse culture. It has become a must-visit destination for art enthusiasts and travelers seeking to explore the unique and captivating world of urban art." \
                        "\n\n\u27A4  316, Beach St, Georgetown, 10300 George Town, Penang"
        elif activity['name'] == "Clan Jetties":
            info_text = "The Clan Jetties of Penang are historic Chinese villages built out over the water on long jetties. Typically, each Jetty belongs to a single family clan, with dozens of wooden houses on each Jetty. Located in George Town, Malaysia, the Clan Jetties are a reminder of Penang’s multicultural history. There have been 10 jetties in total, however devastating fires and recent construction projects means 4 have been since destroyed. The most well-known Jetty is the Chew Jetty, which is open so visitors can observe what life on a Clan Jetty is like." \
                        "\n\nMonday - Sunday  9am - 9pm" \
                        "\n\u27A4  Pengkalan Weld, George Town, 10300 George Town, Pulau Pinang"
        elif activity['name'] == "Kek Lok Si":
            info_text = "Built since the year 1891, Kek Lok Si Temple situated in the island of Penang, Malaysia, is one of the largest and finest temples complexes in Southeast Asia. With millions of magnificent images of Buddha and hundreds of beautiful meaningful carvings, sculptures and murals in the interior and exterior of the temple halls, pagodas and archways, Kek Lok Si Temple is not just a center for Chinese culture and Buddha teaching, but also an unique heritage treasures that have Mahayana Buddhism and traditional Chinese rituals blend into a harmonious whole, in temple architecture and daily activities of worshipers." \
                        "\n\nMonday - Sunday  8:30am - 5:30pm" \
                        "\n\u27A4  Kek Lok Si Temple, Jln Balik Pulau, 11500 Air Itam, Penang"
        elif activity['name'] == "Peranakan Mansion":
            info_text = "The Peranakans, also known as the Babas and Nyonyas, was a prominent community of acculturated Chinese unique to this part of the world, especially in the Straits Settlements (Penang, Malacca and Singapore) hence its other name, the Straits Chinese. Adopting selected ways of the local Malays and later, the colonial British, the Peranakans had created a unique lifestyle and customs which had not only left behind a rich legacy of antiques but its cultural influences like cuisine and language are still evident in Penang today. " \
                        "\nAt the Pinang Peranakan Mansion, the typical home of a rich Baba of a century ago is recreated to offer a glimpse of their opulent lifestyle and of their many customs and traditions. With over 1,000 pieces of antiques and collectibles of the era on display, this Baba-Nyonya museum is also housed in one of Penang heritage mansion of eclectic design and architecture. Built at the end of the 19th century by one of local history famous personalities, the Hai Kee Chan or Sea Remembrance Store had once served as the residence and office of Kapitan Cina Chung Keng Kwee. Though not a Baba himself, his Chinese courtyard house was much like a typical large Baba home of eclectic style, incorporating Chinese carved-wood panels and English floor tiles and Scottish ironworks. Having survived the many decades of neglect and decay, the mansion has now been restored to its former glory of a stately home." \
                        "\n\nMonday - Sunday  9:30am - 5pm" \
                        "\n\u27A4  29, Church Street, 10200 Penang, Malaysia."
        elif activity['name'] == "Upside Down Museum":
            info_text = "One of many popular optical-illusion museums in Southeast Asia, Penang’s Upside Down Museum is set up like an ordinary home but with the furniture and accessories stuck to the ceiling. It’s a favorite among locals and travelers, adults and children alike, who come to take disorienting selfies to post on social media." \
                        "\nAt the Upside Down Museum, you can take photos that make it look as though you’re walking upside down or floating in odd positions. Visitors walk through the “house,” guided by staff for a more orderly procession. Most travelers visit the museum while touring the historic George Town area of Penang. You can visit independently or stop here as part of a half- or full-day guided tour of the city." \
                        "\n\nMonday - Sunday  9:30am - 6:30pm" \
                        "\n\u27A4   45, Lebuh Kimberley, 10100 George Town, Pulau Pinang"
        elif activity['name'] == "Dark Mansion":
            info_text = "Enter a whole new world as you walk through the doors of the Dark Mansion Museum, the only glow-in-the-dark museum in Penang. Be delighted by the modern works of art that are made more fun through a mixture of science and technology." \
                        "\nMarvel at unique pieces that look like they move right before your eyes. See five uniquely themed attractions where you can take creative pictures and see a show of special light effects as your background." \
                        "\nBe amazed by the awe-inspiring \"Fire & Water\" artwork by the world-renowned 3D illusionist Edgar Muller, a German painter with pieces that have inspired the entire world." \
                        "\nTake a sneak peek into the colorful mysteries of the Dark Mansion before heading over the to real Dark Mansion of Penang for a breath-taking experience!" \
                        "\n\nMonday - Sunday  10:30am - 6:30pm" \
                        "\n\u27A4   145, Lebuh Kimberley, George Town, 10100 George Town, Pulau Pinang"

        name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        name_label.pack(fill='both', expand=True, padx=25, pady=10)
        info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        info_label.pack(fill='both', expand=True, padx=25, pady=10)
        # Create a button to go back to the explore_north page
        back_button = ttk.Button(details_frame, text="Back", command=self.explore_north, style='TButton')
        back_button.pack(pady=20)

    def toggle_favorite(self):
        # Toggle the favorite state and update the button's text
        self.favorite = not self.favorite
        if self.favorite:
            self.star_button.configure(text="\u2605")  # Change to ★
        else:
            self.star_button.configure(text="\u2729")  # Change to ☆

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

        # Define the south names and corresponding image paths
        activities = [
            {"name": "Queensbay Mall", "image_path": "queensbay.jpg"},
            {"name": "ATV Ride", "image_path": "bike.jpg"},
            {"name": "Countryside Stables Penang", "image_path": "horse.jpg"},
            {"name": "Audi Dream Farm", "image_path": "audi.jpg"},
            {"name": "Escape", "image_path": "escape.jpg"},
            {"name": "Entopia", "image_path": "entopia.jpg"},
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the activity image
            south_image1 = Image.open(activity["image_path"])
            south_image1 = south_image1.resize((240, 170))  # Adjust the size as needed
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

        # Check the south name and set the appropriate image path
        image_path = ""
        if activity['name'] == "Queensbay Mall":
            image_path = "queensbay2.jpg"
        elif activity['name'] == "ATV Ride":
            image_path = "bike2.jpg"
        elif activity['name'] == "Countryside Stables Penang":
            image_path = "horse2.jpg"
        elif activity['name'] == "Audi Dream Farm":
            image_path = "audi2.jpg"
        elif activity['name'] == "Escape":
            image_path = "escape.jpg"
        elif activity['name'] == "Entopia":
            image_path = "entopia2.jpg"

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"     Details for {activity['name']}", font=("Lato", 20),
                                 fg='Black', bg='white', anchor='w', padx=213)
        details_label.pack(fill='x')

        # Create a frame to display details and additional information
        details_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
        details_frame.pack(fill='x')

        # Load and resize the activity image for the details page
        activity_image = Image.open(image_path)
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

        # Create a label to display information for the activity
        if activity['name'] == "Queensbay Mall":
            name_text = "About Queensbay Mall"
        elif activity['name'] == "ATV Ride":
            name_text = "About ATV Ride"
        elif activity['name'] == "Countryside Stables Penang":
            name_text = "About Countryside Stables Penang"
        elif activity['name'] == "Audi Dream Farm":
            name_text = "About Audi Dream Farm"
        elif activity['name'] == "Escape":
            name_text = "About Escape"
        elif activity['name'] == "Entopia":
            name_text = "About Entopia"

        # Create a label to display information for the activity
        info_text = ""
        if activity['name'] == "Queensbay Mall":
            info_text = "Queensbay Mall is a prominent shopping and entertainment destination located in Bayan Lepas, Penang, Malaysia. Opened for business on December 1, 2006, it is the largest and most modern shopping mall in Penang. With a sprawling area of 73 acres, Queensbay Mall boasts a wide range of retail stores, including a Jusco department store, junior anchors, and numerous retail merchants. It offers a diverse shopping experience, entertainment options, and dining choices, making it a preferred destination for both locals and tourists." \
                        "\n\nMonday - Sunday  10:30am - 10:30pm" \
                        "\n\n\u27A4   Queensbay Mall, 100, Persiaran Bayan Indah, 11900 Bayan Lepas, Pulau Pinang"
        elif activity['name'] == "ATV Ride":
            info_text = "The Penang ATV Eco Tour Family and Corporate Recreation Center was officially opened to the public on 21 October 2015. The recreational activities provided by Penang ATV Eco Tour are for domestic tourism. We also provide Team Building program for both corporate and government sector. We offers various outdoor and indoor recreation activities for the general public including family as well as Team Building program activities that are dedicated to the corporate and government sector. Current economic developments and government initiatives to promote domestic tourism have boosted the business of domestic tourism activities as offered by our company." \
                        "\n\nMonday - Sunday  9am - 6pm" \
                        "\n\u27A4  298, Mukim I, Kampung Perlis, 11000 Balik Pulau, Penang"
        elif activity['name'] == "Countryside Stables Penang":
            info_text = "Countryside Stables is a privately owned property by Wan Aikhsan & Doris Lim. It is nestled in the midst of Sungai Burung agriculture area in Balik Pulau. Away from the hustle and bustle of city life. To date, it is home to 28 horses which consist of miniatures horses, Pure Bred Arabian Horses,Polo Pony, Thai, Myanmar, Malaysian ponies, donkeys and deer. Upon entering Countryside Stables, an entry free of RM5 (adults) & RM3 (children) will be charged. This fee is however deductible when visitors take part in joy ride or guided ride." \
                        "\n\nMonday - Sunday  1:30pm - 6pm" \
                        "\n\u27A4  Lot 10050, Jalan Sungai Burung, Kampung Sungai Burung, 11000 Balik Pulau, Pulau Pinang"
        elif activity['name'] == "Audi Dream Farm":
            info_text = "“Audi Dream Farm”, a mini farm that grow nature growing and non-toxic chemical added plants with several kinds of tame animals. We also provide “Home Delivery Service” as to make sure everyone are able to taste 100% natural ingredients easily. This is the concept of making change in each of our lifestyle to a way that is more friendly to the environment and better time spending with our beloved one. This all goes back to the urging of a pastoral lifestyle where the simplicity of nature was of the most importance." \
                        "\n\nMonday - Sunday  9am - 6pm" \
                        "\n\u27A4  Audi dreamfarm 145, MK B, Sg.Rusa, 11010 Balik Pulau, Pulau Pinang"
        elif activity['name'] == "Escape":
            info_text = "ESCAPE Penang is the fun destination with exciting rides and games hosted in a natural environment. ESCAPE Penang re-introduces the play and values of yesteryear so to inject reality into a world overdependent on an isolation-inducing electronic lifestyle. Through fun activities, with an emphasis on self-directed and self-powered play, the visitor experiences Low Tech, High Fun. ESCAPE Penang demonstrates there’s no age limit to having fun as the rides and games are designed for a wide range of age groups, abilities, and energy levels." \
                        "\n\nMonday                      closed\nTuesday - Sunday  10am - 6pm" \
                        "\n\u27A4  828 Jalan Teluk Bahang, 11050 Penang, Malaysia"
        elif activity['name'] == "Entopia":
            info_text = "The world's first live tropical butterfly sanctuary featuring a nature park with live butterflies of various species & small reptiles living in their natural habitat. With its recent rebirth as ENTOPIA, experience nature’s largest classroom and discovery hub, where the butterflies and insects are free to come out to play - an Entomological Utopia." \
                        "The Natureland, which is a living garden vivarium, is a shared ecological space for a variety of animals from invertebrates and reptiles living in their re-created natural habitat. It is the one of the largest butterfly garden in Malaysia with approximately 15,000 free-flying butterflies at any one time consisting of up to 60 species. The living garden features more than 200 species of plants with waterfalls, ponds, caves and other artistic garden features. Be sure to stroll along the mezzanine-terrace from David’s Garden and get a majestic view of our Home Tree." \
                        "\n\nWednesday                closed" \
                        "\nMonday - Sunday  9am - 5pm\n\u27A4  828 Jalan Teluk Bahang, 11050 Penang, Malaysia"

        name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        name_label.pack(fill='both', expand=True, padx=25, pady=10)
        info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        info_label.pack(fill='both', expand=True, padx=25, pady=10)

        # Create a button to go back to the explore_south page
        back_button = ttk.Button(details_frame, text="Back", command=self.explore_south, style='TButton')
        back_button.pack(pady=20)

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

        # Define the activity names and corresponding image paths
        activities = [
            {"name": "Escape Penang", "money": "  RM155", "image_path": "escape.jpg"},
            {"name": "The Top Penang", "money": "  RM9", "image_path": "thetop.jpg"},
            {"name": "Entopia Penang", "money": "  RM40", "image_path": "entopia.jpg"},
            {"name": "Penang Hill", "money": "  RM10", "image_path": "railway.jpg"},
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the activity image
            activity_image = Image.open(activity["image_path"])
            activity_image = activity_image.resize((240, 170))  # Adjust the size as needed
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
                                                        path=activity["image_path"]: self.open_activity_ticket_page(a,
                                                                                                                    path),
                                         style='TButton')
            activity_button.pack(fill='x', expand=True)
            self.buttons.append(activity_button)

    def open_activity_ticket_page(self, activity, image_path):
        # Reset the hole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Check the activity name and set the appropriate image path
        if activity['name'] == "Escape Penang":
            image_path = "escape2.jpg"
        elif activity['name'] == "The Top Penang":
            image_path = "thetop2.jpg"
        elif activity['name'] == "Entopia Penang":
            image_path = "entopia2.jpg"
        elif activity['name'] == "Penang Hill":
            image_path = "hill.jpg"

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"     Details for {activity['name']}", font=("Lato", 20),
                                 fg='Black', bg='white', anchor='w', padx=215)
        details_label.pack(fill='x')

        # Create a frame to display details and additional information
        details_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
        details_frame.pack(fill='x')

        # Load and resize the activity image for the details page
        activity_image = Image.open(image_path)
        activity_image = activity_image.resize((950, 240))
        activity_image = ImageTk.PhotoImage(activity_image)

        # Create the activity image label on the details page
        activity_image_label = tk.Label(details_frame, image=activity_image)
        activity_image_label.image = activity_image
        activity_image_label.pack(side='top', padx=250)

        blank_label = tk.Label(details_frame, bg='white')
        blank_label.pack(fill='x')

        # Create a frame for information
        info_frame = tk.Frame(details_frame, bg='white', bd=1, relief="solid", width=700, height=200)
        info_frame.pack(side='top', padx=20)

        # Create a label to display information for the activity
        name_text = ""
        if activity['name'] == "Escape Penang":
            name_text = "About Escape"
        elif activity['name'] == "The Top Penang":
            name_text = "About The Top"
        elif activity['name'] == "Entopia Penang":
            name_text = "About Entopia"
        elif activity['name'] == "Penang Hill":
            name_text = "About Penang Hill"

        # Create a label to display information for the activity
        info_text = ""
        if activity['name'] == "Escape Penang":
            info_text = "ESCAPE Penang is the fun destination with exciting rides and games hosted in a natural environment. ESCAPE Penang re-introduces the play and values of yesteryear so to inject reality into a world overdependent on an isolation-inducing electronic lifestyle. Through fun activities, with an emphasis on self-directed and self-powered play, the visitor experiences Low Tech, High Fun. ESCAPE Penang demonstrates there’s no age limit to having fun as the rides and games are designed for a wide range of age groups, abilities, and energy levels." \
                        "\n\nMonday                      closed\nTuesday - Sunday  10am - 6pm\n\u27A4  828 Jalan Teluk Bahang, 11050 Penang, Malaysia"
        elif activity['name'] == "The Top Penang":
            info_text = "Unearth a world of captivating experiences at The TOP Penang! Your portal to excitement and adventure, The TOP Penang promises an array of attractions to delight visitors of all ages. Plunge into the enchanting depths of the Aquarium, step into the prehistoric era at the Jurassic Research Centre, and embark on an interactive voyage of exploration at Tech Dome. And don't overlook the breathtaking Rainbow Skywalk, offering sweeping vistas." \
                        "\n\nMonday - Sunday  10am - 10pm\n\u27A4   1, Jln Penang, George Town, 10000 George Town, Pulau Pinang, Malaysia"
        elif activity['name'] == "Entopia Penang":
            info_text = "The world's first live tropical butterfly sanctuary featuring a nature park with live butterflies of various species & small reptiles living in their natural habitat. With its recent rebirth as ENTOPIA, experience nature’s largest classroom and discovery hub, where the butterflies and insects are free to come out to play - an Entomological Utopia." \
                        "The Natureland, which is a living garden vivarium, is a shared ecological space for a variety of animals from invertebrates and reptiles living in their re-created natural habitat. It is the one of the largest butterfly garden in Malaysia with approximately 15,000 free-flying butterflies at any one time consisting of up to 60 species. The living garden features more than 200 species of plants with waterfalls, ponds, caves and other artistic garden features. Be sure to stroll along the mezzanine-terrace from David’s Garden and get a majestic view of our Home Tree." \
                        "\n\nWednesday                      closed\nMonday - Sunday  9am - 5pm\n\u27A4  828 Jalan Teluk Bahang, 11050 Penang, Malaysia"
        elif activity['name'] == "Penang Hill":
            info_text = "Penang Hill, also known as \"Bukit Bendera\" in Malay, is a prominent hill station and a popular tourist attraction located on Penang Island in Malaysia. Rising to an elevation of about 821 meters (2,690 feet) above sea level, Penang Hill offers breathtaking panoramic views of the surrounding landscapes and the vibrant city of George Town below. Visitors can reach the summit by taking a funicular railway ride, which is an experience in itself. The hill is renowned for its cooler climate compared to the coastal areas, making it a pleasant escape from the tropical heat. At the peak, one can explore lush botanical gardens, a mosque, and historical colonial-era bungalows. Penang Hill is not only a place of natural beauty but also a significant part of Penang's history and heritage." \
                        "\n\nMonday - Sunday  6:30am - 10pm\n\u27A4  Penang Hill, Bukit Bendera, 11300 Bukit Bendera, Penang"

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
        buy_ticket_label = tk.Label(buy_tic_frame3, text="    Buy Tickets", font=("Lato", 20), fg='black', bg='white',
                                    anchor='w')
        buy_ticket_label.pack(fill='x', padx=10)

        # Create a label to display price for the activity
        price_text = ""
        if activity['name'] == "Escape Penang":
            price_text = "RM 155"
        elif activity['name'] == "The Top Penang":
            price_text = "RM 9"
        elif activity['name'] == "Entopia Penang":
            price_text = "RM 40"
        elif activity['name'] == "Penang Hill":
            price_text = "RM 10"

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
        ppl_image = Image.open("ppl2.jpg")
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
        self.date_calendar = Calendar(buy_tic_frame4, locale='en_US', font="Arial 7", date_pattern='dd/MM/yyyy', selectmode='day', mindate=datetime.date.today(),)
        self.date_calendar.pack(fill='x', padx=25)

        # Create a button to book tickets
        book_button = ttk.Button(buy_tic_frame2, text="Book Tickets", style='TButton',
                                 command=lambda: self.show_payment_page(activity, image_path, ticket_count))
        book_button.pack(padx=20, pady=5)

        # blank space
        blank_label = tk.Label(buy_tic_frame3, bg='white')
        blank_label.pack(fill='x')

        # Create a button to go back to the ticket_page
        back_button = ttk.Button(details_frame, text="Back", command=self.ticket_page, style='TButton')
        back_button.pack(pady=10)

    def show_payment_page(self, activity, image_path, ticket_count):
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

        # Calculate the total amount (assuming a fixed price per ticket)
        ticket_price = ""
        if activity['name'] == "Escape Penang":
            ticket_price = 155
        elif activity['name'] == "The Top Penang":
            ticket_price = 9
        elif activity['name'] == "Entopia Penang":
            ticket_price = 40
        elif activity['name'] == "Penang Hill":
            ticket_price = 10
        total_amount = ticket_price * int(ticket_count.get())

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

        selected_date_label2 = tk.Label(x_box, text=self.date_calendar.get_date(), font=("Lato", 14), fg='black',
                                        bg='white')
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
        card_image = Image.open("card.png")
        card_image = card_image.resize((290, 190))
        card_image = ImageTk.PhotoImage(card_image)

        card_image_label = tk.Label(y_info_box2, image=card_image, bg='white')
        card_image_label.image = card_image
        card_image_label.grid(row=0, column=0, sticky='w', padx=10)

        # Create labels and entry widgets for user input
        input_labels = ["Name:", "Email:", "Phone Number:", "Card Number:", "Cardholder Name:", "Date (MM/YY)","CCV"]
        entry_widgets = []

        for i, label_text in enumerate(input_labels):
            label = tk.Label(y_info_box3, text=label_text, font=("Lato", 14), fg='black', bg='white', anchor='w')
            label.grid(row=i, column=1, sticky='w', padx=10)
            entry = tk.Entry(y_info_box3, font=("Lato", 14))
            entry.grid(row=i, column=2, sticky='w', padx=10)
            entry_widgets.append(entry)

        # Create a "Confirm Payment" button (initially disabled)
        confirm_button = ttk.Button(y_info_box3, text="Confirm Payment", style='TButton',
                                    command=lambda: self.confirm_payment(entry_widgets))
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

        # Add event handlers for formatting phone number and card number
        entry_widgets[2].bind("<KeyRelease>",
                              lambda event, widget=entry_widgets[2]: self.format_phone_number(event, widget))
        entry_widgets[3].bind("<KeyRelease>",
                              lambda event, widget=entry_widgets[3]: self.format_card_number(event, widget))

    def confirm_payment(self, entry_widgets):
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
            self.show_error_message("Error", "Please provide a valid 32-digit card number.")
        elif not cardholder_name:
            self.show_error_message("Error", "Please provide the cardholder's name.")
        elif not re.match("^[A-Za-z]+( [A-Za-z]+)*$", cardholder_name):
            self.show_error_message("Error", "Cardholder name must contain only alphabetic characters.")
        elif not date or not re.match(date_pattern, date):
            self.show_error_message("Error", "Invalid date format. Please use MM/YY.")
        elif not ccv or not re.match(ccv_pattern, ccv):
            self.show_error_message("Error", "Please provide a valid CCV (3 digits).")
        else:
            # Reset the whole page
            self.clear_content_frame()
            # Reset the vertical scrollbar to the top
            self.canvas.yview_moveto(0)

            details_frame = tk.Frame(self.content_frame, bg='white', padx=570, pady=200)
            details_frame.pack(fill='x', anchor='center')

            # Create a centered box (Frame) with a shadow effect
            center_box = tk.Frame(details_frame, bg='white', padx=20, pady=20, )
            center_box.pack(fill='x')

            success_image = Image.open("success.jpg")
            success_image = success_image.resize((140, 100))
            success_image = ImageTk.PhotoImage(success_image)

            # Create a label to display the resized image
            success_image_label = tk.Label(center_box, image=success_image, bg='white')
            success_image_label.image = success_image
            success_image_label.pack()

            # Text under the image
            text_label = tk.Label(center_box, text="Payment Successful!", font=("Lato", 20), fg='Black', bg='white')
            text_label.pack()

            # Send email
            self.send_payment_confirmation_email(entry_widgets)

    def send_payment_confirmation_email(self, entry_widgets):
        smtp_port = 587  # Standard secure SMTP port
        smtp_server = "smtp.gmail.com"  # Google SMTP Server
        email_from = "zixin2040@gmail.com"
        pswd = "kwqj qfeo aniu yzzk"
        email_list = ["p23014975@student.newinti.edu.my", "p23015069@student.newinti.edu.my", "p23015080@student.newinti.edu.my", "p23015143@student.newinti.edu.my"]  # Replace the email by fetching the email from the database
        subject = "Payment Confirmation"

        for person in email_list:
            order_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            body = f"Thank you for your payment! Your order ID is: {order_id}"

            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = person
            msg['Subject'] = subject

            # Attach the body of the message
            msg.attach(MIMEText(body, 'plain'))

            filename = "thx.jpg"

            # Open the file in python as a binary
            attachment = open(filename, 'rb')  # r for read and b for binary

            # Encode as base 64
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
            msg.attach(attachment_package)

            # Cast as string
            text = msg.as_string()

            try:
                TIE_server = smtplib.SMTP(smtp_server, smtp_port)
                TIE_server.starttls()
                TIE_server.login(email_from, pswd)

                print(f"Sending email to: {person}...")
                TIE_server.sendmail(email_from, person, text)
                print(f"Email sent to: {person}")
            except Exception as e:
                print(f"Error sending email to {person}: {e}")
            finally:
                TIE_server.quit()

    def show_error_message(self, title, message):
        # You can implement a message box to show the error message
        # Here's a simple example using the tkinter messagebox:
        messagebox.showerror(title, message)

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

        # Define the shopping names and corresponding image paths
        activities = [
            {"name": "Cendul", "image_path": "cendul4.jpg"},
            {"name": "Nasi Kandar", "image_path": "nasi kandar4.jpg"},
            {"name": "Laksa", "image_path": "laksa4.jpg"},
            {"name": "Nasi Lemak", "image_path": "nasilemak4.jpg"},
            {"name": "Nyonya Koay", "image_path": "nyonya4.jpg"},
            {"name": "Curry Mee", "image_path": "currymee4.jpg"}
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the shopping image
            food_image = Image.open(activity["image_path"])
            food_image = food_image.resize((240, 170))  # Adjust the size as needed
            food_image = ImageTk.PhotoImage(food_image)

            # Create a frame to hold both the image and information labels with an outline
            food_frame = tk.Frame(food_label1, bg='white', bd=1, relief="solid")
            food_frame.grid(row=i // 3, column=i % 3, padx=40, pady=20)

            # Create the shopping image label inside the frame
            food_image_label = tk.Label(food_frame, image=food_image)
            food_image_label.image = food_image
            food_image_label.pack()

            # Create a frame to hold both labels and the button vertically
            food_info_frame1 = tk.Frame(food_frame, bg='white')  # No need for a border here
            food_info_frame1.pack(fill='x', expand=True)

            # Create north_info1 inside the info frame
            food_info1 = tk.Label(food_info_frame1, text=f"    {activity['name']}", font=("Lato", 12), fg='Black',
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

        # Check the shopping_name and set the appropriate image path
        image_path = ""
        if activity['name'] == "Cendul":
            image_path = "cendul1.png"
        elif activity['name'] == "Nasi Kandar":
            image_path = "nasikandar1.png"
        elif activity['name'] == "Laksa":
            image_path = "laksa1.png"
        elif activity['name'] == "Nasi Lemak":
            image_path = "nasilemak1.png"
        elif activity['name'] == "Nyonya Koay":
            image_path = "nyonya1.png"
        elif activity['name'] == "Curry Mee":
            image_path = "currymee1.png"

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"     Details for {activity['name']}", font=("Lato", 18),
                                 fg='Black', bg='white', anchor='w', padx=213)
        details_label.pack(fill='x')

        # Create a frame to display details and additional information
        details_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
        details_frame.pack(fill='x')

        # Load and resize the activity image for the details page
        food_image = Image.open(image_path)
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

        # Create a label to display information for the activity
        if activity['name'] == "Cendul":
            name_text = "Penang Road Famous Teochew Cendol "
        elif activity['name'] == "Nasi Kandar":
            name_text = "Hameediyah Restaurant Penang"
        elif activity['name'] == "Laksa":
            name_text = "Penang Road Famous Laksa"
        elif activity['name'] == "Nasi Lemak":
            name_text = "Rasa Rasa 回味"
        elif activity['name'] == "Nyonya Koay":
            name_text = "Moh Teng Pheow Nyonya Koay"
        elif activity['name'] == "Curry Mee":
            name_text = "Air Itam Sister Curry Mee"

        # Create a label to display information for the shopping
        info_text = ""
        if activity['name'] == "Cendul":
            info_text = "Penang Road Famous Teochew Chendul is an iconic cendol stall located on Keng Kwee Street, near Penang Road junction. It's famous for its cendol  and other offerings, established in 1936 by Mr. Tan Chong Kim's father. This stall, despite widespread availability, maintains its immense popularity, often with long queues." \
                        "\n\nMonday - Sunday  10 AM-9.30 PM" \
                        "\n\n\u27A4    27-29, Lebuh Keng Kwee, George Town, 10100 George Town, Pulau Pinang"
        elif activity['name'] == "Nasi Kandar":
            info_text = "Hameediyah Restaurant is located in George Town, Penang, Malaysia, and is renowned for its local cuisine. It's a beloved spot for locals and visitors alike. It's one of Penang's oldest Nasi Kandar restaurants, making it a significant part of the local culinary heritage. Hameediyah Restaurant is located on Campbell Street in Georgetown, Penang, and has been recognized for its traditional Nasi Kandar dishesIt's not only a local favorite but also popular among tourists for its authentic Malaysian flavors." \
                        "\n\nMonday-Sunday  10:00am-10:00pm" \
                        "\n\n\u27A4  164 A, Lebuh Campbell, street, 10100 George Town, Pulau Pinang."
        elif activity['name'] == "Laksa":
            info_text = "Penang Road Famous Laksa is a renowned spicy noodle soup in Penang, Malaysia. It features rice noodles in a tangy fish-based broth with shrimp paste and various garnishes. The dish is known for its unique flavors and can be found at the original stall on Penang Road and other locations throughout Penang." \
                        "\n\nWednesday                  closed" \
                        "\nThursday-Tuesday  9 AM-5.30 PM" \
                        "\n\n\u27A4  Sunway Carnival Mall 3068, Jalan Todak Pusat Bandar Seberang Jaya, Seberang Jaya, 13700 Perai, Pulau Pinang"
        elif activity['name'] == "Nasi Lemak":
            info_text = "Rasa Rasa 回味 is a well-known restaurant located on Chulia Street Ghaut in Georgetown, Penang. It offers Peranakan cuisine, known for its blend of Chinese and Malay flavors. The restaurant's address is 59 Gat Lebuh Chulia, and it's recognized in the 2023 MICHELIN Guide as a Bib Gourmand restaurant, emphasizing its good quality and value. The menu includes dishes like Nasi Lemak, and it's known for its delicious food and friendly owners. Operating hours are from 8:30 am to 3:00 pm, except on Tuesdays and Wednesdays when it's closed. It's a popular spot for those looking to savor authentic Peranakan cuisine in Georgetown, Penang." \
                        "\n\nWednesday- closed  " \
                        "\nTuesday,Thursday,Friday  8.30 AM-3PM     Saturday & Sunday      9AM - 3PM" \
                        "\n\n\u27A4  59, Gat Lebuh Chulia, George Town, 10300 George Town, Pulau Pinang."
        elif activity['name'] == "Nyonya Koay":
            info_text = "In 1933, the owner’s father founded a factory specialising in kuih, a broad term referring to various local cakes, dumplings, pudding and pastries. In 2016, the owner opened a sit-down restaurant behind the factory for guests to try their freshly made kuih, such as kuih lapis, kuih talam, ang koo, and Nyonya chang, alongside a few Nyonya dishes. Head to the rustic patio with exposed brick walls and a vine-covered pergola for some al fresco fun." \
                        "\n\nMonday                  closed" \
                        "\nTuesday - Sunday  10:30 AM-5 PM" \
                        "\n\n\u27A4  Jalan Masjid, Off Lebuh Chulia, George Town, 10200, Malaysia"
        elif activity['name'] == "Curry Mee":
            info_text = "Air Itam Sister Curry Mee is a popular Malaysian dish from Air Itam, Penang. It features yellow egg noodles and rice vermicelli in a flavorful curry broth with sambal belacan (spicy shrimp paste). Topped with tofu puffs, cockles, bean sprouts, and cuttlefish, it's garnished with mint leaves, chili, and lime. It is often served with pork blood cubes and pig skin on the side. The Sister Curry Mee stall near Kek Lok Si Temple is renowned for this authentic and delicious dish. A must-try in Penang!" \
                        "\n\nTuesday              closed" \
                        "\nWednesday - Monday  7:30 AM-1 PM" \
                        "\n\n\u27A4  612-T, Jalan Air Itam, Pekan Ayer Itam, 11500 Ayer Itam, Pulau Pinang"

        name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        name_label.pack(fill='both', expand=True, padx=25, pady=10)
        info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        info_label.pack(fill='both', expand=True, padx=25, pady=10)

        blank_label = tk.Label(details_frame, bg='white')
        blank_label.pack(fill='x')

        # Create a button to go back to the shopping malls page
        back_button = ttk.Button(details_frame, text="Back", command=self.food_page, style='TButton')
        back_button.pack(pady=20)

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

        # Define the shopping names and corresponding image paths
        activities = [
            {"name": "Queensbay Mall", "image_path": "queensbay.jpg"},
            {"name": "Gurney Paragon", "image_path": "gurney1.jpg"},
            {"name": "Straits Quay Retail Marina", "image_path": "straitsquey1.jpg"},
            {"name": "1st Avenue", "image_path": "1stavenue1.jpg"},
            {"name": "Gurney Plaza", "image_path": "gurneyplaza1.jpg"},
            {"name": "Prangin Mall", "image_path": "pranginmall1.jpg"},
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the shopping image
            shopping_image = Image.open(activity["image_path"])
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

        # Check the shopping_name and set the appropriate image path
        image_path = ""
        if activity['name'] == "Queensbay Mall":
            image_path = "queensbay2.jpg"
        elif activity['name'] == "Gurney Paragon":
            image_path = "gurneyparagon2.png"
        elif activity['name'] == "Straits Quay Retail Marina":
            image_path = "straitsquey2.png"
        elif activity['name'] == "1st Avenue":
            image_path = "1stavenue2.jpg"
        elif activity['name'] == "Gurney Plaza":
            image_path = "gurneyplaza2.png"
        elif activity['name'] == "Prangin Mall":
            image_path = "pranginmall2.png"

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"     Details for {activity['name']}", font=("Lato", 18),
                                 fg='Black', bg='white', anchor='w', padx=215, pady=10)
        details_label.pack(fill='x')

        # Create a frame to display details and additional information
        details_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
        details_frame.pack(fill='x')

        # Load and resize the activity image for the details page
        shopping_image = Image.open(image_path)
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

        # Create a label to display information for the activity
        if activity["name"] == "Queensbay Mall":
            name_text = "About Queensbay Mall"
        elif activity["name"] == "Gurney Paragon":
            name_text = "About Gurney Paragon"
        elif activity["name"] == "Straits Quay Retail Marina":
            name_text = "About Straits Quay Retail Marina"
        elif activity["name"] == "1st Avenue":
            name_text = "About 1st Avenue"
        elif activity["name"] == "Gurney Plaza":
            name_text = "About Gurney Plaza"
        elif activity["name"] == "Prangin Mall":
            name_text = "About Prangin Mall"

        # Create a label to display information for the shopping
        info_text = ""
        if activity["name"] == "Queensbay Mall":
            info_text = "Queensbay Mall is a prominent shopping and entertainment destination located in Bayan Lepas, Penang, Malaysia. Opened for business on December 1, 2006, it is the largest and most modern shopping mall in Penang. With a sprawling area of 73 acres, Queensbay Mall boasts a wide range of retail stores, including a Jusco department store, junior anchors, and numerous retail merchants. It offers a diverse shopping experience, entertainment options, and dining choices, making it a preferred destination for both locals and tourists." \
                        "\n\nMonday - Sunday  10:30am - 10:30pm" \
                        "\n\n\u27A4   Queensbay Mall, 100, Persiaran Bayan Indah, 11900 Bayan Lepas, Pulau Pinang"
        elif activity["name"] == "Gurney Paragon":
            info_text = "Gurney Paragon is a prominent shopping and lifestyle destination located in George Town, Penang, Malaysia. This upscale mall offers a diverse range of shops, from high-end fashion boutiques to popular international brands. Visitors can also enjoy a variety of dining options, including restaurants, cafes, and food courts. Gurney Paragon is known for its modern and stylish architecture, making it a favorite among locals and tourists. It's a go-to place for shopping, dining, and entertainment in Penang." \
                        "\n\nMonday-Sunday  10:00am-10:00pm" \
                        "\n\n\u27A4  163d, Gurney Dr, 10250 George Town, Penang"
        elif activity["name"] == "Straits Quay Retail Marina":
            info_text = "Straits Quay Retail Marina is a picturesque and upscale shopping and lifestyle destination located in Tanjung Tokong, Penang, Malaysia. It offers a unique combination of shopping, dining, and leisure experiences with a stunning waterfront setting. Visitors can explore a variety of boutique shops, enjoy a diverse range of international and local cuisine at the waterfront promenade, and take in scenic views of the marina. Straits Quay often hosts events and activities, making it a popular choice for both residents and tourists looking for a leisurely day out. Its charming atmosphere and coastal location make it a notable attraction in Penang's retail and dining scene." \
                        "\n\nMonday-Sunday  10:00am-10:00pm" \
                        "\n\n\u27A4  Jalan Seri Tanjung Pinang 10470 Tanjong Tokong, Penang Malaysia"
        elif activity["name"] == "1st Avenue":
            info_text = "1st Avenue Mall is a prominent shopping center situated in the heart of George Town, Penang, Malaysia. This multi-story mall is a popular destination for both locals and tourists, offering a wide range of retail stores, dining options, and entertainment facilities. It features well-known brands, fashion boutiques, electronics shops, and more. Additionally, the mall is home to a food court and various restaurants serving diverse cuisines. With its convenient location and diverse offerings, 1st Avenue Mall is a go-to place for shopping and leisure in Penang." \
                        "\n\nMonday-Sunday  10:00am-10:00pm" \
                        "\n\n\u27A4  182, Jalan Magazine, 10300 George Town, Pulau Pinang."
        elif activity["name"] == "Gurney Plaza":
            info_text = "Gurney Plaza is a prominent shopping mall located in George Town, Penang, Malaysia. It is known for its diverse range of retail outlets, including international brands, fashion boutiques, and electronics stores. Shoppers can also enjoy a wide selection of dining options, from local delicacies to international cuisine. The mall provides a convenient and enjoyable shopping experience, making it a popular destination for both residents and tourists in Penang. Additionally, Gurney Plaza often hosts various events and activities, adding to its appeal as a lifestyle and entertainment hub in the region." \
                        "\n\nMonday-Sunday  10:00am-10:00pm" \
                        "\n\n\u27A4   170, Gurney Dr, Pulau Tikus, 10250 George Town, Penang"
        elif activity["name"] == "Prangin Mall":
            info_text = "Prangin Mall, located in the heart of George Town, Penang, is a popular shopping and entertainment destination. This multi-story mall offers a wide range of retail stores, dining options, and entertainment facilities. Shoppers can explore numerous shops selling fashion, electronics, and more. The mall is known for its accessibility and central location, making it a convenient choice for both locals and tourists. Prangin Mall also features a cinema, adding to its entertainment appeal. Whether you're looking for shopping or leisure, Prangin Mall is a vibrant hub in Penang." \
                        "\n\nMonday-Sunday  10:00am-10:00pm" \
                        "\n\n\u27A4   Prangin Mall, No 33, Jalan Dr Lim Chwee Leong, George Town, 10100 George Town, Pulau Pinang"

        name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        name_label.pack(fill='both', expand=True, padx=25, pady=10)
        info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        info_label.pack(fill='both', expand=True, padx=25, pady=10)

        blank_label = tk.Label(details_frame, bg='white')
        blank_label.pack(fill='x')

        # Create a button to go back to the shopping malls page
        back_button = ttk.Button(details_frame, text="Back", command=self.shopping_page, style='TButton')
        back_button.pack(pady=20)

    def transport_page(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a title label for Shopping Malls
        transport_label = tk.Label(self.content_frame, text="   Tranport", font=("Lato", 18),
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

        # Define the shopping names and corresponding image paths
        activities = [
            {"name": "Car Renting", "image_path": "Car Renting.png"},
            {"name": "Rapid Bus", "image_path": "Rapid Bus.png"},
            {"name": "Ferry", "image_path": "Ferry.png"},
            {"name": "Grab Car", "image_path": "Grab Car.png"},
            {"name": "Taxi", "image_path": "Taxi.png"},
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the shopping image
            transport_image = Image.open(activity["image_path"])
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

        # Check the shopping_name and set the appropriate image path
        image_path = ""
        if activity['name'] == "Car Renting":
            image_path = "CarRenting2.png"
        elif activity['name'] == "Rapid Bus":
            image_path = "RapidBus2.png"
        elif activity['name'] == "Ferry":
            image_path = "Ferry2.png"
        elif activity['name'] == "Grab Car":
            image_path = "GrabCar2.png"
        elif activity['name'] == "Taxi":
            image_path = "Taxi2.png"

        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"Details for {activity['name']}", font=("Lato", 18),
                                 fg='Black', bg='white', anchor='w', padx=215, pady=10)
        details_label.pack(fill='x')

        # Create a frame to display details and additional information
        details_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
        details_frame.pack(fill='x')

        # Load and resize the activity image for the details page
        transport_image = Image.open(image_path)
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

        # Create a label to display information for the activity
        if activity["name"] == "Car Renting":
            name_text = "\nAbout Car Renting"
        elif activity["name"] == "Rapid Bus":
            name_text = "\nAbout Rapid Bus"
        elif activity["name"] == "Ferry":
            name_text = "\nAbout Ferry"
        elif activity["name"] == "Grab Car":
            name_text = "\nAbout Grab Car"
        elif activity["name"] == "Taxi":
            name_text = "\nAbout Taxi"

        # Create a label to display information for the shopping
        info_text = ""
        if activity["name"] == "Car Renting":
            info_text = "Having a reliable and budget-friendly car rental service. Economy cars are available. Make renting a vehicle more accessible to everyone, so you can go on your travels worry-free and within your budget. Check out their services today!" \
                        "\n\n\nCar Type\t\t\t\t\t\t\tPrices" \
                        "\n\n\nPerodua Bezza AT\t\t\t\tRM160 / DAY\t\t\t RM950 / WEEK" \
                        "\n\n\nPerodua Myvi 1.3 \t\t\t\tRM140/ DAY\t\t\t RM800 / WEEK" \
                        "\n\n\nNew Model Myvi\t\t\t\tRM180/ DAY\t\t\tRM1200 / WEEK\n"
        elif activity["name"] == "Rapid Bus":
            info_text = "Rapid bus, establised in 2007, is one of the most popular transport among tourist and also local in Penang. Although there are lots choices of transport, tourists and local will also choose Rapid Bus because of its low price. Having the air-conditioned internal environment, special attention are also given to the Impaired mobility – Orang Kurang Upaya (OKU), elderly, pregnant women, and children at all times." \
                        "\n\n\nLocation\t\t\t\t\tOperating Hours" \
                        "\n\nLorong Kulit\t\t\t\tMonday - Friday 8am-5pm" \
                        "\n\nTerminal B Weld Quay\t\t\tMonday - Saturday 8am-8pm" \
                        "\n\nKomtar\t\t\t\t\tMonday - Saturday 8am-8pm" \
                        "\n\nBukit Jambul Hub\t\t\t\tMonday - Saturday 11am- 7pm" \
                        "\n\nPenang Sentral\t\t\t\tMonday - Saturday 11am- 7pm" \
                        "\n\nHentian Rayat Parit Buntar\t\t\tMonday - Saturday 11am- 7pm" \
                        "\n\nTerminal Bus Jalan Petri, Sungai Petani\t\t25th - 5th of every month 11am - 7pm\n"
        elif activity["name"] == "Ferry":
            info_text = "The ferry ride are available from the Penang island to the mainland and vice versa. Yes, you did not hear wrong, bicycle and motorcycles are allowed for passengers to bring along to the ferry! The ferry take less than 10 minutes to travel over to Swettenham Pier in Georgetown. Departures are between every 30 minutes (peak hours) to every 60 minutes (off-peak)." \
                        "\n\n\nTicket\t\t\t\t\t\tPrices" \
                        "\n\nChildren below 12 years old\t\t\t\tRM 1 / PER TRIP" \
                        "\n\nAdult\t\t\t\t\t\tRM 2 / PER TRIP" \
                        "\n\nBicycle\t\t\t\t\t\tRM 2 / PER TRIP" \
                        "\n\nMotorcycle\t\t\t\t\tRM 2.5 / PER TRIP\n"
        elif activity["name"] == "Grab Car":
            info_text = "Grab Car is a reliable taxi service in Penang with private hire, taxi and bus. The Grab Ride-hailing mobile app gives a fare estimate and finds you a ride by just keying in where you are going. There will be upfront pricing for you to know how much your trip will cost excluding tolls and surcharges before you book. Economy to premium car options are available if you are traveling in solo or in group." \
                        "\n\n\nSteps to book a Grab Car :" \
                        "\n\n1. Book a ride by setting your pick up and drop off point and tap Next" \
                        "\n\n2. The app will find you the nearest available driver" \
                        "\n\n3. Track yiur driver by knowing your driver’s details, location, and estimated arrival time" \
                        "\n\n4. Share your ride with your family and friends track your ride, and get to your destination with no worries\n"
        elif activity["name"] == "Taxi":
            info_text = "Taxi service is charging passengers using meter, the cost of trip is known after passengers reach their destination. The services provided by taxi includes airport transfer, shuttle and tour guide. Taking a taxi in Penang is quite affordable, and you can find one easily in busy areas such as the airport, bus stations, big shopping malls, and tourist attractions. However, as there are varying levels of reliability, quality, and cost, we recommend using reputable companies for your Penang taxi transfers. This is because, although all taxis in Penang are required by law to operate with a taximeter, very few of them do. So, when hailing a local taxi from the street, make sure you are prepared to haggle with the driver by having a rough estimate of the fare in mind before getting in the vehicle." \
                        "\n\n\nCondition\t\t\t\t\t\tPrices" \
                        "\n\nTaxi Starting Fare\t\t\t\t\tRM 5.50" \
                        "\n\nCost per 1 km\t\t\t\t\tRM 1.80" \
                        "\n\n1-hour Waiting\t\t\t\t\tRM 30.00" \
                        "\n\nhours of 00:00 and 06:00\t\t\t\tSurcharge of 50 %\n"

        name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        name_label.pack(fill='both', expand=True, padx=25, pady=10)
        info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        info_label.pack(fill='both', expand=True, padx=25, pady=10)

        blank_label = tk.Label(details_frame, bg='white')
        blank_label.pack(fill='x')

        # Create a button to go back to the shopping malls page
        back_button = ttk.Button(details_frame, text="Back", command=self.transport_page, style='TButton')
        back_button.pack(pady=20)

    def market_page(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a title label for "Market Everyday"
        market_label = tk.Label(self.content_frame, text="Market Everyday", font=("Lato", 18),fg='Black', bg='white', anchor='w',padx=240,pady=20)
        market_label.pack(fill='x')

        market_label = tk.Label(self.content_frame, bg='white')
        market_label.pack(fill='x')

        market_label = tk.Frame(market_label, bg='white')
        market_label.pack(fill='x', padx=200)
        market_label = tk.Frame(market_label, bg='white')
        market_label.pack(fill='x')

        # Define the market names and corresponding image paths
        activities = [
            {"name": "Cecil Street Market", "image_path": "cecilmarket1.jpg"},
            {"name": "Campbell Street Wet Market", "image_path": "campbellmarket2.jpg"},
            {"name": "Jelutong Market", "image_path": "jelutongmarket1.jpg"},
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, activity in enumerate(activities):
            # Load and resize the market image
            market_image = Image.open(activity["image_path"])
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
            market_button = ttk.Button(market_frame,  text="Details",
                                         command=lambda a=activity: self.open_market_details_page(a, market2),
                                       style='TButton')
            market_button.pack(fill='x', expand=True)
            self.buttons.append(market_button)

        # Create a title label for "Market on Specific Day"
        specific_day_label = tk.Label(self.content_frame, text="Market on Specific Day", font=("Lato", 18),
                                      fg='Black', bg='white', anchor='w',padx=240,pady=20)
        specific_day_label.pack(fill='x')



        # Define the second set of market names and corresponding image paths
        second_market_list = [
            {"name": "Batu Feringghi Night Market", "image_path": "batuferringhimarket.jpg"},
            {"name": "Farlim Wednesday Night Market", "image_path": "farlimnightmarket1.jpg"},
        ]

        # Create a frame to hold the second set of markets
        second_market_frame = tk.Label(self.content_frame, bg='white')
        second_market_frame.pack(fill='x')

        second_market_frame = tk.Frame(second_market_frame, bg='white')
        second_market_frame.pack(fill='x', padx=200)
        second_market_frame = tk.Frame(second_market_frame, bg='white')
        second_market_frame.pack(fill='x')

        for i, market2 in enumerate(second_market_list):
            # Load and resize the market image for the second set
            market_image = Image.open(market2["image_path"])
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
            market_button = ttk.Button(market_frame,  text="Details",
                                         command=lambda b=market2: self.open_market_details_page(b, market2),
                                       style='TButton')
            market_button.pack(fill='x', expand=True)
            self.buttons.append(market_button)

    def open_market_details_page(self, activity, market2):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Check the shopping_name and set the appropriate image path
        image_path = ""
        if activity['name'] == "Cecil Street Market":
            image_path = "cecilmarket2.jpg"
        elif activity['name'] == "Campbell Street Wet Market":
            image_path = "campbellmarket1.jpg"
        elif activity['name'] == "Jelutong Market":
            image_path = "jelutongmarket2.jpg"
        elif market2['name'] == "Batu Feringghi Night Market":
            image_path = "batuferringhimarket2.jpeg"
        elif market2['name'] == "Farlim Wednesday Night Market":
            image_path = "farlimnightmarket2.jpg"


        # Create a label for the details page content
        details_label = tk.Label(self.content_frame, text=f"     Details for {activity['name']}", font=("Lato", 18),
                                 fg='Black', bg='white', anchor='w', padx=215, pady=10)
        details_label.pack(fill='x')

        # Create a frame to display details and additional information
        details_frame = tk.Frame(self.content_frame, bg='white', width=900, height=600)
        details_frame.pack(fill='x')

        # Load and resize the activity image for the details page
        market_image = Image.open(image_path)
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

        # Create a label to display information for the activity
        if activity["name"] == "Cecil Street Market":
            name_text = "Cecil Street Market"
        elif activity["name"] == "Campbell Street Wet Market":
            name_text = "About Campbell Street Wet Market"
        elif activity["name"] == "Jelutong Market":
            name_text = "About Jelutong Market"
        elif market2['name'] == "Batu Feringghi Night Market":
            name_text = "About Batu Feringghi Night Market"
        elif market2['name'] == "Farlim Wednesday Night Market":
            name_text = "About Farlim Wednesday Night Market"

        # Create a label to display information for the shopping
        info_text = ""
        if activity["name"] == "Cecil Street Market":
            info_text = "Cecil Street market is known to be one of the biggest food courts in George Town, Penang.The official name of this market is called Cecil Street Market, but the locals here know it better as the 7th Street Market (which translates to 七条路巴刹 in Chinese or Pasar Jalan Tujuh in Malay). Probably it has something to do with the fact that it’s exactly seven streets away from the Komtar Tower" \
                        "\n\nMonday - Sunday  7:30am - 7:00pm" \
                        "\n\n\u27A4   40-48, Lebuh Cecil, 10300 George Town, Pulau Pinang"
        elif activity["name"] == "Campbell Street Wet Market":
            info_text = "Campbell Street Wet Market is a historic and bustling market located in George Town, Penang. It serves as a vibrant hub for locals and visitors to shop for fresh produce, seafood, meats, vegetables, and a wide variety of local ingredients. This market is well-known for its traditional atmosphere and is one of the oldest markets in Penang. Visitors can immerse themselves in the sights, sounds, and flavors of Penang's culinary culture by exploring the stalls and interacting with friendly local vendors. It's a must-visit destination for those looking to experience the authentic local market scene in Penang." \
                        "\n\nMonday - Sunday  7:00am - 12:00pm" \
                        "\n\n\u27A4  4, Lebuh Campbell, George Town, 10100 George Town, Pulau Pinang"
        elif activity["name"] == "Jelutong Market":
            info_text = "Jelutong Market is a bustling marketplace located in the town of Jelutong, Penang, Malaysia. It's a popular spot for locals and visitors to shop for fresh produce, street food, and a variety of goods. The market offers a vibrant and authentic Penang experience, with stalls selling fruits, vegetables, seafood, and other daily necessities. Additionally, Jelutong Market is renowned for its street food vendors, serving up delicious local dishes, making it a favorite food destination. It's a great place to immerse yourself in the local culture and enjoy the flavors of Penang." \
                        "\n\nMonday - Sunday  5:30am - 11:00pm" \
                        "\n\n\u27A4 94, Lrg Batu, Taman Jelutong, 11600 George Town, Pulau Pinang"
        elif market2['name'] == "Batu Feringghi Night Market":
            info_text = "Batu Ferringhi Night Market is a vibrant and popular open-air market located in the coastal town of Batu Ferringhi, Penang, Malaysia. It operates in the evenings, offering a wide array of stalls selling an assortment of items, including clothing, accessories, handicrafts, souvenirs, and local artwork. This market is a must-visit for tourists looking for a fun and lively shopping experience while enjoying the sea breeze. It's an excellent place to pick up gifts, mementos, and savor the local street food that lines the market, creating a lively and colorful atmosphere." \
                        "\n\nMonday - Sunday  7:00pm- 12:00am" \
                        "\n\n\u27A4 Jalan Pantai Batu, Taman Pantai Batu, 11200 Tanjong Bungah, Pulau Pinang"
        elif market2['name'] == "Farlim Wednesday Night Market":
            info_text = "The Farlim Wednesday Night Market is a popular weekly market located in Farlim, Penang, Malaysia. Held every Wednesday evening, it offers a wide range of goods, including fresh produce, clothing, accessories, and various street food options. The market is a vibrant and bustling hub for both locals and tourists to enjoy shopping, explore local culture, and savor delicious street food, making it a lively midweek destination in Penang." \
                        "\n\nWednesday  5:00pm - 11:00pm" \
                        "\nThursday- Tuesday     closed" \
                        "\n\n\u27A4 27-75, Medan Angsana, Bandar Baru Ayer Itam, 11500 Ayer Itam, Pulau Pinang"


        name_label = tk.Label(info_frame, text=name_text, font=("Lato", 14), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        name_label.pack(fill='both', expand=True, padx=25, pady=10)
        info_label = tk.Label(info_frame, text=info_text, font=("Lato", 12), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        info_label.pack(fill='both', expand=True, padx=25, pady=10)

        blank_label = tk.Label(details_frame, bg='white')
        blank_label.pack(fill='x')

        # Create a button to go back to the shopping malls page
        back_button = ttk.Button(details_frame, text="Back", command=self.market_page, style='TButton')
        back_button.pack(pady=20)

    # Inside your App class, where you create an instance of the Map class:
    def map_page(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create an instance of the Map class
        map_instance = Map(self.content_frame)
        map_instance.button()


    def search_activities(self, keyword):
        # Perform a search based on the keyword
        self.search_results = []  # Clear previous search results

        # Define the activities list with sample data
        activities = [
            {"name": "Escape Penang", "image_path": "escape.jpg"},
            {"name": "The Top Penang", "image_path": "thetop.jpg"},
            {"name": "Entopia Penang", "image_path": "entopia.jpg"},
            {"name": "Penang Hill", "image_path": "railway.jpg"},
            {"name": "Street Art", "image_path": "StreetArt1.jpg"},
            {"name": "Clan Jetties", "image_path": "clan.jpg"},
            {"name": "Kek Lok Si", "image_path": "KekLokSiTemple.jpg"},
            {"name": "Peranakan Mansion", "image_path": "PeranakanMansion.jpg"},
            {"name": "Upside Down Museum", "image_path": "UpsideDownMuseum.jpg"},
            {"name": "Dark Mansion", "image_path": "darkmansion.jpg"},
            {"name": "ATV Ride", "image_path": "bike.jpg"},
            {"name": "Countryside Stables Penang", "image_path": "horse.jpg"},
            {"name": "Audi Dream Farm", "image_path": "audi.jpg"},
            {"name": "Cendul", "image_path": "cendul4.jpg"},
            {"name": "Nasi Kandar", "image_path": "nasikandar4.jpg"},
            {"name": "Laksa", "image_path": "laksa4.jpg"},
            {"name": "Nasi Lemak", "image_path": "nasilemak4.jpg"},
            {"name": "Nyonya Koay", "image_path": "nyonya4.jpg"},
            {"name": "Curry Mee", "image_path": "currymee4.jpg"},
            {"name": "Queensbay Mall", "image_path": "queensbay.jpg"},
            {"name": "Gurney Paragon", "image_path": "gurney1.jpg"},
            {"name": "Sunway Carnival Mall", "image_path": "sunwaycarnival.jpg"},
            {"name": "1st Avenue", "image_path": "1stavenue1.jpg"},
            {"name": "Gurney Plaza", "image_path": "gurneyplaza1.jpg"},
            {"name": "Prangin Mall", "image_path": "pranginmall1.jpg"},
            {"name": "Car Renting", "image_path": "Car Renting.png"},
            {"name": "Rapid Bus", "image_path": "Rapid Bus.png"},
            {"name": "Ferry", "image_path": "Ferry.png"},
            {"name": "Grab Car", "image_path": "Grab Car.png"},
            {"name": "Taxi", "image_path": "Taxi.png"},
            # Add more activities as needed
        ]

        for activity in activities:  # Remove 'enumerate' here
            if keyword.lower() in activity["name"].lower():
                self.search_results.append(activity)

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
        for i, activity in enumerate(self.search_results):
            # Load and resize the activity image
            activity_image = Image.open(activity["image_path"])
            activity_image = activity_image.resize((240, 170))  # Adjust the size as needed
            activity_image = ImageTk.PhotoImage(activity_image)
            self.image_references.append(activity_image)

            # Create a frame to hold both the image and information labels with an outline
            activity_frame = tk.Frame(activity_label, bg='white', bd=1, relief="solid")  # Add the border
            activity_frame.grid(row=i // 3, column=i % 3, padx=40, pady=20)
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

            # Place activity_info1 and activity_info2 inside the info frame
            activity_info1.pack(fill='x', expand=True)
            if activity["name"] in ["Escape Penang", "The Top Penang", "Entopia Penang", "Penang Hill"]:
                activity_button = ttk.Button(activity_frame, text="Details",
                                             command=lambda a=activity,
                                                            path=activity["image_path"]: self.open_activity_ticket_page(
                                                 a, path), style='TButton')
                activity_button.pack(fill='x', expand=True)
                self.buttons.append(activity_button)
            elif activity["name"] in ["Street Art", "Clan Jetties", "Kek Lok Si", "Peranakan Mansion",
                                      "Upside Down Museum", "Dark Mansion"]:
                north_info_button1 = ttk.Button(activity_frame, text="Details",
                                                command=lambda a=activity: self.open_north_details_page(a),
                                                style='TButton')
                north_info_button1.pack(fill='x', expand=True)
                self.buttons.append(north_info_button1)
            elif activity["name"] in ["ATV Ride", "Countryside Stables Penang", "Audi Dream Farm"]:
                south_info_button1 = ttk.Button(activity_frame, text="Details",
                                                command=lambda a=activity: self.open_south_details_page(a),
                                                style='TButton')
                south_info_button1.pack(fill='x', expand=True)
                self.buttons.append(south_info_button1)
            elif activity["name"] in ["Cendul", "Nasi Kandar", "Laksa", "Nasi Lemak"]:
                south_info_button1 = ttk.Button(activity_frame, text="Details",
                                                command=lambda a=activity: self.open_food_page(a), style='TButton')
                south_info_button1.pack(fill='x', expand=True)
                self.buttons.append(south_info_button1)
            elif activity["name"] in ["Queensbay Mall", "Gurney Paragon", "Sunway Carnival Mall", "1st Avenue","Gurney Plaza", "Pragin Mall"]:
                shopping_button = ttk.Button(activity_frame, text="Details",
                                             command=lambda a=activity: self.open_shopping_details_page(a),
                                             style='TButton')
                shopping_button.pack(fill='x', expand=True)
                self.buttons.append(shopping_button)
            elif activity["name"] in ["Car Renting", "Rapid Bus", "Ferry", "Grab Car", "Taxi"]:
                transport_button = ttk.Button(activity_frame, text="Details",
                                              command=lambda a=activity, path=activity["image_path"]: self.open_transport_details_page(a, path),
                                              style='TButton')
                transport_button.pack(fill='x', expand=True)
                self.buttons.append(transport_button)

    def create_chatbot(dataset='chatterbot.corpus.english'):
        """
        Create a chatbot with optional training on a specific dataset.

        Args:
            dataset (str): The dataset to train the chatbot on. Defaults to 'chatterbot.corpus.english'.

        Returns:
            ChatBot: The initialized chatbot instance.
        """
        # Create a new chatbot instance
        chatbot = ChatBot('MyChatBot')

        # Create a new trainer for the chatbot
        trainer = ChatterBotCorpusTrainer(chatbot)

        # Train the chatbot on the specified dataset
        trainer.train(dataset)

        return chatbot

    def chat_with_bot(chatbot):
        """
        Engage in a conversation with the chatbot.

        Args:
            chatbot (ChatBot): The initialized chatbot instance.
        """
        print("Bot: Hi, I'm your chatbot. You can start a conversation. Type 'exit' to end the chat.")

        while True:
            user_input = input("You: ")

            if user_input.lower() == 'exit':
                print("Bot: Goodbye!")
                break

            response = chatbot.get_response(user_input)
            print("Bot:", response)

    def open_help_center(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create a title label for "Contact Us" and center it horizontally
        help_center_label = tk.Label(self.content_frame, text="   Contact Us", font=("Lato", 60),
                                  fg='Black', bg='white', anchor='w',padx=500,pady=20)
        help_center_label.pack(fill='x')

        help_center_label = tk.Frame(self.content_frame, bg='white')
        help_center_label.pack(fill='x')

        help_center_label = tk.Frame(help_center_label, bg='white')
        help_center_label.pack(fill='x')
        help_center_label = tk.Frame(help_center_label, bg='white')
        help_center_label.pack(fill='x')

        # Define the activity names and corresponding image paths
        contactus = [
            {"name": "Email Us: penang123@gmail.com", "time": "Monday to Friday (9am to 4pm)",
             "image_path": "email.png"},
            {"name": "Give Feedback", "time": "", "image_path": "feedback.jpg"},  # Removed the feedback option
            {"name": "Ask any information with our chatbot", "time": "", "image_path": "chatbot.jpg"},
        ]

        self.buttons = []  # Create a list to store the buttons

        for i, contactus_item in enumerate(contactus):
            # Load and resize the activity image
            contactus_image = Image.open(contactus_item["image_path"])
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


            # Define a new method to open the chatbot window

    def open_chatbot_window(self, event):
        # Destroy the current frame to clear the content
        self.clear_content_frame()

        # Create a new frame for the chatbot content
        chatbot_frame = tk.Frame(self.content_frame, bg='black')
        chatbot_frame.pack(fill='both', expand=True)

        # You can customize the chatbot content here
        # For example, you can create an entry field and a chat history area
        entry_field = tk.Entry(chatbot_frame)
        chat_history = tk.Text(chatbot_frame)

        # Add the widgets to the chatbot frame
        entry_field.pack(fill='x')
        chat_history.pack(fill='both', expand=True)

        # You can also initialize the chatbot and start a conversation here
        chatbot = self.create_chatbot()
        chat_history.insert(tk.END,
                            "Bot: Hi, I'm your chatbot. You can start a conversation. Type 'exit' to end the chat.\n")

        def send_message():
            user_input = entry_field.get()
            chat_history.insert(tk.END, "You: " + user_input + "\n")
            entry_field.delete(0, tk.END)

            if user_input.lower() == 'exit':
                chat_history.insert(tk.END, "Bot: Goodbye!\n")
                return

            response = chatbot.get_response(user_input)
            chat_history.insert(tk.END, "Bot: " + str(response) + "\n")

        send_button = tk.Button(chatbot_frame, text="Send", command=send_message)
        send_button.pack()

        # You can customize this function to display help content
        print("Opening Help Center")

    def game_page(self):
        # Reset the content frame
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        # Create an instance of the Quiz class
        quiz = Quiz(self.content_frame)

    def on_canvas_configure(self, event):
        # Update the canvas scroll region when the content frame size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()  # Add this line to update idletasks

    def clear_content_frame(self):
        # Destroy all widgets inside the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

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
        profile_image = Image.open('Profile.png')
        profile_image = profile_image.resize((300, 300))
        profile_image = ImageTk.PhotoImage(profile_image)

        # Create the activity image label on the details page
        profile_image_label = tk.Label(profile_details_frame, image=profile_image)
        profile_image_label.image = profile_image
        profile_image_label.grid(row=0, column=2, padx=240, pady=20, rowspan=2)  # Adjust padx, pady as needed

        # Example user information (replace with actual user data)
        user_name_label = tk.Label(profile_details_frame, text="Username: Traveller", font=("Lato", 18),
                                   fg='Black', bg='white', anchor='w')
        user_name_label.grid(row=0, column=3, sticky='w', padx=20, pady=5)

        email_label = tk.Label(profile_details_frame, text="Email Address: travel@gmail.com", font=("Lato", 18),
                               fg='Black', bg='white', anchor='w')
        email_label.grid(row=1, column=3, sticky='w', padx=20, pady=5)

        # Button to manage the account
        # Button to manage the account
        manage_account_button = ttk.Button(profile_details_frame, text="Manage your account",
                                           command=self.manage_account_page,
                                           style='TButton')
        manage_account_button.grid(row=2, column=1, columnspan=2, padx=20, pady=20)  # Adjust column and columnspan

        # Button to view payment history
        view_payment_history_button = ttk.Button(profile_details_frame, text="View Payment History",
                                                 command=self.view_payment_history,
                                                 style='TButton')
        view_payment_history_button.grid(row=3, column=1, columnspan=2, pady=20)

        # Load and resize the logout image
        logout_image = Image.open('logout.png')
        logout_image = logout_image.resize((100, 100))
        logout_image = ImageTk.PhotoImage(logout_image)

        # Create a label for the logout image
        logout_label = tk.Label(profile_details_frame, image=logout_image)
        logout_label.image = logout_image
        logout_label.grid(row=4, column=5, padx=10, pady=10)

        # Bind a callback function to the click event of the logout label
        logout_label.bind("<Button-1>", lambda event: self.open_login_page())

    def view_payment_history(self):
        # Reset the whole page
        self.clear_content_frame()
        # Reset the vertical scrollbar to the top
        self.canvas.yview_moveto(0)

        payment_history_label = tk.Label(self.content_frame, text="Payment History", font=("Lato", 18), fg='Black',
                                         bg='white',
                                         anchor='w', padx=330, pady=20)
        payment_history_label.pack(fill='x')
        payment_history_label = tk.Label(self.content_frame, bg='white')
        payment_history_label.pack(fill='x')

        # Create a frame to display payment history using Treeview
        payment_history_frame1 = tk.Frame(self.content_frame, bg='white', padx=330)
        payment_history_frame1.pack(fill='both', expand=True)
        payment_history_frame = tk.Frame(payment_history_frame1, bg='white', width=900, height=600)
        payment_history_frame.pack(fill='both', expand=True)

        # Create a Treeview widget
        tree = ttk.Treeview(payment_history_frame, columns=("Activity", "Purchase Date", "Quantity", "Total Price"),
                            show="headings", selectmode="none")

        # Define column headings
        tree.heading("Activity", text="Activity")
        tree.heading("Purchase Date", text="Purchase Date")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Total Price", text="Total Price")

        # Set the width of each column (adjust the values as needed)
        tree.column("Activity", width=250)
        tree.column("Purchase Date", width=100)
        tree.column("Quantity", width=300)
        tree.column("Total Price", width=100)

        # Add data to the Treeview (replace with your payment history data)
        payment_history_data = [
            {"activity": "Escape Penang", "purchase_date": "2023-11-01", "quantity": 2, "total_price": "RM 35"},
            {"activity": "The Top Penang", "purchase_date": "2023-10-25", "quantity": 1, "total_price": "RM 9"},
            # Add more payment records as needed
        ]

        for record in payment_history_data:
            tree.insert("", "end", values=(record["activity"], record["purchase_date"],
                                           record["quantity"], record["total_price"]))

        # Add the Treeview to the frame
        tree.pack(fill='both', expand=True)

        # Create a button to go back to the ticket_page
        back_button = ttk.Button(payment_history_frame, text="Back", command=self.open_account,
                                 style='TButton')
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
        save_changes_button = ttk.Button(manage_account_frame, text="Save Changes",
                                         command=lambda: self.validate_changes_and_apply(username_entry.get(),
                                                                                         email_entry.get(),
                                                                                         password_entry.get(),
                                                                                         confirm_password_entry.get()),
                                         style='TButton')
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
        elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@_#$%])[a-zA-Z\d!@_#$%]{5,}$", new_username):
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
            # Check if the username already exists in the database
            user = get_user(new_username)
            if user:
                messagebox.showerror("Validation Failed", "Username already exists.")
            else:
                # Apply changes (e.g., update database)
                update_user_data(new_username, new_email, new_password)
                messagebox.showinfo("Changes Applied", "Your changes have been applied successfully.")

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

        button_1 = tk.Button(frame_left, text="Set Marker", bg='white',command=self.set_marker_event)
        button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        button_2 = tk.Button(frame_left, text="Clear Markers", bg='white',command=self.clear_marker_event)
        button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        map_label = tk.Label(frame_left, text="Tile Server:", anchor="w",bg='white',)
        map_label.grid(row=2, column=0, padx=(20, 0), pady=(10,5))

        # Combobox for selecting map styles
        maps_style = [
            {"name": "OpenStreetMap"},
            {"name": "Google normal"},
            {"name": "Google satellite"}]
        self.map_option_menu = ttk.Combobox(frame_left, values=[maps['name'] for maps in maps_style])
        self.map_option_menu.grid(row=3, column=0, padx=20)
        self.map_option_menu.bind("<<ComboboxSelected>>", self.change_map)

        button_3 = tk.Button(frame_left, text="Google Map", bg='white',command=self.ggmap)
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

        button_5 = tk.Button(frame_right, text="Search", width=10, bg='white',command=self.search_event)
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
        map_frame = HtmlFrame( horizontal_scrollbar="auto", vertical_scrollbar="auto")
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
            marker_x, marker_y = self.map_widget.get_position_on_map(location_info["latitude"], location_info["longitude"])
            if abs(x - marker_x) < 10 and abs(y - marker_y) < 10:
                # Marker clicked, handle your action here
                self.map_widget.set_center(location_info["latitude"], location_info["longitude"])  # Move map to the marker's coordinates
                print(f"Clicked on marker at {location_info['name']} ({location_info['latitude']}, {location_info['longitude']})")
                break

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_map(self, event=None):
        new_map = self.map_option_menu.get()
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_size(width=800, height=600)


class Quiz:
    def __init__(self, parent):
        self.parent = parent
        self.questions = self.generate_questions()
        self.num_questions = 5
        self.current_question = 0
        self.score = 0
        # Create a white canvas to act as a background
        self.canvas = tk.Canvas(parent, bg="white")
        self.shuffle_questions()
        self.display_question()

    def generate_questions(self):
        # Define and return your list of questions here
        questions = [
            {
                #"image_path": "",
                "question": "Penang is located in the Straits of Malacca.",
                "options": ["TRUE", "FALSE"],
                "answer": "TRUE"
            },
            {
                #"image_path": "",
                "question": "What is Penang known for?",
                "options": ["George Town", "Kuala Lumpur", "Ipoh", "Johor Bahru"],
                "answer": "George Town"
            },
            {
                #"image_path": "",
                "question": "Which famous temple is located in Penang?",
                "options": ["Batu Caves", "Kek Lok Si", "Thean Hou Temple", "Sri Mahamariamman Temple"],
                "answer": "Kek Lok Si"
            },
            {
                #"image_path": "",
                "question": "How high is Penang Hill above sea level?",
                "options": ["~600 Meters", "~700 Meters", "~800 Meters", "~900 Meters"],
                "answer": "~800 Meters"
            },
            {
                "image_path": "",
                "question": "Which of the following is \"NOT\" a colour of the flag of Penang?",
                "options": ["Yellow", "White", "Light Blue", "Pink"],
                "answer": "Pink"
            },
            {
                "image_path": "StreetArt1.jpg",
                "question": "This famous street art can be found in ...",
                "options": ["George Town", "Balik Pulau", "Bayan Lepas", "Air Itam"],
                "answer": "George Town"
            },
            {
                "image_path": "KekLokSiTemple.jpg",
                "question": "This famous landmark can be found in ...",
                "options": ["George Town", "Balik Pulau", "Bayan Lepas", "Air Itam"],
                "answer": "Air Itam"
            },
            {
                #"image_path": "",
                "question": "What is the name of the bridge that connects Penang Island to the mainland?",
                "options": ["Penang Bridge", "Sultan Abdul Halim Bridge", "Sultan Iskandar Bridge", "Seri Saujana Bridge"],
                "answer": "Penang Bridge"
            },
            {
                #"image_path": "",
                "question": "Who is the current Chief Minister of Penang?",
                "options": ["Chong Eng", "Chow Kon Yeow", "Lim Guan Eng", "Yeoh Soon Hin"],
                "answer": "Chow Kon Yeow"
            },
            {
                #"image_path": "",
                "question": "What is the nickname used to describe Penang?",
                "options": ["The City of Dreams", "Paradise by the Sea", "An Island of Smiles", "Pearl of the Orient"],
                "answer": "Pearl of the Orient"
            },
            {
                #"image_path": "",
                "question": "Georgetown was established as a UNESCO World Heritage Site in which year?",
                "options": ["2004", "2008", "2012", "2014"],
                "answer": "2008 "
            },
        ]

        return questions

    def shuffle_questions(self):
        random.shuffle(self.questions)
        self.questions = self.questions[:self.num_questions]

    def display_question(self):
        blank_label = tk.Label(self.parent, bg='white')
        blank_label.pack(fill='x')
        quiz_frame1 = tk.Frame(self.parent, bg='white', padx=385)
        quiz_frame1.pack(fill='both', expand=True, anchor='center')
        quiz_frame = tk.Frame(quiz_frame1, bg='white', padx=40, pady=20, bd=1, relief="solid")
        quiz_frame.pack(fill='both', expand=True)

        # Existing code...

        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            question_label = tk.Label(quiz_frame, text=question_data["question"], font=("Lato", 18), fg='Black',
                                      bg='white', anchor='w',
                                      justify='left', wraplength=900)
            question_label.pack()

            image_path = question_data.get("image_path", "")  # Get the image path or use an empty string
            if image_path:  # Check if image_path is not empty
                try:
                    quiz_image = Image.open(image_path)
                    quiz_image = quiz_image.resize((250, 200))
                    quiz_image = ImageTk.PhotoImage(quiz_image)

                    quiz_image_label = tk.Label(quiz_frame, image=quiz_image)
                    quiz_image_label.image = quiz_image
                    quiz_image_label.pack(side='top', padx=150)
                except Exception as e:
                    print(f"Error opening image: {e}")

            self.options_var = StringVar()
            self.options_var.set(None)

            for i, option in enumerate(question_data["options"]):
                ans_frame1 = tk.Frame(quiz_frame, bg='white', padx=60, pady=10)
                ans_frame1.pack(fill='both')
                ans_frame = tk.Frame(ans_frame1, bg='#4F795E', padx=10, pady=10, bd=1, relief="solid")
                common_bg = '#' + ''.join([hex(x)[2:].zfill(2) for x in (79, 121, 94)])  # RGB in dec
                common_fg = '#ffffff'
                option_radio = tk.Radiobutton(ans_frame, text=option, variable=self.options_var, value=option,fg=common_fg, bg=common_bg,
                            activebackground=common_bg, activeforeground=common_fg, selectcolor=common_bg)
                option_radio.pack(anchor='w')
                ans_frame.pack(fill='both', expand=True)

            next_button = tk.Button(quiz_frame, text="Next", command=self.check_answer, bg='#505d58', fg='white',
                                    font=("Lato", 14), padx=30, pady=5)
            next_button.pack()
        else:
            self.display_result(quiz_frame)

    def check_answer(self):
        question_data = self.questions[self.current_question]
        user_answer = self.options_var.get()  # Get the selected answer

        if user_answer == question_data["answer"]:
            self.score += 1

        self.current_question += 1
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.display_question()

    def display_result(self, quiz_frame):
        result_frame = tk.Frame(quiz_frame, bg='white')  # Create a white frame for displaying the result
        result_frame.pack(fill='both', expand=True)

        result_label = tk.Label(result_frame, text=f"Your Score: {self.score}/{self.num_questions}", font=("Lato", 14), fg='Black', bg='white', anchor='w',
                              justify='left', wraplength=900)
        result_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelKiosk(root)

    # Set the background color of the main window
    root.configure(bg='white')  # Change 'white' to the color you desire

    root.geometry("1420x700")
    root.mainloop()
