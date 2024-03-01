import asyncclick as click

from .expense_commands import add_expense, add_expenses_from_csv, list_expenses
from .investment_commands import add_investment, add_investments_from_csv
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
cli.add_command(register)
cli.add_command(login)
cli.add_command(add_expense)
cli.add_command(add_investment)
cli.add_command(add_expenses_from_csv)
cli.add_command(add_investments_from_csv)
cli.add_command(show)
cli.add_command(list_expenses)

if __name__ == "__main__":
    cli(_anyio_backend="asyncio")
