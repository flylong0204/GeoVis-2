from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^users/$', views.user_list),
    url(r'^datavalue/$', views.data_value),
]

#urlpatterns = format_suffix_patterns(urlpatterns)