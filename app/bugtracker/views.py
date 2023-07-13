from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import Project, Project_type, Issue_priority, Issue_type, Issue
from .forms import UserForm, ProjectDetailsForm, RegisterForm, LoginForm, ProjectModalForm, IssueModalForm


projects_list = Project.objects.order_by("-starred")
project_types_list = Project_type.objects.all()

issue_types_list = Issue_type.objects.all()
issue_priority_list = Issue_priority.objects.all()

user = User.objects.get(id=1)


@login_required(login_url="/login/")
def projects(request):
    context = {
        'projects_list': projects_list,
        'project_types_list': project_types_list,
        'user_id': user.id,
        'issue_types_list': issue_types_list,
        'issue_priority_list': issue_priority_list,
    }

    if request.method == 'POST':
        project_modal_form = ProjectModalForm(request.POST or None)
        issue_modal_form = IssueModalForm(request.POST or None)


        if project_modal_form.is_valid():
            project_modal_form.save()
            context['projects_list'] = Project.objects.order_by("-starred")

        if issue_modal_form.is_valid():
            cd = issue_modal_form.cleaned_data

            Issue.objects.create(
                project=cd["project"],
                title=cd["title"],
                description=cd["description"],
                type=cd["type"],
                priority=cd["priority"],
                status="To do",
                author_id=user.id,
                duedate=cd["duedate"]
            )
        
        context['project_modal_form'] = project_modal_form
        context['issue_modal_form'] = issue_modal_form

    else:
        project_modal_form = ProjectModalForm()
        issue_modal_form = IssueModalForm()

        context['project_modal_form'] = project_modal_form
        context['issue_modal_form'] = issue_modal_form

    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def boards(request, project_id):  

    project = Project.objects.get(id=project_id)
    all_issues = Issue.objects.order_by('status')
    user = User.objects.get(id=1)

    todo_issues = 0
    in_progress_issues = 0
    done_issues  = 0
    issue_list = []

    for issue in all_issues:
        if issue.project_id == project.id:
            if issue.status == "To do":
                todo_issues += 1
            elif issue.status == "In progress":
                in_progress_issues += 1
            else:
                done_issues += 1           
            issue_list.append(issue)

    context = {
        'project': project,
        'user_id': user.id,
        'project_id': project.id,
        'projects_list': projects_list,
        'issues_list': issue_list,
        'issue_types_list': issue_types_list,
        'issue_priority_list': issue_priority_list,
        'todo_issues': todo_issues,
        'in_progress_issues': in_progress_issues,
        'done_issues': done_issues,
    }

    return render(request, "boards.html", context)


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
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


def logout_view(request):
    logout(request)
    return redirect("login")


def password_reset(request):
    return render(request, "password-reset.html")
 