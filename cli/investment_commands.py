from typing import List, Tuple

import asyncclick as click
from asyncclick import Context

from config import INVESTMENT_CSV_HEADERS
from controllers.main_controller import MainController
from models.finance_record import FinanceRecord

from .io_clients.csv_client import CsvClient
from .utilities import requires_login


@click.command()
@requires_login
@click.option("-t", "--investment-type", required=True, help="Type of investment.")
@click.option("-a", "--amount", required=True, type=float, help="Amount invested.")
@click.option(
    "-d",
    "--date",
    "date_str",
    required=True,
    help="Date of the investment in YYYY-MM-DD format.",
)
@click.option("-desc", "--description", required=False, help="Description of the expense.")
@click.pass_context
async def add_investment(
    ctx: Context,
    investment_type: str,
    amount: float,
    date_str: str,
    description: str = None,
) -> None:
    """Add a new investment."""
    user_id: int = MainController().get_user_id_from_session(ctx.obj.session_token)
    investment_record = FinanceRecord(
        user_id=user_id,
        investment_type=investment_type,
        amount=amount,
        date=date_str,
        description=description,
    )
    success, message = MainController().add_investment(investment_record)
    if success:
        click.echo(f"Investment added successfully. | {message}")
    else:
        click.echo(f"Failed to add investment. | {message}")


@click.command()
@requires_login
@click.option(
    "-f",
    "--file-path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the CSV file containing investments.",
)
@click.pass_context
async def add_investments_from_csv(ctx: Context, file_path: str) -> None:
    """Add investments fromadd_investments_from_csv a CSV file."""
    user_id: int = MainController().get_user_id_from_session(ctx.obj.session_token)

    headers: List[str] = INVESTMENT_CSV_HEADERS
    csv_client: CsvClient = CsvClient(file_path=file_path, headers=headers)

    successful_rows: int = 0
    failed_rows: int = 0
    failed_details: List[Tuple[dict, str]] = []

    async for row in csv_client.read_large_csv():  # Directly iterate over each row
        try:
            investment_name: str = row["TYPE"]
            amount: float = float(row["AMOUNT"])  # Ensure amount is a float
            date_str: str = row["DATE"]
            success, message = MainController().add_investment(
                user_id, investment_name, amount, date_str
            )
            if success:
                click.echo(
                    f"Added investment: {investment_name}, {amount}, {date_str}. | {message}"
                )
                successful_rows += 1
            else:
                click.echo(
                    f"Failed to add investment: {investment_name}, {amount}, {date_str}. | {message}"
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
