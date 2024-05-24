from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from bugtracker.models import Project, Issue


class ViewsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.project = Project.objects.create(
            name="Testing1", key="TEST1",
            type="FULLSTACK", author_id=self.user.id
            )
        self.issue = Issue.objects.create(
            project_id=self.project.id,
            title="Issue",
            description="Big Socks Just Big Socks",
            type="Feature",
            priority="Medium",
            status="TO_DO",
            author_id=self.user.id
            )
        self.project_url = f"http://testserver/api/projects/{self.project.id}/"
        self.token = Token.objects.get(user__username="testing")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_index_page_authorized(self):
        r = self.client.get(reverse("api-root"))
        self.assertEqual(r.status_code, 200)

    def test_index_page_unauthorized(self):
        self.client.credentials()
        r = self.client.get(reverse("api-root"))

        self.assertEqual(r.status_code, 401)
        self.assertEqual(
            r.data["detail"],
            "Authentication credentials were not provided."
            )

    def test_projects_view_get(self):
        r = self.client.get(reverse("project-list"))
        self.assertEqual(r.status_code, 200)

    def test_projects_view_post_correct(self):
        data = {
            "name": "Testing",
            "key": "TEST",
            "type": "FULLSTACK",
            "starred": 1,
            "author_id": self.user.id
        }
        r = self.client.post(reverse("project-list"), data=data)
        self.assertEqual(r.status_code, 201)

    def test_projects_view_post_incorrect(self):
        data = {
            "name": "T",
            "key": "T",
            "starred": 1,
            "author_id": self.user.id
        }
        r = self.client.post(reverse("project-list"), data=data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(
            r.data["name"][0],
            "Ensure this field has at least 3 characters."
            )
        self.assertEqual(
            r.data["key"][0],
            "Ensure this field has at least 3 characters."
            )
        self.assertEqual(
            r.data["type"][0],
            "This field is required."
            )

    def test_project_details_get(self):
        r = self.client.get(reverse("project-detail", args=[self.project.id]))
        self.assertEqual(r.status_code, 200)

    def test_project_details_put_correct(self):
        data = {
            "name": "Testing",
            "key": "TEST",
            "type": "BACKEND",
            "starred": 1
        }
        r = self.client.put(
            reverse("project-detail", args=[self.project.id]),
            data=data
            )
        self.assertEqual(r.status_code, 200)

    def test_project_details_put_incorrect(self):
        data = {
            "name": "T",
            "key": "TEST",
            "starred": 1
        }
        r = self.client.put(
            reverse("project-detail", args=[self.project.id]),
            data=data
            )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(
            r.data["name"][0],
            "Ensure this field has at least 3 characters."
        )
        self.assertEqual(
            r.data["type"][0],
            "This field is required."
        )

    def test_project_details_delete(self):
        r = self.client.delete(
            reverse("project-detail", args=[self.project.id])
            )
        self.assertEqual(r.status_code, 204)

#       ---------------------------------

    def test_issues_view_get(self):
        r = self.client.get(reverse("issue-list"))
        self.assertEqual(r.status_code, 200)

    def test_issues_view_post_correct(self):
        data = {
            "project": self.project_url,
            "title": "Title issue",
            "type": "Feature",
            "priority": "Medium",
            "status": "TO_DO",
            "author": self.user.id
        }
        r = self.client.post(reverse("issue-list"), data=data)
        self.assertEqual(r.status_code, 201)

    def test_issues_view_post_incorrect(self):
        data = {
            "project": self.project_url,
            "title": "Title issue",
            "priority": "Medium",
            "status": "TO_DO",
            "author": self.user.id
        }
        r = self.client.post(reverse("issue-list"), data=data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(
            r.data["type"][0],
            "This field is required."
            )

    def test_issue_details_get(self):
        r = self.client.get(
            reverse("issue-detail", args=[self.issue.id])
            )
        self.assertEqual(r.status_code, 200)

    def test_issue_details_put_correct(self):
        data = {
            "project": self.project_url,
            "title": "Test title",
            "type": "Bug",
            "priority": "Highest",
            "status": "IN_PROGRESS",
        }
        r = self.client.put(
            reverse("issue-detail", args=[self.issue.id]),
            data=data
            )
        self.assertEqual(r.status_code, 200)

    def test_issue_details_put_incorrect(self):
        data = {
            "project": self.project_url,
            "title": "Test title",
            "priority": "Highest",
            "status": "IN_PROGRESS",
        }
        r = self.client.put(
            reverse("issue-detail", args=[self.issue.id]),
            data=data
            )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(
            r.data["type"][0],
            "This field is required."
        )

    def test_issue_details_delete(self):
        r = self.client.delete(
            reverse("issue-detail", args=[self.issue.id])
            )
        self.assertEqual(r.status_code, 204)
