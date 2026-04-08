from celery import Celery
from mail import mail, create_message
from config import Config

celery_app = Celery(
    "tasks",
    broker=Config.REDIS_URL,
    backend=Config.REDIS_URL
)


@celery_app.task
def send_email(recipients, subject: str, body: str):
    """Send an email via Celery background task."""
    message = create_message(
        recipients=recipients if isinstance(recipients, list) else [recipients],
        subject=subject,
        body=body
    )
    import asyncio
    asyncio.run(mail.send_message(message))