from django.db import models
from django.conf import settings

class Issue(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Citizen', 'Citizen'),
        ('Admin', 'Admin'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200, blank=True, default='')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Citizen')
    locality = models.CharField(max_length=200, blank=True, default='')
    ward_number = models.CharField(max_length=50, blank=True, default='')
    mobile = models.CharField(max_length=20, blank=True, default='')
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name or self.user.get_username()
