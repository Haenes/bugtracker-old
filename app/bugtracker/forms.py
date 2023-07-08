from django.forms import ModelForm
from django.contrib.auth.models import User

from bugtracker.models import Issue_type, Issue_status, Issue_priority, Project_type, Project, Issue


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
