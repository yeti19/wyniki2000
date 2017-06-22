from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    url(r'^obwod$', precinct),
    url(r'^gmina$', commune),
    url(r'^okrag$', district),
    url(r'^woj$', voivodeship),

    url(r'^obwod/([0-9]+)', precinct),
    url(r'^gmina/([0-9]+)', commune),
    url(r'^okrag/([0-9]+)', district),
    url(r'^woj/([0-9]+)', voivodeship),
    url(r'^kraj', country),
    
    url(r'^auth/login', auth_login),
    url(r'^auth/logout', auth_logout),
    url(r'^auth/register', auth_register),
    
    url(r'^admin/', admin.site.urls),
    url(r'^szukaj', search),
    url(r'^', TemplateView.as_view(template_name='main_rest.html')),
]
