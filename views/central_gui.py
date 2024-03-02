import tkinter as tk
from tkinter import messagebox, ttk

from config import APP_TITLE
from views.expense_gui import ExpenseGUI
from views.investment_gui import InvestmentGUI
from views.login_gui import LoginGUI
from views.register_gui import RegisterGUI


class PyFinanceGUI:
    def __init__(self, master, main_controller):
        self.master = master
        self.controller = main_controller
        self.master.title(APP_TITLE)

        # Set initial size and position
        self.set_initial_size_and_position()

        # Setup notebook
        self.tab_control = ttk.Notebook(master)

        # Initialize the GUI components for login, register, expenses, and investments
        self.login_gui = LoginGUI(
            self.tab_control, self.controller, self.on_login_success
        )
        self.register_gui = RegisterGUI(
            self.tab_control, self.controller, self.on_login_success
        )

        # Add login and register tabs
        self.tab_control.add(self.login_gui.frame, text="Login")
        self.tab_control.add(self.register_gui.frame, text="Register")

        # These tabs will be added after successful login or registration
        self.expense_gui = None
        self.investment_gui = None

        self.tab_control.pack(expand=1, fill="both")

        # Bind the closing event
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_initial_size_and_position(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        width = int(screen_width * 0.8)
        height = int(screen_height * 0.8)
        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x_position}+{y_position}")

    def initialize_application_tabs(self):
        # Initialize and add tabs for expenses and investments
        self.expense_gui = ExpenseGUI(self.tab_control, self.controller)
        self.investment_gui = InvestmentGUI(self.tab_control, self.controller)

        self.tab_control.add(self.expense_gui.frame, text="Expenses")
        self.tab_control.add(self.investment_gui.frame, text="Investments")

        # Add a logout option
        self.add_logout_option()

        # Optionally, reset the login and register forms here

    def add_logout_option(self):
        # Create a frame for the logout button to control its positioning
        self.logout_frame = ttk.Frame(self.master)
        self.logout_frame.pack(fill=tk.X, side=tk.TOP)

        self.logout_button = ttk.Button(
            self.logout_frame, text="Logout", command=self.logout_user
        )
        self.logout_button.pack(pady=10, padx=10)

    def on_login_success(self):
        self.initialize_application_tabs()  # Proceed to initialize application tabs

        # Additional steps to remove login and register tabs, as previously defined
        self.tab_control.forget(self.login_gui.frame)
        self.tab_control.forget(self.register_gui.frame)

    def logout_user(self):
        # Method to log out the user and show the login and register tabs again
        if self.expense_gui and self.investment_gui:
            self.tab_control.forget(self.expense_gui.frame)
            self.tab_control.forget(self.investment_gui.frame)
            self.expense_gui = None
            self.investment_gui = None

        # Show the Login/Register tabs again
        self.tab_control.add(self.login_gui.frame, text="Login")
        self.tab_control.add(self.register_gui.frame, text="Register")
        self.tab_control.select(self.login_gui.frame)  # Focus on login tab

        # Remove or hide the logout button
        if self.logout_button:
            self.logout_button.pack_forget()  # This hides the button without destroying it
            self.logout_button = None  # Reset the button attribute

    def on_closing(self):
        # Handle the application closure
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.controller.close_sessions()  # Assuming this method exists to handle cleanup
            self.master.destroy()
