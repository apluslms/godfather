from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Additional user information and methods.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_administrator = models.BooleanField(
        default=False,
        help_text=('Designates whether the user is administrator of the group'),
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{} ({} {})".format(self.user.username, self.user.first_name, self.user.last_name)


class UserGroup(models.Model):

    parent_group = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='child_groups')
    members = models.ManyToManyField(UserProfile, related_name='belonged_groups')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
