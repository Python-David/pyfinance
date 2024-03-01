from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def plot_expenses_over_time(vis_frame, months, expenses):
    """
    Plot expenses over time.

    Parameters:
    - vis_frame: The tkinter frame where the plot will be placed.
    - months: A list of months.
    - expenses: A list of expense values corresponding to each month.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.plot(months, expenses)
    plot.set_title("Expenses Over Time")
    plot.set_ylabel("Amount")
    plot.set_xlabel("Month")

    canvas = FigureCanvasTkAgg(fig, master=vis_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=(0, 10))


def plot_expense_distribution(vis_frame, categories, values):
    """
    Plot expense distribution among categories.

    Parameters:
    - vis_frame: The tkinter frame where the plot will be placed.
    - categories: A list of categories.
    - values: A list of values corresponding to each category.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.pie(values, labels=categories, autopct="%1.1f%%")
    plot.set_title("Category-wise Expense Distribution")

    canvas = FigureCanvasTkAgg(fig, master=vis_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=1, padx=(10, 0))


def plot_investment_distribution_by_type(vis_frame, investments):
    """
    Plot the distribution of investments by type.

    Parameters:
    - vis_frame: The tkinter frame where the plot will be placed.
    - investments: A list of investment records.
    """
    from collections import Counter

    investment_types = [investment for investment in investments]
    type_counts = Counter(investment_types)
    labels = list(type_counts.keys())
    sizes = list(type_counts.values())

    fig = Figure(figsize=(6, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.pie(sizes, labels=labels, autopct="%1.1f%%")
    plot.set_title("Investment Distribution by Type")

    canvas = FigureCanvasTkAgg(fig, master=vis_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=(0, 10))


def plot_total_investments_over_time(vis_frame, dates, total_investments):
    """
    Plot the total investment amount over time.

    Parameters:
    - vis_frame: The tkinter frame where the plot will be placed.
    - dates: A list of dates.
    - total_investments: A list of total investment amounts corresponding to each date.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.plot(dates, total_investments, marker="o", linestyle="-")
    plot.set_title("Total Investments Over Time")
    plot.set_ylabel("Total Investment Amount")
    plot.set_xlabel("Date")
    plot.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=vis_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=1, padx=(10, 0))
