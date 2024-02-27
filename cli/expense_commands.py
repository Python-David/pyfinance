import click
from controllers.main_controller import MainController
from .utilities import requires_login


@click.command()
@requires_login
@click.option('--category', required=True, help='Expense category.')
@click.option('--amount', required=True, type=float, help='Amount spent.')
@click.option('--date', 'date_str', required=True, help='Date of the expense in YYYY-MM-DD format.')
@click.pass_context
def add_expense(ctx, category, amount, date_str):
    """Add a new expense."""
    user_id = MainController().get_user_id_from_session(ctx.obj.session_token)
    success, message = MainController().add_expense(user_id, category, amount, date_str)
    if success:
        click.echo(f"Success. | {message}")
    else:
        click.echo(f"Failed. | {message}")
