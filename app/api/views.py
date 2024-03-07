from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .serializers import ProjectSerializer, IssueSerializer
from .models import Project, Issue


class ProjectViewSet(viewsets.ModelViewSet):
    """ API endpoint that shows user projects. """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        queryset = cache.get_or_set(
            f"project_query_{user_id}",
            Project.objects.filter(author_id=user_id)
            .order_by('-starred', '-created'))

        return queryset


class IssueViewSet(viewsets.ModelViewSet):
    """ API endpoint that shows user created issues. """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth.key).user_id
        queryset = cache.get_or_set(
            f"issue_query_{user_id}",
            Issue.objects.filter(author_id=user_id).order_by('project'))

        return queryset
