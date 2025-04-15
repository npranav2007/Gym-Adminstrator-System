"""
User model for Gym Management System.
Handles user authentication and profile management.
"""

import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_db


class User:
    """
    User model for authentication and profile management.
    """

    def __init__(self, username=None, password=None, user_data=None):
        """
        Initialize a user instance.

        Args:
            username (str): Username for the user
            password (str): Plain text password
            user_data (dict): User data dictionary (for loading from DB)
        """
        if user_data:
            self.username = user_data.get('username')
            self.password_hash = user_data.get('password')
            self.created_at = user_data.get('created_at')
        else:
            self.username = username
            self.password_hash = generate_password_hash(password) if password else None
            self.created_at = datetime.datetime.now().isoformat()

    @staticmethod
    def get(username):
        """
        Get a user by username.

        Args:
            username (str): Username to look up

        Returns:
            User: User instance or None if not found
        """
        db = get_db()
        users = db.get('users', {})

        if username in users:
            return User(user_data=users[username])
        return None

    @staticmethod
    def get_all():
        """
        Get all users.

        Returns:
            list: List of User instances
        """
        db = get_db()
        users = db.get('users', {})

        return [User(user_data=user_data) for username, user_data in users.items()]

    def save(self):
        """
        Save the user to the database.

        Returns:
            bool: True if successful, False otherwise
        """
        db = get_db()
        users = db.get('users', {})

        users[self.username] = {
            'username': self.username,
            'password': self.password_hash,
            'created_at': self.created_at
        }

        db['users'] = users
        db.sync()
        return True

    def verify_password(self, password):
        """
        Verify a password against the stored hash.

        Args:
            password (str): Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert user to dictionary representation.

        Returns:
            dict: Dictionary representation of user
        """
        return {
            'username': self.username,
            'created_at': self.created_at
        }