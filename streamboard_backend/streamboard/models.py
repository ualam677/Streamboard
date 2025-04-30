import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Streamboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='streamboards')
    title = models.CharField(max_length=255, blank=True)
    background_image = models.ImageField(upload_to='streamboards/backgrounds/')
    logo = models.ImageField(upload_to='streamboards/logo/', null=True, blank=True)
    layout_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_view = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f'Streamboard {self.id}'
