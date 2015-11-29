from django.conf.urls import url
from scatterdatareview import views
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^review$', views.index, name='index'),
    url(r'getDataset/$', views.getDataset, name='getdataset'),
    url(r'saveClusterData', views.saveClusterData, name='savedataset'),
    
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_user, name='authuser'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
]
