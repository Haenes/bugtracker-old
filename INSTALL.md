# Installation Instructions
<h3>Docker compose:</h3> 

1) Clone repository: `git clone https://github.com/Haenes/bugtracker.git`
2) Add the .env file contains the following contents in the root directory (where it's located README.md):
```python3
# You can leave everything as it is,
# the application will start and work correctly
# (except for the mail service)

DJANGO_SECRET = "SECRETKEY"

# This is necessary for the mail service
# to send emails to users and admins in the following situations:
# confirmation of registration, password reset and server error.
EMAIL_HOST_USER = "EMAIL"
EMAIL_HOST_PASSWORD = "PASSWORD"
EMAIL_ADMIN = "EMAIL"
ADMIN_NAME = "Name"

POSTGRES_PASSWORD = "Testing123#"
POSTGRES_USER = "test"
POSTGRES_HOST = "db"
POSTGRES_PORT = "5432"
POSTGRES_DB = "test"
PGDATA = "var/lib/postgresql/data/pgdata"

REDIS_USER = "bugtracker"
REDIS_PASSWORD = "Testing"

CELERY_BROKER_URL = "pyamqp://bugtracker:Testing@rabbitmq/"
```
3)  Startup from the same directory as in the previous step: `docker compose up`
>If you have permission denied error - add sudo to the beginning of the command. 
4) To log in, go to [this](http://0.0.0.0) or [this](http://localhost) login page and use this credentialls: `Username - test, Password - Test123#` after the following input:
```web    | ----------- Run -----------
web    | [2024-02-15 06:38:41 +0000] [12] [INFO] Starting gunicorn 21.2.0
web    | [2024-02-15 06:38:41 +0000] [12] [INFO] Listening at: http://0.0.0.0:8000 (12)
web    | [2024-02-15 06:38:41 +0000] [12] [INFO] Using worker: sync
web    | [2024-02-15 06:38:41 +0000] [13] [INFO] Booting worker with pid: 13
```
> If you encounter an error in RabbitMQ container - repeat step 3 again.
