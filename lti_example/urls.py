from django.conf.urls import url, include


from .views import frontpage



urlpatterns = [
    url(r'^$', frontpage, name='frontpage'),
]