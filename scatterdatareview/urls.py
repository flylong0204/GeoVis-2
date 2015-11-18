from django.conf.urls import url
from scatterdatareview import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
     url(r'getDataset/$', views.getDataset, name='getdataset'),
]
