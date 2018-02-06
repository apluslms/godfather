from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, UserGroup
from .forms import UserGroupForm

class UserGroupListView(ListView):
    model = UserGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nodes'] = UserGroup.objects.all()
        return context


def edit_group(request, group_name=None):
    if group_name:
        usergroup = get_object_or_404(UserGroup, group_name=group_name)
        form = UserGroupForm(request.POST or None, instance=usergroup)
    else:
        usergroup = None
        form = UserGroupForm(request.POST or None)
    for name in form.fields:
        form.fields[name].widget.attrs = {'class': 'form-control'}
    if request.method == 'POST' and form.is_valid():
        form_obj = form.save(commit=False)
        form_obj.save()
        return redirect('usergroup-list')
    return render(request, 'groups/edit.html', {
        'usergroup': usergroup,
        'form': form,
    })