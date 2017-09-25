from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(
        r'^dashboard/(?P<pk>[0-9]+)/$',
        views.photo_detail,
        name='photo_detail'
    ),
    url(r'^photo$', views.photo_add, name='photo_add'),
    url(
        r'^dashboard/(?P<pk>[0-9]+)/delete$',
        views.photo_delete,
        name='photo_delete'),
]
