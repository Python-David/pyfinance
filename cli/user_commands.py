import asyncclick as click
from .utilities import save_session_token
from controllers.main_controller import MainController


@click.command()
@click.argument('name')
@click.argument('email')
@click.argument('password')
async def register(name, email, password):
    """Register a new user."""
    # Ideally, MainController.register_new_user should be an async function
    controller = MainController()
    result = controller.register_new_user(name, email, password)
    click.echo(result)


@click.command()
@click.option('--email', required=True, help='Your email address.')
@click.option('--password', required=True, help='Your password.', hide_input=True)
@click.pass_context
async def login(ctx, email, password):
    """Login a user."""
    # Ideally, MainController.validate_login should be an async function
    controller = MainController()
    success, message, token = controller.validate_login(email, password)
    if success:
        click.echo(message)
        save_session_token(token)
        ctx.obj.session_token = token
    else:
        click.echo(message)
