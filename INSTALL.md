# Installation Instructions
>Note that there are three instructions here: for SQLite, MySQL and Docker (with SQLite).

In the end, you should have such a structure (without db.sqlite3 if you're using MySQL):

![Screenshot of project structure](https://github.com/Haenes/BugTracker/assets/138951721/97c019b5-4e20-4adb-b370-9c434b2fbbb9)

<h3>Docker:</h3> 

1) Pull and run image: `docker run -dp 8000:8000 haenes/bugtracker`
2) To log in use this credentialls: Username - test, Password - test123#
>Please note that the email services will not work! As a result, you will not be able to register/reset your password.


<h3>SQLite:</h3> 	

1) Clone project: `git clone https://github.com/Haenes/BugTracker.git`
2) Create venv: `python3 -m venv venv`
3) Activate venv: `source venv/bin/activate`
4) Install requirements: `pip install -r requirements.txt`
5) Go to settings.py (BugTracker/app/app/settings.py) and change "DATABASES" to:

```python3
DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': BASE_DIR / 'db.sqlite3',
    }
 }
```

6) Create .env file in app folder (BugTracker/app): email settings required to send emails for user registration and password reset
7) Do migrations: `python3 manage.py makemigrations && python3 manage.py migrate`
8) Create a superuser:  `python3 manage.py createsuperuser`
   
   > Create a password containing at least 1 special character, 1 lowercase and uppercase letters, 1 digit, equal/longer than 8 characters

10) Also, if you want to run tests, you can enter (in BugTracker/app): `python3 manage.py test bugtracker/tests --keepdb --verbosity 2`
11) After that, you can run server:  `python3 manage.py runserver`


<h3>.env file example:</h3>

>NOTE: if you prefer to use SQLite, then you DON'T needed to last two lines

```python3
EMAIL_HOST_USER = "YOUR EMAIL ADDRESS"   # it's better to create a new one, specifically for this project
EMAIL_HOST_PASSWORD = "YOUR EMAIL PASSWORD"
EMAIL_ADMIN = ["YOUR EMAIL ADDRESS"]     # there you can use email from above or one of yours primary emails

DATABASE_USER = "USER THAT U CREATED"
DATABASE_PASSWORD = "PASSWORD FOR THAT USER"
DATABASE_PORT = "PORT"
DATABASE_HOST = "HOST"
```

<h3>MySQL:</h3>

1) Steps 1-4 is absolutely identical to those specified for SQLite above
2) Create a MySQL user, database itself and don't forget to give privileges to the created user
3) Steps 6-10 is also identical to those specified for SQLite above
