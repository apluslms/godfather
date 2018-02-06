from django import forms

from .models import UserGroup, UserProfile


class UserGroupForm(forms.ModelForm):

    parent = forms.ModelChoiceField(queryset=UserGroup.objects.all(), required=False)
    members = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all(), required=False)

    class Meta:
        model = UserGroup
        fields = [
            'group_name',
            'parent',
            'members',
        ]
