from django.contrib import admin

from discovers.models import HomeDiscover


@admin.register(HomeDiscover)
class HomeDiscoverAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'link', 'button_title')
    search_fields = ('id', 'title', 'description', 'link', 'button_title')
    list_filter = ('button_title', )
