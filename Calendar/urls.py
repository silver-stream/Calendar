"""Calendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from boards import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.table, name='home'),
    path('admin/', admin.site.urls),
    path('oxford/',views.oxford),
    path('shift/',views.shift,name='shift'),
    path('table/',views.table),
    url(r'^table/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$',
        views.day_view,
        name='day-view'),
    url(
        r'^events/add/$',
        views.add_event,
        name='add-event'
    ),
]


