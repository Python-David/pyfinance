import click
from controllers.main_controller import MainController
from .utilities import requires_login


@click.command()
@requires_login
@click.option('--investment-type', required=True, help='Type of investment.')
@click.option('--amount', required=True, type=float, help='Amount invested.')
@click.option('--date', 'date_str', required=True, help='Date of the investment in YYYY-MM-DD format.')
@click.pass_context
def add_investment(ctx, investment_type, amount, date_str):
    """Add a new investment."""
    user_id = MainController().get_user_id_from_session(ctx.obj.session_token)
    success, message = MainController().add_investment(user_id, investment_type, amount, date_str)
    if success:
        click.echo(f"Success. | {message}")
    else:
        click.echo(f"Failed. | {message}")
