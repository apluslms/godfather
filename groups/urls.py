from django.conf.urls import url

from groups.views import UserProfileListView, UserGroupListView, edit_group

urlpatterns = [
    url(r'users$', UserProfileListView.as_view(), name='userprofile-list'),
    url(r'^$', UserGroupListView.as_view(), name='usergroup-list'),
    url(r'^new/$', edit_group, name='group-edit'),
    url(r'^([\w-]+)/$', edit_group, name='group-edit')

]