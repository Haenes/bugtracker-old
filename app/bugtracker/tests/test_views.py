import re

from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from bugtracker.models import Project, Issue
from bugtracker.views import (
    last_modified_issue_of_project, last_created_project,
    last_update_of_issue
    )


def remove_html(string: str) -> str:
    """ Clean string from any HTML """
    pattern = re.compile("<.*?>")
    clean = re.sub(pattern, "", string)

    return clean


class ETagTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.factory = RequestFactory()

    def test_last_modified_issue_of_project_datetime(self):
        project = Project.objects.create(
            name="Testing", key="TEST", type="Fullstack",
            starred=1, author_id=self.user.id
            )
        Issue.objects.create(
            project_id=project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="To do",
            author_id=self.user.id
            )
        request = self.factory.get(reverse("boards", args=[project.id]))
        request.user = self.user
        r = last_modified_issue_of_project(request, project.id)

        self.assertIsNotNone(r)

    def test_last_modified_issue_of_project_none(self):
        project = Project.objects.create(
            name="Testing", key="TEST", type="Fullstack",
            starred=1, author_id=self.user.id
            )
        request = self.factory.get(reverse("boards", args=[project.id]))
        request.user = self.user
        r = last_modified_issue_of_project(request, project.id)

        self.assertIsNone(r)

    def test_last_created_project_datetime(self):
        Project.objects.create(
            name="Testing", key="TEST", type="Fullstack",
            starred=1, author_id=self.user.id
            )
        request = self.factory.get(reverse("projects"))
        request.user = self.user
        r = last_created_project(request)

        self.assertIsNotNone(r)

    def test_last_created_project_none(self):
        request = self.factory.get(reverse("projects"))
        request.user = self.user
        r = last_created_project(request)

        self.assertIsNone(r)

    def test_last_update_of_issue_datetime(self):
        project = Project.objects.create(
            name="Testing", key="TEST", type="Fullstack",
            starred=1, author_id=self.user.id
            )
        issue = Issue.objects.create(
            project_id=project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="To do",
            author_id=self.user.id
            )
        request = self.factory.get(
            reverse("issue-details", args=[project.id, issue.id])
            )
        request.user = self.user
        r = last_update_of_issue(request, project.id, issue.id)

        self.assertIsNotNone(r)


class ProjectsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.project = Project.objects.create(
            name="Testing", key="TEST", type="Fullstack",
            starred=1, author_id=self.user.id
            )

    def test_call_view_anonymous(self):
        response = self.client.get(reverse("projects"))
        self.assertRedirects(response, "/login/?next=/")

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_post_success(self):
        self.client.force_login(self.user)
        data = {
            "author": self.user.id,
            "name": "Test",
            "key": "TESTII",
            "type": "Fullstack",
            "starred": 1
            }

        response = self.client.post(reverse("projects"), data=data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(remove_html(str(messages[0])), "Project created!")

    def test_post_fail(self):
        self.client.force_login(self.user)
        data = {
            "author": self.user.id,
            "name": "Testing",
            "key": "TEST",
            "type": "Fullstack",
            "starred": 1
            }

        response = self.client.post(reverse("projects"), data=data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 2)
        self.assertEqual(remove_html(str(messages[0])),
                         "That project already exists"
                         )
        self.assertEqual(remove_html(str(messages[1])),
                         "Project with that key already exists"
                         )


class BoardsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.project = Project.objects.create(
            name="Testing1", key="TEST1",
            type="Fullstack", author_id=self.user.id
            )
        self.issue = Issue.objects.create(
            project_id=self.project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="To do",
            author_id=self.user.id
            )

    def test_call_view_anonymous(self):
        response = self.client.get(reverse("boards", args=[self.project.id]))

        self.assertRedirects(
            response,
            f"/login/?next=/boards/{self.project.id}/"
            )

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("boards", args=[self.project.id]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "boards.html")

    def test_post_success(self):
        self.client.force_login(self.user)
        data = {
            "project": self.project.id,
            "key": 1,
            "title": "Title issue",
            "description": "Testing test",
            "type": "Feature",
            "priority": "Medium",
            "status": "To do",
            "author": self.user.id
            }

        response = self.client.post(
            reverse("boards", args=[self.project.id]), data=data
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(remove_html(str(messages[0])), "Issue created!")

    def test_post_fail(self):
        self.client.force_login(self.user)
        data = {
            "project": self.project.id,
            "title": "Issue",
            "description": "Testing test",
            "type": "Feature",
            "priority": "Medium",
            "status": "To do",
            "author": self.user.id
            }

        response = self.client.post(
            reverse("boards", args=[self.project.id]), data=data
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])),
                         "Issue with that title already exists"
                         )


class IssueDetailsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.project = Project.objects.create(
            name="Testing", key="TEST",
            type="Fullstack", author_id=self.user.id
            )

        self.issue1 = Issue.objects.create(
            project_id=self.project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="To do",
            author_id=self.user.id
            )

        self.issue2 = Issue.objects.create(
            project_id=self.project.id,
            title="Issue2",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="To do",
            author_id=self.user.id
            )

    def test_call_view_anonymous(self):
        response = self.client.get(
            reverse("issue-details", args=[self.project.id, self.issue1.id])
            )

        self.assertRedirects(
            response,
            f"/login/?next=/boards/{self.project.id}/{self.issue1.id}"
            "/issue-details/"
            )

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("issue-details", args=[self.project.id, self.issue1.id])
            )

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "issue-details.html")

    def test_post_success(self):
        self.client.force_login(self.user)
        data = {
            "project": self.project.id,
            "title": "Title issue",
            "type": "Feature",
            "priority": "Medium",
            "status": "To do",
            "author": self.user.id
        }

        response = self.client.post(
            reverse("issue-details", args=[self.project.id, self.issue1.id]),
            data=data
            )

        self.assertEqual(response.status_code, 200)

    def test_post_fail(self):
        self.client.force_login(self.user)
        data = {
            "project": self.project.id,
            "title": "Issue2",
            "type": "Feature",
            "priority": "Medium",
            "status": "To do",
            "author": self.user.id
            }

        response = self.client.post(
            reverse("issue-details", args=[self.project.id, self.issue1.id]),
            data=data
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])),
                         "Issue with this Title already exists."
                         )


class ProjectSettingsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.project1 = Project.objects.create(
            name="TestingI", key="TEST",
            type="Fullstack", author_id=self.user.id
            )
        self.project2 = Project.objects.create(
            name="TestingII", key="TESTII",
            type="Fullstack", author_id=self.user.id
            )

    def test_call_view_anonymous(self):
        response = self.client.get(
            reverse("project-settings", args=[self.project1.id])
            )

        self.assertRedirects(
            response,
            f"/login/?next=/boards/{self.project1.id}/project-settings/"
            )

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(
            path=reverse("project-settings", args=[self.project1.id])
            )

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "project-settings.html")

    def test_post_success(self):
        self.client.force_login(self.user)
        data = {"name": "Test", "key": "TESTI"}

        response = self.client.post(
            path=reverse("project-settings", args=[self.project1.id]),
            data=data
            )

        self.assertEqual(response.status_code, 200)

    def test_post_fail(self):
        self.client.force_login(self.user)
        data = {"name": "TestingII", "key": "TESTII"}

        response = self.client.post(
            path=reverse("project-settings", args=[self.project1.id]),
            data=data
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"Project with this Name already exists." in response.content
            )
        self.assertTrue(
            b"Project with this Key already exists." in response.content
            )


class AccountsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.user2 = User.objects.create_user(
            first_name="Test", last_name="Test", username="testingII",
            email="testemail2@gmail.com", password="Password123#"
            )

    def test_call_view_anonymous(self):
        response = self.client.get(reverse("accounts", args=[self.user.id]))
        self.assertRedirects(response,
                             f"/login/?next=/accounts/{self.user.id}/"
                             )

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts", args=[self.user.id]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts.html")

    def test_post_success(self):
        self.client.force_login(self.user)
        data = {
            "user_details": True,
            "first_name": "Test",
            "last_name": "Test",
            "username": "testi",
            "email": "test@gmail.com"
            }

        response = self.client.post(
            path=reverse("accounts", args=[self.user.id]), data=data
            )

        self.assertEqual(response.status_code, 302)

    def test_post_fail(self):
        self.client.force_login(self.user)
        data = {
            "user_details": True,
            "first_name": "Test",
            "last_name": "Test",
            "username": "testingII",
            "email": "testemail2@gmail.com"
            }

        response = self.client.post(
            path=reverse("accounts", args=[self.user.id]), data=data
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 2)
        self.assertEqual(remove_html(str(messages[0])),
                         "A user with that username already exists."
                         )
        self.assertEqual(remove_html(str(messages[1])),
                         "User with this Email address already exists."
                         )


class SearchTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view_anonymous(self):
        response = self.client.get(reverse("search"))
        self.assertRedirects(response, "/login/?next=/search/")

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("search"))

        self.assertTrue(response.status_code, 200)


class SearchResultsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view_anonymous(self):
        q = "bug"
        response = self.client.get(reverse("search-results", args=[q]))

        self.assertRedirects(response, f"/login/?next=/search-results/{q}/")

    def test_call_view_logged_in(self):
        q = "bug"
        self.client.force_login(self.user)

        response = self.client.get(reverse("search-results", args=[q]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "search-results.html")


class LoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view(self):
        response = self.client.get(reverse("login"))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_post_success(self):
        data = {"username": "testing", "password": "Password123#"}

        self.client.login(username=data["username"], password=data["password"])
        response = self.client.post(reverse("login"), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_post_fail(self):
        data = {"username": "wrong", "password": "Password123#"}

        self.client.login(username=data["username"], password=data["password"])
        response = self.client.post(reverse("login"), data=data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])),
                         "Invalid username and/or password"
                         )


class RegisterTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

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

        response = self.client.post(
            path=reverse("register"), data=data, follow=True
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            remove_html(str(messages[0])),
            "Almost done! "
            "Check your email to confirm it and complete the registration!"
            )
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
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.get(
            path=reverse("register_confirm", args=[uid, token])
            )

        self.assertTrue(response.status_code, 200)


class LogoutTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("logout"))

        self.assertTrue(response.status_code, 301)


class PasswordResetTestCase(TestCase):

    def test_call_view(self):
        response = self.client.get(reverse("password-reset"))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "password-reset.html")

    def test_post(self):
        data = {"email": "testemail@gmail.com"}

        response = self.client.post(
            path=reverse("password-reset"), data=data, follow=True
            )

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
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.get(
            path=reverse("password_reset_confirm", args=[uid, token]))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "password-reset-confirm.html")

    def test_post_success(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        data = {
            "new_password1": "Password123#",
            "new_password2": "Password123#"
            }

        response = self.client.post(
            path=reverse("password_reset_confirm", args=[uid, token]),
            data=data, follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login"))
        self.assertTemplateUsed(response, "login.html")

    def test_post_fail(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        data = {"new_password1": "testing1", "new_password2": "Password123#"}

        response = self.client.post(
            path=reverse("password_reset_confirm", args=[uid, token]),
            data=data, follow=True
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "password-reset-confirm.html")
        self.assertEqual(len(messages), 2)
        self.assertEqual(remove_html(str(messages[0])),
                         "The password doesn&#x27;t meet the conditions"
                         )
        self.assertEqual(remove_html(str(messages[1])),
                         "Passwords don&#x27;t match"
                         )


class DeleteProjectTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.project = Project.objects.create(
            name="Testing1", key="TEST1",
            type="Fullstack", author_id=self.user.id
            )

    def test_call_view_anonymous(self):
        response = self.client.get(
            reverse("delete-project", args=[self.project.id])
            )

        self.assertRedirects(
            response,
            f"/login/?next=/delete-project/{self.project.id}/"
            )

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(
            path=reverse("delete-project", args=[self.project.id])
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(response.status_code, 301)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Project deleted!")


class DeleteIssueTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.project = Project.objects.create(
            name="Testing1", key="TEST1",
            type="Fullstack", author_id=self.user.id
            )
        self.issue = Issue.objects.create(
            project_id=self.project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="To do",
            author_id=self.user.id)

    def test_call_view_anonymous(self):
        response = self.client.get(
            path=reverse("delete-issue", args=[self.project.id, self.issue.id])
            )

        self.assertRedirects(
            response,
            f"/login/?next=/delete-issue/{self.project.id}/{self.issue.id}/")

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(
            path=reverse("delete-issue", args=[self.project.id, self.issue.id])
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(response.status_code, 301)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Issue deleted!")


class DeleteAccountTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view_anonymous(self):
        response = self.client.get(
            reverse("delete-account", args=[self.user.id])
            )

        self.assertRedirects(
            response,
            f"/login/?next=/delete-account/{self.user.id}/"
            )

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("delete-account", args=[self.user.id])
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(response.status_code, 301)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Account deleted!")
