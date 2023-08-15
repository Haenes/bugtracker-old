from rest_framework import serializers

from .models import Project, Issue


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("created", )


class IssueSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = "__all__"
