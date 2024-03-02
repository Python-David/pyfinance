import os
from functools import wraps
from typing import Any, Callable, Coroutine, Optional

import asyncclick as click

from controllers.main_controller import MainController


def save_session_token(token: str) -> None:
    token_dir: str = os.path.join(os.path.expanduser("~"), ".pyfinance")
    if not os.path.exists(token_dir):
        os.makedirs(token_dir)
    token_path: str = os.path.join(token_dir, "session_token.txt")
    with open(token_path, "w") as token_file:
        token_file.write(token)


def get_session_token() -> Optional[str]:
    token_path: str = os.path.join(
        os.path.expanduser("~"), ".pyfinance", "session_token.txt"
    )
    try:
        with open(token_path, "r") as token_file:
            return token_file.read().strip()
    except FileNotFoundError:
        return None


def requires_login(
    f: Callable[..., Coroutine[Any, Any, Any]]
) -> Callable[..., Coroutine[Any, Any, Any]]:
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        ctx = click.get_current_context()

        session_token = get_session_token()
        if session_token is None:
            click.echo("Session token not found. Please login.")
            ctx.abort()

        if not MainController().is_session_valid(session_token):
            click.echo("Session is invalid or has expired. Please login again.")
            ctx.abort()

        ctx.obj.session_token = session_token
        return await f(*args, **kwargs)

    return decorated_function
