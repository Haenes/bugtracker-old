# Installation Instructions
>Note that there are two instructions here: for SQLite and MySQL.

In the end, you should have such a structure (without db.sqlite3 if you're using MySQL):

![Screenshot of project structure](https://github.com/Haenes/BugTracker/assets/138951721/97c019b5-4e20-4adb-b370-9c434b2fbbb9)

<h3>SQLite:</h3> 	

1) Clone project: `git clone https://github.com/Haenes/BugTracker.git`
2) Create venv: `python3 -m venv venv`
3) Activate venv: `source venv/bin/activate`
4) Install requirements in app folder (BugTracker/app): `cd app -> pip install -r requirements.txt`
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
7) Do migrations: `python3 manage.py migrate`
8) Create a superuser:  `python3 manage.py createsuperuser`
9) Also, if you want to run tests, you can enter (in BugTracker/app): `python3 manage.py test bugtracker/tests --keepdb --verbosity 2`
10) After that, you can run server:  `python3 manage.py runserver`


<h3>.env file example:</h3>

>NOTE: if you prefer to use SQLite, then you DON'T needed to last two lines

```python3
EMAIL_HOST_USER = "YOUR EMAIL ADDRESS"   # it's better to create a new one, specifically for this project
EMAIL_HOST_PASSWORD = "YOUR EMAIL PASSWORD"
EMAIL_ADMIN = ["YOUR EMAIL ADDRESS"]     # there you can use email from above or one of yours primary emails

DATABASE_USER = "USER THAT U CREATED"
DATABASE_PASSWORD = "PASSWORD FOR THAT USER"
```

<h3>MySQL:</h3>

1) Steps 1-4 is absolutely identical to those specified for SQLite above
2) Create a MySQL user and the database itself
3) Steps 6-10 is also identical to those specified for SQLite above
