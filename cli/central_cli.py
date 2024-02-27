import click
from .user_commands import register, login
from .expense_commands import add_expense
from .investment_commands import add_investment


class Context:
    def __init__(self):
        self.session_token = None


@click.group()
@click.pass_context
def cli(ctx):
    """PyFinance CLI"""
    ctx.obj = Context()


# Add commands to your CLI
cli.add_command(register)
cli.add_command(login)
cli.add_command(add_expense)
cli.add_command(add_investment)

if __name__ == '__main__':
    cli()
