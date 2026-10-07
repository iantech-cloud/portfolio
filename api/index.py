import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iano.settings")

from iano.wsgi import application


app = application
