"""
Configuration settings for the Gym Management System
"""

import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLiteDict database settings
DATABASE = {
    'path': os.path.join(BASE_DIR, 'instance', 'gym.sqlite'),
    'autocommit': True,
}

# SMS settings (placeholder for future implementation)
SMS = {
    'enabled': False,  # Set to True when you have integrated an SMS provider
    'provider': 'console',  # Options: 'console', 'twilio', etc.
    # Twilio settings (add these when implementing Twilio)
    # 'account_sid': 'your_twilio_sid',
    # 'auth_token': 'your_twilio_auth_token',
    # 'from_number': 'your_twilio_phone_number',
}

# Application settings
APP = {
    'name': 'Gym Management System',
    'debug': True,
    'secret_key': os.environ.get('SECRET_KEY', os.urandom(24)),
}

# Security settings
SECURITY = {
    'password_hash_method': 'pbkdf2:sha256',
    'password_salt_length': 8,
}