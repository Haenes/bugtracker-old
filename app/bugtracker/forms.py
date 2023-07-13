from django import forms
from django.forms import ModelForm, TextInput, Textarea, EmailInput, PasswordInput, Select, DateInput, CheckboxInput
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

from bugtracker.models import Project, Issue

import re


def validate_string(string):
    # Returns True if string contain only letters
    pattern = re.compile("^([a-zA-Z]+$)")
    if pattern.match(string):
        return True
        

class RegisterForm(forms.Form):


    first_name = forms.CharField(
        label="First name", 
        min_length=2, 
        max_length=255, 
        widget=TextInput(
            attrs={
            "required": True, 
            "class": "form-control mb-2"}))

    last_name = forms.CharField(
        label="Last name", 
        min_length=2, 
        max_length=255, 
        widget=TextInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))

    username = forms.CharField(
        label="Username", 
        min_length=4, 
        max_length=150, 
        widget=TextInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))

    email = forms.EmailField(
        label="Email", 
        max_length=255, 
        widget=TextInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))

    password1 = forms.CharField(
        label="Password", 
        max_length=32, 
        widget=PasswordInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))

    password2 = forms.CharField(
        label="Password confirmation", 
        max_length=32, 
        widget=PasswordInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))


    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].capitalize()

        if not validate_string(first_name):
            raise ValidationError("First name must have only letters")
        
        return first_name

    
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].capitalize()
        
        if not validate_string(last_name):
            raise ValidationError("Last name must have only letters")
        
        return last_name
    

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not validate_string(username):
            raise ValidationError("Username must have only letters")
        elif User.objects.filter(username=username):
            raise ValidationError("That username already exists")

        return username
    

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email):
            raise ValidationError("That email already exists")

        return email

    
    def clean_password1(self):
        """ 
        Returns True if password have:
            1) a 8 - 32 characters             {8,};
            2) at least one uppercase letter   (?=.*?[A-Z]);
            3) at least one lowercase letter   (?=.*?[a-z]); 
            4) at least one digit              (?=.*?[0-9]);
            5) at least one special character  (?=.*?[#?!@$%^&*-]). """
        
        password1 = self.cleaned_data["password1"]
        pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
        if not pattern.match(password1):
            raise ValidationError("The password doesn't match the conditions")

        return password1
    

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error("password2", "Passwords don't match")


    def save(self, commit=True): 
        cd = self.cleaned_data

        data = {
            "first_name": cd["first_name"],
            "last_name": cd["last_name"]
        }

        user = User.objects.create_user(
            username=cd["username"],
            email=cd["email"],
            password=cd["password1"],
            **data
        )

        return user 

        
class LoginForm(forms.Form):
        

    username = forms.CharField(
        min_length=4, 
        max_length=150, 
        widget=TextInput(
            attrs={
                "class": "form-control", 
                "id": "floatingUsername", 
                "placeholder": "Username", 
                "autofocus": True}))
    
    password = forms.CharField(
        min_length=8, 
        max_length=32, 
        widget=PasswordInput(
            attrs={
                "class": "form-control", 
                "id": "floatingPassword", 
                "placeholder": "Password"}))


# TODO: ADD USERNAME VALIDATION
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
        first_name = self.cleaned_data["first_name"].capitalize()

        if not validate_string(first_name):
            raise ValidationError("Name must have only letters")

        return first_name
    

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].capitalize()

        if not validate_string(last_name):
            raise ValidationError("Name must have only letters")
        
        return last_name


# TODO: CHANGE MIN_LENGHT OF FIELDS IN PROJECT MODEL. AFTER THAT - DELETE LEN CHECKS IN THE FORM
class ProjectDetailsForm(ModelForm):


    class Meta:
        model = Project
        fields = ["name", "key"]

        widgets = {
            "name": TextInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
            "key": TextInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
        }


    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise ValidationError("Project name length must be more than 3 characters") 

        return name
    

    def clean_key(self):
        key = self.cleaned_data["key"].upper()
        if len(key) < 3:
            raise ValidationError("Project key length must be more than 3 letters")
        elif not validate_string(key):
            raise ValidationError("Key must have only letters")
        
        return key


class ProjectModalForm(ModelForm):


    class Meta:
        model = Project
        fields = ["name", "key", "type", "starred"]

        widgets = {
            "name": TextInput(attrs={"class": "form-control bg-body-tertiary"}),
            "key": TextInput(attrs={"class": "form-control bg-body-tertiary"}),
            "type": Select(attrs={"class": "form-control bg-body-tertiary"}),
            "starred": CheckboxInput(attrs={"name": "Favorite",}),
        }

    def save(self): 
        cd = self.cleaned_data

        project = Project.objects.create(
            name=cd["name"],
            key=cd["key"],
            type=cd["type"],
            starred=cd["starred"]
        )

        return project 


class IssueModalForm(ModelForm):


    class Meta:
        model = Issue
        fields = ["project", "type", "priority", "title", "description", "duedate", "author"]

        widgets = {
            "project": Select(attrs={"class": "form-control bg-body-tertiary"}),
            "type": Select(attrs={"class": "form-control bg-body-tertiary"}),
            "priority": Select(attrs={"class": "form-control bg-body-tertiary"}),
            "title": TextInput(attrs={"class": "form-control bg-body-tertiary"}),
            "description": Textarea(attrs={"class": "form-control bg-body-tertiary", "rows": "5"}),
            "duedate": DateInput(attrs={"type": "date", "placeholder": "mm-dd-yyyy", "class": "form-control bg-body-tertiary"}),
            "author": TextInput(attrs={"author": forms.HiddenInput(),"class": "form-control bg-body-tertiary"}),
        }
