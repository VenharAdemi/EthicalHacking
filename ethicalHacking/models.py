from django.db import models
from django.contrib.auth.models import AbstractUser

class UserPost(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="userpost_users",  # Avoids clash with default User model
        blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="userpost_permissions",  # Avoids clash
        blank=True
    )
# Create your models here.
class Post(models.Model):
    objects = None
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
