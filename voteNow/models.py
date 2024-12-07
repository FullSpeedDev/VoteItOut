from django.db import models

# Create your models here.
from django.db import models
import uuid

class Session(models.Model):
    title = models.CharField(max_length=255)  # Title of the session
    session_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique session identifier
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of session creation

    def __str__(self):
        return self.title
