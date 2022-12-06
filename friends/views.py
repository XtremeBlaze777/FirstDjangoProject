from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *

@login_required()
def index(request):
    curUser = User.objects.get(username=request.user)

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
            myList.remove_friend(traitor=receiver)
            myList.save()
            context['top_text'] = "Removed " + str(receiver) + " as a friend..."

    try:
        context['friends'] = list(FriendList.objects.filter(user=curUser)[0].friends.all())
    except IndexError:
        pass

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

@login_required
def SearchResults(request):
    curUser = User.objects.get(username=request.user)

    object_list = list(User.objects.all())
    print(object_list)
    object_list.remove(curUser)

    # Exclude anyone who is already a friend
    list_of_friend_list = FriendList.objects.filter(user=curUser)
    for fl in list_of_friend_list:
        for f in fl.friends.all():
            try:
                object_list.remove(f)
            except ValueError:
                pass

    # Exclude anyone who has been requested
    pend_list = FriendRequest.objects.filter(sender=curUser, is_pending=True)
    for req in pend_list:
        try:
            object_list.remove(req.sender)
        except ValueError:
            pass
        try:
            object_list.remove(req.receiver)
        except ValueError:
            pass

    # Exclude anyone who has requested
    pend_list = FriendRequest.objects.filter(receiver=curUser, is_pending=True)
    for req in pend_list:
        try:
            object_list.remove(req.sender)
        except ValueError:
            pass
        try:
            object_list.remove(req.receiver)
        except ValueError:
            pass

    return render(request, 'user_search.html', { 'object_list' : object_list })