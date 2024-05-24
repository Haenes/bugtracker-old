import re
import json

from django.core import mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import translation
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

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        cls.factory = RequestFactory()

    def test_last_modified_issue_of_project_datetime(self):
        project = Project.objects.create(
            name="Testing", key="TEST", type="FULLSTACK",
            starred=1, author_id=self.user.id
            )
        Issue.objects.create(
            project_id=project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="TO_DO",
            author_id=self.user.id
            )
        request = self.factory.get(reverse("boards", args=[project.id]))
        request.user = self.user
        response = last_modified_issue_of_project(request, project.id)

        self.assertIsNotNone(response)

    def test_last_modified_issue_of_project_none(self):
        project = Project.objects.create(
            name="Testing", key="TEST", type="FULLSTACK",
            starred=1, author_id=self.user.id
            )
        request = self.factory.get(reverse("boards", args=[project.id]))
        request.user = self.user
        response = last_modified_issue_of_project(request, project.id)

        self.assertIsNone(response)

    def test_last_created_project_datetime(self):
        Project.objects.create(
            name="Testing", key="TEST", type="FULLSTACK",
            starred=1, author_id=self.user.id
            )
        request = self.factory.get(reverse("projects"))
        request.user = self.user
        response = last_created_project(request)

        self.assertIsNotNone(response)

    def test_last_created_project_none(self):
        request = self.factory.get(reverse("projects"))
        request.user = self.user
        response = last_created_project(request)

        self.assertIsNone(response)

    def test_last_update_of_issue_datetime(self):
        project = Project.objects.create(
            name="Testing", key="TEST", type="FULLSTACK",
            starred=1, author_id=self.user.id
            )
        issue = Issue.objects.create(
            project_id=project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="TO_DO",
            author_id=self.user.id
            )
        request = self.factory.get(
            reverse("issue-details", args=[project.id, issue.id])
            )
        request.user = self.user
        response = last_update_of_issue(request, project.id, issue.id)

        self.assertIsNotNone(response)


class SettingsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view_anon(self):
        response = self.client.get(reverse("settings"))
        self.assertRedirects(response, expected_url="/login/?next=/settings/")

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("settings"))

        self.assertEqual(response.status_code, 200)

    def test_change_timezone(self):
        self.client.force_login(self.user)
        data = {"timezone": "UTC"}
        response = self.client.post(reverse("settings"), data=data)

        self.assertRedirects(response, "/settings/")

    def test_change_language(self):
        self.client.force_login(self.user)
        data = {"language": "ru"}
        response = self.client.post(
            path="/settings/setlang/",
            data=data, follow=True
            )

        self.assertRedirects(response, "/")
        self.assertEqual(response.headers["Content-Language"], "ru")


class ProjectsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        cls.project = Project.objects.create(
            name="Testing", key="TEST", type="FULLSTACK",
            starred=1, author_id=cls.user.id
            )
        cls.project2 = Project.objects.create(
            name="TestO", key="TESTO", type="BACKEND",
            starred=0, author_id=cls.user.id
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
            "type": "FULLSTACK",
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
            "type": "FULLSTACK",
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

    def test_put_unfavorite(self):
        self.client.force_login(self.user)
        data = {"icon_id": f"star{self.project.id}", "icon_color": "grey"}

        response = self.client.put(reverse("projects"), data=json.dumps(data))
        project_starred = Project.objects.only(
            "starred"
            ).get(id=self.project.id).starred

        self.assertEqual(response.status_code, 200)
        self.assertEqual(project_starred, 0)

    def test_put_favorite(self):
        self.client.force_login(self.user)
        data = {"icon_id": f"star{self.project2.id}", "icon_color": "gold"}

        response = self.client.put(reverse("projects"), data=json.dumps(data))
        project_starred = Project.objects.only(
            "starred"
            ).get(id=self.project2.id).starred

        self.assertEqual(response.status_code, 200)
        self.assertEqual(project_starred, 1)


class BoardsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        cls.project = Project.objects.create(
            name="Testing1", key="TEST1",
            type="FULLSTACK", author_id=cls.user.id
            )
        cls.issue = Issue.objects.create(
            project_id=cls.project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="TO_DO",
            author_id=cls.user.id
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

        self.assertEqual(response.status_code, 200)
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
            "status": "TO_DO",
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
            "status": "TO_DO",
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

    def test_put_status(self):
        self.client.force_login(self.user)
        data = {"target": "In Progress", "issue_id": self.issue.id}

        response = self.client.put(
            reverse("boards", args=[self.project.id]), data=json.dumps(data)
            )
        issue_status = Issue.objects.only(
            "status"
            ).get(id=self.issue.id).status

        self.assertEqual(response.status_code, 200)
        self.assertEqual(issue_status, "In Progress")


class IssueDetailsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        cls.project = Project.objects.create(
            name="Testing", key="TEST",
            type="FULLSTACK", author_id=cls.user.id
            )

        cls.issue1 = Issue.objects.create(
            project_id=cls.project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="TO_DO",
            author_id=cls.user.id
            )

        cls.issue2 = Issue.objects.create(
            project_id=cls.project.id,
            title="Issue2",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="TO_DO",
            author_id=cls.user.id
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

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "issue-details.html")

    def test_post_success(self):
        self.client.force_login(self.user)
        data = {
            "project": self.project.id,
            "title": "Title issue",
            "type": "Feature",
            "priority": "Medium",
            "status": "TO_DO",
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
            "status": "TO_DO",
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

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        cls.project1 = Project.objects.create(
            name="TestingI", key="TEST",
            type="FULLSTACK", author_id=cls.user.id
            )
        cls.project2 = Project.objects.create(
            name="TestingII", key="TESTII",
            type="FULLSTACK", author_id=cls.user.id
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

        self.assertEqual(response.status_code, 200)
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

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        cls.user2 = User.objects.create_user(
            first_name="Test", last_name="Test", username="testingII",
            email="testemail2@gmail.com", password="Password123#"
            )

    def test_call_view_anonymous(self):
        response = self.client.get(reverse("accounts", args=[self.user.id]))
        self.assertRedirects(
            response,
            f"/login/?next=/accounts/{self.user.id}/"
            )

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts", args=[self.user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts.html")

    def test_post_user_success(self):
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

    def test_post_user_fail(self):
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

    def test_post_password_success(self):
        self.client.force_login(self.user)
        data = {
            "change_password": True,
            "new_password1": "pASSword123#",
            "new_password2": "pASSword123#",
            }

        response = self.client.post(
            path=reverse("accounts", args=[self.user.id]),
            data=data, follow=True
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertContains(
            response,
            "Your password was successfully updated!"
            )

    def test_post_password_fail(self):
        self.client.force_login(self.user)
        data = {
            "change_password": True,
            "new_password1": "pASSword",
            "new_password2": "pASS123#",
            }

        response = self.client.post(
            path=reverse("accounts", args=[self.user.id]),
            data=data, follow=True
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 2)
        self.assertContains(
            response,
            "The password doesn&#x27;t meet the conditions",
            )
        self.assertContains(response, "Passwords don&#x27;t match")


class SearchTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view_anonymous(self):
        response = self.client.get(reverse("search"))
        self.assertRedirects(response, "/login/?next=/search/")

    def test_call_view_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("search"))

        self.assertEqual(response.status_code, 302)

    def test_search_success(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("search"), {"q": "Issue"})

        self.assertRedirects(
            response,
            reverse("search-results", args=["Issue"])
            )

    def test_search_empty(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("search"), {"q": " "})
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, "/")
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Please, give a data for search")

    def test_search_many_words(self):
        self.client.force_login(self.user)
        data = {"q": "Hi there! I'm testing you."}

        response = self.client.get(reverse("search"), data)
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, "/")
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Please, give just one word to search"
            )

    def test_search_special_symbols(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("search"), {"q": "!"})
        messages = list(get_messages(response.wsgi_request))

        self.assertRedirects(response, "/")
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Please, don't use special symbols in search"
            )


class SearchResultsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
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

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search-results.html")


class LoginTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_call_view_already_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("login"))

        self.assertRedirects(response, reverse("projects"))

    def test_post_success(self):
        data = {"username": "testing", "password": "Password123#"}

        self.client.login(username=data["username"], password=data["password"])
        response = self.client.post(reverse("login"), data=data, follow=True)
        cookies = dict(self.client.cookies.get("sessionid"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cookies["max-age"], 3600)
        self.assertTemplateUsed(response, "projects.html")

    def test_post_success_remember_me(self):
        data = {
            "username": "testing",
            "password": "Password123#",
            "remember": True
            }

        self.client.login(username=data["username"], password=data["password"])
        response = self.client.post(reverse("login"), data=data, follow=True)
        cookies = dict(self.client.cookies.get("sessionid"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cookies["max-age"], 2592000)
        self.assertTemplateUsed(response, "projects.html")

    def test_post_fail(self):
        data = {"username": "wrong", "password": "Password123#"}

        self.client.login(username=data["username"], password=data["password"])
        response = self.client.post(reverse("login"), data=data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            remove_html(str(messages[0])),
            "Invalid username and/or password"
            )


class RegisterTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
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

    def test_post_success_rus(self):
        data = {
            "first_name": "Second",
            "last_name": "PreLast",
            "username": "nameuser",
            "email": "liaem@gmail.com",
            "password1": "Test123#",
            "password2": "Test123#"
            }

        response = self.client.post(
            path=reverse("register"), data=data, follow=True,
            headers={"accept-language": "ru"}
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Ссылка для активации была отправлена на ваш электронный адрес"
            )
        self.assertTemplateUsed(response, "login.html")
        translation.activate(settings.LANGUAGE_CODE)

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

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view_success(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.get(
            path=reverse("register_confirm", args=[uid, token])
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]),
            "Email is confirmed, you can log in now!"
            )
        self.assertEqual(response.status_code, 302)

    def test_call_view_fail(self):
        fake_user_id = 451
        fake_uid = urlsafe_base64_encode(force_bytes(fake_user_id))
        token = default_token_generator.make_token(self.user)

        response = self.client.get(
            path=reverse("register_confirm", args=[fake_uid, token])
            )
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]), "Email confirmation is failed!")
        self.assertEqual(response.status_code, 302)


class LogoutTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 302)


class PasswordResetTestCase(TestCase):

    def test_call_view(self):
        response = self.client.get(reverse("password-reset"))

        self.assertEqual(response.status_code, 200)
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

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "password-reset-done.html")


class PasswordResetConfirmTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )

    def test_call_view(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.get(
            path=reverse("password_reset_confirm", args=[uid, token]))

        self.assertEqual(response.status_code, 200)
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

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        cls.project = Project.objects.create(
            name="Testing1", key="TEST1",
            type="FULLSTACK", author_id=cls.user.id
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

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Project deleted!")


class DeleteIssueTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        cls.project = Project.objects.create(
            name="Testing1", key="TEST1",
            type="FULLSTACK", author_id=cls.user.id
            )
        cls.issue = Issue.objects.create(
            project_id=cls.project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="TO_DO",
            author_id=cls.user.id)

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

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Issue deleted!")


class DeleteAccountTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
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

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(remove_html(str(messages[0])), "Account deleted!")
