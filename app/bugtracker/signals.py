from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Project, Issue


# Signals for cache invalidation


@receiver(post_delete, sender=Project, dispatch_uid="project_deleted")
def object_project_delete_handler(sender, instance, **kwargs):
    cache.delete(f"projects_list_{instance.author_id}")
    cache.delete(f"project_query_{instance.author_id}")


@receiver(post_save, sender=Project, dispatch_uid="projects_updated")
def object_project_save_handler(sender, instance, **kwargs):
    cache.delete(f"projects_list_{instance.author_id}")
    cache.delete(f"project_query_{instance.author_id}")


@receiver(post_delete, sender=Issue, dispatch_uid="issue_deleted")
def object_issue_delete_handler(sender, instance, **kwargs):
    cache.delete(f"all_issues_{instance.project.id}")
    cache.delete(f"issue_query_{instance.author_id}")


@receiver(post_save, sender=Issue, dispatch_uid="issues_updated")
def object_issue_save_handler(sender, instance, **kwargs):
    cache.delete(f"all_issues_{instance.project.id}")
    cache.delete(f"issue_query_{instance.author_id}")
