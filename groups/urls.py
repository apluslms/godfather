from django.conf.urls import url

from groups.views import UserGroupListView, UserGroupDeleteView, UserGroupEditView

urlpatterns = [
    url(r'^$', UserGroupListView.as_view(), name='usergroup-list'),
    url(r'^new/$', UserGroupEditView.as_view(), name='group-edit'),
    url(r'^(?P<group_name>[\w\s-]+)/$', UserGroupEditView.as_view(), name='group-edit'),
    url(r'^delete/(?P<group_name>[\w\s-]+)/$', UserGroupDeleteView.as_view(), name='group-delete')

]