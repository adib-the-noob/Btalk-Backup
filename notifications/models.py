from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Notifications(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, blank=True)
    message = models.JSONField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.message['type']} - {self.is_read}"