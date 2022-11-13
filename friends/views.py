from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import *

def index(request):
    context = {
        'request_method' : request.method,
        'top_text' : "",
    }
    if request.method == "POST":
        receiver = User.objects.filter(username=request.POST.get("receiver", ""))[0]
        comrades = FriendRequest(sender=request.user, receiver=receiver)
        context['top_text'] = str(comrades)
    return render(request, 'friends.html', context)

class SearchResultsView(ListView):
    model = User
    template_name = "user_search.html"

    def get_queryset(self):  
        query = self.request.GET.get("q")
        object_list = self.model.objects.filter(
            Q(username__icontains=query)
        )
        if len(object_list) == 0:
            return []
        
        # Exclude anyone who is already a friend
        friend_list = FriendList.objects.filter(user=self.request.user)
        for user in object_list:
            if user in friend_list:
                object_list.remove(user)
        return object_list
