from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import *

def index(request):
    curUser = User.objects.filter(username=request.user)[0]
    request_list = FriendRequest.objects.filter(receiver=curUser)
    received_list = []
    for req in request_list:
        received_list.append(req.sender)

    request_list = FriendRequest.objects.filter(sender=curUser)
    sender_list = []
    for req in request_list:
        sender_list.append(req.receiver)

    context = {
        'request_method' : request.method,
        'top_text' : "",
        'received' : received_list,
        'sent' : sender_list,
        'friends' : []
    }

    try:
        context['friends'] = FriendList.objects.filter(user=curUser)[0].friends
    except:
        pass

    if request.method == "POST":
        receiver = User.objects.filter(username=request.POST.get("receiver", ""))[0]
        comrades = FriendRequest.objects.create(sender=curUser, receiver=receiver)
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
        
        # # Exclude anyone who is already a friend
        # friend_list = FriendList.objects.filter(user=self.curUser)
        # for list in friend_list:
        #     try:
        #         object_list.exclude(list.user)
        #     except:
        #         pass

        # # Exclude anyone who has been requested
        # pend_list = FriendRequest.objects.filter(sender=self.curUser)
        # for request in pend_list:
        #     try:
        #         object_list.exclude(request.sender)
        #         object_list.exclude(request.receiver)
        #     except:
        #         pass

        return object_list
