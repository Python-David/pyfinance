import os

import asyncclick as click
from matplotlib import pyplot as plt

from cli.utilities import requires_login
from controllers.main_controller import MainController


@click.command()
@requires_login
@click.pass_context
async def show(ctx):
    """Generate and save a plot of expenses by category."""
    user_id = MainController().get_user_id_from_session(ctx.obj.session_token)

    expenses_generator = MainController().get_expenses_by_category(user_id)

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
                categories.append(item['category'])
                amounts.append(item['total_amount'])

        if not categories:
            click.echo("No expenses to plot.")
            return

        # Proceed with plotting only if data is available
        plt.figure(figsize=(10, 6))
        plt.bar(categories, amounts, color='skyblue')
        plt.xlabel('Category')
        plt.ylabel('Total Amount Spent')
        plt.title('Expenses by Category')
        plt.xticks(rotation=45, ha="right")

        # Saving the plot to a file
        plot_filename = f"user_{user_id}_expenses_by_category.png"
        plt.savefig(plot_filename)
        plt.close()  # Close the figure to free memory

        # Providing the file path to the user
        click.echo(f"Plot saved to: {os.path.abspath(plot_filename)}")

    except Exception as e:
        click.echo(f"An error occurred while generating the plot: {e}")
