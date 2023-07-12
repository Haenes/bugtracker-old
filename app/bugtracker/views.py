from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .models import Project, Project_type, Issue_priority, Issue_type, Issue
from .forms import UserForm, ProjectDetailsForm, RegisterForm, LoginForm


projects_list = Project.objects.order_by("-starred")
project_types_list = Project_type.objects.all()

issue_types_list = Issue_type.objects.all()
issue_priority_list = Issue_priority.objects.all()

user = User.objects.get(id=1)


def projects(request):
    context = {
        'projects_list': projects_list,
        'project_types_list': project_types_list,
        'user_id': user.id,
        'issue_types_list': issue_types_list,
        'issue_priority_list': issue_priority_list,
    }

    return render(request, "projects.html", context)


def boards(request, project_id):  
    all_issues = Issue.objects.order_by('status_id')

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

    context = {
        'project': project,
        'project_id': project.id,
        'user_id': user.id,
        'projects_list': projects_list,
        'issue_types_list': issue_types_list,
        'issue_priority_list': issue_priority_list,
    }

    if request.method == 'POST':
        project_form = ProjectDetailsForm(request.POST or None, instance=project)

        if project_form.is_valid():
            project_form.save()
        
        context['project_form'] = project_form


        
    else:
        project_form = ProjectDetailsForm(
            initial = {
                "name": project.name, 
                "key": project.key
            }
        )

        context['project_form'] = project_form

    return render(request, "project-settings.html", context)


def accounts(request, user_id):
    user = User.objects.get(id=user_id)
    project = Project.objects.get(name='BugTracker')

    context = {
        'user': user,
        'user_id': user.id,
        'project':project,
        'projects_list': projects_list,
        'issue_types_list': issue_types_list,
        'issue_priority_list': issue_priority_list,
    }
  
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, instance=user)

        if user_form.is_valid():
            user_form.save()

        context['user_form'] = user_form

    else:
        user_form = UserForm(
            initial = {
                "username": user.username, 
                "first_name": user.first_name, 
                "last_name": user.last_name, 
                "email": user.email,
            }
        )

        context['user_form'] = user_form

    return render(request, "accounts.html", context)


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():         
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                return redirect("projects")
            
        messages.error(request, f"Invalid username and/or password")
           
    else: 
        if request.user.is_authenticated:
            return redirect("projects")
        
        login_form = LoginForm()

    return render(request, "login.html", {"login_form": login_form})


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return redirect("login")

    else:
        register_form = RegisterForm()

    return render(request, "register.html", {"register_form": register_form})


def password_reset(request):
    return render(request, "password-reset.html")
 