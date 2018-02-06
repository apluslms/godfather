from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from mptt.models import MPTTModel, TreeForeignKey

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


class UserGroup(MPTTModel):

    group_name = models.CharField(max_length=40, default='', unique=True)
    parent = TreeForeignKey('self', null=True, on_delete=models.CASCADE, related_name='children')
    members = models.ManyToManyField(UserProfile, related_name='belonged_groups', through='Membership')
    created_time = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['group_name']

    def __str__(self):
        return "{} ".format(self.group_name)

class Membership(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    usergroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    is_administrator = models.BooleanField(default=True)
    joined_time = models.DateTimeField(auto_now_add=True)

