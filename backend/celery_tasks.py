# from celery import Celery
# from backend.mail import mail, create_message
# from config import Config

# celery_app = Celery(
#     "tasks",
#     broker=Config.REDIS_URL,
#     backend=Config.REDIS_URL
# )


# @celery_app.task
# def send_email(recipients, subject: str, body: str):
#     """Send an email via Celery background task."""
#     message = create_message(
#         recipients=recipients if isinstance(recipients, list) else [recipients],
#         subject=subject,
#         body=body
#     )
#     import asyncio
#     asyncio.run(mail.send_message(message))

from celery import Celery
from asgiref.sync import async_to_sync
from config import get_settings
from mail import mail, create_message

settings = get_settings()

c_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

c_app.conf.update(
    broker_connection_retry_on_startup=True
)

@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):

    message = create_message(recipients=recipients, subject=subject, body=body)

    async_to_sync(mail.send_message)(message)
    print("Email sent")