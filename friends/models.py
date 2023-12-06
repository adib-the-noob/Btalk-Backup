from typing import Iterable, Optional
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserLocation(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.latitude} - {self.longitude}"

# This model file will be changed accordingly
class Contacts(BaseModel):
    """
    This model class was previously known as Friend
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contacts')
    contacts = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s contact list"

# Create a friend req model
class FriendRequest(BaseModel):
    STATUS_TYPE = (
        ("pending", "pending"),
        ("accepted", "accepted"),
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="freq_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="freq_receiver")
    status = models.CharField(max_length=10, choices=STATUS_TYPE)

    def __str__(self) -> str:
        return f"{self.sender.username} >> {self.receiver.username}: {self.status}"