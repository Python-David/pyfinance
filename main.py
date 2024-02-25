import tkinter as tk
from views.central_gui import PyFinanceGUI
from controllers.main_controller import MainController


def main():
    root = tk.Tk()
    main_controller = MainController()
    app = PyFinanceGUI(root, main_controller)  # Passing the controller instance
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Ensure proper closure
    root.mainloop()


if __name__ == '__main__':
    main()
