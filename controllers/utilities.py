import uuid


def generate_session_token() -> str:
    """Generates a unique session token."""
    return str(uuid.uuid4())
