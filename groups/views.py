from django.views.generic import ListView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import UserProfile, UserGroup, Membership
from .forms import UserGroupForm
from .permissions import GroupEditPermission
from lib.viewbase import BaseFormView

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserGroupListView(ListView):
    model = UserGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nodes'] = UserGroup.objects.all()
        return context

class UserGroupDeleteView(DeleteView):
    model = UserGroup
    slug_url_kwarg = 'group_name'
    success_url = reverse_lazy('usergroup-list')

    def get_object(self, queryset=None):
        group_name = self.kwargs['group_name']
        try:
            usergroup = self.model.objects.get(group_name=group_name)
        except UserGroup.DoesNotExist:
            usergroup = None
        return usergroup

class UserGroupEditView(BaseFormView):
    template_name = 'groups/edit.html'
    form_class = UserGroupForm
    success_url = 'usergroup-list'

    module_permissions_classes = (
        GroupEditPermission,
    )

    def get_permissions(self):
        perms = super().get_permissions()
        perms.extend((Perm() for Perm in self.module_permissions_classes))
        return perms

    def get_resource_objects(self, *args, **kwargs):
        usergroup = None
        super().get_resource_objects()
        groupname = ''
        if 'group_name' in self.kwargs:
            groupname = self.kwargs['group_name']

        if groupname:
            usergroup = get_object_or_404(UserGroup, group_name=groupname)

        self.usergroup = usergroup


    def get_context_data(self, **kwargs):
        group_name = ''
        if 'group_name' in kwargs:
            group_name = self.kwargs['group_name']
        if group_name:
            usergroup = get_object_or_404(UserGroup, group_name=group_name)
            form = UserGroupForm(self.request.POST or None, instance=usergroup)
            form.fields['administrators'].queryset = UserProfile.objects.all()
            form.fields['administrators'].initial = self.get_administrators(usergroup)
            form.fields['parent'].queryset = UserGroup.objects.all().exclude(group_name=group_name)
        else:
            usergroup = None
            form = UserGroupForm(self.request.POST or None)
        for name in form.fields:
            form.fields[name].widget.attrs = {'class': 'form-control'}
        context = {
                'usergroup': usergroup,
                'form': form,
            }
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['form']
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, context)

    @staticmethod
    def get_administrators(usergroup):
        current_administrators_memberships = Membership.objects.filter(usergroup=usergroup, is_administrator=True)
        current_administrators_id = []
        for current_administrators_membership in current_administrators_memberships:
            administrator_id = current_administrators_membership.userprofile.id
            current_administrators_id.append(administrator_id)
        return UserProfile.objects.filter(id__in=current_administrators_id)
