from django import forms

from .models import UserGroup, UserProfile, Membership


class UserGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["members"].help_text = ""
        self.fields['members'].queryset = UserProfile.objects.all()
        self.fields['members'].required = False

    parent = forms.ModelChoiceField(queryset=UserGroup.objects.all(), required=False)

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


