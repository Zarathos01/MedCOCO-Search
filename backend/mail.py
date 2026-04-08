from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from config import Config

# Mail connection config — reads from .env via Config
mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

mail = FastMail(mail_config)


def create_message(recipients: list, subject: str, body: str) -> MessageSchema:
    """Create an email message schema."""
    return MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html
    )