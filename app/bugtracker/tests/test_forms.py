from django.test import TestCase
from django.contrib.auth.models import User

from bugtracker.models import Project, Issue
from bugtracker.forms import ( 
    IssueModalForm,
    ProjectDetailsForm, 
    ProjectModalForm, 
    RegisterForm, 
    UserPasswordChangeForm,
    UserForm
    )


class RegisterFormTestCase(TestCase):


    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_first_name_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields["first_name"].label == "First name")


    def test_first_name_field(self):
        data_invalid = {
            "first_name": "Asd1", 
            "last_name": "Last", 
            "username": "username", 
            "email": "email@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"
            }

        data_valid = {
            "first_name": "First", 
            "last_name": "Last", 
            "username": "username", 
            "email": "email@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"
            }

        form_invalid = RegisterForm(data_invalid)
        form_valid = RegisterForm(data_valid)

        self.assertEqual(form_invalid.errors["first_name"], ["First name must have only letters"])
        self.assertEqual(form_valid.errors, {})


    def test_last_name_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields["last_name"].label == "Last name")


    def test_last_name_field(self):
        data_invalid = {
            "first_name": "First", 
            "last_name": "Last1", 
            "username": "username", 
            "email": "email@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"
            }

        data_valid = {"first_name": "First", "last_name": "Last", "username": "username", "email": "email@gmail.com", "password1": "Test123#", "password2": "Test123#"}
        
        form_invalid = RegisterForm(data_invalid)
        form_valid = RegisterForm(data_valid)
        
        self.assertEqual(form_invalid.errors["last_name"], ["Last name must have only letters"])
        self.assertEqual(form_valid.errors, {})


    def test_username_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields["username"].label == "Username")
  

    def test_username_field(self):
        data_invalid1 = {
            "first_name": "First", 
            "last_name": "Last", 
            "username": "username1", 
            "email": "email@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"}

        data_invalid2 = {
            "first_name": "First", 
            "last_name": "Last", 
            "username": "testing", 
            "email": "email@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"
            }

        data_valid = {
            "first_name": "First", 
            "last_name": "Last", 
            "username": "username", 
            "email": "email@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"
            }

        form_invalid1 = RegisterForm(data_invalid1)
        form_invalid2 = RegisterForm(data_invalid2)
        form_valid = RegisterForm(data_valid)
        
        self.assertEqual(form_invalid1.errors["username"], ["Username must have only letters"])
        self.assertEqual(form_invalid2.errors["username"], ["That username already exists"])
        self.assertEqual(form_valid.errors, {})


    def test_email_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields["email"].label == "Email")


    def test_email_field(self):
        data_invalid = {
            "first_name": "First", 
            "last_name": "Last", 
            "username": "username1", 
            "email": "testemail@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"
            }
        
        data_valid = {
            "first_name": "First", 
            "last_name": "Last", 
            "username": "username", 
            "email": "email@gmail.com", 
            "password1": "Test123#", 
            "password2": "Test123#"
            }

        form_invalid = RegisterForm(data_invalid)
        form_valid = RegisterForm(data_valid)
        
        self.assertEqual(form_invalid.errors["email"], ["That email already exists"])
        self.assertEqual(form_valid.errors, {})


    def test_password1_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields["password1"].label == "Password")
    

    def test_password1_field(self):
        data_invalid = {"first_name": "First", "last_name": "Last", "username": "username1", "email": "email@gmail.com", "password1": "Test1234", "password2": "Test123#"}
        data_valid = {"first_name": "First", "last_name": "Last", "username": "username", "email": "email@gmail.com", "password1": "Test123#", "password2": "Test123#"}
        
        form_invalid = RegisterForm(data_invalid)
        form_valid = RegisterForm(data_valid)
        
        self.assertEqual(form_invalid.errors["password1"], ["The password doesn't meet the conditions"])
        self.assertEqual(form_valid.errors, {})


    def test_password2_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields["password2"].label == "Password confirmation")


    def test_password2_field(self):
        data_invalid = {"first_name": "First", "last_name": "Last", "username": "username1", "email": "email@gmail.com", "password1": "Test123#", "password2": "Test1234#"}
        data_valid = {"first_name": "First", "last_name": "Last", "username": "username", "email": "email@gmail.com", "password1": "Test123#", "password2": "Test123#"}
        
        form_invalid = RegisterForm(data_invalid)
        form_valid = RegisterForm(data_valid)
        
        self.assertEqual(form_invalid.errors["password2"], ["Passwords don't match"])
        self.assertEqual(form_valid.errors, {})


