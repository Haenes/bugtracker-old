from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bugtracker.urls')),
    path("settings/", include("django.conf.urls.i18n")),
    path('', include('api.urls')),
]
