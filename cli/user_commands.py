import asyncclick as click
from asyncclick import Context

from controllers.main_controller import MainController

from .utilities import save_session_token


@click.command()
@click.option("-n", "--name", required=True, help="Your name.")
@click.option("-e", "--email", required=True, help="Your email address.")
@click.option("-p", "--password", required=True, help="Your password.", hide_input=True)
async def register(name: str, email: str, password: str) -> None:
    """Register a new user."""
    # Ideally, MainController.register_new_user should be an async function
    controller: MainController = MainController()
    success, message = controller.register_new_user(name, email, password)
    if success:
        click.echo(message)
    else:
        click.echo(message)


@click.command()
@click.option("-e", "--email", required=True, help="Your email address.")
@click.option("-p", "--password", required=True, help="Your password.", hide_input=True)
@click.pass_context
async def login(ctx: Context, email: str, password: str) -> None:
    """Login a user."""
    # Ideally, MainController.validate_login should be an async function
    controller: MainController = MainController()
    success, message, token = controller.validate_login(email, password)
    if success:
        click.echo(message)
        save_session_token(token)
        ctx.obj.session_token = token
    else:
        click.echo(message)
