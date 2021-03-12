from django.conf.urls import *
from django.urls import path
import geophotoapp.views as views

urlpatterns = [
    url(r'^$',views.search_photo, name="project_index"),
    url(r'search/$',views.search_photo, name="search_page"),
    url(r'preset_list/$',views.list_preset, name="preset_list"),
    url(r'fav_list/$',views.list_fav, name="fav_list"),

    url(r'preset_list/(?P<latitude>\w+)/(?P<longitude>\w+)/$',views.search_photo, name="search_from_preset_list"),
]