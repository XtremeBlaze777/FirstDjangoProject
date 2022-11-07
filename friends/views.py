from django.shortcuts import render

def index(request):
    search_terms = ['admin']
    html_input = {
        'request_method' : request.method,
        'search_terms' : search_terms
    }
    return render(request, 'friends.html', html_input)
