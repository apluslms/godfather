from django.conf.urls import url

from groups.views import UserGroupListView, UserGroupDeleteView, edit_group

urlpatterns = [
    url(r'^$', UserGroupListView.as_view(), name='usergroup-list'),
    url(r'^new/$', edit_group, name='group-edit'),
    url(r'^([\w\s-]+)/$', edit_group, name='group-edit'),
    url(r'^delete/(?P<group_name>[\w\s-]+)/$', UserGroupDeleteView.as_view(), name='group-delete')

]