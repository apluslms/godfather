from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env

# check for guide
# http://jonathanchu.is/posts/upgrading-jinja2-templates-django-18-with-admin/
# https://stackoverflow.com/questions/30701631/how-to-use-jinja2-as-a-templating-engine-in-django-1-8
