from django import forms

from .models import UserGroup, UserProfile, Membership


class UserGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['members'].help_text = ""
        self.fields['members'].queryset = UserProfile.objects.all()
        self.fields['members'].required = False
        self.fields['administrators'].queryset = self.get_administrators()
        self.fields['administrators'].initial = self.get_administrators()

    parent = forms.ModelChoiceField(queryset=UserGroup.objects.all(), required=False)
    administrators = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all(), required=False)

    def save(self, commit=True):
        usergroup = super(UserGroupForm, self).save(commit=False)
        usergroup.group_name = self.cleaned_data['group_name']
        usergroup.parent = self.cleaned_data['parent']
        usergroup.save()
        self.save_members(usergroup)

    def get_administrators(self):
        usergroup = super(UserGroupForm, self).save(commit=False)

        current_administrators_memberships = Membership.objects.filter(usergroup=usergroup, is_administrator=True)
        current_administrators_id = []
        for current_administrators_membership in current_administrators_memberships:
            administrator_id = current_administrators_membership.userprofile.id
            current_administrators_id.append(administrator_id)

        return UserProfile.objects.filter(id__in = current_administrators_id)

    def save_members(self, usergroup):
        administrators = self.cleaned_data['administrators']
        # delete members
        current_membership = Membership.objects.filter(usergroup=usergroup)
        current_members = []
        for membership in current_membership:
            current_members.append(membership.userprofile)
        for member in current_members:
            if member not in self.cleaned_data['members']:
                removed_memberships = Membership.objects.filter(usergroup=usergroup, userprofile=member)
                removed_memberships.delete()

        for member in self.cleaned_data['members']:
            try:
                membership = Membership.objects.get(userprofile=member, usergroup=usergroup)
            except Membership.DoesNotExist:
                membership = None
            # Set or unset member as administrator
            if membership:
                if member in administrators:
                    membership.is_administrator = True
                else:
                    membership.is_administrator = False
                membership.save()
            # Create new membership
            else:
                if member in administrators:
                    membership = Membership.objects.create(userprofile=member, usergroup=usergroup, is_administrator=True)
                else:
                    membership = Membership.objects.create(userprofile=member, usergroup=usergroup, is_administrator=False)
                membership.save()


    class Meta:
        model = UserGroup
        fields = [
            'group_name',
            'parent',
            'members',
        ]


