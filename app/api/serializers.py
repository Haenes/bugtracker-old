from rest_framework import serializers

from .models import Project, Issue


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ["id", "url", "author", "name", "description",
                  "key", "type", "starred", "created"
                  ]
        read_only_fields = ("created",)


class IssueSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = ["id", "url", "project", "author", "title", "description",
                  "key", "type", "priority", "status", "created", "updated"
                  ]
        read_only_fields = ("created",)
