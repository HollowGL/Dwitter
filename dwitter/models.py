from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username


# Create a Profile for each new user with a follow relationship to itself & the admin
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

        admin_user = User.objects.get(username='admin')
        user_profile.follows.set([admin_user.profile, instance.profile])
        user_profile.save()


class Dweet(models.Model):
    user = models.ForeignKey(
        User, related_name="dweets", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_dweets", blank=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dweet = models.ForeignKey(Dweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'dweet')
