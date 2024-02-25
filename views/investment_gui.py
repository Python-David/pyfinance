import tkinter as tk
from tkinter import ttk, messagebox

from views.utilities import validate_date


class InvestmentGUI:
    def __init__(self, parent, controller):
        self.parent = parent  # The parent widget, likely a tab in a Notebook widget
        self.controller = controller  # The main controller instance

        # Create the investment frame as part of the parent
        self.frame = ttk.Frame(self.parent)

        # Initialize variables to store user input
        self.investment_type = tk.StringVar()
        self.investment_amount = tk.DoubleVar()
        self.investment_date = tk.StringVar()

        # Build the investment UI components
        self.build_ui()

    def build_ui(self):
        # Create a frame within the tab to hold form elements, make it expandable
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill="both", expand=True)
        input_frame.grid_columnconfigure(1, weight=1)  # Make the entry fields expand

        # Define the form fields
        fields = [
            ("Type:", self.investment_type),
            ("Amount:", self.investment_amount),
            ("Date (YYYY-MM-DD):", self.investment_date)
        ]

        # Create and pack the form fields
        for i, (label, var) in enumerate(fields, start=0):
            ttk.Label(input_frame, text=label).grid(column=0, row=i, padx=10, pady=5, sticky='w')
            entry = ttk.Entry(input_frame, textvariable=var)
            entry.grid(column=1, row=i, padx=10, pady=5, sticky='ew')  # Make the entry widget expand with the window

        # Submit button, avoid over-expansion by not using 'sticky'
        submit_btn = ttk.Button(input_frame, text='Submit', command=self.add_investment)
        submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

        # Ensure the frame expands with the tab
        self.frame.pack(fill="both", expand=True)

    def add_investment(self):
        investment_type = self.investment_type.get()
        amount = self.investment_amount.get()
        date_str = self.investment_date.get()

        # Basic validation before attempting to add the investment
        if not investment_type or not date_str or amount <= 0:
            messagebox.showerror("Error", "Please fill all fields correctly. Amount must be positive.")
            return

        valid_date, date_message = validate_date(date_str)
        if not valid_date:
            messagebox.showerror("Error", date_message)
            return

        # Delegate the investment addition logic to the controller
        success, message = self.controller.add_investment(self.controller.current_user_id, investment_type, amount, date_str)
        if success:
            messagebox.showinfo("Success", "Investment added successfully.")
            # Any additional logic to update the UI or reset fields
        else:
            messagebox.showerror("Error", message)
