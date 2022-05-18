from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

MAX_LENGTH = 200


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Recipe(models.Model):
    title = models.CharField(max_length=MAX_LENGTH)
    url = models.CharField(max_length=MAX_LENGTH)
    comments = models.CharField(max_length=MAX_LENGTH, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, related_name="updated_recipe"
    )
    owner = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, related_name="recipe_owner"
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
