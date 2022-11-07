from django.shortcuts import render
from django.views.generic import ListView
from django.conf import settings

def index(request):
    search_terms = ['admin']
    html_input = {
        'request_method' : request.method,
        'search_terms' : search_terms
    }
    return render(request, 'friends.html', html_input)

class SearchResultsView(ListView):
    model = settings.AUTH_USER_MODEL
    template_name = "user_search.html"

    def get_queryset(self):  
        query = self.request.GET.get("q")
        object_list = Course.objects.filter(
            Q(subject__icontains=query)
        )
        return object_list
