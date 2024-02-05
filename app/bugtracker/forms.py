import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.forms import (   
    CheckboxInput,
    EmailInput,
    ModelForm, 
    PasswordInput,
    Select, 
    Textarea, 
    TextInput    
    )
from django.utils.translation import gettext_lazy as _

from bugtracker.models import Project, Issue


def validate_string(string: str):
    """  Returns True if the string consists of only letters  """

    pattern = re.compile("^([a-zA-Z]+$)")   
    if pattern.match(string):
        return True


def validate_password(password: str):
    """ 
    Returns True if the password is:
    1) a 8+ characters                 {8,};
    2) at least one uppercase letter   (?=.*?[A-Z]);
    3) at least one lowercase letter   (?=.*?[a-z]); 
    4) at least one digit              (?=.*?[0-9]);
    5) at least one special character  (?=.*?[#?!@$%^&*-]). 
    """

    pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
    if pattern.match(password):
        return True


class RegisterForm(forms.Form):


    first_name = forms.CharField(
        label=_("First name"), 
        min_length=2, 
        max_length=255, 
        widget=TextInput(
            attrs={
            "required": True, 
            "class": "form-control mb-2"}))

    last_name = forms.CharField(
        label=_("Last name"), 
        min_length=2, 
        max_length=255, 
        widget=TextInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))

    username = forms.CharField(
        label=_("Username"), 
        min_length=4, 
        max_length=150, 
        widget=TextInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))

    email = forms.EmailField(
        label=_("Email"), 
        max_length=255, 
        widget=TextInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))

    password1 = forms.CharField(
        label=_("Password"),
        min_length=8, 
        max_length=32, 
        widget=PasswordInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))

    password2 = forms.CharField(
        label=_("Password confirmation"),
        min_length=8, 
        max_length=32, 
        widget=PasswordInput(
            attrs={
                "required": True, 
                "class": "form-control mb-2"}))


    def clean_first_name(self):       
        first_name = self.cleaned_data["first_name"].capitalize()

        if not validate_string(first_name):
            raise ValidationError(_("First name must have only letters"))

        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].capitalize()

        if not validate_string(last_name):
            raise ValidationError(_("Last name must have only letters"))

        return last_name


    def clean_username(self):
        username = self.cleaned_data["username"].lower()

        if not validate_string(username):
            raise ValidationError(_("Username must have only letters"))
        elif User.objects.filter(username=username):
            raise ValidationError(_("That username already exists"))

        return username


    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email):
            raise ValidationError(_("That email already exists"))

        return email


    def clean_password1(self):     
        password1 = self.cleaned_data["password1"]

        if not validate_password(password1):
            raise ValidationError(_("The password doesn't meet the conditions"))

        return password1


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error("password2", _("Passwords don't match"))


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
        label=_("username"),
        min_length=4, 
        max_length=150, 
        widget=TextInput(
            attrs={
                "class": "form-control", 
                "id": "floatingUsername", 
                "placeholder": _("Username"), 
                "autofocus": True}))

    password = forms.CharField(
        label=_("password"),
        min_length=8, 
        max_length=32, 
        widget=PasswordInput(
            attrs={
                "class": "form-control", 
                "id": "floatingPassword", 
                "placeholder": _("Password")}))

    remember = forms.CharField(
        required=False,
        widget=CheckboxInput(
            attrs={
                "class": "form-check-input", 
                "id": "remember_me"}))


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


    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]

        if len(first_name) < 2:
            raise ValidationError(_("First name must contain at least 2 letters"))       
        elif not validate_string(first_name):
            raise ValidationError(_("First name must have only letters"))

        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]

        if len(last_name) < 2:
            raise ValidationError(_("Last name must contain at least 2 letters")) 
        elif not validate_string(last_name):
            raise ValidationError(_("Last name must have only letters"))

        return last_name


