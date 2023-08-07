import re

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from bugtracker.models import Project, Issue


def remove_html(string):
    """ Clean string from any HTML """
    pattern = re.compile("<.*?>")
    clean = re.sub(pattern, "", string)

    return clean


class ProjectsTestCase(TestCase):


    def setUp(self):
        user = User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")
        Project.objects.create(name="Testing", key="TEST", type="Fullstack software", starred=1, author_id=user.id)


    def test_call_view_anonymous(self):      
        response = self.client.get(reverse("projects"))
        self.assertRedirects(response, "/login/?next=/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")     
        self.client.force_login(user)     

        response = self.client.get(reverse("projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")


    def test_post_success(self):
        user = User.objects.get(username="testing")
        self.client.force_login(user)
        data = {"author": user.id, "name": "Test", "key": "TESTII", "type": "Fullstack software", "starred":1}

        response = self.client.post(reverse("projects"), data=data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(remove_html(str(messages[0])), "Project created!")


    def test_post_fail(self):
        user = User.objects.get(username="testing")
        self.client.force_login(user)
        data = {"author": user.id, "name": "Testing", "key": "TEST", "type": "Fullstack software", "starred":1}

        response = self.client.post(reverse("projects"), data=data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 2)
        self.assertEqual(remove_html(str(messages[0])), "That project already exists")
        self.assertEqual(remove_html(str(messages[1])), "Project with that key already exists")


class BoardsTestCase(TestCase):


    def setUp(self):
        user = User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")
        project = Project.objects.create(name="Testing1", key="TEST1", type="Fullstack software", author_id=user.id)
        Issue.objects.create(
            project_id=project.id,
            title="Issue", 
            description="Big Socks Just Big Socks", 
            type="Feature",
            priority="Medium", 
            status="To do", 
            author_id=user.id)


    def test_call_view_anonymous(self):      
        project = str(Project.objects.get(key="TEST1").id)
        response = self.client.get(reverse("boards", args=[project]))

        self.assertRedirects(response, f"/login/?next=/boards/{project}/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")
        project = str(Project.objects.get(key="TEST1").id)     
        self.client.force_login(user)

        response = self.client.get(reverse("boards", args=[project]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "boards.html")


    def test_post_success(self):
        user = User.objects.get(username="testing")
        project = Project.objects.get(key="TEST1")
        self.client.force_login(user)
        data = {
            "project": project.id,
            "key": 1,
            "title": "Title issue", 
            "description": "Testing test", 
            "type": "Feature",
            "priority": "Medium", 
            "status": "To do", 
            "author": user.id
        }

        response = self.client.post(reverse("boards", args=[project.id]), data=data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(remove_html(str(messages[0])), "Issue created!")


    def test_post_fail(self):
        user = User.objects.get(username="testing")
        project = str(Project.objects.get(key="TEST1").id) 
        self.client.force_login(user)
        data = {
            "project": project,
            "title": "Issue", 
            "description": "Testing test", 
            "type": "Feature",
            "priority": "Medium", 
            "status": "To do", 
            "author": user.id
        }

        response = self.client.post(reverse("boards", args=[project]), data=data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Issue with that title already exists")


class IssueDetailsTestCase(TestCase):


    def setUp(self):
        user = User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")
        project = Project.objects.create(name="Testing", key="TEST", type="Fullstack software", author_id=user.id)
        Issue.objects.create(
            project_id=project.id,
            title="Issue", 
            description="Big Socks Just Big Socks", 
            type="Feature",
            priority="Medium", 
            status="To do", 
            author_id=user.id)


    def test_call_view_anonymous(self):      
        project = str(Project.objects.get(key="TEST").id)
        issue = str(Issue.objects.get(title="Issue").id)

        response = self.client.get(reverse("issue-details", args=[project, issue]))

        self.assertRedirects(response, f"/login/?next=/boards/{project}/{issue}/issue-details/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")
        project = str(Project.objects.get(key="TEST").id)
        issue = str(Issue.objects.get(title="Issue").id)     
        self.client.force_login(user)

        response = self.client.get(reverse("issue-details", args=[project, issue]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "issue-details.html")


    def test_post_success(self):
        user = User.objects.get(username="testing")
        project = Project.objects.get(key="TEST")
        issue = Issue.objects.get(title="Issue")  
        self.client.force_login(user)
        data = {
            "project": project.id,
            "title": "Title issue",  
            "type": "Feature",
            "priority": "Medium", 
            "status": "To do", 
            "author": user.id
        }

        response = self.client.post(reverse("issue-details", args=[project.id, issue.id]), data=data)

        self.assertEqual(response.status_code, 200)


# TODO 1:
    def test_post_fail(self): pass


class ProjectSettingsTestCase(TestCase):


    def setUp(self):
        user = User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")
        Project.objects.create(name="Testing", key="TEST", type="Fullstack software", author_id=user.id)


    def test_call_view_anonymous(self):      
        project = str(Project.objects.get(key="TEST").id)
        response = self.client.get(reverse("project-settings", args=[project]))

        self.assertRedirects(response, f"/login/?next=/boards/{project}/project-settings/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")
        project = str(Project.objects.get(key="TEST").id)     
        self.client.force_login(user)

        response = self.client.get(reverse("project-settings", args=[project]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "project-settings.html")


    def test_post_success(self):
        user = User.objects.get(username="testing")
        project = Project.objects.get(key="TEST")
        self.client.force_login(user)
        data = {
            "name": "Test",
            "key": "TESTI" 
        }

        response = self.client.post(reverse("project-settings", args=[project.id]), data=data)

        self.assertEqual(response.status_code, 200)


# TODO 2: 
    def test_post_fail(self): pass


class AccountsTestCase(TestCase):


    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_call_view_anonymous(self):      
        user = User.objects.get(username="testing")
        response = self.client.get(reverse("accounts", args=[user.id]))

        self.assertRedirects(response, f"/login/?next=/accounts/{user.id}/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")
        self.client.force_login(user)

        response = self.client.get(reverse("accounts", args=[user.id]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts.html")


    def test_post_success(self):
        user = User.objects.get(username="testing")
        self.client.force_login(user)
        data = {
            "first_name": "Test",
            "last_name": "Test", 
            "username": "testi", 
            "email": "test@gmail.com"
        }

        response = self.client.post(reverse("accounts", args=[user.id]), data=data)

        self.assertEqual(response.status_code, 302)


# TODO 3:
    def test_post_fail(self): pass


class SearchTestCase(TestCase):


    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_call_view_anonymous(self):      
        response = self.client.get(reverse("search"))
        self.assertRedirects(response, f"/login/?next=/search/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")
        self.client.force_login(user)

        response = self.client.get(reverse("search"))

        self.assertTrue(response.status_code, 200)


class SearchResultsTestCase(TestCase):


    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_call_view_anonymous(self):   
        q = "bug"   
        response = self.client.get(reverse("search-results", args=[q]))

        self.assertRedirects(response, f"/login/?next=/search-results/{q}/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")
        q = "bug"
        self.client.force_login(user)

        response = self.client.get(reverse("search-results", args=[q]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "search-results.html")


class LoginTestCase(TestCase):


    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")

    def test_call_view(self):
        response = self.client.get(reverse("login"))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")


    def test_post_success(self):
        data = {
            "username": "testing",
            "password": "Password123#"
        }

        self.client.login(username=data["username"], password=data["password"])
        response = self.client.post(reverse("login"), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")


    def test_post_fail(self):
        data = {
            "username": "wrong",
            "password": "Password123#"
        }

        self.client.login(username=data["username"], password=data["password"])
        response = self.client.post(reverse("login"), data=data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Invalid username and/or password")


class RegisterTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_call_view(self):
        response = self.client.get(reverse("register"))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")


    def test_post_success(self):
        data = {
            "first_name": "First", 
            "last_name": "Last", 
            "username": "username", 
            "email": "email@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"
        }

        response = self.client.post(reverse("register"), data=data, follow=True)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(remove_html(str(messages[0])), "Almost done! Check your email to confirm it and complete the registration!")
        self.assertTemplateUsed(response, "login.html")


    def test_post_fail(self):
        data = {
            "first_name": "First", 
            "last_name": "Last", 
            "username": "testing", 
            "email": "testemail@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"
        }

        response = self.client.post(reverse("register"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertIn(b"That username already exists", response.content)
        self.assertIn(b"That email already exists", response.content)


class RegisterConfirmTestCase(TestCase):


    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_call_view(self):
        user = User.objects.get(username="testing")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.get(reverse("register_confirm", args=[uid, token]))

        self.assertTrue(response.status_code, 200)


class LogoutTestCase(TestCase):


    def setUp(self):
       User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_call_view(self):
        user = User.objects.get(username="testing")
        self.client.force_login(user)

        response = self.client.get(reverse("logout"))

        self.assertTrue(response.status_code, 301)


class PasswordResetTestCase(TestCase):


    def test_call_view(self):
        response = self.client.get(reverse("password-reset"))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "password-reset.html")


    def test_post(self):
        data = {
            "email": "testemail@gmail.com" 
        }

        response = self.client.post(reverse("password-reset"), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("password-reset-done"))
        self.assertTemplateUsed(response, "password-reset-done.html")


class PasswordResetDoneTestCase(TestCase):


    def test_call_view(self):
        response = self.client.get(reverse("password-reset-done"))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "password-reset-done.html")


class PasswordResetConfirmTestCase(TestCase):


    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_call_view(self):
        user = User.objects.get(username="testing")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.get(reverse("password_reset_confirm", args=[uid, token]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "password-reset-confirm.html")


    def test_post_success(self):
        user = User.objects.get(username="testing")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        data = {
            "new_password1": "Password123#",
            "new_password2": "Password123#"
        }

        response = self.client.post(reverse("password_reset_confirm", args=[uid, token]), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login"))
        self.assertTemplateUsed(response, "login.html")


    def test_post_fail(self):
        user = User.objects.get(username="testing")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        data = {
            "new_password1": "testing1",
            "new_password2": "Password123#"
        }

        response = self.client.post(reverse("password_reset_confirm", args=[uid, token]), data=data, follow=True)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "password-reset-confirm.html")
        self.assertEqual(len(messages), 2)
        self.assertEqual(remove_html(str(messages[0])), "The password doesn&#x27;t meet the conditions")
        self.assertEqual(remove_html(str(messages[1])), "Passwords don&#x27;t match")


class DeleteProjectTestCase(TestCase):


    def setUp(self):
        user = User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")
        Project.objects.create(name="Testing1", key="TEST1", type="Fullstack software", author_id=user.id)


    def test_call_view_anonymous(self):   
        project = str(Project.objects.get(key="TEST1").id)  
        response = self.client.get(reverse("delete-project", args=[project]))

        self.assertRedirects(response, f"/login/?next=/delete-project/{project}/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")
        project = str(Project.objects.get(key="TEST1").id) 
        self.client.force_login(user)

        response = self.client.get(reverse("delete-project", args=[project]))
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(response.status_code, 301)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Project deleted!")


class DeleteIssueTestCase(TestCase):


    def setUp(self):
        user = User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")
        project = Project.objects.create(name="Testing1", key="TEST1", type="Fullstack software", author_id=user.id)
        Issue.objects.create(
            project_id=project.id,
            title="Issue", 
            description="Big Socks Just Big Socks", 
            type="Feature",
            priority="Medium", 
            status="To do", 
            author_id=user.id)


    def test_call_view_anonymous(self):   
        project = str(Project.objects.get(key="TEST1").id)  
        issue = str(Issue.objects.get(title="Issue").id)

        response = self.client.get(reverse("delete-issue", args=[project, issue]))

        self.assertRedirects(response, f"/login/?next=/delete-issue/{project}/{issue}/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")
        project = str(Project.objects.get(key="TEST1").id) 
        issue = str(Issue.objects.get(title="Issue").id)
        self.client.force_login(user)

        response = self.client.get(reverse("delete-issue", args=[project, issue]))
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(response.status_code, 301)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Issue deleted!")


class DeleteAccountTestCase(TestCase):


    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_call_view_anonymous(self):   
        user = User.objects.get(username="testing")
        response = self.client.get(reverse("delete-account", args=[user.id]))

        self.assertRedirects(response, f"/login/?next=/delete-account/{user.id}/")


    def test_call_view_logged_in(self):
        user = User.objects.get(username="testing")
        self.client.force_login(user)

        response = self.client.get(reverse("delete-account", args=[user.id]))
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(response.status_code, 301)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Account deleted!")
