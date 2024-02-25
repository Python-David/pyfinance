import tkinter as tk
from views.py_finance_gui import PyFinanceGUI
from controllers.finance_controller import FinanceController


def main():
    root = tk.Tk()
    controller = FinanceController()
    app = PyFinanceGUI(root, controller)  # Passing the controller instance
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Ensure proper closure
    root.mainloop()


if __name__ == '__main__':
    main()
