import uuid
from django.db import models

class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    birthdate = models.DateField()
    my_email_password = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.username} - {self.email}"
