"""godfather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth
from django.conf.urls import url, include

if hasattr(auth, 'LoginView'):
    auth_login = auth.LoginView.as_view()
    auth_logout = auth.LogoutView.as_view()
else:
    auth_login = auth.login
    auth_logout = auth.logout

auth_urlpatterns = [
    url(r'^login/$', auth_login,
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_logout,
        {'next_page': '/'},
        name='logout'),
]

urlpatterns = [
    url(r'^auth/', include('django_lti_login.urls')),  # XXX: for django-lti-login
    url(r'^auth/', include(auth_urlpatterns)),
    url('admin/', admin.site.urls),
    url(r'^', include('lti_example.urls')),
    url(r'groups/', include('groups.urls')),
]