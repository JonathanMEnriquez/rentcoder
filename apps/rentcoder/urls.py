from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.landing_page),
    url(r'^register$', views.register),
    url(r'^home$', views.home),
    url(r'^process/(?P<action>\w+)$', views.process),
]