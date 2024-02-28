import asyncclick as click

from config import EXPENSE_CSV_HEADERS
from controllers.main_controller import MainController
from .io_clients.csv_client import CsvClient
from .utilities import requires_login


@click.command()
@requires_login
@click.option('--category', required=True, help='Expense category.')
@click.option('--amount', required=True, type=float, help='Amount spent.')
@click.option('--date', 'date_str', required=True, help='Date of the expense in YYYY-MM-DD format.')
@click.pass_context
async def add_expense(ctx, category, amount, date_str):
    """Add a new expense."""
    # Assuming get_user_id_from_session is synchronous, directly using without await
    user_id = MainController().get_user_id_from_session(ctx.obj.session_token)

    # Assuming add_expense is synchronous as well
    success, message = MainController().add_expense(user_id, category, amount, date_str)
    if success:
        click.echo(f"Success. | {message}")
    else:
        click.echo(f"Failed. | {message}")


@click.command()
@requires_login
@click.option('--file-path', required=True, type=click.Path(exists=True), help='Path to the CSV file containing expenses.')
@click.pass_context
async def add_expenses_from_csv(ctx, file_path):
    """Add expenses from a CSV file."""
    user_id = MainController().get_user_id_from_session(ctx.obj.session_token)
    if not user_id:
        click.echo("You need to login first.")
        return

    headers = EXPENSE_CSV_HEADERS
    csv_client = CsvClient(file_path=file_path, headers=headers)

    successful_rows = 0
    failed_rows = 0
    failed_details = []

    async for row in csv_client.read_large_csv():  # Directly iterate over each row
        try:
            category = row["CATEGORY"]
            amount = float(row["AMOUNT"])  # Ensure amount is a float
            date_str = row["DATE"]
            success, message = MainController().add_expense(user_id, category, amount, date_str)
            if success:
                click.echo(f"Added expense: {category}, {amount}, {date_str}. | {message}")
                successful_rows += 1
            else:
                click.echo(f"Failed to add expense: {category}, {amount}, {date_str}. | {message}")
        except Exception as e:
            click.echo(f"Error processing row: {row} | Error: {str(e)}")
            failed_rows += 1
            failed_details.append((row, str(e)))
    # Final report to the user
    click.echo(f"Upload complete. Successfully added {successful_rows} investments.")
    if failed_rows > 0:
        click.echo(f"Failed to add {failed_rows} investments. Review the errors for details.")
        for detail in failed_details:
            click.echo(f"Failed row: {detail[0]} | Error: {detail[1]}")

