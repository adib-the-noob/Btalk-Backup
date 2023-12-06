from django.conf import settings
from celery import shared_task
from twilio.rest import Client


@shared_task
def send_otp(phone_number: str, otp: int):
    try:
        client = Client(
            settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
        )
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )
    except Exception as e:
        return False