class UserFormTestCase(TestCase):
    

    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_first_name_field_label(self):
        form = UserForm()
        self.assertTrue(form.fields["first_name"].label == "First name")


    def test_first_name_field(self):
        data_invalid1 = {"first_name": "Fi", "last_name": "Last", "username": "username", "email": "email@gmail.com"}
        data_invalid2 = {"first_name": "First1", "last_name": "Last", "username": "testing", "email": "email@gmail.com"}
        data_valid = {"first_name": "First", "last_name": "Last", "username": "username", "email": "email@gmail.com"}
        
        form_invalid1 = UserForm(data_invalid1)
        form_invalid2 = UserForm(data_invalid2)
        form_valid = UserForm(data_valid)
        
        self.assertEqual(form_invalid1.errors["first_name"], ["First name must contain at least 3 letters"])
        self.assertEqual(form_invalid2.errors["first_name"], ["Name must have only letters"])
        self.assertEqual(form_valid.errors, {})


    def test_last_name_field_label(self):
        form = UserForm()
        self.assertTrue(form.fields["last_name"].label == "Last name")


    def test_last_name_field(self):
        data_invalid1 = {"first_name": "First", "last_name": "La", "username": "username", "email": "email@gmail.com"}
        data_invalid2 = {"first_name": "First1", "last_name": "Last1", "username": "testing", "email": "email@gmail.com"}
        data_valid = {"first_name": "First", "last_name": "Last", "username": "username", "email": "email@gmail.com"}
        
        form_invalid1 = UserForm(data_invalid1)
        form_invalid2 = UserForm(data_invalid2)
        form_valid = UserForm(data_valid)
        
        self.assertEqual(form_invalid1.errors["last_name"], ["Last name must contain at least 3 letters"])
        self.assertEqual(form_invalid2.errors["last_name"], ["Name must have only letters"])
        self.assertEqual(form_valid.errors, {})


    def test_username_field_label(self):
        form = UserForm()
        self.assertTrue(form.fields["username"].label == "Username")


    def test_email_field_label(self):
        form = UserForm()
        self.assertTrue(form.fields["email"].label == "Email address")


class UserPasswordChangeFormTestCase(TestCase):


    def setUp(self):
        User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")


    def test_new_password1_field_label(self):
        user = User.objects.get(username="testing")
        form = UserPasswordChangeForm(user)
        self.assertTrue(form.fields["new_password1"].label == "New password")


    def test_password1_field(self):
        user = User.objects.get(username="testing")
        data_invalid = {"new_password1": "Test1234", "new_password2": "Test123#"}
        data_valid = {"new_password1": "Test123#", "new_password2": "Test123#"}
        
        form_invalid = UserPasswordChangeForm(user, data_invalid)
        form_valid = UserPasswordChangeForm(data_valid)
        
        self.assertEqual(form_invalid.errors["new_password1"], ["The password doesn't meet the conditions"])
        self.assertEqual(form_valid.errors, {})


    def test_new_password2_field_label(self):
        user = User.objects.get(username="testing")
        form = UserPasswordChangeForm(user)
        self.assertTrue(form.fields["new_password2"].label == "New password confirmation")


    def test_new_password2_field(self):
        user = User.objects.get(username="testing")
        data_invalid = {"new_password1": "Test123#", "new_password2": "Test1234#"}
        data_valid = {"new_password1": "Test123#", "new_password2": "Test123#"}
        
        form_invalid = UserPasswordChangeForm(user, data_invalid)
        form_valid = UserPasswordChangeForm(user, data_valid)
        
        self.assertEqual(form_invalid.errors["new_password2"], ["Passwords don't match"])
        self.assertEqual(form_valid.errors, {})


