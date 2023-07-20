from django.urls import path

from . import views


urlpatterns = [
    path("", views.projects, name="projects"),
    path("boards/<int:project_id>/", views.boards, name="boards"),
    path("boards/<int:project_id>/project-settings/", views.project_settings, name="project-settings"),
    path("boards/<int:project_id>/<int:issue_id>/issue-details/", views.issue_details, name="issue-details"),
    path("accounts/<int:user_id>/", views.accounts, name="accounts"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("password-reset/", views.password_reset, name="password-reset"),
    path("password-reset-done/", views.password_reset_done, name="password-reset-done"),
    path("password-reset-confirm/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("delete-project/<int:id>/", views.delete_project, name="delete-project"),
    path("delete-issue/<int:project_id>/<int:issue_id>/", views.delete_issue, name="delete-issue"),
    path("delete-account/<int:user_id>/", views.delete_account, name="delete-account"),
]