from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Project, Project_type, Issue_priority, Issue_status, Issue_type, Issue
from .forms import UserForm, ProjectDetailsForm


projects_list = Project.objects.order_by("-starred")
project_types_list = Project_type.objects.all()

issue_types_list = Issue_type.objects.all()
issue_priority_list = Issue_priority.objects.all()

user = User.objects.get(id=1)


def projects(request):
    context = {'projects_list': projects_list,
               'project_types_list': project_types_list,
               'user_id': user.id,
               'issue_types_list': issue_types_list,
               'issue_priority_list': issue_priority_list,
               }

    return render(request, "projects.html", context)


def boards(request, project_id):  
    all_issues = Issue.objects.order_by('status_id')
    # issues_num = 0
    # issue_list = []

    # for issue in all_issues:
    #     if issue.project_id == project_id:
    #         issues_num += 1
    #         issue_list.append(issue)

    todo_issues = 0
    in_progress_issues = 0
    done_issues  = 0
    issue_list = []

    for issue in all_issues:
        if issue.project_id == project_id:
            if issue.status_id == 1:
                todo_issues += 1
            elif issue.status_id == 2:
                in_progress_issues += 1
            else:
                done_issues += 1           
            issue_list.append(issue)
    

    project = Project.objects.get(id=project_id)
    project_id = project.id
    user = User.objects.get(id=1)
    # issue_list = Issue.objects.all() 
    # issues = Issues.objects.get(project_id=project_id)
    # context = {
    #     'project': project,
    #     'user_id': user.id,
    #     'project_id': project_id,
    #     'projects_list': projects_list,
    #     'issues_list': issue_list,
    #     'issue_types_list': issue_types_list,
    #     'issue_priority_list': issue_priority_list,
    #     'issues_num': issues_num,
    # }

    context = {
        'project': project,
        'user_id': user.id,
        'project_id': project_id,
        'projects_list': projects_list,
        'issues_list': issue_list,
        'issue_types_list': issue_types_list,
        'issue_priority_list': issue_priority_list,
        'todo_issues': todo_issues,
        'in_progress_issues': in_progress_issues,
        'done_issues': done_issues,
    }

    return render(request, "boards.html", context)


def project_settings(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        project_form = ProjectDetailsForm(request.POST or None, instance=project)

        if project_form.is_valid():
            project_form.save()

        context = {
            'project': project,
            'project_id': project.id,
            'user_id': user.id,
            'projects_list': projects_list,
            'issue_types_list': issue_types_list,
            'issue_priority_list': issue_priority_list,
            'project_form': project_form,
        }
        
    else:
        project_form = ProjectDetailsForm(
            initial = {
                "name": project.name, 
                "key": project.key
            }
        )

        context = {
            'project': project,
            'project_id': project.id,
            'user_id': user.id,
            'projects_list': projects_list,
            'issue_types_list': issue_types_list,
            'issue_priority_list': issue_priority_list,
            'project_form': project_form,
        }

    return render(request, "project-settings.html", context)


def accounts(request, user_id):
    user = User.objects.get(id=user_id)
    project = Project.objects.get(name='BugTracker')
  
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, instance=user)

        if user_form.is_valid():
            user_form.save()

        context = {
            'user': user,
            'user_id': user.id,
            'project':project,
            'projects_list': projects_list,
            'issue_types_list': issue_types_list,
            'issue_priority_list': issue_priority_list,
            'user_form': user_form,
        }

    else:
        user_form = UserForm(
            initial = {
                "username": user.username, 
                "first_name": user.first_name, 
                "last_name": user.last_name, 
                "email": user.email
            }
        )

        context = {
            'user': user,
            'user_id': user.id,
            'project':project,
            'projects_list': projects_list,
            'issue_types_list': issue_types_list,
            'issue_priority_list': issue_priority_list,
            'user_form': user_form,
        }

    return render(request, "accounts.html", context)


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def password_reset(request):
    return render(request, "password-reset.html")
