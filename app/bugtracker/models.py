from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone


# Make email field in User modal unique (for UserForm)
User._meta.get_field("email")._unique = True


class Project(models.Model):


    PROJECT_TYPE = [
        ("Fullstack software", "Fullstack software"),
        ("Front-end software", "Front-end software"),
        ("Back-end software", "Back-end software"),
    ]

    name = models.CharField(max_length=255, unique=True, validators=[MinLengthValidator(3, "Name field must contain at least 3 letters")])
    description = models.CharField(max_length=255, default="")
    key = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(3, "Key field must contain at least 3 letters")])
    type = models.CharField(max_length=18, choices=PROJECT_TYPE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    starred = models.BooleanField(verbose_name="favorite project", default=False)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-starred", "created"]


class Issue(models.Model):


    ISSUE_TYPE = [
        ("Bug", "Bug"),
        ("Feature", "Feature"),
    ]

    ISSUE_PRIORITY = [
        ("Lowest", "Lowest"),
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Highest", "Highest"),
    ]

    ISSUE_STATUS = [
        ("To do", "To do"),
        ("In progress", "In progress"),
        ("Done", "Done"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    key = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    type = models.CharField(max_length=8, choices=ISSUE_TYPE)
    priority = models.CharField(max_length=8, choices=ISSUE_PRIORITY)
    status = models.CharField(max_length=11, choices=ISSUE_STATUS)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
