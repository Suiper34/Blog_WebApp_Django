from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('regular', 'Regular'),
)


class User(AbstractUser):
    """Custom User model that extends the default Django User model."""
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='regular')

    def is_admin(self):
        return self.role == 'admin' or self.is_staff or self.is_superuser


class Profile(models.Model):
    """Profile model to store additional user information."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create profile on new user and ensure profile exists on save."""
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
        except Exception as e:
            print(e)
            pass
