from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^twitter/$', views.twitter, name="twitter"),
]