import tkinter as tk
from tkinter import ttk, messagebox

from views.utilities import validate_non_empty, validate_email


class LoginGUI:
    def __init__(self, parent, controller, login_success_callback):
        self.parent = parent  # The parent widget, likely to be a tab in a Notebook widget
        self.controller = controller  # The main controller instance

        self.login_success_callback = login_success_callback

        # Create the login frame as part of the parent
        self.frame = ttk.Frame(self.parent)

        # Variables for login form
        self.login_email_var = tk.StringVar()
        self.login_password_var = tk.StringVar()

        # Build the login UI components
        self.build_ui()

    def build_ui(self):
        # Create a frame within the tab to hold form elements
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(padx=20, pady=20)

        # Define the form fields
        fields = [
            ("Email", self.login_email_var),
            ("Password", self.login_password_var)
        ]

        # Create and pack the form fields
        for label, var in fields:
            row = ttk.Frame(input_frame)
            row.pack(fill="x", padx=5, pady=5)
            ttk.Label(row, text=label, width=20).pack(side="left")

            if label == "Password":
                entry = ttk.Entry(row, textvariable=var, show="*", width=30)
            else:
                entry = ttk.Entry(row, textvariable=var, width=30)
            entry.pack(side="right")

        # Submit button
        submit_btn = ttk.Button(input_frame, text="Submit", command=self.login_user)
        submit_btn.pack(side="bottom", pady=10)

        # Pack the main frame onto the parent widget
        self.frame.pack(expand=1, fill="both")

    def login_user(self):
        email = self.login_email_var.get()
        password = self.login_password_var.get()

        # Validation before attempting to log in
        if not validate_non_empty(email) or not validate_non_empty(password):
            messagebox.showerror("Login Failed", "All fields are required.")
            return

        if not validate_email(email):
            messagebox.showerror("Login Failed", "Invalid email format.")
            return

        # Delegate the login logic to the controller
        success, message, user_id = self.controller.validate_login(email, password)
        if success:
            messagebox.showinfo("Login Successful", message)
            # Now, we use the user_id to set the current user in the MainController
            self.controller.current_user_id = user_id  # Set the current_user_id in MainController
            self.login_success_callback()  # Call the callback without user_id
        else:
            messagebox.showerror("Login Failed", message)
