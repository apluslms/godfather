from django.utils.translation import string_concat, ugettext_lazy as _

try:
    from django.utils.text import format_lazy
except ImportError: # implemented in Django 1.11
    from django.utils.functional import lazy as _lazy
    def _format_lazy(format_string, *args, **kwargs):
        return format_string.format(*args, **kwargs)
    format_lazy = _lazy(_format_lazy, str)

"""
Provides a set of pluggable permission policies.
"""


class BasePermission(object):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class MessageMixin(object):
    """
    Adds easy way to specify what exactly caused the PermissionDenied
    """
    def error_msg(self, message: str, delim=None, format=None, replace=False):
        """
        Add extra text to self.message about the reason why permission
        was denied. Uses lazy object so the message string is evaluated
        only when rendered.

        If optional argument `format` is given, then it's used with format_lazy
        to format the message with the dictionary arguments from `format` arg.

        Optional argument `delim` can be used to change the string used to join
        self.message and `message`.

        If optional argument `replace` is true, then self.message is replaced with
        the `message`.
        """
        if delim is None:
            delim = ': '

        if format:
            message = format_lazy(message, **format)

        if replace:
            self.message = message
        else:
            assert 'message' not in self.__dict__, (
                "You are calling error_msg without replace=True "
                "after calling it with it firts. Fix your code by removing "
                "firts method call add replace=True to second method call too."
            )
            self.message = string_concat(self.message, delim, message)


class ObjectVisibleBasePermission(MessageMixin, BasePermission):
    """
     It allows access to admin users, and skip objects that are not model.
    """
    model = None
    obj_var = None

    def has_permission(self, request, view):
        obj = getattr(view, self.obj_var, None)
        return (
            obj is None or
            self.has_object_permission(request, view, obj)
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            not isinstance(obj, self.model) or # skip objects that are not model in question
            user.is_staff or
            user.is_superuser or
            self.is_object_visible(request, view, obj)
            )

    def is_object_visible(self, request, view, obj):
        raise NotImplementedError
