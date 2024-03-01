from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Make email field in User modal unique (for UserForm)
User._meta.get_field("email")._unique = True


class Project(models.Model):

    PROJECT_TYPE = [
        ("Fullstack", "Fullstack"),
        ("Front-end", "Front-end"),
        ("Back-end", "Back-end"),
    ]

    name = models.CharField(
        max_length=255, unique=True,
        validators=[MinLengthValidator(
            3, _("Name field must contain at least 3 letters")
            )]
        )
    description = models.CharField(max_length=255, default="")
    key = models.CharField(
        max_length=10, unique=True,
        validators=[MinLengthValidator(
            3, _("Key field must contain at least 3 letters")
            )]
        )
    type = models.CharField(max_length=18, choices=PROJECT_TYPE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    starred = models.BooleanField(
        verbose_name="favorite project",
        default=False
        )
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-starred", "created"]
        indexes = [models.Index(fields=["author"], name="author_idx")]


class Issue(models.Model):

    ISSUE_TYPE = [
        ("Bug", _("Bug")),
        ("Feature", _("Feature")),
    ]

    ISSUE_PRIORITY = [
        ("Lowest", _("Lowest")),
        ("Low", _("Low")),
        ("Medium", _("Medium")),
        ("High", _("High")),
        ("Highest", _("Highest")),
    ]

    ISSUE_STATUS = [
        ("To do", _("To do")),
        ("In progress", _("In progress")),
        ("Done", _("Done")),
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

    class Meta:
        indexes = [models.Index(fields=["project"], name="project_idx")]
