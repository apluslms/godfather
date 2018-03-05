from django.utils.translation import ugettext_lazy as _
from .models import UserGroup, UserProfile, Membership
from authorization.permissions import MessageMixin, BasePermission

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GroupEditPermission(MessageMixin, BasePermission):
    message = _("The user group is not currently visible")

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, view.usergroup)

    def has_object_permission(self, request, view, usergroup):

        user = request.user
        # super user have access to all groups
        if user.is_superuser:
            return True

        if not user.is_authenticated:
            return False
        # get user profile by request.user.get_full_name
        try:
            userprofile = UserProfile.objects.get(name=user.get_full_name())
        except UserProfile.DoesNotExist:
            userprofile = None
        # get administrators
        administrators = self.get_administrators(usergroup)
        # no administrators in this group, all members will pass
        if not administrators.exists():
            return True
        # user is not administrator
        if userprofile not in administrators:
            return False

        return True

    @staticmethod
    def get_administrators(usergroup):
        current_administrators_memberships = Membership.objects.filter(usergroup=usergroup, is_administrator=True)
        current_administrators_id = []
        for current_administrators_membership in current_administrators_memberships:
            administrator_id = current_administrators_membership.userprofile.id
            current_administrators_id.append(administrator_id)
        return UserProfile.objects.filter(id__in=current_administrators_id)

