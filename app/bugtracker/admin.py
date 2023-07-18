from django.contrib import admin

from .models import Project, Issue


admin.site.register(Issue)
admin.site.register(Project)
