from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count() * 2 + 1


max_requests = 1000
worker_class = 'gevent'
workers = max_workers()
reload = True
# Access log - records HTTP req goings-on
accesslog = '/home/user/prof/backend/logs/prof.access.log'
# Error log - records Gunicorn server goings-on
errorlog = '/home/user/prof/backend/logs/prof.error.log'
# Whether to send Django output to the error log
capture_output = True
bind = "unix:/home/user/prof/backend/run/project.sock"
