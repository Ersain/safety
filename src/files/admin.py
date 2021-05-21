from django.contrib import admin

from .models import File, ProfilePhoto

admin.site.register(ProfilePhoto)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'code', 'title', 'type')
    list_filter = ('type',)
