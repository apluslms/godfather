from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserProfile(AbstractBaseUser):
    """
    Additional user information and methods.
    """
    name = models.CharField(max_length=100, unique=True)

    USERNAME_FIELD = 'name'

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.name)


class UserGroup(models.Model):

    group_name = models.CharField(max_length=40, default='', unique=True)
    parent_group = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='child_groups')
    members = models.ManyToManyField(UserProfile, related_name='belonged_groups', through='Membership')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return "{} ".format(self.group_name)

class Membership(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    usergroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    is_administator = models.BooleanField(default=True)
    joined_time = models.DateTimeField(auto_now_add=True)
