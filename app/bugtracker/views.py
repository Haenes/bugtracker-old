from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.http import urlsafe_base64_decode

from .models import Issue, Project
from .forms import ( 
    IssueDetailsForm,
    IssueModalForm,
    LoginForm,
    ProjectDetailsForm, 
    ProjectModalForm, 
    RegisterForm, 
    UserPasswordChangeForm,
    UserForgotPasswordForm,
    UserSetNewPasswordForm,
    UserForm,
    )


@login_required(login_url="/login/")
def projects(request):

    user = request.user
    projects_list = Project.objects.filter(author_id=user.id)

    paginator = Paginator(projects_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'projects_list': projects_list,
        'user_id': user.id,
        'page_obj': page_obj,
    }
    
    if request.method == 'POST':
        project_modal_form = ProjectModalForm(request.POST or None)

        if project_modal_form.is_valid():
            cd = project_modal_form.cleaned_data
            
            Project.objects.create(
                author_id=user.id,
                name=cd["name"].capitalize(),
                key=cd["key"].upper(),
                type=cd["type"],
                starred=cd["starred"]
            )          
            messages.success(request, "Project created!")
        
        context['project_modal_form'] = project_modal_form

        for field in project_modal_form.errors:
            if project_modal_form.errors[field]:
                messages.error(request, project_modal_form.errors[field])

    else:
        project_modal_form = ProjectModalForm(initial={"author": user.id})
        context['project_modal_form'] = project_modal_form

    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def boards(request, project_id):  

    project = Project.objects.get(id=project_id)
    all_issues = Issue.objects.order_by('status')
    user = request.user

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
        'issues_list': issue_list,
        'todo_issues': todo_issues,
        'in_progress_issues': in_progress_issues,
        'done_issues': done_issues,
    }

    if request.method == 'POST':
        issue_modal_form = IssueModalForm(request.POST or None)

        if issue_modal_form.is_valid():
            cd = issue_modal_form.cleaned_data

            Issue.objects.create(
                project=cd["project"],
                title=cd["title"].capitalize(),
                description=cd["description"],
                type=cd["type"],
                priority=cd["priority"],
                status="To do",
                author_id=user.id,
                duedate=cd["duedate"]
            )          
            messages.success(request, "Issue created!")
            return redirect('boards', project.id)
        
        context['issue_modal_form'] = issue_modal_form

        for field in issue_modal_form.errors:
            if issue_modal_form.errors[field]:
                messages.error(request, issue_modal_form.errors[field])

    else:
        issue_modal_form = IssueModalForm(initial={"project":project.id, "author": user.id})   
        context['issue_modal_form'] = issue_modal_form

    return render(request, "boards.html", context)


@login_required(login_url="/login/")
def issue_details(request, project_id, issue_id):

    user = request.user
    project = Project.objects.get(id=project_id)
    issue = Issue.objects.get(id=issue_id)

    context = {
        'user_id': user.id,
        'project': project,
        'issue': issue,
    }

    if request.method == 'POST':
        issue_details_form = IssueDetailsForm(request.POST or None, instance=issue)

        if issue_details_form.is_valid():
            issue_details_form.save()

        context['issue_details_form'] = issue_details_form

    else:
        issue_details_form = IssueDetailsForm(
            initial = {
                "project": project.id,
                "status": issue.status,
                "type": issue.type,
                "priority": issue.priority,
                "title": issue.title,
                "description": issue.description,
                "duedate": issue.duedate,
                "author": issue.author,
            }
        )
        context['issue_details_form'] = issue_details_form

    return render(request, "issue-details.html", context)


@login_required(login_url="/login/")
def project_settings(request, project_id):

    user = request.user
    project = Project.objects.get(id=project_id)

    context = {
        'project': project,
        'project_id': project.id,
        'user_id': user.id,
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

    context = {
        'user': user,
        'user_id': user.id,
    }
  
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, instance=user)
        password_change_form = UserPasswordChangeForm(request.user, request.POST or None)

        if user_form.is_valid():
            user_form.save()

        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect("accounts", user.id)
          
        context['user_form'] = user_form
        context['password_change_form'] = password_change_form

        for field in password_change_form.errors:
            if password_change_form.errors[field]:
                messages.error(request, password_change_form.errors[field])

        return redirect("accounts", user.id)
    
    else:
        user_form = UserForm(
            initial = {
                "first_name": user.first_name, 
                "last_name": user.last_name, 
                "username": user.username,
                "email": user.email,
            }
        )
        password_change_form = UserPasswordChangeForm(request.user)
                
        context['user_form'] = user_form
        context['password_change_form'] = password_change_form

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

    if request.method == 'POST':
        reset_password_form = UserForgotPasswordForm(request.POST)

        if reset_password_form.is_valid():
            reset_password_form.save(from_email="***REMOVED***" ,request=request)

            return redirect("password-reset-done")

    else:
        reset_password_form = UserForgotPasswordForm()

    return render(request, "password-reset.html", {"reset_password_form": reset_password_form})


def password_reset_done(request):
    return render(request, "password-reset-done.html")


def password_reset_confirm(request, uidb64, token): 

    uid = urlsafe_base64_decode(uidb64) 
    user = User.objects.get(pk=uid)

    if request.method == 'POST':
        set_password_form = UserSetNewPasswordForm(user, request.POST)

        if set_password_form.is_valid():
            set_password_form.save()
            return redirect("login")

    else:
        set_password_form = UserSetNewPasswordForm(user=user)

    return render(request, "password-reset-confirm.html", {"set_password_form": set_password_form})


def delete_project(request, id):

    project = Project.objects.get(id=id)
    project.delete()

    messages.success(request, "Project deleted!")
    
    return redirect("projects")


def delete_issue(request, project_id, issue_id):

    issue = Issue.objects.get(id=issue_id)
    issue.delete() 

    messages.success(request, "Issue deleted!")

    return redirect('boards', project_id)


def delete_account(request, user_id):

    user = User.objects.get(id=user_id)
    user.delete()

    messages.success(request, "Account deleted!")

    return redirect('login')
