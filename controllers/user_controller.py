from datetime import datetime, timedelta

from sqlalchemy import and_

from controllers.utilities import generate_session_token
from database import SessionLocal
from models.sessions import Session
from models.user import User
import bcrypt
import pytz


class UserController:
    def __init__(self):
        # Initialize a new SQLAlchemy session, similar to FinanceTracker
        self.db_session = SessionLocal()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, provided_password: str, stored_hash: str) -> bool:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

    def register_new_user(self, name: str, email: str, password: str) -> (bool, str):
        email = email.lower()
        name = ' '.join(part.capitalize() for part in name.split())

        # Check if email already exists
        existing_user = self.db_session.query(User).filter(User.email == email).first()
        if existing_user:
            return False, "Email is already in use."

        # Hash password and create new user
        try:
            hashed_password = self.hash_password(password)
            new_user = User(name=name, email=email, hashed_password=hashed_password)
            self.db_session.add(new_user)
            self.db_session.commit()
            return True, "Registration successful."
        except Exception as e:
            # Log the error for debugging
            print(f"Error during user registration: {e}")
            return False, "An error occurred during registration."

    def create_session(self, user_id):
        token = generate_session_token()
        expires_at = datetime.utcnow() + timedelta(hours=1)  # 1 hour from now
        new_session = Session(token=token, user_id=user_id, expires_at=expires_at)
        self.db_session.add(new_session)
        self.db_session.commit()
        return token

    def validate_login(self, email: str, password: str) -> (bool, str, str):
        email = email.lower()
        user = self.db_session.query(User).filter(User.email == email).first()
        if user:
            if self.verify_password(password, user.hashed_password):
                # Generate a session token upon successful login
                session_token = self.create_session(user.id)
                return True, "Login successful.", session_token
            else:
                return False, "Incorrect password.", None
        else:
            return False, "User not found.", None

    def is_session_valid(self, session_token):
        # Query the database for the session token
        session = self.db_session.query(Session).filter(
            and_(
                Session.token == session_token,
                Session.expires_at > datetime.utcnow()  # Check if the session has not expired
            )
        ).first()

        # If a session is found and it's not expired, return True
        if session:
            return True
        else:
            # If no session is found or it's expired, return False
            return False

    def get_user_id_from_session(self, session_token):
        # Query the database for the session using the token
        session = self.db_session.query(Session).filter(Session.token == session_token).first()

        # Ensure datetime.now() is timezone-aware, using UTC in this example
        now_utc = datetime.now(pytz.utc)

        # Check if the session exists and has not expired
        if session and session.expires_at > now_utc:
            return session.user_id
        else:
            # Handle the case where the session is not found or has expired
            return None

    def close_session(self):
        # Make sure to close the session when it's no longer needed
        self.db_session.close()
