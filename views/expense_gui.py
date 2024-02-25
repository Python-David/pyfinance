import tkinter as tk
from tkinter import ttk, messagebox


from views.utilities import validate_date


class ExpenseGUI:
    def __init__(self, parent, controller):
        self.parent = parent  # The parent widget, likely a tab in a Notebook widget
        self.controller = controller  # The main controller instance

        # Create the expense frame as part of the parent
        self.frame = ttk.Frame(self.parent)

        # Initialize variables to store user input
        self.expense_category = tk.StringVar()
        self.expense_amount = tk.DoubleVar()
        self.expense_date = tk.StringVar()

        # Build the expense UI components
        self.build_ui()

    def build_ui(self):
        # Create a frame within the tab to hold form elements, make it expandable
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill="both", expand=True)
        input_frame.grid_columnconfigure(1, weight=1)  # Make the entry fields expand

        # Define the form fields
        fields = [
            ("Category:", self.expense_category),
            ("Amount:", self.expense_amount),
            ("Date (YYYY-MM-DD):", self.expense_date)
        ]

        # Setup the form fields using grid
        for i, (label, var) in enumerate(fields):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            entry = ttk.Entry(input_frame, textvariable=var)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')  # Ensure entries expand with the frame

        # Submit button, avoid over-expansion by not using 'sticky'
        submit_btn = ttk.Button(input_frame, text='Submit', command=self.add_expense)
        submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

        # Ensure the frame expands with the tab
        self.frame.pack(fill="both", expand=True)

    def add_expense(self):
        category = self.expense_category.get()
        amount = self.expense_amount.get()
        date_str = self.expense_date.get()

        # Basic validation before attempting to add the expense
        if not category or not date_str or amount <= 0:
            messagebox.showerror("Error", "Please fill all fields correctly. Amount must be positive.")
            return

        valid_date, date_message = validate_date(date_str)
        if not valid_date:
            messagebox.showerror("Error", date_message)
            return

        if self.controller.current_user_id is None:
            messagebox.showerror("Error", "No user is logged in.")
            return

        # Delegate the expense addition logic to the controller
        success, message = self.controller.add_expense(self.controller.current_user_id, category, amount, date_str)
        if success:
            messagebox.showinfo("Success", "Expense added successfully.")
            # Any additional logic to update the UI or reset fields
        else:
            messagebox.showerror("Error", message)
