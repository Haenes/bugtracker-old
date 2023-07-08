from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Issue_type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Issue_priority(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Issue_status(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Project_type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, default='')
    key = models.CharField(max_length=10, default=name, unique=True)
    type = models.ForeignKey(Project_type, on_delete=models.PROTECT)
    starred = models.BooleanField(verbose_name="favorite project", default=False)
    created = models.DateTimeField(timezone.now())

    
    def __str__(self):
        return self.name


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    issue_num = models.PositiveIntegerField(unique=True)
    # key_issue = models.ForeignKey(projects, on_delete=models.CASCADE, unique=True,)
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    type = models.ForeignKey(Issue_type, on_delete=models.PROTECT)
    priority = models.ForeignKey(Issue_priority, on_delete=models.PROTECT)
    status = models.ForeignKey(Issue_status, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    duedate = models.DateTimeField()
    closed  = models.DateTimeField(default=None)
    timespent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
