from django.conf.urls import *
from django.urls import path
import geophotoapp.views as views

urlpatterns = [
    url(r'^$',views.search_photo, name="project_index"),
    url(r'search/$',views.search_photo, name="search_page"),
    url(r'preset_list/$',views.list_preset, name="preset_list"),
    url(r'fav_list/$',views.list_fav, name="fav_list"),

    url(r'post/ajax/add_to_fav/$',views.add_fav, name="add_to_fav"),
    url(r'post/ajax/delete_from_fav/$',views.delete_fav, name="delete_from_fav"),
    url(r'post/ajax/delete_from_preset/$',views.delete_preset, name="delete_from_preset"),

    url(r'preset_list/(?P<in_latitude>[-]?\d+\.?\d*)/(?P<in_longitude>[-]?\d+\.?\d*)/$',views.search_photo, name="search_from_preset_list"),
]