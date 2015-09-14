from django.conf.urls import url
from weathervis import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
#     url(r'glyphvalues/$', views.glyphValues, name='index'),
#     url(r'kmeansValues/$', views.kmeansValues, name='kmeans'),
#     url(r'hierarValues/$', views.hierarValues, name='hierar'),
#     url(r'linearOpt/$', views.linearOpt, name='linear'),
    url(r'generateCand/$', views.generateCand, name='generateCand'),
    url(r'updateUncertainty/$', views.updateUncertaintyValues, name='updateUn'),
    url(r'execSingleOpt/$', views.singleLevelOpt, name='singopt'),
    url(r'getOptResult/$', views.getOptResult, name='getresult'),
    url(r'getApcpForecast/$', views.getApcpForecast, name='getApcpForecast'),
    url(r'consistencyOpt/$', views.consistencyOpt, name='consistencyOpt'),
]
