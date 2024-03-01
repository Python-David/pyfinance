from typing import Dict, List, Optional, Tuple

import asyncclick as click
from asyncclick import Context

from config import CSV_PATH, EXPENSE_CSV_HEADERS
from controllers.main_controller import MainController
from models import Expense

from .io_clients.csv_client import CsvClient
from .utilities import requires_login


@click.command()
@requires_login
@click.option("-c", "--category", required=True, help="Expense category.")
@click.option("-a", "--amount", required=True, type=float, help="Amount spent.")
@click.option(
    "-d",
    "--date",
    "date_str",
    required=True,
    help="Date of the expense in YYYY-MM-DD format.",
)
@click.pass_context
async def add_expense(
    ctx: Context, category: str, amount: float, date_str: str
) -> None:
    """Add a new expense."""
    # Assuming get_user_id_from_session is synchronous, directly using without await
    user_id: int = MainController().get_user_id_from_session(ctx.obj.session_token)

    # Assuming add_expense is synchronous as well
    success, message = MainController().add_expense(user_id, category, amount, date_str)
    if success:
        click.echo(f"Success. | {message}")
    else:
        click.echo(f"Failed. | {message}")


@click.command()
@requires_login
@click.option(
    "-f",
    "--file-path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the CSV file containing expenses.",
)
@click.pass_context
async def add_expenses_from_csv(ctx: Context, file_path: str) -> None:
    """Add expenses from a CSV file."""
    user_id: int = MainController().get_user_id_from_session(ctx.obj.session_token)

    headers: List[str] = EXPENSE_CSV_HEADERS
    csv_client: CsvClient = CsvClient(file_path=file_path, headers=headers)

    successful_rows: int = 0
    failed_rows: int = 0
    failed_details: List[Tuple[dict, str]] = []

    async for row in csv_client.read_large_csv():  # Directly iterate over each row
        try:
            category: str = row["CATEGORY"]
            amount: float = float(row["AMOUNT"])  # Ensure amount is a float
            date_str: str = row["DATE"]
            success, message = MainController().add_expense(
                user_id, category, amount, date_str
            )
            if success:
                click.echo(
                    f"Added expense: {category}, {amount}, {date_str}. | {message}"
                )
                successful_rows += 1
            else:
                click.echo(
                    f"Failed to add expense: {category}, {amount}, {date_str}. | {message}"
                )
        except Exception as e:
            click.echo(f"Error processing row: {row} | Error: {str(e)}")
            failed_rows += 1
            failed_details.append((row, str(e)))
    # Final report to the user
    click.echo(f"Upload complete. Successfully added {successful_rows} investments.")
    if failed_rows > 0:
        click.echo(
            f"Failed to add {failed_rows} investments. Review the errors for details."
        )
        for detail in failed_details:
            click.echo(f"Failed row: {detail[0]} | Error: {detail[1]}")


@click.command()
@requires_login
@click.option("-y", "--year", type=int, help="Filter expenses by year.")
@click.option("-m", "--month", type=int, help="Filter expenses by month (1-12).")
@click.option("-d", "--day", type=int, help="Filter expenses by day (1-31).")
@click.option("-s", "--show-csv", is_flag=True, help="Show the expenses in CSV format.")
@click.pass_context
async def list_expenses(
    ctx: Context,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    show_csv: Optional[bool] = False,
) -> None:
    """List out expenses, optionally filtered by month. Shows current month if no month is specified."""
    user_id: int = MainController().get_user_id_from_session(ctx.obj.session_token)

    expenses: List[Expense] = MainController().get_expenses(
        user_id, year=year, month=month, day=day
    )

    if not expenses:
        click.echo("No expenses found.")
        return

    if show_csv:
        # Define the path where you want to save the CSV
        csv_path: str = CSV_PATH
        headers: List[str] = ["Category", "Amount", "Date"]
        csv_client: CsvClient = CsvClient(file_path=csv_path, headers=headers)

        # Convert expenses to a list of dictionaries matching the CSV headers
        data: List[Dict[str, str]] = [
            {"Category": e.category, "Amount": e.amount, "Date": e.date}
            for e in expenses
        ]

        # Write the data to a CSV
        success, message = await csv_client.write_to_csv(data)
        if not success:
            click.echo(message)
        else:
            click.echo(f"Expenses saved to CSV: {csv_path}")
    else:
        for expense in expenses:
            click.echo(
                f"Category: {expense.category}, Amount: {expense.amount}, Date: {expense.date}"
            )
