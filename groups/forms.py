from django import forms

from .models import UserGroup


class UserGroupForm(forms.ModelForm):

    class Meta:
        model = UserGroup
        fields = [
            'group_name',
            'parent_group',
            'members',
        ]
