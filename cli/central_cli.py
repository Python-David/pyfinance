import asyncclick as click

from .expense_commands import add_expense, add_expenses_from_csv, list_expenses
from .investment_commands import (add_investment, add_investments_from_csv,
                                  list_investments)
from .plot_commands import show
from .user_commands import login, register


class Context:
    def __init__(self):
        self.session_token = None


@click.group()
@click.pass_context
async def cli(ctx):
    """PyFinance CLI"""
    ctx.obj = Context()


# Add commands to your CLI

# User commands
cli.add_command(register)
cli.add_command(login)

# Expense commands
cli.add_command(add_expense)
cli.add_command(add_expenses_from_csv)
cli.add_command(list_expenses)

# Investment commands
cli.add_command(add_investment)
cli.add_command(add_investments_from_csv)
cli.add_command(list_investments)

# Plot commands
cli.add_command(show)


if __name__ == "__main__":
    cli(_anyio_backend="asyncio")
