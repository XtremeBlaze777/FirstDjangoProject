from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *

def index(request):
    curUser = None
    try:
        curUser = User.objects.filter(username=request.user)[0]
    except IndexError:
        pass

    context = {
        'request_method' : request.method,
    }

    if request.method == "POST":
        src = request.POST.get("src", "")
        receiver = User.objects.get(username=request.POST.get("receiver", ""))

        if src == "user_search.html":
            comrades = FriendRequest.objects.create(sender=curUser, receiver=receiver)
            context['top_text'] = str(comrades)

        elif src == "accept":
            brother = FriendRequest.objects.get(receiver=curUser, sender=receiver, is_pending=True)
            brother.accept_request()
            brother.save()
            context['top_text'] = "Added " + str(receiver) + " as a friend!"

        elif src == "cancel":
            no_brother = FriendRequest.objects.get(sender=curUser, receiver=receiver, is_pending=True)
            no_brother.cancel_request()
            no_brother.save()
            context['top_text'] = "Cancelled friend request to " + str(receiver)

        elif src == "reject":
            no_brother = FriendRequest.objects.get(receiver=curUser, sender=receiver, is_pending=True)
            no_brother.reject_request()
            no_brother.save()
            context['top_text'] = "Rejected friend request from " + str(receiver)

        elif src == "remove":
            myList = FriendList.objects.get(user=curUser)
            myList.remove_friend(traitor = receiver)
            myList.save()
            context['top_text'] = "Removed " + str(receiver) + " as a friend..."

    try:
        context['friends'] = list(FriendList.objects.filter(user=curUser)[0].friends.all())
    except IndexError: # This means the user isn't logged in
        return render(request, 'friends.html', context)

    request_list = FriendRequest.objects.filter(receiver=curUser)
    received_list = []
    for req in request_list:
        if req.is_pending == True:
            received_list.append(req.sender)
    context['received'] = received_list

    request_list = FriendRequest.objects.filter(sender=curUser)
    sender_list = []
    for req in request_list:
        if req.is_pending == True:
            sender_list.append(req.receiver)
    context['sent'] = sender_list

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
