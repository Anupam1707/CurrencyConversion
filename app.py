import tkinter as tk
from tkinter import ttk, messagebox
import requests
import sqlite3
from datetime import datetime
import pytz
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
import sys
import matplotlib.pyplot as plt
from SecuriPy import Text

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#1e1f26")
        
        self.root.bind("<Escape>", self.exit_app)
        self.root.bind("<Return>", self.handle_enter_key)   
        
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.username = None
        self.conn = sqlite3.connect("currency_converter.db")
        self.cursor = self.conn.cursor()

        self.setup_database()

        self.currencies = self.fetch_currencies()

        label_style = {"bg": "#1e1f26", "fg": "#ffffff", "font": ("Arial", 14)}
        entry_style = {"bg": "#2b2d3c", "fg": "#ffffff", "font": ("Arial", 12)}
        button_style = {"bg": "#3c91e6", "fg": "#ffffff", "font": ("Arial", 12, "bold")}
        dropdown_style = {"background": "#2b2d3c", "foreground": "#000000"}

        self.show_login_page()
        
    def exit_app(self, event=None):
        self.root.destroy()

    def handle_enter_key(self, event=None):
        if self.root.focus_get() == self.username_entry or self.root.focus_get() == self.password_entry:
            self.login()
            
    def setup_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        self.conn.commit()

    def fetch_currencies(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()["rates"]
            top = {c: data[c] for c in data.keys() if c in ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "HKD", "NZD", "INR"]}
            return top
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch currencies: {e}")
            return {}

    def show_login_page(self):
        self.clear_root()

        bg_image = Image.open("media/acc.jpg")
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.create_image(0, 0, image=bg_image, anchor="nw")
        self.canvas.image = bg_image
        self.canvas.pack(fill="both", expand=True)

        label_style = {"bg": "#1e1f26", "fg": "#ffffff", "font": ("Arial", 16)}
        entry_style = {"bg": "#2b2d3c", "fg": "#ffffff", "font": ("Arial", 14)}
        button_style = {"bg": "#3c91e6", "fg": "#ffffff", "font": ("Arial", 14, "bold")}

        self.header_label = tk.Label(self.root, text="Welcome to the Currency Converter", font=("Calibri", 35, "bold"), bg="#e85e38", fg="#ffffff")
        self.header_label.place(relx=0.5, rely=0.0, anchor="n")

        self.login_frame = tk.Frame(self.canvas, bg="", bd=0)
        self.login_frame.place(relx=0.1, rely=0.5, width=450, height=300, anchor="w")

        self.username_label = tk.Label(self.login_frame, text="Username:", **label_style)
        self.username_label.grid(row=0, column=0, padx=20, pady=10)
        self.username_entry = tk.Entry(self.login_frame, **entry_style)
        self.username_entry.grid(row=0, column=1, padx=20, pady=10)

        self.password_label = tk.Label(self.login_frame, text="Password:", **label_style)
        self.password_label.grid(row=1, column=0, padx=20, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*", **entry_style)
        self.password_entry.grid(row=1, column=1, padx=20, pady=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, **button_style)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=15)
        self.username_entry.focus()
        
        self.create_account_button = tk.Button(self.login_frame, text="Create Account", command=self.show_create_account_page, **button_style)
        self.create_account_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=sys.exit, font=("Arial", 16, "bold"), bg="#ff0000", fg="#ffffff")
        self.exit_button.place(relx=1, rely=0.0, anchor="ne")

    def show_create_account_page(self):
        self.clear_root()

        bg_image = Image.open("media/acc.jpg")
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.create_image(0, 0, image=bg_image, anchor="nw")
        self.canvas.image = bg_image
        self.canvas.pack(fill="both", expand=True)

        label_style = {"bg": "#1e1f26", "fg": "#ffffff", "font": ("Arial", 16)}
        entry_style = {"bg": "#2b2d3c", "fg": "#ffffff", "font": ("Arial", 14)}
        button_style = {"bg": "#3c91e6", "fg": "#ffffff", "font": ("Arial", 14, "bold")}

        self.header_label = tk.Label(self.root, text="Welcome to the Currency Converter", font=("Calibri", 35, "bold"), bg="#e85e38", fg="#ffffff")
        self.header_label.place(relx=0.5, rely=0.0, anchor="n")

        self.create_account_frame = tk.Frame(self.canvas, bg="", bd=0)
        self.create_account_frame.place(relx=0.1, rely=0.5, width=450, height=300, anchor="w")

        self.create_username_label = tk.Label(self.create_account_frame, text="Username:", **label_style)
        self.create_username_label.grid(row=0, column=0, padx=20, pady=10)
        self.create_username_entry = tk.Entry(self.create_account_frame, **entry_style)
        self.create_username_entry.grid(row=0, column=1, padx=20, pady=10)

        self.create_password_label = tk.Label(self.create_account_frame, text="Password:", **label_style)
        self.create_password_label.grid(row=1, column=0, padx=20, pady=10)
        self.create_password_entry = tk.Entry(self.create_account_frame, show="*", **entry_style)
        self.create_password_entry.grid(row=1, column=1, padx=20, pady=10)

        self.create_account_button = tk.Button(self.create_account_frame, text="Create Account", command=self.create_account, **button_style)
        self.create_account_button.grid(row=2, column=0, columnspan=2, pady=15)

        self.create_account_button = tk.Button(self.create_account_frame, text="Login Instead", command=self.show_login_page, **button_style)
        self.create_account_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=sys.exit, font=("Arial", 16, "bold"), bg="#ff0000", fg="#ffffff")
        self.exit_button.place(relx=1, rely=0.0, anchor="ne")


    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password")
            return

        try:
            self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, Text.encrypt(password, "currentconv")))
            user = self.cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
            return

        if user:
            self.username = username
            self.show_currency_converter_page(username)
        else:
            messagebox.showerror("Login Error", "Invalid username or password")


    def create_account(self):
        username = self.create_username_entry.get()
        password = self.create_password_entry.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password")
            return

        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, Text.encrypt(password, "currentconv")))
            self.conn.commit()
            messagebox.showinfo("Success", "Account created successfully! Please log in.")
            self.show_login_page()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def show_currency_converter_page(self, username):
        self.clear_root()

        bg_image = Image.open("media/home.jpg")
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.create_image(0, 0, image=bg_image, anchor="nw")
        self.canvas.image = bg_image
        self.canvas.pack(fill="both", expand=True)

        rect_x1 = self.root.winfo_screenwidth() * 0.2
        rect_x2 = self.root.winfo_screenwidth() * 0.8
        rect_y1 = 150
        rect_y2 = 650
        self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="#ffffff", stipple="gray75", outline="")

        label_style = {"bg": "#1e1f26", "fg": "#ffffff", "font": ("Arial", 18)}
        entry_style = {"bg": "#2b2d3c", "fg": "#ffffff", "font": ("Arial", 16)}
        button_style = {"bg": "#3c91e6", "fg": "#ffffff", "font": ("Arial", 16, "bold")}
        dropdown_style = {"background": "#2b2d3c", "foreground": "#000000"}

        self.header_label = tk.Label(self.root, text="Currency Converter", font=("Calibri", 45, "bold"), bg="#e85e38", fg="#ffffff")
        self.header_label.place(relx=0.5, y=50, anchor="n")

        self.logged_in_label = tk.Label(self.root, text=f"Logged in as {username}", **label_style)
        self.logged_in_label.place(x=0, y=0, anchor="nw")

        self.amount_label = tk.Label(self.root, text="Amount:", **label_style)
        self.amount_label.place(relx=0.25, y=200, anchor="w")
        self.amount_entry = tk.Entry(self.root, **entry_style)
        self.amount_entry.place(relx=0.4, y=200, width=300, height=35, anchor="w")
        self.amount_entry = tk.Entry(self.root, bg="#ffffff", fg="#000000", font=("Arial", 16)) 
        self.amount_entry.place(relx=0.4, y=200, width=300, height=35, anchor="w")

        self.from_currency_label = tk.Label(self.root, text="From Currency:", **label_style)
        self.from_currency_label.place(relx=0.25, y=270, anchor="w")
        self.from_currency_dropdown = ttk.Combobox(self.root, values=list(self.currencies.keys()), font=("Arial", 16))
        self.from_currency_dropdown.place(relx=0.4, y=270, width=300, height=35, anchor="w")
        self.from_currency_dropdown.set("USD")

        self.to_currency_label = tk.Label(self.root, text="To Currency:", **label_style)
        self.to_currency_label.place(relx=0.25, y=340, anchor="w")
        self.to_currency_dropdown = ttk.Combobox(self.root, values=list(self.currencies.keys()), font=("Arial", 16))
        self.to_currency_dropdown.place(relx=0.4, y=340, width=300, height=35, anchor="w")
        self.to_currency_dropdown.set("INR")

        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_currency, **button_style)
        self.convert_button.place(relx=0.5, y=420, width=150, height=50, anchor="n")

        self.result_label = tk.Label(self.root, text="Converted Amount: ", **label_style)
        self.result_label.place(relx=0.5, y=500, anchor="n")

        self.visualize_button = tk.Button(self.root, text="Visualize Rates", command=self.visualize_rates, **button_style)
        self.visualize_button.place(relx=0.5, y=580, width=200, height=50, anchor="n")

        self.exit_button = tk.Button(self.root, text="Exit", command=sys.exit, font=("Arial", 16, "bold"), bg="#ff0000", fg="#ffffff")
        self.exit_button.place(relx=1, rely=0.0, anchor="ne")

        self.logout = tk.Button(self.root, text="Logout", command=self.show_login_page, font=("Arial", 16, "bold"), bg="#ff0000", fg="#ffffff")
        self.logout.place(relx=1, rely=1, anchor="se")

    def update_button_position(self):
        self.exit_button.place(x=self.root.winfo_width() - 100, y=10, anchor="ne")

    def convert_currency(self):
        amount = self.amount_entry.get()
        from_currency = self.from_currency_dropdown.get()
        to_currency = self.to_currency_dropdown.get()

        if not amount or not from_currency or not to_currency:
            messagebox.showerror("Input Error", "Please fill in all fields")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid amount")
            return

        rates = self.currencies
        if rates and from_currency in rates and to_currency in rates:
            rate = rates[to_currency] / rates[from_currency]
            converted_amount = amount * rate
            self.result_label.config(text=f"Converted Amount: {converted_amount:.2f} {to_currency}")

            kolkata_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
            user_history_table = f"history_{self.username}"
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {user_history_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL,
                    from_currency TEXT,
                    to_currency TEXT,
                    rate REAL,
                    converted_amount REAL,
                    timestamp TEXT
                )
            """)
            self.cursor.execute(f"""
                INSERT INTO {user_history_table} (amount, from_currency, to_currency, rate, converted_amount, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (amount, from_currency, to_currency, rate, converted_amount, kolkata_time))
            self.conn.commit()
        else:
            messagebox.showerror("Conversion Error", "Invalid currency code or rate not found")

    def visualize_rates(self):
        rates = self.currencies
        if not rates:
            return

        image = Image.open("media/graph.jpg")

        currencies = list(rates.keys())
        values = [rates[currency] for currency in currencies]

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.imshow(image, extent=[-0.5, len(currencies) - 0.5, 0, max(values) * 1.1], aspect='auto', zorder=0)

        bars = ax.bar(currencies, values, zorder=1, color='blue')

        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value:.2f}", ha='center', va='bottom', fontsize=10, color='black', weight='bold')

        ax.set_title("Exchange Rates")
        ax.set_ylabel("Rate")
        ax.set_xlabel("Currency")
        ax.set_xlim(-0.5, len(currencies) - 0.5)
        ax.set_ylim(0, max(values) * 1.1)

        plt.show()

root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()
