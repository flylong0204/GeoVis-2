from django.conf.urls import url
from weathervis import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'glyphvalues/$', views.glyphValues, name='index'),
    url(r'kmeansValues/$', views.kmeansValues, name='kmeans'),
    url(r'hierarValues/$', views.hierarValues, name='hierar'),
]
