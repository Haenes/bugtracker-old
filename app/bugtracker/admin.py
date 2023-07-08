from django.contrib import admin

# Register your models here.
from .models import Issue_type, Issue_priority, Issue_status, Project_type, Project, Issue

admin.site.register(Issue_type)
admin.site.register(Issue_priority)
admin.site.register(Issue_status)
admin.site.register(Issue)
admin.site.register(Project_type)
admin.site.register(Project)
