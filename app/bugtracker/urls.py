from django.urls import path

from . import views

urlpatterns = [
    path("", views.projects, name="projects"),
    path("boards/<int:project_id>/", views.boards, name="boards"),
    path("boards/<int:project_id>/project-settings/", views.project_settings, name="project-settings"),
    path("accounts/<int:user_id>/", views.accounts, name="accounts"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("password-reset/", views.password_reset, name="password-reset"),
]
