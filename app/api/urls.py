from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'issues', views.IssueViewSet, basename='issue')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token)
]
