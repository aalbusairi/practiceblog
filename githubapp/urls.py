from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^org_members/$', views.org_members,name="org_members"),
    url(r'^list_branches/$', views.listbranches,name="list_branches"),
]