class ProjectDetailsFormTestCase(TestCase):
    

    def setUp(self):
        user = User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")
        Project.objects.create(name="Testing", key="TEST", type="Fullstack software", starred=1, author_id=user.id)


    def test_name_field_label(self):
        project = Project.objects.get(key="TEST")
        form = ProjectDetailsForm(instance=project)
        
        self.assertTrue(form.fields["name"].label == "Name")


    def test_name_field(self):
        data_invalid = {"name": "Testing1", "key": "TESTII", "starred":1}
        data_valid = {"name": "Test", "key": "TESTI", "starred":1}

        form_invalid = ProjectDetailsForm(data_invalid)
        form_valid = ProjectDetailsForm(data_valid)
        
        self.assertEqual(form_invalid.errors["name"], ["Project name must have only letters"])
        self.assertEqual(form_valid.errors, {})


    def test_key_field_label(self):
        form = ProjectDetailsForm()
        
        self.assertTrue(form.fields["key"].label == "Key")


    def test_key_field(self):
        data_invalid = {"name": "Test", "key": "TEST1", "starred":1}
        data_valid = {"name": "Test", "key": "TESTII", "starred":1}

        form_invalid = ProjectDetailsForm(data_invalid)
        form_valid = ProjectDetailsForm(data_valid)
        
        self.assertEqual(form_invalid.errors["key"], ["Key must have only letters"])
        self.assertEqual(form_valid.errors, {})


class ProjectModalFormTestCase(TestCase):


    def setUp(self):
        user = User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")
        Project.objects.create(name="Testing", key="TEST", type="Fullstack software", starred=1, author_id=user.id)


    def test_name_field(self):
        user = User.objects.get(username="testing")
        data_invalid = {"author": user.id, "name": "Testing", "key": "TESTI", "type": "Fullstack software", "starred":1}
        data_valid = {"author": user.id, "name": "Test", "key": "TESTII", "type": "Fullstack software", "starred":1}

        form_invalid = ProjectModalForm(data_invalid)
        form_valid = ProjectModalForm(data_valid)
        
        self.assertEqual(form_invalid.errors["name"], ["That project already exists"])
        self.assertEqual(form_valid.errors, {})


    def test_key_field(self):
        user = User.objects.get(username="testing")
        data_invalid = {"author": user.id, "name": "Test", "key": "TEST", "type": "Fullstack software", "starred":1}
        data_valid = {"author": user.id, "name": "Test", "key": "TESTII", "type": "Fullstack software", "starred":1}

        form_invalid = ProjectModalForm(data_invalid, initial={"author_id": user.id})
        form_valid = ProjectModalForm(data_valid, initial={"author_id": user.id})
        
        self.assertEqual(form_invalid.errors["key"], ["Project with that key already exists"])
        self.assertEqual(form_valid.errors, {})


class IssueModalFormTestCase(TestCase):


    def setUp(self):
        user = User.objects.create_user(first_name="Test", last_name="Test", username="testing", email="testemail@gmail.com", password="Password123#")
        project = Project.objects.create(name="Testing", key="TEST", type="Fullstack software", starred=1, author_id=user.id)
        Issue.objects.create(
            project_id=project.id,
            title="Issue", 
            description="Big Socks Just Big Socks", 
            type="Feature",
            priority="Medium", 
            status="To do", 
            author_id=user.id)


    def test_title_field(self):
        user = User.objects.get(username="testing")
        project = Project.objects.get(key="TEST")
        
        
        data_invalid = {
            "author": user.id, 
            "project": project.id, 
            "title": "Issue", 
            "description": "Test", 
            "type": "Feature", 
            "priority": "Medium", 
            "status": "To do"
            }
        
        data_valid = {
            "author": user.id, 
            "project": project.id, 
            "title": "Valid issue", 
            "description": "Test", 
            "type": "Feature", 
            "priority": "Medium", 
            "status": "To do"
            }
        
        form_invalid = IssueModalForm(data_invalid)
        form_valid = IssueModalForm(data_valid)
        self.assertEqual(form_invalid.errors["title"], ["Issue with that title already exists"])
        self.assertEqual(form_valid.errors, {})


class UserSetNewPasswordFormTestCase(UserPasswordChangeFormTestCase):
    # Tests for this form is ABSOLUTELY identical for the UserPasswordChangeForm
	pass
