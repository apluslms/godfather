from django.apps import AppConfig


class LtiExampleConfig(AppConfig):
    name = 'lti_example'
    verbose_name = 'LTI_Example'

    def ready(self):
        # Load our receivers
        # This is important as receiver hooks are not connected otherwise.
        from . import receivers  # NOQA
