import tkinter as tk
from tkinter import ttk, messagebox
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from datetime import datetime
import pytz

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"

        # Database setup
        self.setup_database()

        # Fetch currencies and rates
        self.currencies = self.fetch_currencies()

        # GUI Elements
        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.from_currency_label = tk.Label(root, text="From Currency:")
        self.from_currency_label.grid(row=1, column=0, padx=10, pady=10)
        self.from_currency_dropdown = ttk.Combobox(root, values=list(self.currencies.keys()))
        self.from_currency_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.from_currency_dropdown.set("USD")  # Default value

        self.to_currency_label = tk.Label(root, text="To Currency:")
        self.to_currency_label.grid(row=2, column=0, padx=10, pady=10)
        self.to_currency_dropdown = ttk.Combobox(root, values=list(self.currencies.keys()))
        self.to_currency_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.to_currency_dropdown.set("EUR")  # Default value

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="Converted Amount: ")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.visualize_button = tk.Button(root, text="Visualize Rates", command=self.visualize_rates)
        self.visualize_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Enable filtering for dropdowns
        self.from_currency_dropdown.bind("<KeyRelease>", lambda e: self.filter_currency(self.from_currency_dropdown, e))
        self.to_currency_dropdown.bind("<KeyRelease>", lambda e: self.filter_currency(self.to_currency_dropdown, e))

    def setup_database(self):
        self.conn = sqlite3.connect("conversion_history.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                from_currency TEXT,
                to_currency TEXT,
                rate REAL,
                converted_amount REAL,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def fetch_currencies(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()["rates"]
            print(data)
            return data
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch currencies: {e}")
            return {}

    def filter_currency(self, dropdown, event):
        value = event.widget.get()
        filtered_values = [key for key in self.currencies.keys() if value.upper() in key]
        dropdown["values"] = filtered_values
        if filtered_values:
            dropdown.set(value)

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

            # Save to database
            kolkata_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("""
                INSERT INTO history (amount, from_currency, to_currency, rate, converted_amount, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (amount, from_currency, to_currency, rate, converted_amount, kolkata_time))
            self.conn.commit()
        else:
            messagebox.showerror("Conversion Error", "Invalid currency code or rate not found")

    def visualize_rates(self):
        rates = self.currencies
        if not rates:
            return

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)

        currencies = list(rates.keys())[:10]  # Limit to first 10 currencies
        values = [rates[currency] for currency in currencies]

        ax.bar(currencies, values)
        ax.set_title("Exchange Rates")
        ax.set_ylabel("Rate")
        ax.set_xlabel("Currency")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().grid(row=6, column=0, columnspan=2)
        canvas.draw()

# Run the app
root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()
