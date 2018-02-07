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

        # delete members
        current_membership = Membership.objects.filter(usergroup=usergroup)
        current_members = []
        for membership in current_membership:
            current_members.append(membership.userprofile)
        for member in current_members:
            if member not in self.cleaned_data['members']:
                removed_memberships = Membership.objects.filter(usergroup=usergroup, userprofile=member)
                removed_memberships.delete()
        # add new members
        for member in self.cleaned_data['members']:
            if not Membership.objects.filter(userprofile=member, usergroup=usergroup):
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