class UserPasswordChangeForm(forms.Form):


    new_password1 = forms.CharField(
        label=_("New password"),
        min_length=8,
        max_length=32,
        widget=forms.PasswordInput(attrs={"class": "col-4 mb-3 form-control bg-body-tertiary", "autofocus": True}),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        min_length=8,
        max_length=32,
        widget=forms.PasswordInput(attrs={"class": "col-2  mb-4 form-control bg-body-tertiary"}),
    )


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


    def clean_new_password1(self):
        password1 = self.cleaned_data.get("new_password1")
        if not validate_password(password1):
            raise ValidationError(_("The password doesn't meet the conditions"))
        return password1


    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2


    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ProjectDetailsForm(ModelForm):


    class Meta:
        model = Project
        fields = ["name", "key", "starred"]

        labels = {
            "name": _("name"),
            "key": _("key"),
        }

        widgets = {
            "name": TextInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
            "key": TextInput(attrs={"required": True, "class": "form-control bg-body-tertiary"}),
            "starred": CheckboxInput(attrs={"name": "Favorite", "style": "width:20px; height:20px", "class": "form-check-input"}),
        }


    def clean_name(self):
        name = self.cleaned_data["name"]

        if not validate_string(name):
            raise ValidationError(_("Project name must have only letters"))

        return name
  

    def clean_key(self):
        key = self.cleaned_data["key"]

        if not validate_string(key):
            raise ValidationError(_("Key must have only letters"))

        return key


class ProjectModalForm(ModelForm):


    class Meta:
        model = Project
        fields = ["author", "name", "key", "type", "starred"]

        labels = {
            "name": _("name"),
            "key": _("key"),
            "type": _("type"),
        }

        widgets = {
            "author": TextInput(),
            "name": TextInput(attrs={"class": "form-control bg-body-tertiary"}),
            "key": TextInput(attrs={"class": "form-control bg-body-tertiary"}),
            "type": Select(attrs={"class": "form-control bg-body-tertiary"}),
            "starred": CheckboxInput(attrs={"name": _("Favorite"), "style": "width:20px; height:20px", "class": "form-check-input"}),
        }


    def clean_name(self):
        cd = self.cleaned_data
        name = cd["name"].capitalize()

        if Project.objects.filter(name=name):
            raise ValidationError(_("That project already exists"))

        return name


    def clean_key(self):
        cd = self.cleaned_data
        key = cd["key"].upper()

        if Project.objects.filter(key=key):
            raise ValidationError(_("Project with that key already exists"))

        return key


class IssueModalForm(ModelForm):


    class Meta:
        model = Issue
        fields = ["project", "type", "priority", "title", "description", "author"]
        labels = {
            "type": _("type"),
            "priority": _("priority"),
            "title": _("title"),
            "description": _("description"),
        }

        widgets = {
            "project": Select(),
            "type": Select(attrs={"class": "form-control bg-body-tertiary"}),
            "priority": Select(attrs={"class": "form-control bg-body-tertiary"}),
            "title": TextInput(attrs={"class": "form-control bg-body-tertiary"}),
            "description": Textarea(attrs={"class": "form-control bg-body-tertiary", "rows": "5"}),
            "author": TextInput(),
        }


    def clean_title(self):
        title = self.cleaned_data["title"].capitalize()

        if Issue.objects.filter(title=title):
            raise ValidationError(_("Issue with that title already exists"))

        return title


class IssueDetailsForm(ModelForm):


    class Meta:
        model = Issue
        fields = ["project", "status", "type", "priority", "title", "description", "author"]

        labels = {
            "status": _("status"),
            "type": _("type"),
            "priority": _("priority"),
            "title": _("title"),
            "description": _("description"),
        }

        widgets = {
            "project": Select(),
            "status": Select(attrs={"class": "form-select bg-body-tertiary"}),
            "type": Select(attrs={"class": "form-select bg-body-tertiary"}),
            "priority": Select(attrs={"class": "form-select bg-body-tertiary"}),
            "title": TextInput(attrs={"class": "form-control bg-body-tertiary"}),
            "description": Textarea(attrs={"class": "form-control bg-body-tertiary", "rows": "7"}),
            "author": TextInput(),
        }


class UserForgotPasswordForm(PasswordResetForm):
    """  Request to reset password  """


    # Change style of field 
    email = forms.CharField(
        label=_("email"),
        min_length=4, 
        max_length=150, 
        widget=EmailInput(
            attrs={
                "class": "form-control", 
                "id": "floatingEmail", 
                "placeholder": _("Email"),
                "autofocus": True}))


class UserSetNewPasswordForm(UserPasswordChangeForm):
    """  Change user password after confirm via link in email  """


    # Change style of fields:
    new_password1 = forms.CharField(
        label=_("New password"),
        min_length=8,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "class": "mb-3 form-control", 
                "autofocus": True
                }))

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        min_length=8,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={"class": "mb-4 form-control"}))
