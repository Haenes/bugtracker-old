import os
import json
from dotenv import load_dotenv

load_dotenv()


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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
    UserForm
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

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = json.load(request)

        icon_id = data["icon_id"].removeprefix("star")
        icon_color = data["icon_color"]

        project = Project.objects.get(id=icon_id)

        if icon_color == "grey":
            project.starred = 0
            project.save()
        else:
            project.starred = 1
            project.save()

    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def boards(request, project_id):  

    project = Project.objects.get(id=project_id)
    all_issues = Issue.objects.order_by('status')
    user = request.user


    issue_list = []

    for issue in all_issues:
        if issue.project_id == project.id:         
            issue_list.append(issue)

    context = {
        'project': project,
        'user_id': user.id,
        'project_id': project.id,        
        'issues_list': issue_list
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

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = json.load(request)
        target = data["target"] 
    
        issue_id = data["data"].removeprefix("card")      
        issue = Issue.objects.get(id=issue_id)

        if issue.status != target:
            issue.status = target
            issue.save()

            return JsonResponse({
                "id": issue.id,
                "source": issue.status,
            })
           
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
                "key": project.key,
                "starred": project.starred
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

        if "user_details" in request.POST:
            user_form = UserForm(request.POST or None, instance=user)

            if user_form.is_valid():
                user_form.save()

            context['user_form'] = user_form

        elif "change_password" in request.POST:
            password_change_form = UserPasswordChangeForm(request.user, request.POST or None)

            if password_change_form.is_valid():
                user = password_change_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                    
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


@login_required(login_url="/login/")
def search(request):

    if 'q' in request.GET and request.GET['q']:
        q = request.GET.get("q")
        q = q.strip()
    
        if len(q) == 0:
            messages.error(request,"Please, give a data for search")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        elif " " in q:
            messages.error(request,"Please give just one word to search")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        return redirect("search-results", q)
    
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="/login/")
def search_results(request, q):

    query = q 
    user = request.user

    if query is not None:
        lookups_projects = Q(name__icontains=query) | Q(key__icontains=query) | Q(id__icontains=query)
        lookups_issues = Q(title__icontains=query) | Q(type__icontains=query) | Q(status__icontains=query) | Q(priority__icontains=query) | Q(id__icontains=query)

        results_projects = Project.objects.filter(lookups_projects).distinct()
        results_issues = Issue.objects.filter(lookups_issues).distinct()

        context = {'query':query, 'results_projects':results_projects, 'results_issues': results_issues, 'user_id': user.id}

    return render(request, "search-results.html", context)


def login_view(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():         
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            
            if user:
                # Set the session expiration time.
                # If the user hasn't checked the "Remember me" checkbox - the session will last 30 min.
                # Otherwise - 1 month.  

                if not request.POST.get('remember', None):
                    request.session.set_expiry(60 * 30)
                else:
                    request.session.set_expiry(60 * 60 * 24 * 30)

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
            user = register_form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email' 
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            message = render_to_string('register-activate.html', { 
                'user': user, 
                'domain': current_site.domain, 
                'uid':uid, 
                'token':token
            }) 
            to_email = register_form.cleaned_data.get('email') 
            email = EmailMessage(mail_subject, message, to=[to_email]) 
            email.send() 
            messages.success(request, "Almost done! Check your email to confirm it and complete the registration!")

            return redirect("login")

    else:
        register_form = RegisterForm()


    return render(request, "register.html", {"register_form": register_form})

def register_confirm(request, uidb64, token):
    try: 
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None 

    if user is not None and default_token_generator.check_token(user, token): 
        user.is_active = True 
        user.save() 
        messages.success(request, "Email is confirmed, you can log in now!")
        return redirect('login') 
    else: 
        messages.error(request, "Email confirmation is failed!")
        return redirect('login') 


def logout_view(request):
    logout(request)  
    return redirect("login")


def password_reset(request):

    if request.method == 'POST':
        reset_password_form = UserForgotPasswordForm(request.POST)

        if reset_password_form.is_valid():
            reset_password_form.save(from_email=os.environ.get("EMAIL_HOST_USER") ,request=request)

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
        for field in set_password_form.errors:
                if set_password_form.errors[field]:
                    messages.error(request, set_password_form.errors[field])

    else:
        set_password_form = UserSetNewPasswordForm(user=user)

    return render(request, "password-reset-confirm.html", {"set_password_form": set_password_form})


@login_required(login_url="/login/")
def delete_project(request, id):

    project = Project.objects.get(id=id)
    project.delete()

    messages.success(request, "Project deleted!")
    
    return redirect("projects")


@login_required(login_url="/login/")
def delete_issue(request, project_id, issue_id):

    issue = Issue.objects.get(id=issue_id)
    issue.delete() 

    messages.success(request, "Issue deleted!")

    return redirect('boards', project_id)


@login_required(login_url="/login/")
def delete_account(request, user_id):

    user = User.objects.get(id=user_id)
    user.delete()

    messages.success(request, "Account deleted!")

    return redirect('login')
