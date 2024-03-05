import calendar
import os
from typing import Dict, Iterable, List, Optional

import asyncclick as click
from asyncclick import Context
from matplotlib import pyplot as plt

from cli.utilities import requires_login, plot_expenses_by_category
from controllers.main_controller import MainController
from models.finance_data import FinanceFilter


@click.command()
@requires_login
@click.option("-y", "--year", type=int, help="Filter expenses by year.")
@click.option("-m", "--month", type=int, help="Filter expenses by month (1-12).")
@click.option("-d", "--day", type=int, help="Filter expenses by day (1-31).")
@click.pass_context
async def show(
    ctx: Context,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None
) -> None:
    """Generate and save a plot of expenses by category."""
    user_id: int = MainController().get_user_id_from_session(ctx.obj.session_token)

    finance_filter = FinanceFilter(user_id=user_id, year=year, month=month, day=day)
    expenses_generator: Iterable[Dict[str, float]] = (
        MainController().get_expenses_by_category(finance_filter)
    )

    categories = []
    amounts = []

    try:
        for item in expenses_generator:
            if "error" in item:
                # If an error item is encountered, print the error and exit the loop
                click.echo(item["message"])
                return
            else:
                # Append category and total_amount to their respective lists
                categories.append(item["category"])
                amounts.append(item["total_amount"])

        if not categories:
            click.echo("No expenses to plot.")
            return

        # Construct the title with filter information
        title = "Expenses by Category"
        if year:
            title += f" in {year}"
            if month:
                title += f" - {calendar.month_name[month]}"
                if day:
                    title += f" {day}"
        elif month:
            title += f" in {calendar.month_name[month]}"
            if day:
                title += f" {day}"

        plot_filename = f"user_{user_id}_expenses_by_category.png"
        plot_expenses_by_category(categories, amounts, title, plot_filename)

        # Providing the file path to the user
        click.echo(f"Plot saved to: {os.path.abspath(plot_filename)}")

    except Exception as e:
        click.echo(f"An error occurred while generating the plot: {e}")
