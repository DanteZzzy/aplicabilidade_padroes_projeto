import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

def before_all(context):
    django.setup()