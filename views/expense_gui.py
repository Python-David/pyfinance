import _tkinter
import tkinter as tk
from calendar import monthrange
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from views.plotting_utils import (plot_expense_distribution,
                                  plot_expenses_over_time)
from views.utilities import validate_date


class ExpenseGUI:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(self.parent)

        self.expense_category = tk.StringVar()
        self.expense_amount = tk.DoubleVar()
        self.selected_year = tk.StringVar()
        self.selected_month = tk.StringVar()
        self.selected_day = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill="both", expand=True)
        input_frame.grid_columnconfigure(1, weight=1)

        # Setup for Category and Amount
        ttk.Label(input_frame, text="Category:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Entry(input_frame, textvariable=self.expense_category).grid(
            row=0, column=1, padx=10, pady=5, sticky="ew"
        )

        ttk.Label(input_frame, text="Amount:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Entry(input_frame, textvariable=self.expense_amount).grid(
            row=1, column=1, padx=10, pady=5, sticky="ew"
        )

        # Date Dropdowns
        self.setup_date_dropdowns(input_frame)

        input_frame.grid_rowconfigure(3, minsize=20)

        # Submit button
        submit_btn = ttk.Button(input_frame, text="Submit", command=self.add_expense)
        submit_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Visualization frame setup
        vis_frame = ttk.Frame(self.frame)  # Frame to hold the charts
        vis_frame.pack(
            fill="both", expand=True, pady=20
        )  # Add some space between the input frame and visualizations
        vis_frame.grid_columnconfigure(0, weight=1)
        vis_frame.grid_columnconfigure(1, weight=1)

        # Use imported functions to plot
        months = ["Jan", "Feb", "Mar", "Apr", "May"]  # Example data
        expenses = [200, 150, 300, 250, 180]  # Example data
        plot_expenses_over_time(vis_frame, months, expenses)

        categories = ["Rent", "Food", "Utilities", "Entertainment"]  # Example data
        values = [400, 300, 150, 100]  # Example data
        plot_expense_distribution(vis_frame, categories, values)

        self.frame.pack(fill="both", expand=True)

    def setup_date_dropdowns(self, frame):
        ttk.Label(frame, text="Date:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )

        # Frame to hold year, month, and day dropdowns together
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        frame.grid_columnconfigure(1, weight=1)  # Allow the date frame to expand

        # Year Dropdown
        years = list(range(1900, 2101))
        self.selected_year = tk.StringVar(value="2021")
        year_cb = ttk.Combobox(
            date_frame, textvariable=self.selected_year, values=years, width=10
        )
        year_cb.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Month Dropdown
        months = [str(i).zfill(2) for i in range(1, 13)]  # Leading zeros
        self.selected_month = tk.StringVar(value="01")
        month_cb = ttk.Combobox(
            date_frame, textvariable=self.selected_month, values=months, width=5
        )
        month_cb.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Day Dropdown
        days = [str(i).zfill(2) for i in range(1, 32)]  # Leading zeros
        self.selected_day = tk.StringVar(value="01")
        day_cb = ttk.Combobox(
            date_frame, textvariable=self.selected_day, values=days, width=5
        )
        day_cb.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Ensure date_frame fills its cell
        date_frame.grid_columnconfigure(0, weight=1)
        date_frame.grid_columnconfigure(1, weight=1)
        date_frame.grid_columnconfigure(2, weight=1)

        # Update days based on year and month selection
        month_cb.bind(
            "<<ComboboxSelected>>",
            lambda e: self.update_days(month_cb, year_cb, day_cb),
        )
        year_cb.bind(
            "<<ComboboxSelected>>",
            lambda e: self.update_days(month_cb, year_cb, day_cb),
        )

    def update_days(self, month_cb, year_cb, day_cb):
        year = int(self.selected_year.get())
        month = int(self.selected_month.get())
        days_in_month = monthrange(year, month)[1]
        day_cb["values"] = list(range(1, days_in_month + 1))

    def add_expense(self):
        category = self.expense_category.get()
        try:
            # Since self.expense_amount is a DoubleVar, this conversion may raise a _tkinter.TclError
            amount = self.expense_amount.get()
            # Format the amount to two decimal places
            amount = round(amount, 2)
        except _tkinter.TclError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid number for the amount."
            )
            return
        year = self.selected_year.get()
        month = self.selected_month.get()
        day = self.selected_day.get()
        date_str = (
            f"{year}-{month.zfill(2)}-{day.zfill(2)}"  # Format the date as YYYY-MM-DD
        )

        # Basic validation before attempting to add the expense
        if not category or amount <= 0:
            messagebox.showerror(
                "Error", "Please fill all fields correctly. Amount must be positive."
            )
            return

        # Assuming validate_date is a function that validates the constructed date_str
        valid_date, date_message = validate_date(date_str)
        if not valid_date:
            messagebox.showerror("Error", date_message)
            return

        if self.controller.current_user_id is None:
            messagebox.showerror("Error", "No user is logged in.")
            return

        # Delegate the expense addition logic to the controller
        success, message = self.controller.add_expense(
            self.controller.current_user_id, category, amount, date_str
        )
        if success:
            messagebox.showinfo("Success", "Expense added successfully.")
            # Any additional logic to update the UI or reset fields
        else:
            messagebox.showerror("Error", message)
