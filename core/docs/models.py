from django.db import models
import uuid

class Document(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    send_to = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return f"{self.title} (UUID: {self.uuid} - {self.send_to}"
    
class Pay(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    