# from gevent import monkey
#
# monkey.patch_all()
# from psycogreen.gevent import patch_psycopg
#
# patch_psycopg()

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

application = get_wsgi_application()
