from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    # CRUD Institute User
    url(r'^list/$', views.UserList.as_view(), name='user_list'),
    url(r'^create/$', views.UserCreate.as_view(), name='user_add'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.UserEdit.as_view(), name='user_edit'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.UserDelete.as_view(), name='user_delete'),

]
