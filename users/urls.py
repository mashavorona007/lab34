from django.conf.urls import include, url
from django.contrib import admin

from users import views

urlpatterns = [
    url(r'^login/$', views.LoginPage.as_view(), name='login'), 
    url(r'^signup/$', views.RegisterPage.as_view(), name='signup'), 
    url(r'^logout/$', views.LogoutPage.as_view(), name='logout'), 
    url(r'^logout/success/$', views.LogoutLandingPage.as_view(), name='logout_landing'), 
    url(r'^settings/$', views.SettingsPage.as_view(), name='settings'), 
]