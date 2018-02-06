from django import forms

from .models import UserGroup, UserProfile, Membership


class UserGroupForm(forms.ModelForm):

    parent = forms.ModelChoiceField(queryset=UserGroup.objects.all(), required=False)
    members = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all(), required=False)

    def save(self, commit=True):
        usergroup = super(UserGroupForm, self).save(commit=False)
        usergroup.group_name = self.cleaned_data['group_name']
        usergroup.parent = self.cleaned_data['parent']
        for member in self.cleaned_data['members']:
            membership = Membership.objects.create(userprofile=member, usergroup=usergroup)
            membership.save()
        if commit:
            usergroup.save()

    class Meta:
        model = UserGroup
        fields = [
            'group_name',
            'parent',
            'members',
        ]
