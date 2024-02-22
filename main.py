import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tracker.finance_tracker import FinanceTracker


class PyFinanceGUI:
    def __init__(self, master):
        self.master = master
        master.title('PyFinance Tracker')

        self.finance_tracker = FinanceTracker()  # Instantiate your FinanceTracker

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
        # Labels and Fields for Expense Entry
        ttk.Label(self.expense_tab, text='Category:').grid(column=0, row=0, padx=10, pady=10)
        self.expense_category = tk.StringVar()
        ttk.Entry(self.expense_tab, textvariable=self.expense_category).grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.expense_tab, text='Amount:').grid(column=0, row=1, padx=10, pady=10)
        self.expense_amount = tk.DoubleVar()
        ttk.Entry(self.expense_tab, textvariable=self.expense_amount).grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(self.expense_tab, text='Date (YYYY-MM-DD):').grid(column=0, row=2, padx=10, pady=10)
        self.expense_date = tk.StringVar()
        ttk.Entry(self.expense_tab, textvariable=self.expense_date).grid(column=1, row=2, padx=10, pady=10)

        # Submit Button
        ttk.Button(self.expense_tab, text='Add Expense', command=self.add_expense).grid(column=1, row=3, padx=10,
                                                                                        pady=10)

    def setup_investment_tab(self):
        # Labels and Fields for Investment Entry
        ttk.Label(self.investment_tab, text='Type:').grid(column=0, row=0, padx=10, pady=10)
        self.investment_type = tk.StringVar()
        ttk.Entry(self.investment_tab, textvariable=self.investment_type).grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.investment_tab, text='Amount:').grid(column=0, row=1, padx=10, pady=10)
        self.investment_amount = tk.DoubleVar()
        ttk.Entry(self.investment_tab, textvariable=self.investment_amount).grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(self.investment_tab, text='Date (YYYY-MM-DD):').grid(column=0, row=2, padx=10, pady=10)
        self.investment_date = tk.StringVar()
        ttk.Entry(self.investment_tab, textvariable=self.investment_date).grid(column=1, row=2, padx=10, pady=10)

        # Submit Button
        ttk.Button(self.investment_tab, text='Add Investment', command=self.add_investment).grid(column=1, row=3,
                                                                                                 padx=10, pady=10)

    def add_expense(self):
        try:
            category = self.expense_category.get()
            amount = self.expense_amount.get()
            date = datetime.strptime(self.expense_date.get(), '%Y-%m-%d').date()
            user_id = 1  # Placeholder user ID

            self.finance_tracker.add_expense(user_id, category, amount, date)
            messagebox.showinfo("Success", "Expense added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_investment(self):
        try:
            investment_type = self.investment_type.get()
            amount = self.investment_amount.get()
            date = datetime.strptime(self.investment_date.get(), '%Y-%m-%d').date()
            user_id = 1  # Placeholder user ID

            self.finance_tracker.add_investment(user_id, investment_type, amount, date)
            messagebox.showinfo("Success", "Investment added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_closing(self):
        self.finance_tracker.close_session()  # Properly close the session
        self.master.destroy()


def main():
    root = tk.Tk()
    app = PyFinanceGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Ensure proper closure
    root.mainloop()


if __name__ == '__main__':
    main()
