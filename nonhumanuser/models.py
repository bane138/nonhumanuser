from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
  # This line is required. Links UserProfile to a User model instance.
  user = models.ForeignKey(User, unique=True)

  # Additional attributes
  avatar = models.ImageField(upload_to='profile_images', blank=True)

  def __str__(self):
    return self.user.username