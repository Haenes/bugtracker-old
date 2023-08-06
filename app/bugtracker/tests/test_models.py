from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from bugtracker.models import Project, Issue


class ProjectTestCase(TestCase):


    def setUp(self):
        user = User.objects.create(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")      
        Project.objects.create(name="Testing1", key="TEST1", type="Fullstack software", author_id=user.id)
        Project.objects.create(name="Testing2", description="Description for second test project", key="TEST2", type="Fullstack software", author_id=user.id)
        Project.objects.create(name="Testing3", description="Description for second test project", key="TEST3", type="Fullstack software", starred=1, author_id=user.id)


    def test_model_validation(self):
        try:
            user = User.objects.get(username="testing")
            project = Project(name="Te", description="Description for test project", key="TE", type="Fullstack software", author_id=user.id)
            project.full_clean()
        except ValidationError as e:
           self.assertEqual(
               {
                   'name': ['Name field must contain at least 3 letters'],
                   'key': ['Key field must contain at least 3 letters']
                }, 
                e.message_dict
            )


    def test_description(self):
        project1 = Project.objects.get(name="Testing1")
        project2 = Project.objects.get(name="Testing2")

        self.assertEqual(project1.description, "")
        self.assertNotEqual(project2.description, "")


    def test_starred(self):
        project1 = Project.objects.get(name="Testing1")
        project3 = Project.objects.get(name="Testing3")

        self.assertEqual(project1.starred, 0)
        self.assertEqual(project3.starred, 1)


class IssueTestCase(TestCase):


    def setUp(self):
        user = User.objects.create(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")      
        project = Project.objects.create(name="Testing1", key="TEST1", type="Fullstack software", author_id=user.id)
        Issue.objects.create(
            project_id=project.id,
            title="Issue", 
            description="Big Socks Just Big Socks", 
            type="Feature",
            priority="Medium", 
            status="To do", 
            author_id=user.id)


    def test_description(self):
        issue = Issue.objects.get(title="Issue")

        self.assertNotEqual(issue.description, "")
        self.assertEqual(issue.description, "Big Socks Just Big Socks")
