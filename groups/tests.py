from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserGroup, UserProfile, Membership


# Create your tests here.
class GroupTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = User(username='testUser1')
        self.user1.last_name = 'testUser1'
        self.user1.set_password('testPassword1')
        self.user1.save()

        self.user2 = User(username='testUser2')
        self.user2.last_name = 'testUser2'
        self.user2.set_password('testPassword2')
        self.user2.save()

        self.userprofile1 = UserProfile(name='testUser1')
        self.userprofile1.save()
        self.userprofile2 = UserProfile(name='testUser2')
        self.userprofile2.save()
        self.usergroup = UserGroup(group_name='testGroup')
        self.usergroup.save()
        self.memberships = Membership(usergroup=self.usergroup, userprofile=self.userprofile1, is_administrator=True)
        self.memberships.save()

    def test_create_group(self):
        self.client.login(username='testUser1', password='testPassword1')
        form_data = {'group_name': 'testGroup_Created'}
        response = self.client.post('/groups/new/', form_data)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(UserGroup.objects.get(group_name='testGroup_Created'))

    def test_edit_group_permission_forbidden(self):
        self.client.login(username='testUser2', password='testPassword2')
        form_data_changed = {'group_name': 'testGroup_Changed'}
        response = self.client.post(reverse('group-edit', args=(self.usergroup.group_name,)), form_data_changed, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_edit_group_permission_passed(self):
        self.client.login(username='testUser1', password='testPassword1')
        form_data_changed = {'group_name': 'testGroup_Changed'}
        response = self.client.post(reverse('group-edit', args=(self.usergroup.group_name,)), form_data_changed, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(UserGroup.objects.get(group_name='testGroup_Changed'))

    def test_delete_group(self):
        self.client.login(username='testUser1', password='testPassword1')
        get_response = self.client.get(reverse('group-delete', args=(self.usergroup.group_name,)), follow=True)
        self.assertContains(get_response, 'Are you sure you want to delete')

        post_response = self.client.post(reverse('group-delete', args=(self.usergroup.group_name,)), follow=True)
        self.assertRedirects(post_response, reverse('usergroup-list'), status_code=302)

    def test_view_userprofile(self):
        self.client.login(username='testUser1', password='testPassword1')
        response = self.client.get(reverse('user-detail', args=('testUser1',)), follow=True)
        self.assertEqual(response.status_code, 200)

