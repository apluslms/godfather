from django.conf.urls import url

from groups.views import UserGroupListView, UserGroupDeleteView, UserGroupEditView, UserProfileDetailView

urlpatterns = [
    url(r'^$', UserGroupListView.as_view(), name='usergroup-list'),
    url(r'^new/$', UserGroupEditView.as_view(), name='group-edit'),
    url(r'^(?P<group_name>[\w\s-]+)/$', UserGroupEditView.as_view(), name='group-edit'),
    url(r'^delete/(?P<group_name>[\w\s-]+)/$', UserGroupDeleteView.as_view(), name='group-delete'),
    url(r'^user/(?P<user_name>[\w\s-]+)/$', UserProfileDetailView.as_view(), name='user-detail'),

]