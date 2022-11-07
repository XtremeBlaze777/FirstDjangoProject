from django.views.generic import TemplateView
from .models import *


class HomeView(TemplateView):
    template_name = "home.html"


