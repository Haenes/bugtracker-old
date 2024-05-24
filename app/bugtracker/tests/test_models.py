from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from bugtracker.models import Project, Issue


class ProjectTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test", last_name="Test", username="testing",
            email="testemail@gmail.com", password="Password123#"
            )
        self.project1 = Project.objects.create(
            name="Testing1", key="TEST1",
            type="FULLSTACK", author_id=self.user.id
            )
        self.project2 = Project.objects.create(
            name="Testing2", description="Test project2", key="TEST2",
            type="FULLSTACK", author_id=self.user.id
            )
        self.project3 = Project.objects.create(
            name="Testing3", description="Test project3", key="TEST3",
            type="FULLSTACK", starred=1, author_id=self.user.id
            )

    def test_model_validation(self):
        try:
            project = Project.objects.create(
                name="Te", description="Description for test project",
                key="TE", type="FULLSTACK", author_id=self.user.id
                )
            project.full_clean()
        except ValidationError as e:
            self.assertEqual(
               {
                   "name": ["Name field must contain at least 3 letters"],
                   "key": ["Key field must contain at least 3 letters"]
                   }, e.message_dict
                )

    def test_description(self):
        self.assertEqual(self.project1.description, "")
        self.assertNotEqual(self.project2.description, "")

    def test_starred(self):
        self.assertEqual(self.project1.starred, 0)
        self.assertEqual(self.project3.starred, 1)

    def test_str(self):
        self.assertEqual(str(self.project1), "Testing1")


class IssueTestCase(TestCase):

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

    def test_description(self):
        self.assertNotEqual(self.issue.description, "")
        self.assertEqual(self.issue.description, "Big Socks Just Big Socks")

    def test_str(self):
        self.assertEqual(str(self.issue), "Issue")
