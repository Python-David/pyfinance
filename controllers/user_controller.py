from database import SessionLocal  # Assuming this is your session factory
from models.user import User
import bcrypt


class UserController:
    def __init__(self):
        # Initialize a new SQLAlchemy session, similar to FinanceTracker
        self.db_session = SessionLocal()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, provided_password: str, stored_hash: str) -> bool:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

    def register_new_user(self, name: str, email: str, password: str) -> (bool, str):
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

    def validate_login(self, email: str, password: str) -> (bool, str, int):
        user = self.db_session.query(User).filter(User.email == email).first()
        if user:
            if self.verify_password(password, user.hashed_password):
                return True, "Login successful.", user.id
            else:
                return False, "Incorrect password.", None
        else:
            return False, "User not found.", None

    def close_session(self):
        # Make sure to close the session when it's no longer needed
        self.db_session.close()
