import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agendamento_system.settings")

def before_all(context):
    django.setup()