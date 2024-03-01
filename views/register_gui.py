import tkinter as tk
from tkinter import messagebox, ttk

from views.utilities import (validate_email, validate_non_empty,
                             validate_password_strength)


class RegisterGUI:
    def __init__(self, parent, controller, register_success_callback):
        self.parent = parent  # The parent widget, likely a tab in a Notebook widget
        self.controller = controller  # The main controller instance

        self.register_success_callback = register_success_callback

        # Create the register frame as part of the parent
        self.frame = ttk.Frame(self.parent)

        # Variables for register form
        self.register_username_var = tk.StringVar()
        self.register_email_var = tk.StringVar()
        self.register_password_var = tk.StringVar()

        # Build the register UI components
        self.build_ui()

    def build_ui(self):
        # Create a frame within the tab to hold form elements
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(padx=20, pady=20)

        # Define the form fields
        fields = [
            ("Username", self.register_username_var),
            ("Email", self.register_email_var),  # Optional, for password reset feature
            ("Password", self.register_password_var),
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
        submit_btn = ttk.Button(input_frame, text="Submit", command=self.register_user)
        submit_btn.pack(side="bottom", pady=10)

        # Pack the main frame onto the parent widget
        self.frame.pack(expand=1, fill="both")

    def register_user(self):
        username = self.register_username_var.get()
        email = (
            self.register_email_var.get()
        )  # Optional, based on your application requirements
        password = self.register_password_var.get()

        # Validation before attempting to register
        if (
            not validate_non_empty(username)
            or not validate_non_empty(email)
            or not validate_non_empty(password)
        ):
            messagebox.showerror("Registration Failed", "All fields are required.")
            return

        if not validate_email(email):
            messagebox.showerror("Registration Failed", "Invalid email format.")
            return

        password_valid, password_message = validate_password_strength(password)
        if not password_valid:
            messagebox.showerror("Registration Failed", password_message)
            return

        # Delegate the registration logic to the controller
        success, message = self.controller.register_new_user(username, email, password)
        if success:
            messagebox.showinfo(
                "Registration Successful",
                message,
                command=self.register_success_callback,
            )
            # Any additional logic to transition to another part of the application
        else:
            messagebox.showerror("Registration Failed", message)
