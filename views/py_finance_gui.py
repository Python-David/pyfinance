import tkinter as tk
from tkinter import ttk, messagebox
from controllers.finance_controller import FinanceController


class PyFinanceGUI:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller  # Instance of FinanceController
        master.title('PyFinance Tracker')

        # Initialize variables to store user input
        self.expense_category = tk.StringVar()
        self.expense_amount = tk.DoubleVar()
        self.expense_date = tk.StringVar()

        self.investment_type = tk.StringVar()
        self.investment_amount = tk.DoubleVar()
        self.investment_date = tk.StringVar()

        # Setup notebook
        self.tab_control = ttk.Notebook(master)

        # Expense Tab
        self.expense_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.expense_tab, text='Expenses')
        self.setup_expense_tab()

        # Investment Tab
        self.investment_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.investment_tab, text='Investments')
        self.setup_investment_tab()

        self.tab_control.pack(expand=1, fill="both")

    def setup_expense_tab(self):
        fields = [
            ("Category:", self.expense_category),
            ("Amount:", self.expense_amount),
            ("Date (YYYY-MM-DD):", self.expense_date)
        ]
        self.setup_tab(self.expense_tab, fields, self.add_expense)

    def setup_investment_tab(self):
        fields = [
            ("Type:", self.investment_type),
            ("Amount:", self.investment_amount),
            ("Date (YYYY-MM-DD):", self.investment_date)
        ]
        self.setup_tab(self.investment_tab, fields, self.add_investment)

    def setup_tab(self, tab, fields, submit_command):
        for i, (label, entry_var) in enumerate(fields, start=0):
            ttk.Label(tab, text=label).grid(column=0, row=i, padx=10, pady=10)
            ttk.Entry(tab, textvariable=entry_var).grid(column=1, row=i, padx=10, pady=10)

        # Submit Button
        ttk.Button(tab, text='Submit', command=submit_command).grid(column=1, row=len(fields), padx=10, pady=10)

    def add_expense(self):
        self.process_entry(self.controller.add_expense, "Expense", self.expense_category, self.expense_amount,
                           self.expense_date)

    def add_investment(self):
        self.process_entry(self.controller.add_investment, "Investment", self.investment_type, self.investment_amount,
                           self.investment_date)

    def process_entry(self, action, entry_type, category_var, amount_var, date_var):
        category_type = category_var.get()
        amount = amount_var.get()
        date_str = date_var.get()
        user_id = 1  # Placeholder for user identification

        success, message = action(user_id, category_type, amount, date_str)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def on_closing(self):
        self.controller.close_session()
        self.master.destroy()
