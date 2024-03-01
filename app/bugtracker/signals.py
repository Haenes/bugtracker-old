from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Project, Issue


# Signals for cache invalidation


@receiver(post_delete, sender=Project, dispatch_uid="project_deleted")
def object_project_delete_handler(sender, instance, **kwargs):
    template_en, template_ru = [
        make_template_fragment_key(
            fragment_name="projects",
            vary_on=[f"{instance.author_id}{lang[0]}"]
            ) for lang in settings.LANGUAGES
        ]
    cache.delete_many(
        keys=[
            f"projects_list_{instance.author_id}",
            f"project_query_{instance.author_id}",
            template_en,
            template_ru
            ]
        )


@receiver(post_save, sender=Project, dispatch_uid="project_updated")
def object_project_save_handler(sender, instance, **kwargs):
    template_en, template_ru = [
        make_template_fragment_key(
            fragment_name="projects",
            vary_on=[f"{instance.author_id}{lang[0]}"]
            ) for lang in settings.LANGUAGES
        ]
    cache.delete_many(
        keys=[
            f"projects_list_{instance.author_id}",
            f"project_query_{instance.author_id}",
            template_en,
            template_ru
            ]
        )


@receiver(post_delete, sender=Issue, dispatch_uid="issue_deleted")
def object_issue_delete_handler(sender, instance, **kwargs):
    template_en, template_ru = [
        make_template_fragment_key(
            fragment_name="boards",
            vary_on=[f"{instance.project_id}{lang[0]}"]
            ) for lang in settings.LANGUAGES
        ]
    cache.delete_many(
        keys=[
            f"all_issues_{instance.project_id}",
            f"issue_query_{instance.author_id}",
            template_en,
            template_ru
            ]
        )


@receiver(post_save, sender=Issue, dispatch_uid="issue_updated")
def object_issue_save_handler(sender, instance, **kwargs):
    template_en, template_ru = [
        make_template_fragment_key(
            fragment_name="boards",
            vary_on=[f"{instance.project_id}{lang[0]}"]
            ) for lang in settings.LANGUAGES
        ]
    cache.delete_many(
        keys=[
            f"all_issues_{instance.project_id}",
            f"issue_query_{instance.author_id}",
            template_en,
            template_ru
            ]
        )
