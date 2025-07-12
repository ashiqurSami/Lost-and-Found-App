from django.conf import settings
from django.db import models

# Create your models here.
class LostFoundItem(models.Model):
    STATUS_CHOICES = (
        ('lost', 'Lost'),
        ('found', 'Found'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items',
    )

    name=models.CharField(max_length=255)
    category=models.CharField(max_length=100)
    description=models.TextField()
    location=models.CharField(max_length=255)
    image=models.ImageField(upload_to='item/images/')
    date=models.DateField()
    status=models.CharField(max_length=5,choices=STATUS_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.status.upper()}'