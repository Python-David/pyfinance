import asyncclick as click

from config import INVESTMENT_CSV_HEADERS
from controllers.main_controller import MainController
from .io_clients.csv_client import CsvClient
from .utilities import requires_login


@click.command()
@requires_login
@click.option('--investment-type', required=True, help='Type of investment.')
@click.option('--amount', required=True, type=float, help='Amount invested.')
@click.option('--date', 'date_str', required=True, help='Date of the investment in YYYY-MM-DD format.')
@click.pass_context
async def add_investment(ctx, investment_type, amount, date_str):
    """Add a new investment."""
    controller = MainController()
    user_id = controller.get_user_id_from_session(ctx.obj.session_token)
    if not user_id:
        click.echo("Session is invalid or has expired. Please login again.")
        return

    success, message = controller.add_investment(user_id, investment_type, amount, date_str)
    if success:
        click.echo(f"Investment added successfully. | {message}")
    else:
        click.echo(f"Failed to add investment. | {message}")


@click.command()
@requires_login
@click.option('--file-path', required=True, type=click.Path(exists=True), help='Path to the CSV file containing investments.')
@click.pass_context
async def add_investments_from_csv(ctx, file_path):
    """Add investments from a CSV file."""
    user_id = MainController().get_user_id_from_session(ctx.obj.session_token)
    if not user_id:
        click.echo("You need to login first.")
        return

    headers = INVESTMENT_CSV_HEADERS
    csv_client = CsvClient(file_path=file_path, headers=headers)

    async for row in csv_client.read_large_csv():  # Directly iterate over each row
        investment_name = row["TYPE"]
        amount = float(row["AMOUNT"])  # Ensure amount is a float
        date_str = row["DATE"]
        success, message = MainController().add_investment(user_id, investment_name, amount, date_str)
        if success:
            click.echo(f"Added investment: {investment_name}, {amount}, {date_str}. | {message}")
        else:
            click.echo(f"Failed to add investment: {investment_name}, {amount}, {date_str}. | {message}")

