from django.conf.urls import include, url
from django.contrib import admin

from lists import views

urlpatterns = [
    url(r'^$', views.ListsIndexPage.as_view(), name='lists_main'), 
    url(r'^(?P<id>\d+)/$', views.ListPage.as_view(), name='list'), 
    
    url(r'^new/$', views.AddList.as_view(), name='add_list'), 
    url(r'^delete/$', views.DeleteList.as_view(), name='delete_list'), 

    url(r'^(?P<id>\d+)/add/$', views.AddProduct.as_view(), name='add_product'),
    url(r'^(?P<id>\d+)/delete/$', views.DeleteProduct.as_view(), name='delete_product'),
    
    url(r'thumbnails', views.GetThumbnails.as_view(), name='thumbnails'),
]
