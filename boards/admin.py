

# Register your models here.
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from boards.models import *
from boards.models import Category


admin.site.register(Category)