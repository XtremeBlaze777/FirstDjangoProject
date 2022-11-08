from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q

def index(request):
    search_terms = ['admin']
    html_input = {
        'request_method' : request.method,
        'search_terms' : search_terms
    }
    return render(request, 'friends.html', html_input)

class SearchResultsView(ListView):
    model = User
    template_name = "user_search.html"

    def get_queryset(self):  
        query = self.request.GET.get("q")
        object_list = self.model.objects.filter(
            Q(username__icontains=query)
        )
        if len(object_list) > 0:
            return object_list
        else:
            return []
