import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = "LousListA8.settings"
django.setup()
from django.contrib.sites.models import Site
