## Firstly installations [nginx, postgres]

```
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

___

## Postgres installation

```
sudo -u postgres psql
CREATE DATABASE prof;
CREATE USER prof WITH PASSWORD '***env***';

ALTER ROLE prof SET client_encoding TO 'utf8';
ALTER ROLE prof SET default_transaction_isolation TO 'read committed';
ALTER ROLE prof SET timezone TO 'Asia/Tashkent';
ALTER DATABASE prof OWNER TO prof;

GRANT ALL PRIVILEGES ON DATABASE prof TO prof;
```

___

## Redis Installation

```
sudo apt install redis-server

sudo nano /etc/redis/redis.conf
# and supervised no -> supervised systemd

sudo systemctl enable redis-server

sudo systemctl start redis
sudo systemctl status redis
```

___

## Pip Installation

```
pip install -r requirements.txt
```

___

## Gunicorn Installation

```
from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count() * 2 + 1


max_requests = 1000
# worker_class = 'gevent'
workers = max_workers()
reload = True
# Access log - records HTTP req goings-on
accesslog = '/home/user/prof/backend/logs/prof.access.log'
# Error log - records Gunicorn server goings-on
errorlog = '/home/user/prof/backend/logs/prof.error.log'
# Whether to send Django output to the error log
capture_output = True
bind = "unix:/home/user/prof/backend/run/project.sock"
```

___

## Systemd service Installation  [prof.service]

```
[Unit]
Description=Gunicorn daemon for Prof-talim Edu Uz
Before=nginx.service
After=network.target

[Service]
User=user
Group=user
WorkingDirectory=/home/user/prof/backend/project
ExecStart=/home/user/prof/backend/venv/bin/gunicorn project.wsgi:application -c /home/user/prof/backend/project/gunicorn.conf.py
Restart=always
SyslogIdentifier=gunicorn

[Install]
WantedBy=multi-user.target
```

### 2nd temp

```
[Unit]
Description=Gunicorn daemon for Prof-talim Edu Uz
Before=nginx.service
After=network.target

[Service]
User=user
Group=user
WorkingDirectory=/home/user/prof/backend/project
ExecStart=/home/user/prof/backend/venv/bin/gunicorn \
 --access-logfile /home/user/prof/backend/logs/prof.access.log \
 --error-logfile /home/user/prof/backend/logs/prof.error.log \
 --workers 13 \
 --bind unix:/home/user/prof/backend/run/project.sock \
 project.wsgi:application
Restart=always
SyslogIdentifier=gunicorn

[Install]
WantedBy=multi-user.target
```

___

## Nginx Installation [prof_user]

```
server {
    listen 80;

    server_name prof-talim.edu.uz www.prof-talim.edu.uz;
    
    root /home/user/prof/frontend/prof/build;
    
    location / {  # frontga yo'naltiradi
        try_files $uri $uri/ /index.html =404;
    }
}
```

___

## Nginx Installation [prof_backoffice]

```
server {
    listen 80;

    client_max_body_size 200M;
    server_name backoffice.prof.edu.uz www.backoffice.prof.edu.uz;
    
    root /home/user/prof/frontend/backoffice/build;

    # keepalive_timeout 5;
    location = /favicon.ico { access_log off; log_not_found off; }

    location /media  {
        alias /home/user/prof/backend/project/media;
    }

    location /static-files {
        alias /home/user/prof/backend/project/static-files;
    }

    location ~ ^/(api|admin)/ {  # /api/ yoki /admin/ bilan boshlansa backendga yo'naltiradi
        include proxy_params;
        proxy_pass http://unix:/home/user/prof/backend/run/project.sock;
    }
    
    location / {  # frontga yo'naltiradi
        try_files $uri $uri/ /index.html =404;
    }
}
```

___

# Backup [pg_dump]

___
> `dumpdata`, `dump`, `pg_dump`

```postgresql
pg_dump -h localhost -U prof -d prof -W > db.sql

-h — --host
-U — --username
-d — --dbname
-W — --password (force password prompt)
```

___
> `loaddata`, `load`, `psql`

```postgresql
psql -d prof < db.sql

-d — --dbname
```

___

# Test

___

> O'quv rejalar almashib qolmaganligini testlash

```python
from django.db.models import F
from apps.longs.models import LongTermGroup

LongTermGroup.objects.exclude(curriculum=F('semester__curriculum'))
# <QuerySet []>
```

___

> Talabani mutaxassisligi almashib qolmaganini

```python
from django.db.models import F
from apps.students.models import Student

Student.objects.exclude(classifier_id=F('long_term_group__curriculum__self_classifier__classifier_id'))
# <QuerySet []>
```

___
