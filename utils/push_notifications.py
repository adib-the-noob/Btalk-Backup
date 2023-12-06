from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification, Message


def send_push_notification(user, title, body, data = None):
    devices = FCMDevice.objects.filter(user=user)
    if devices is not None:
        for device in devices:
            device.send_message(
                Message(
                    data=data,
                    notification=Notification(
                        title=title,
                        body=body,
                    ),
                )
            )
