# Register your models here.
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from boards.models import *
from boards.models import Category
from boards.models import Wind


class WindAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'wind_speed', 'highest_gust')


admin.site.register(Category)
admin.site.register(Wind, WindAdmin)
