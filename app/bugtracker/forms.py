from django.forms import ModelForm, TextInput, EmailInput
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from bugtracker.models import Issue_type, Issue_status, Issue_priority, Project_type, Project, Issue

import re


def validate_string(string):
    pattern = re.compile("^([a-zA-Z]+$)")
    if pattern.match(string):
        return True
    return False


class UserForm(ModelForm):

      
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

        widgets = {
            "first_name": TextInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
            "last_name": TextInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
            "username": TextInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
            "email": EmailInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
        }

        help_texts = {
            "username": (""),
        }


    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if len(first_name) < 2:
            raise ValidationError("Name length must be more than 2 characters")
        elif not validate_string(first_name):
            raise ValidationError("Name must have only letters")

        return first_name
    

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if len(last_name) < 2:
            raise ValidationError("Name length must be more than 2 characters") 
        elif not validate_string(last_name):
            raise ValidationError("Name must have only letters")
        
        return last_name
    

class RegisterForm(UserForm):
    class Meta():
        fields = ["password"]



class ProjectDetailsForm(ModelForm):


    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise ValidationError("Project name length must be more than 3 characters") 

        return name
    

    def clean_key(self):
        key = self.cleaned_data["key"]
        if len(key) < 3:
            raise ValidationError("Project key length must be more than 4 letters")
        elif not validate_string(key):
            raise ValidationError("Key must have only letters")
        
        return key


    class Meta:
        model = Project
        fields = ["name", "key"]

        widgets = {
            "name": TextInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
            "key": TextInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
        }