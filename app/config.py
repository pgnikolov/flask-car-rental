from dotenv import load_dotenv
import os

# Load environment variables from a .env file if available
load_dotenv()


class Config:
    """
    Configuration class for managing Flask application's email settings.

    Attributes:
        MAIL_SERVER (str): The mail server hostname. Defaults to Gmail's SMTP server.
        MAIL_PORT (int): The port for the mail server. Uses 587 for Gmail's TLS configuration.
        MAIL_USE_TLS (bool): Enables Transport Layer Security (TLS) for email. Typically used with port 587.
        MAIL_USE_SSL (bool): Enables Secure Sockets Layer (SSL) encryption. Typically used with port 465. Defaults to False.
        MAIL_USERNAME (str): The email address used to authenticate with the mail server, sourced from environment variables.
        MAIL_PASSWORD (str): The password for the email account, sourced from environment variables.
        MAIL_DEFAULT_SENDER (str): The default "from" address for outgoing emails, sourced from environment variables.
    """

    # SMTP server configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # Credentials and default sender information
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
