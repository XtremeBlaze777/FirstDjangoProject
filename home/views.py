from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

class HomeView(TemplateView):
    template_name = "home.html"

    def home_view(request):
    	print("test")
    	print("test")
    	return HttpResponse("test")
