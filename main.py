import tkinter as tk

from controllers.main_controller import MainController
from views.central_gui import PyFinanceGUI


def main():
    root = tk.Tk()
    main_controller = MainController()
    app = PyFinanceGUI(root, main_controller)  # Passing the controller instance
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Ensure proper closure
    root.mainloop()


if __name__ == "__main__":
    main()
