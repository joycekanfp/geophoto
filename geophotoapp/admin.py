from django.contrib import admin
from .models import *

class favListAdmin(admin.ModelAdmin):
    list_display = ('geophoto_title',)
    list_display_links = ('geophoto_title',)

    def geophoto_title(self, obj):
        return obj.geophoto.title
        geophoto_title.short_description = 'The title of Geophoto'


class presetListAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name','latitude','longitude',)
    ordering = ('name',)

admin.site.register(FavList, favListAdmin)
admin.site.register(PresetList, presetListAdmin)
