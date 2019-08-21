from django.conf.urls import url
from . import views

app_name = 'IntroManager'
urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^query/$', views.ConnectionsView.as_view(), name='query'),
]

