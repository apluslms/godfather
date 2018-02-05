from django.urls import path

from groups.views import UserProfileListView, UserGroupListView

urlpatterns = [
    path('users', UserProfileListView.as_view(), name='userprofile-list'),
    path('groups', UserGroupListView.as_view(), name='usergroup-list'),
]